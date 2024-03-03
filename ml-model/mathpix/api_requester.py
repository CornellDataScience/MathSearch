import requests
import json

#Hardcoded CDS account response headers (placeholders for now)
headers = {
  "app_id": "PLACEHOLDER_APP_ID",
  "app_key": "PLACEHOLDER_APP_KEY"
}

mathpix_url = "https://api.mathpix.com/v3/text"

def s3_image_to_latex(image_s3_url) :
    
    #Declare api request payload (refer to https://docs.mathpix.com/?python#introduction for description)
    data = {
        "src": image_s3_url, 
        "formats": "latex_styled", 
        "rm_fonts": True, 
        "idiomatic_braces": True
    }

    #Post rquest and get response
    response = requests.post(mathpix_url, json=data, headers=headers)

    print("\nResult object:", json.dumps(response, indent=4, sort_keys=True))

    #Get LaTeX representation from resonse
    return response['latex_styled']