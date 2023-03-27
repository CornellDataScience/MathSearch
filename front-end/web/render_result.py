import cv2
import sys
import argparse
import PyPDF2
import pdf2image
from typing import List

'''

Takes in an image from path [./src], and a bounding box coordinates in yolov5 format
Render the bounding boxes on the image, and save the image to the output path [./render]

Example usage:
python3 render_result.py -f ex1.pdf -c 0 0.3392857142857143 0.17142857142857146 0.30952380952380953 0.12698412698412698 1 0.3392857142857143 0.17142857142857146 0.30952380952380953 0.12698412698412698
@ Author: Emerald
'''

def write_pdf(pdf_in, pdf_out, new_pages:List[int]):
	with open(pdf_in, 'rb') as file:
		pdf = PyPDF2.PdfFileReader(file)
		# Create a new PDF with the replacement page
		new_pdf = PyPDF2.PdfFileWriter()
		for page in pdf:
			print(page)
			if page in new_pages:
				new_pdf.merge_page(page)

		# Replace the page in the existing PDF
		# pdf.getPage(page_number)  # Replace `page_number` with the page number you want to replace
		# pdf.removePage(page_number - 1)
		# pdf.insertPage(new_pdf.getPage(0), page_number - 1)

		# Save the updated PDF
		with open('updated_pdf.pdf', 'wb') as output:
			pdf.write(output)
		

def draw_bounding_boxes(image_path_in, bounding_box, image_path_out):
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

	# cv2 uses BGR color instead of RGB
	cv2.rectangle(image, upper_left, bottom_right, SKYBLUE, 3)
	cv2.imwrite(image_path_out, image)


def main(argv):

	parser = argparse.ArgumentParser(
					prog='render_results.py',
					description='render yolov5 equation bonding box on image',
					epilog='Example usage: \npython3 render_result.py -f ex1.pdf -c 0 0.3392857142857143 0.17142857142857146 0.30952380952380953 0.12698412698412698 1 0.3392857142857143 0.17142857142857146 0.30952380952380953 0.12698412698412698')
	
	parser.add_argument('-f','--file', help='pdf file name', required=True)
	parser.add_argument('-c','--coordinates', nargs='+', help='bounding box coordinates', required=True)

	IMG_IN_DIR = "src/"
	IMG_OUT_DIR = "render/"
	PDF_IN_DIR = "pdf_in/"
	PDF_OUT_DIR = "pdf_out/"

	pdf_in = PDF_IN_DIR + parser.parse_args().file
	pdf_out = PDF_OUT_DIR + parser.parse_args().file
	pdf_no_ext = parser.parse_args().file[:-4]

	bounding_boxes = [float(x) for x in parser.parse_args().coordinates]
	
	if(len(bounding_boxes) % 5 != 0):
		print("Invalid number of coordinates, must be multiple of 5")
		return
	
	table = {}
	for i in range(0, len(bounding_boxes), 5):
		table[int(bounding_boxes[i])] = bounding_boxes[i+1:i+5]
	pages = list(table.keys())

	# TODO 1: get result list, convert need box page in the pdf to png, save to /src
	# TODO 2: call draw_bounding_boxes for each png, save to /render
	images = pdf2image.convert_from_path(pdf_in)
	for page in pages:
		image_path_in = IMG_IN_DIR + pdf_no_ext + "_"+ str(page) + ".png"
		images[page].save(image_path_in)
		image_pat_out = IMG_OUT_DIR + pdf_no_ext + "_"+ str(page) + ".png"
		draw_bounding_boxes(image_path_in,table[page],image_pat_out)
	
	# TODO 3: merge the rendered images to the pdf, save to /pdf_out
	write_pdf(pdf_in, pdf_out, pages)

if __name__ == "__main__":
   main(sys.argv[1:])
   
