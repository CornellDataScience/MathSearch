import pandas as pd
from datasets import load_dataset
import matplotlib.pyplot as plt
from zss import Node, distance
import sympy as sp
from sympy.parsing.latex import parse_latex

# Add an extra backslash to any of the string elements which are in python file escape
def escape_chars(latex_src):
  escape_char = ["\n", "\r", "\f", "\b", "\t"]
  rep_char = ["\\n", "\\r", "\\f", "\\b", "\\t"]
  for i in range(0, len(escape_char)):
    latex_src = latex_src.replace(escape_char[i], rep_char[i])
  return latex_src

  # Get preprocessed LaTeX representation of query
def preprocess_latex(latex_src): 
  
  self_contained_elemeents_to_remove = ["&", "\\begin{align*}", "\\end{align*}", '\\left', '\\right', "\\big", "\\Big"]
  for elem in self_contained_elemeents_to_remove :
     latex_src = latex_src.replace(elem, "")
  
  wrapper_elements_to_remove = ["\\mathrm{", "\\mathcal{", "\\text{"]
  for elem in wrapper_elements_to_remove :
     latex_src = remove_wrapper(latex_src, elem)

  return latex_src
 
def remove_wrapper(latex_src, rem):
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

# Input is string of LaTeX source code. Runs sympy parser and ZSS tree parser.
# Returns parsed ZSS tree.
def source_to_zss(latex_expr):
    sympy_expr = parse_latex(latex_expr) # r"J"+ is only nescessary when the input eq doesn't include a variable
    zss_tree = sympy_to_zss(sympy_expr)
    return zss_tree

# used in ZSS tree edit distance
def custom_edit_distance(query_tree, other_tree):
    return distance(query_tree, other_tree, get_children=Node.get_children,
        insert_cost=lambda node: 10, remove_cost=lambda node: 10, update_cost=lambda a, b: 1)

def show_image(image):
    plt.imshow(image)
    plt.axis('off')
    plt.show()

data = load_dataset("OleehyO/latex-formulas", "cleaned_formulas", trust_remote_code=True)
df = pd.DataFrame(data['train'][:100])

# show_image(df['image'][0]) # <class 'PIL.JpegImagePlugin.JpegImageFile'>
# print(df['latex_formula'][0]) # string

print("Started")

zss_trees = []
count = 0
"""
for index, input in enumerate(df['latex_formula']) :
   preprocessed = preprocess_latex(escape_chars(input))
   zss_trees.append(source_to_zss(preprocessed))
   print()
   print(index)
   print(preprocessed)
   print()
"""

# We've learned that a comma in a subscript breaks parse_latex
# However commas in superscripts are fine
# This is bizarre but we should be able to deal with it,

input = df['latex_formula'][2]
print(input)
preprocessed = preprocess_latex(escape_chars(input))

print(preprocessed)
print()
zss_trees.append(source_to_zss(preprocessed))
print()
print()

print("Finished")

"""
print()
input = df['latex_formula'][0]
preprocessed = preprocess_latex(escape_chars(input))
zss_1 = source_to_zss(preprocessed)
print(preprocessed)
print(zss_1)
print()
preprocessed = preprocess_latex(escape_chars(input))
zss_2 = source_to_zss(preprocessed)
print(preprocessed)
print(zss_2)
print()
print(custom_edit_distance(zss_1,zss_2))
print()
"""