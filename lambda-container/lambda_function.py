from constants import *
import os
import boto3
import json
import dataHandler
import subprocess
import os
#import sympy as sp
#from sympy.parsing.latex import parse_latex
#from zss import Node, distance
import PyPDF2
from PIL import Image, ImageDraw
import pdf2image
import cv2
from sagemaker.pytorch import PyTorchPredictor
from sagemaker.deserializers import JSONDeserializer
import traceback
import requests
#import io
#import numpy as np
import time
import Levenshtein

print("Finished imports")

# Initialize S3 client
s3 = boto3.client('s3')


def levenshtein_distance(query_string, latex_list, top_n):
  # elem of latex_list is (latex string, page num, eqn num)
  ranked_list = []
  n = len(latex_list)
  for i in range(n):
    latex1 = latex_list[i][0] # string is first element 
  
    similarity_score = Levenshtein.distance(latex1, query_string)
    ranked_list.append((latex_list[i][0], latex_list[i][1], latex_list[i][2], similarity_score))
  
  # Sort based on similarity score
  ranked_list.sort(key=lambda x: x[3])
  return ranked_list[:top_n]

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
    
    images = pdf2image.convert_from_path(local_pdf, dpi=500)
    
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
def draw_bounding_box(image_path_in, bounding_boxes):
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
  
  return image
  # save img as pdf
  #image.save(image_path_out[:-4]+".pdf")

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
  pdf_out = PDF_OUT_DIR + pdf_name[:-4]+"_pdf"
  #pdf_no_ext = pdf_name[:-4]

  result_pages = list(bounding_boxes.keys())
  print("bounding boxes dict: ", bounding_boxes)

  # call "draw_bounding_boxes" for each png page, save to IMG_OUT_DIR
  # merge the rendered images (with bounding boxes) to the pdf, and upload to S3
  pages = []
  with open(pdf_in, 'rb') as file: 
    pdf = PyPDF2.PdfReader(file)
    for i, page in enumerate(pdf.pages):
        image_path_in = IMG_IN_DIR + str(i) + ".png"
        if str(i) in result_pages:  
          # pass in list of bounding boxes for each page
          img = draw_bounding_box(image_path_in, bounding_boxes[str(i)])
          pages.append(img)
        else:
          img = Image.open(image_path_in).convert('RGB')
          pages.append(img)
  pages[0].save(pdf_out, save_all=True, append_images=pages[1:])
  
  try:
    s3.upload_file(pdf_out, OUTPUT_BUCKET, pdf_out)
    print(f"merged final pdf, uploaded {pdf_out} to {OUTPUT_BUCKET}")
  except:
    raise Exception("Upload failed")

print("Finished final_output")

# Store string repr. of LaTeX equation and its page number in list
def rank_eqn_similarity(yolo_result, query_path, pdf_name):
  with open(query_path, "rb") as f:
    data = f.read()
    query_text = image_to_latex_convert(data, query_bool=True)
  query_text = query_text.replace(" ", "")
  print(f"query_text: {query_text}")
      
  equations_list = []
  for dict_elem, page_num in yolo_result:
    eqn_num = 1
    
    total_eqns = 0
    skipped_eqns = 0
    for bboxes in dict_elem["boxes"]:
      total_eqns += 1
      # crop from original iamge, and send that to MathPix
      x1, y1, x2, y2, _, label = bboxes

      # skip in-line equations (not skipping everything, but not sure if its correct)
      if label > 0.0:
        eqn_num += 1
        skipped_eqns += 1
        continue
      
      IMG_OUT_DIR = f"/tmp/cropped_imgs_{pdf_name}/"
      subprocess.run(["rm", "-rf", IMG_OUT_DIR])
      subprocess.run(["mkdir", "-p", IMG_OUT_DIR])

      crop_path = IMG_OUT_DIR + "_p"+ str(page_num) + "_e" + str(eqn_num) + ".png"
      page_png_path = f"/tmp/converted_pdfs_{pdf_name}/" + str(page_num) + ".png"
      model_width, model_height = 640,640
      image = Image.open(page_png_path).convert('RGB')
      width, height = image.size
      x_ratio, y_ratio = width/model_width, height/model_height

      # CROP original PNG with yolo bounding box coordinates
      x1, x2 = int(x_ratio*x1), int(x_ratio*x2)
      y1, y2 = int(y_ratio*y1), int(y_ratio*y2)
      cropped_image = image.crop((x1, y1, x2, y2))  
      cropped_image.save(crop_path)
      
      latex_string = image_to_latex_convert(open(crop_path, "rb"), query_bool=False)
      latex_string = latex_string.replace(" ", "")
      print(f"{eqn_num} on {page_num}: {latex_string}")
      equations_list.append((latex_string, page_num, eqn_num))
      eqn_num += 1
    print(f"page {page_num}: skipped {skipped_eqns} in-line eqns, out of {total_eqns}.")
    
  print("Finished all MathPix API calls!")

  # sort equations by second element in tuple i.e. edit_dist_from_query
  # return equations with top_n smallest edit distances
  top_n = 5
  sorted_lst = levenshtein_distance(query_string=query_text, latex_list=equations_list, top_n=top_n)
  print("most similar eqns: ", sorted_lst)
  return sorted_lst

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

          top5_eqns = rank_eqn_similarity(yolo_result=yolo_result, query_path=local_target, pdf_name=pdf_name)
          print("MathPix API calls completed, and tree similarity generated!")

          page_nums_5 = sorted([page_num for (latex_string, page_num, eqn_num, dist) in top5_eqns])
          top_5_eqns_info = [(page_num, eqn_num) for (latex_string, page_num, eqn_num, dist) in top5_eqns]
          #print("top_5_eqns_info ", top_5_eqns_info)

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
            
          # draws the bounding boxes for the top 5 equations and converts pages back to PDF
          # final PDF with bounding boxes saved in directory pdf_out
          final_output(pdf_name, bboxes_dict)

          # return JSON with the following keys
          # id: UUID
          # pdf : path / pdf name
          # pages : list of page numbers sorted in order of most to least similar to query []
          # bbox: list of tuples (page_num, [list of equation label + four coordinates of bounding box])
          #pages = sorted(page_nums_5)
          json_result = {"statusCode" : 200, "body": "Successfully queried and processed your document!", 
                        "id": uuid, "pdf": pdf_name, "pages": page_nums_5, "bbox": bboxes}
          # json_result = {"statusCode" : 200, "body": "Successfully queried and processed your document!", 
          #               "id": uuid, "pdf": pdf_name, "pages": page_nums_5}
            
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