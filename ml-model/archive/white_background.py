from PIL import Image

image = Image.open('formula_images/1a0a0dfbac.png')
# Create a white rgba background
new_image = Image.new("RGBA", image.size, "WHITE")
# Paste the image on the background. Go to the links given below for details.
new_image.paste(image, (0, 0), image)
new_image.convert('RGB').save('test.jpg', "JPEG")
