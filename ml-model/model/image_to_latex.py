from rapid_latex_ocr import LatexOCR

image_resizer_path = 'models/image_resizer.onnx'
encoder_path = 'models/encoder.onnx'
decoder_path = 'models/decoder.onnx'
tokenizer_json = 'models/tokenizer.json'
model = LatexOCR(image_resizer_path=image_resizer_path,
                encoder_path=encoder_path,
                decoder_path=decoder_path,
                tokenizer_json=tokenizer_json)

img_path = "tests/test_files/6.png"
with open(img_path, "rb") as f:
    data = f. read()

result, elapse = model(data)

print(result)
# {\frac{x^{2}}{a^{2}}}-{\frac{y^{2}}{b^{2}}}=1

print(elapse)
# 0.4131628000000003