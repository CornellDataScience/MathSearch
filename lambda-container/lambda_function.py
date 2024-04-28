from constants import *
import os
import boto3
import json
import dataHandler
import subprocess
import os
import sympy as sp
from sympy.parsing.latex import parse_latex
from zss import Node, distance
import PyPDF2
from PIL import Image, ImageDraw
import pdf2image
import cv2
from sagemaker.pytorch import PyTorchPredictor
from sagemaker.deserializers import JSONDeserializer
import traceback
import requests
import io
import numpy as np
import time

print("Finished imports")

# Initialize S3 client
s3 = boto3.client('s3')

def preprocess_latex(latex_src, rem):
  """
  latex_src: string of LaTeX source code to pre-process
  rem: string of formatting element which we want to remove from latex_src. includes opening curly brace. ex. \mathrm{
  """
  final_string = latex_src
  format_index = latex_src.find(rem)
  while format_index != -1:
    # iterate through string until you find the right closing curly brace to remove
    index = format_index + len(rem)
    closing_brace = -1
    num_opening = 0
    while index < len(final_string):
      if final_string[index:index+1] == "{":
        num_opening += 1
      elif final_string[index:index+1] == "}":
        if num_opening == 0:
          closing_brace = index
          break
        else:
          num_opening -= 1
      index += 1

    # entering this if statement means something went wrong.
    # nothing is removed in this case
    if closing_brace == -1:
      return final_string

    final_string = final_string[:format_index]+final_string[format_index+len(rem):closing_brace]+final_string[closing_brace+1:]
    format_index = final_string.find(rem)
  
  return final_string

print("Finished preprocess_latex")

# Parses sympy expression into Zss tree
def sympy_to_zss(expr):
    if isinstance(expr, sp.Symbol) or isinstance(expr, sp.Number):
        return Node(str(expr))
    else:
        full_class_str = str(expr.func)
        class_name = full_class_str.split('.')[-1].rstrip("'>")
        node = Node(class_name)
        for arg in expr.args:
            child_node = sympy_to_zss(arg)
            node.addkid(child_node)
    return node

print("Finished sympy_to_zss")

# Input is string of LaTeX source code. Runs sympy parser and ZSS tree parser.
# Returns parsed ZSS tree.
def source_to_zss(latex_expr):
    try:
        sympy_expr = parse_latex(latex_expr)
        zss_tree = sympy_to_zss(sympy_expr)
        return zss_tree
    except:
        return Node("ERROR")

print("Finished source_to_zss")
        
# used in ZSS tree edit distance
def custom_edit_distance(query_tree, other_tree):
    return distance(query_tree, other_tree, get_children=Node.get_children,
        insert_cost=lambda node: 10, remove_cost=lambda node: 10, update_cost=lambda a, b: 1)

print("Finished custom_edit_distance")

# Returns a well-formatted LaTeX string represent the equation image 'image'
# Makes the MathPix API call
def image_to_latex_convert(image, query_bool):

    # Hardcoded CDS account response headers (placeholders for now)
    headers = {
        "app_id": "mathsearch_ff86f3_059645",
        "app_key": os.environ.get("APP_KEY")
    }
      
    # Declare api request payload (refer to https://docs.mathpix.com/?python#introduction for description)
    data = {
        "formats": ["latex_styled"], 
        "rm_fonts": True, 
        "rm_spaces": False,
        "idiomatic_braces": True
    }

    print(f"type of img sent to mathpix {type(image)}, {query_bool}")
    #print(f"type after buffered reader stuff {type(io.BufferedReader(io.BytesIO(image)))}")
    # assume that image is stored in bytes
    response = requests.post("https://api.mathpix.com/v3/text",
                                files={"file": image},
                                data={"options_json": json.dumps(data)},
                                headers=headers)
       
    # Check if the request was successful
    if response.status_code == 200:
        print("Successful API call!!")
        response_data = response.json()
        #print(json.dumps(response_data, indent=4, sort_keys=True))  # Print formatted JSON response
        return response_data.get("latex_styled", "")  # Get the LaTeX representation from the response, safely access the key
    else:
        print("Failed to get LaTeX on API call. Status code:", response.status_code)
        return ""

print("Finished image_to_latex_convert")

def downloadDirectoryFroms3(bucketName, remoteDirectoryName):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketName) 
    for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key) # save to same path

print("Finished downloadDirectoryFroms3")

def download_files(pdf_name, query_name, png_converted_pdf_path, pdfs_from_bucket_path):
    """
    Returns path to PDF and query image after downloading PDF and query from the S3 bucket
    """
    local_pdf = pdfs_from_bucket_path + "/" + pdf_name + ".pdf"
    local_target = png_converted_pdf_path+"_"+ pdf_name + "/" + "query.png"
    print("local_pdf",local_pdf)
    print("pdf_name",pdf_name)
    print("local_target", local_target)

    # download and preprocess pdf to png
    s3.download_file(
        Bucket=BUCKET, Key="inputs/"+pdf_name, Filename=local_pdf
    )
    
    images = pdf2image.convert_from_path(local_pdf)
    
    # create directory to put the converted pngs into
    subprocess.run(f'mkdir -p {png_converted_pdf_path}_{pdf_name}', shell=True)
    for i in range(len(images)):
        pdf_image = png_converted_pdf_path + "_" + pdf_name + "/"+ str(i) + ".png"
        images[i].save(pdf_image)
    
    # download query png
    s3.download_file(
        Bucket=BUCKET, Key="inputs/"+query_name, Filename=local_target
    )

    # return paths to the pdf and query that we downloaded
    return local_pdf, f"{png_converted_pdf_path}_{pdf_name}", local_target

print("Finished download_files")

# Call draw_bounding_box on each PNG page of PDF
def draw_bounding_box(image_path_in, bounding_boxes, image_path_out):
  """"
  image_path_in : path to PNG which represents page from pdf
  bounding_boxes: list of list of bounding boxes
  """
  model_width, model_height = 640,640
  image = Image.open(image_path_in).convert('RGB')
  draw = ImageDraw.Draw(image)
  width, height = image.size
  x_ratio, y_ratio = width/model_width, height/model_height
  SKYBLUE = (55,161,253)

  # create rectangle for each bounding box on this page
  for bb in bounding_boxes:
    x1, y1, x2, y2 = bb
    x1, x2 = int(x_ratio*x1), int(x_ratio*x2)
    y1, y2 = int(y_ratio*y1), int(y_ratio*y2)
    draw.rectangle(xy=(x1, y1, x2, y2), outline=SKYBLUE, width=6)
  
  # save img as pdf
  image.save(image_path_out[:-4]+".pdf")

print("Finished draw_bounding_box")

def final_output(pdf_name, bounding_boxes):
  """
  bounding_boxes : dict with keys page numbers, and values list of bounding boxes 
  """
  IMG_IN_DIR = f"/tmp/converted_pdfs_{pdf_name}/"
  IMG_OUT_DIR = "/tmp/img_out/"
  subprocess.run(["rm", "-rf", IMG_OUT_DIR])
  subprocess.run(["mkdir", "-p", IMG_OUT_DIR])
  
  PDF_IN_DIR = "/tmp/pdfs_from_bucket/"
  PDF_OUT_DIR = "/tmp/pdf_out/"
  subprocess.run(["rm", "-rf", PDF_OUT_DIR])
  subprocess.run(["mkdir", "-p", PDF_OUT_DIR])

  pdf_in = PDF_IN_DIR + pdf_name + ".pdf"
  pdf_out = PDF_OUT_DIR + pdf_name[:-4]+".pdf"
  pdf_no_ext = pdf_name[:-4]

  result_pages = list(bounding_boxes.keys())
  print(result_pages)
  # call draw_bounding_boxes for each png page, save to IMG_OUT_DIR
  for i in result_pages:
    image_path_in = IMG_IN_DIR + str(i) + ".png"
    image_path_out = IMG_OUT_DIR + pdf_no_ext + "_"+ str(i) + ".png"
    # pass in list of bounding boxes for each page
    draw_bounding_box(image_path_in, bounding_boxes[i], image_path_out)
    #s3.upload_file(image_path_out[:-4]+".pdf", OUTPUT_BUCKET, str(i) + ".pdf")
  print("drew bounding boxes!")

  # merge the rendered images (with bounding boxes) to the pdf, and upload to S3
  with open(pdf_in, 'rb') as file:
    with open(pdf_out, 'wb') as pdf_out_file:
      pdf = PyPDF2.PdfReader(file)
      output = PyPDF2.PdfWriter()
      for i, page in enumerate(pdf.pages):
        if str(i) in result_pages:
          new_page = PyPDF2.PdfReader(IMG_OUT_DIR + pdf_no_ext + "_"+ str(i) + ".pdf").pages[0]
          new_page.scale_by(0.36)
          output.add_page(new_page)
        else:
          output.add_page(page)
      output.write(pdf_out_file)
    
    try:
      s3.upload_file(pdf_out, OUTPUT_BUCKET, pdf_name[:-4]+".pdf")
      print(f"merged final pdf, uploaded {pdf_out} to {OUTPUT_BUCKET}")
    except:
      raise Exception("Upload failed")

print("Finished final_output")


# Store string repr. of LaTeX equation and its page number in list
def parse_tree_similarity(yolo_result, query_path):
  # list containing all formatting elements we want to remove

  with open(query_path, "rb") as f:
      data = f.read()
      query_text = image_to_latex_convert(data, query_bool=True)
  query_text.replace(" ", "")
  print(f"query_text: {query_text}")

  # ADD code to pre-process query string (from ML subteam)
      
  equations_list = []
  for dict_elem, page_num in yolo_result:
    eqn_num = 1
    for img_array in dict_elem["cropped_ims"]:
      try:
        image = Image.fromarray(np.array(img_array, dtype=np.uint8))
        byte_stream = io.BytesIO()
        image.save(byte_stream, format='PNG')  # Save the image to a byte stream
        byte_stream.seek(0)
        img_bytes = byte_stream.read()
    
        # Assuming image_to_latex_convert can directly handle byte array of an image
        latex_string = image_to_latex_convert(img_bytes, query_bool=False)
        print(f"{eqn_num} on {page_num}: {latex_string}")
        equations_list.append((latex_string, page_num, eqn_num))
      except Exception as e:
        print(f"Failed to process image or convert to LaTeX: {e}")
      eqn_num += 1

  # equations_list = []
  # for dict_elem, page_num in yolo_result:
  #   eqn_num = 1
  #   for img_elem in dict_elem["cropped_ims"]:
  #     print(f"img_elem {img_elem}")
  #     print(f"type of img_elem {type(img_elem)}")

  #     #byte_elem = np.array(byte_elem).tobytes()
  #     byte_elem = bytes(img_elem)
  #     print(f"type of byte_elem {type(byte_elem)}")
  #     #print(img_elem)
  #     latex_string = image_to_latex_convert(byte_elem, query_bool=False)
  #     print(f"{eqn_num} on {page_num}: {latex_string}")

  #     # ENTER CODE FROM ML SUB-TEAM to edit the latex string
  #     # editing the escape_chars and preprocess_latex function
  #     equations_list.append((latex_string, page_num, eqn_num))
  #     eqn_num += 1 # increment equation num
    
  print("Finished all MathPix API calls!")
  
  # create ZSS tree of query  
  zss_query = source_to_zss(query_text)
  
  # now parse all LaTeX source code into ZSS tree and compute edit distance with query for every equation
  # each element in tree_dist is (latex_string, edit_dist_from_query, page_num, eqn_num)
  tree_dists = []
  for eqn, page_num, eqn_num in equations_list:
    zss_tree = source_to_zss(eqn)
    dist = custom_edit_distance(zss_query, zss_tree)
    tree_dists.append((eqn, dist, page_num, eqn_num))

  # sort equations by second element in tuple i.e. edit_dist_from_query
  # return equations with (top_n-1) smallest edit distances
  top_n = 6 
  sorted(tree_dists, key=lambda x: x[1])
  return tree_dists[:top_n]

print("Finished parse_tree_similarity")

def lambda_handler(event, context):
  try:
      print("Running backend...")
      handler = dataHandler.DataHandler()
      objects = handler.list_s3_objects("mathsearch-intermediary")

      body = json.loads(event['Records'][0]['body'])
      receipt_handle = event['Records'][0]['receiptHandle']
      file = body['Records'][0]['s3']['object']['key']
      print("File name: ", file)

      uuid = handler.extract_uuid(file)
      expected_image = f'{uuid}_image'

      if handler.is_expected_image_present(objects, expected_image):
          print('Found image, run ML model')
      
          # clear tmp folder before running the ML model
          subprocess.call('rm -rf /tmp/*', shell=True)

          # folders which we download S3 bucket PDF to
          png_converted_pdf_path = "/tmp/converted_pdfs"
          pdfs_from_bucket_path = "/tmp/pdfs_from_bucket"
          yolo_crops_path = "/tmp/crops/"

          # create the pdfs_from_bucket directory if it doesn't exist
          subprocess.run(f'mkdir -p {pdfs_from_bucket_path}', shell=True, cwd="/tmp")
          subprocess.run(f'mkdir -p {yolo_crops_path}', shell=True, cwd="/tmp")

          pdf_name = uuid+"_pdf"
          query_name = uuid+"_image"
          local_pdf, png_pdf_path, local_target = download_files(pdf_name, query_name, png_converted_pdf_path, pdfs_from_bucket_path)

          ## CALL TO SAGEMAKER TO RUN YOLO
          sm_client = boto3.client(service_name="sagemaker")
          ENDPOINT_NAME = "mathsearch-yolov8-production-v1"
          endpoint_created = False
          # start_time = time.time()
          response = sm_client.list_endpoints()
          for ep in response['Endpoints']:
              print(f"Endpoint Status = {ep['EndpointStatus']}")
              if ep['EndpointName']==ENDPOINT_NAME and ep['EndpointStatus']=='InService':
                  endpoint_created = True

          # return error if endpoint not created successfully
          if not endpoint_created:
            return {
              'statusCode': 400,
              'body': json.dumps('Error with Sagemaker Endpoint'),
              'error': str("Error with Sagemaker Endpoint")
            }

          predictor = PyTorchPredictor(endpoint_name=ENDPOINT_NAME,
                            deserializer=JSONDeserializer())

          print("Sending to Sagemaker...")
          yolo_result = []
          os.chdir(png_converted_pdf_path+"_"+ pdf_name)
          infer_start_time = time.time()
          for file in os.listdir(png_pdf_path):
            # don't need to run SageMaker on query.png
            if file == "query.png": continue

            print(f"Processing {file}")
            
            orig_image = cv2.imread(file)
            model_height, model_width = 640, 640

            resized_image = cv2.resize(orig_image, (model_height, model_width))
            payload = cv2.imencode('.png', resized_image)[1].tobytes()

            page_num = file.split(".")[0]
            yolo_result.append((predictor.predict(payload), page_num))
          infer_end_time = time.time()
          print(f"Sagemaker Inference Time = {infer_end_time - infer_start_time:0.4f} seconds")

          print("Sagemaker results received!")
          print(f"Length of Sagemaker results: {len(yolo_result[0])}")
          print(yolo_result)

          top5_eqns = parse_tree_similarity(yolo_result=yolo_result, query_path=local_target)
          print("MathPix API calls completed, and tree similarity generated!")

          page_nums_5 = sorted([page_num for (latex_string, edit_dist, page_num, eqn_num) in top5_eqns])
          top_5_eqns_info = [(page_num, eqn_num) for (latex_string, edit_dist, page_num, eqn_num) in top5_eqns]

          # get bboxes for top5 equations
          bboxes_dict = {}
          for dict_elem, page_num in yolo_result:
            # don't draw bounding boxes on pages that don't have top 5 equation
            if page_num not in page_nums_5:
              continue

            count = 1
            for bboxes in dict_elem["boxes"]:
              # only collect bounding boxes from top 5 equation
              if (page_num, count) in top_5_eqns_info:
                if page_num in bboxes_dict.keys():
                  bboxes_dict[page_num].append(bboxes[:4])
                else:
                  bboxes_dict[page_num] = [bboxes[:4]]
              count += 1
            
          # return JSON with the following keys
          # id: UUID
          # pdf : path / pdf name
          # pages : list of page numbers sorted in order of most to least similar to query []
          # bbox: list of tuples (page_num, [list of equation label + four coordinates of bounding box])
          pages = sorted(page_nums_5)
          json_result = {"statusCode" : 200, "body": "Successfully queried and processed your document!", 
                        "id": uuid, "pdf": pdf_name, "pages": pages, "bbox": bboxes}
            
          # draws the bounding boxes for the top 5 equations and converts pages back to PDF
          # final PDF with bounding boxes saved in directory pdf_out
          final_output(pdf_name, bboxes_dict)
          print(f"final json_result {json_result}")
      
      # Dequeue from SQS
      handler.delete_sqs_message(QUEUE_URL, receipt_handle)

      # Upload json_result to OUTPUT_BUCKET
      with open(f"/tmp/{uuid}_results.json", "w") as outfile: 
        json.dump(json_result, outfile)

      s3.upload_file(f"/tmp/{uuid}_results.json", OUTPUT_BUCKET, f"{uuid}_results.json")
      return json_result
       
  except:
    exception = traceback.format_exc()
    print(f"Error: {exception}")
    return {
        'statusCode': 400,
        'body': json.dumps(f'Error processing the document.'),
        'error': exception
    }