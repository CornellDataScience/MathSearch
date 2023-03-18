import cv2
import sys
import argparse

'''

Takes in an image from path [./src], and a bounding box coordinates in yolov5 format
Render the bounding boxes on the image, and save the image to the output path [./render]

Example usage:
python3 render_result.py -i ex1_yolov5.png -c 0.3392857142857143 0.17142857142857146 0.30952380952380953 0.12698412698412698
python3 render_result.py -i ex2_yolov5.png -c 0.32242063492063494 0.4380952380952381 0.26785714285714285 0.08888888888888889

@ Author: Emerald
'''


def draw_bounding_boxes(image_path, bounding_box, output_path):
	image = cv2.imread(image_path)
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
	cv2.imwrite(output_path, image)


def main(argv):
	parser = argparse.ArgumentParser(
                    prog='render_results.py',
                    description='render yolov5 equation bonding box on image',
                    epilog='''Example usage: \npython3 render_result.py -i ex1_yolov5.png -c 0.3392857142857143 0.17142857142857146 0.30952380952380953 0.12698412698412698''')
	
	parser.add_argument('-i','--image', help='image name', required=True)
	parser.add_argument('-c','--coordinates', nargs='+', help='bounding box coordinates', required=True)

	INPUT_DIR = "src/"
	OUTPUT_DIR = "render/"
	image_path = INPUT_DIR + parser.parse_args().image
	bounding_boxe = [float(x) for x in parser.parse_args().coordinates]
	output_path = OUTPUT_DIR + parser.parse_args().image
	draw_bounding_boxes(image_path, bounding_boxe, output_path)

if __name__ == "__main__":
   main(sys.argv[1:])
   
