from PIL import Image

image = Image.open('formula_images/1a0a0dfbac.png')
new_image = Image.new("RGBA", image.size, "WHITE") # Create a white rgba background
new_image.paste(image, (0, 0), image)              # Paste the image on the background. Go to the links given below for details.
new_image.convert('RGB').save('test.jpg', "JPEG")