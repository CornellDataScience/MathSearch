import requests
import json
import io
from zss import Node, distance
import numpy as np
import sympy as sp
from sympy.parsing.latex import parse_latex
import os

"""
#Hardcoded CDS account response headers (placeholders for now)
headers = {
  "app_id": "CDS_mathsearch-mathpix-test",
  "app_key": "71e46420dcdbad2cdd86d7cb119d2075c8de8ce107350be8cdc8518d49dc2d6d"
}

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
        #print(json.dumps(response_data, indent=4, sort_keys=True))  # Print formatted JSON response
        #print()
        return response_data.get("latex_styled", "")  # Get the LaTeX representation from the response, safely access the key
    else:
        print("Failed to get LaTeX. Status code:", response.status_code)
        return ""

def jpg_image_to_latex(image_jpg_path) :
    
    #Declare api request payload (refer to https://docs.mathpix.com/?python#introduction for description)
    data = {
        "formats": ["latex_styled"], 
        "rm_fonts": True, 
        "rm_spaces": False,
        "idiomatic_braces": True
    }

    # It's better to use the with statement when dealing with file operations
    response = requests.post("https://api.mathpix.com/v3/text",
                              files={"file": open(image_jpg_path,"rb").read()},
                              data={"options_json": json.dumps(data)},
                              headers=headers)
    

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        #print(json.dumps(response_data, indent=4, sort_keys=True))  # Print formatted JSON response
        #print()
        return response_data.get("latex_styled", "")  # Get the LaTeX representation from the response, safely access the key
    else:
        print("Failed to get LaTeX. Status code:", response.status_code)
        return ""
    
def bytes_arry_to_latex(bytes_array) :
    
    #Declare api request payload (refer to https://docs.mathpix.com/?python#introduction for description)
    data = {
        "formats": ["latex_styled"], 
        "rm_fonts": True, 
        "rm_spaces": False,
        "idiomatic_braces": True
    }

    # It's better to use the with statement when dealing with file operations
    response = requests.post("https://api.mathpix.com/v3/text",
                              files={"file": io.BufferedReader(io.BytesIO(bytes_array))},
                              data={"options_json": json.dumps(data)},
                              headers=headers)
    

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        #print(json.dumps(response_data, indent=4, sort_keys=True))  # Print formatted JSON response
        #print()
        return response_data.get("latex_styled", "")  # Get the LaTeX representation from the response, safely access the key
    else:
        print("Failed to get LaTeX. Status code:", response.status_code)
        return ""
"""

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

# used in ZSS tree edit distance
def custom_edit_distance(query_tree, other_tree):
    return distance(query_tree, other_tree, get_children=Node.get_children,
        insert_cost=lambda node: 10, remove_cost=lambda node: 10, update_cost=lambda a, b: 1)

# Input is string of LaTeX source code. Runs sympy parser and ZSS tree parser.
# Returns parsed ZSS tree.
def source_to_zss(latex_expr):
    try:
        print('Started: ' + latex_expr)
        sympy_expr = parse_latex('latex_expr')
        print('SymPy')
        zss_tree = sympy_to_zss(sympy_expr)
        print('ZSS')
        print(type(zss_tree))
        print()
        return zss_tree
    except Exception as e:  # Catch the base Exception class
        print(f"An error occurred: {e}")
        return Node("ERROR")

# Returns a well-formatted LaTeX string represent the equation image 'image'
# 'image' should be the string path to a jpg image if 'query_bool' is true
# 'image' should represent a numpy or non-numpy array of image bytes if 'query_bool' is false
def image_to_latex_convert(image, query_bool):
    
    #Hardcoded CDS account response headers (placeholders for now)
    headers = {
      "app_id": "CDS_mathsearch-mathpix-test",
      "app_key": "71e46420dcdbad2cdd86d7cb119d2075c8de8ce107350be8cdc8518d49dc2d6d"
    }
    
    # Declare api request payload (refer to https://docs.mathpix.com/?python#introduction for description)
    data = {
        "formats": ["latex_styled"], 
        "rm_fonts": True, 
        "rm_spaces": False,
        "idiomatic_braces": True
    }

    response = requests.post("https://api.mathpix.com/v3/text",
                                files={"file": open(image,"rb").read() if query_bool else io.BufferedReader(io.BytesIO(image))},
                                data={"options_json": json.dumps(data)},
                                headers=headers)
       
    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        #print(json.dumps(response_data, indent=4, sort_keys=True))  # Print formatted JSON response
        #print()
        return response_data.get("latex_styled", "")  # Get the LaTeX representation from the response, safely access the key
    else:
        print("Failed to get LaTeX on API call. Status code:", response.status_code)
        return ""

def raw_string(s) : return s #return s.encode('unicode_escape').decode('ascii') #return r'{}'.format(s)

def parse_tree_similarity(source_path, query_path):
  
  # source_path : path to source directory of images to search
  # query_path : path to the query image which was downloaded from S3
  
  # rem is list containing all formatting elements we want to remove
  formatting_elements_to_remove = ["\mathrm{", "\mathcal{", "\\text{", "\left", "\right"]

  print("#1")

  # Get preprocessed LaTeX representation of query
  query_latex = image_to_latex_convert(query_path, query_bool=True)
  for elem in formatting_elements_to_remove :
        query_latex = preprocess_latex(query_latex, elem)
  query_latex = raw_string(query_latex)

  print("#2")

  # Get a list of tuples of (LaTeX OCR of image, image filename)
  source_latex = []
  for filename in os.listdir(source_path):
    if filename.endswith('.jpg'):
        print(filename)
        latex_string = image_to_latex_convert(os.path.join(source_path, filename), query_bool=True)
        for elem in formatting_elements_to_remove :
            latex_string = preprocess_latex(latex_string, elem)
        source_latex.append( (latex_string, filename) )

  
  print("#3")

  # create ZSS tree of the query  
  zss_query = source_to_zss(query_latex)

  print("#4")

  # now parse all LaTeX source code into ZSS tree and compute edit distance with query for every equation
  # each element in tree_dist is (latex_string, edit_dist_from_query, filename)
  tree_dists = []
  for eqn, filename in source_latex:
    print(filename)
    zss_tree = source_to_zss(raw_string(eqn))
    dist = custom_edit_distance(zss_query, zss_tree)
    tree_dists.append((eqn, dist, filename))

  print("#5")

  # sort equations by second element in tuple i.e. edit_dist_from_query
  # return equations with (top_n-1) smallest edit distances
  return tree_dists

print()
output = parse_tree_similarity('test-eqn', 'test-query/query.jpg')
for _, dist, filename in output :
   print(filename + " : " + str(dist))
print()

