import requests
import json

#Hardcoded CDS account response headers (placeholders for now)
headers = {
  "app_id": "CDS_mathsearch-mathpix-test",
  "app_key": "71e46420dcdbad2cdd86d7cb119d2075c8de8ce107350be8cdc8518d49dc2d6d"
}

mathpix_url = "https://api.mathpix.com/v3/text"

mathpix_url = "https://api.mathpix.com/v3/text"

def s3_image_to_latex(image_s3_url) :
    
    #Declare api request payload (refer to https://docs.mathpix.com/?python#introduction for description)
    #s3 url version: 
    data = {
        "src": image_s3_url, 
        "formats": ["latex_styled"], 
        "rm_fonts": True, 
        "rm_spaces": False,
        "idiomatic_braces": True
    }

    #Post rquest and get response
    response = requests.post(mathpix_url, json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        print(json.dumps(response_data, indent=4, sort_keys=True))  # Print formatted JSON response
        print()
        return response_data.get("latex_styled", "")  # Get the LaTeX representation from the response, safely access the key
    else:
        print("Failed to get LaTeX. Status code:", response.status_code)
        return ""

def jpg_image_to_latex(image_jpg_path) :
    
    #Declare api request payload (refer to https://docs.mathpix.com/?python#introduction for description)
    #s3 url version: 
    data = {
        "formats": ["latex_styled"], 
        "rm_fonts": True, 
        "rm_spaces": False,
        "idiomatic_braces": True
    }

    # It's better to use the with statement when dealing with file operations
    response = requests.post("https://api.mathpix.com/v3/text",
                              files={"file": open(image_jpg_path,"rb")},
                              data={"options_json": json.dumps(data)},
                              headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        print(json.dumps(response_data, indent=4, sort_keys=True))  # Print formatted JSON response
        print()
        return response_data.get("latex_styled", "")  # Get the LaTeX representation from the response, safely access the key
    else:
        print("Failed to get LaTeX. Status code:", response.status_code)
        return ""

#print(jpg_image_to_latex('big-eqn/im.jpg14.jpg'))
print()
#print(jpg_image_to_latex('big-eqn/im.jpg17.jpg'))
print()
#print(jpg_image_to_latex('big-eqn/im.jpg714.jpg')) # This one is hard, the OCR getting this seems really impressive
print()
print(jpg_image_to_latex('big-eqn/im.jpg728.jpg')) # matrix

    