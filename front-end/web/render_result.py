import cv2
import sys
import argparse
import PyPDF2
import pdf2image
from PIL import Image
import json
import time

'''
Takes in two parameters: -f filename -c coordinates
Save pdf [filename.pdf] with bounding boxes and the result page list [filename.json] to dir pdf_out

@ Param:
-f filename.pdf
-c in (regex) syntax of: [page_number x y w h]+

@ Example:
python3 render_result.py -f ex1.pdf -c 0 0.3392857142857143 0.17142857142857146 0.30952380952380953 0.12698412698412698 1 0.32242063492063494 0.4380952380952381 0.26785714285714285 0.08888888888888889

@ Author: Emerald

'''	


# page.scale_to(width: float, height: float)→ None

#? Code that pdf -> png -> pdf
def draw_bounding_box(image_path_in, bounding_box, image_path_out):
	image = cv2.imread(image_path_in)
	height, width, _ = image.shape
	x, y, w, h = bounding_box
	x1 = int((x - w/2) * width)
	y1 = int((y - h/2) * height)
	x2 = int((x + w/2) * width)
	y2 = int((y + h/2) * height)
	upper_left = (x1, y1)
	bottom_right = (x2, y2)

	RED = (0,0,255)
	BLUE = (255,0,0)
	GREEN = (0,255,0)
	SKYBLUE = (255,191,0)

	# note cv2 uses BGR color instead of RGB
	cv2.rectangle(image, upper_left, bottom_right, SKYBLUE, 3)
	cv2.imwrite(image_path_out, image)
def main(argv):
	if len(argv)==1:
		argv = argv[0].split()
	# print(type(argv),type(argv[0]),argv)
	parser = argparse.ArgumentParser(
					prog='render_results.py',
					description='render yolov5 equation bonding box on image',
					epilog='Example usage: \npython3 render_result.py -f ex1.pdf -c 0 0.3392857142857143 0.17142857142857146 0.30952380952380953 0.12698412698412698 1 0.32242063492063494 0.4380952380952381 0.26785714285714285 0.08888888888888889')
	
	parser.add_argument('-f','--file', help='pdf file name', required=True)
	parser.add_argument('-c','--coordinates', nargs='+', help='bounding box coordinates', required=True)

	IMG_IN_DIR = "img_in/"
	IMG_OUT_DIR = "img_out/"
	PDF_IN_DIR = "pdf_in/"
	PDF_OUT_DIR = "pdf_out/"

	pdf_name = parser.parse_args(argv).file
	pdf_in = PDF_IN_DIR + pdf_name
	pdf_out = PDF_OUT_DIR + pdf_name
	pdf_no_ext = pdf_name[:-4]

	bounding_boxes = [float(x) for x in parser.parse_args(argv).coordinates]
	
	if(len(bounding_boxes) % 5 != 0):
		print("Invalid number of coordinates, must be multiple of 5")
		return
	
	table = {}
	for i in range(0, len(bounding_boxes), 5):
		table[int(bounding_boxes[i])] = bounding_boxes[i+1:i+5]
	result_pages = list(table.keys())

	# Done 1: get result list, convert need box page in the pdf to png, save to /img_in
	# Done 2: call draw_bounding_boxes for each png, save to /img_out
	images = pdf2image.convert_from_path(pdf_in)
	for i in result_pages:
		image_path_in = IMG_IN_DIR + pdf_no_ext + "_"+ str(i) + ".png"
		images[i].save(image_path_in)
		image_path_out = IMG_OUT_DIR + pdf_no_ext + "_"+ str(i) + ".png"
		draw_bounding_box(image_path_in,table[i],image_path_out)
		# save img as pdf
		image = Image.open(image_path_out).convert('RGB')
		image.save(image_path_out[:-4]+".pdf")
	
	# Done 3: merge the rendered images to the pdf, save to /pdf_out
	with open(pdf_in, 'rb') as file:
		with open(pdf_out, 'wb') as pdf_out:
			pdf = PyPDF2.PdfReader(file)
			output = PyPDF2.PdfWriter()
			for i, page in enumerate(pdf.pages):
				if i in result_pages:
					new_page = PyPDF2.PdfReader(IMG_OUT_DIR + pdf_no_ext + "_"+ str(i) + ".pdf").pages[0]
					new_page.scale_by(0.36)
					output.add_page(new_page)
				else:
					output.add_page(page)
			output.write(pdf_out)
	
	# Done 4: save the result list to json file
	result_pages_json = PDF_OUT_DIR + pdf_no_ext+".json"
	with open(result_pages_json,'w') as file:
		json.dump(result_pages, file, indent=4, separators=(",", ":"))
	
	with open("/home/ubuntu/MathSearch/front-end/web/result_log","a") as file:
		argv_str = " ".join(str(x) for x in argv)
		print(argv_str)
		file.write("\n",time.strftime("%H:%M:%S", time.localtime()) + "\t" + argv_str)


# python3 render_result.py -f ex1.pdf -c 0 0.3392857142857143 0.17142857142857146 0.30952380952380953 0.12698412698412698 1 0.32242063492063494 0.4380952380952381 0.26785714285714285 0.08888888888888889
if __name__ == "__main__":
	start = time.time()
	main(sys.argv[1:])
	end = time.time()
	print("PDF saved! Time used:",end - start)

"""
box

x1,y1 -------
|			|
|			|
--------- x2,y2

--------x2,y1
|			|
|			|
x1,y2--------

"""