import pandas as pd
from datasets import load_dataset
import matplotlib.pyplot as plt
from zss import Node, distance
import sympy as sp
from sympy.parsing.latex import parse_latex

def preprocess_latex(latex_src):
  # Get preprocessed LaTeX representation of query
  formatting_elements_to_remove = []
  for elem in formatting_elements_to_remove :
     latex_src = preprocess_latex(latex_src, elem)
  return latex_src

def remove_expr_from_latex(latex_src, rem):
  #latex_src: string of LaTeX source code to pre-process
  #rem: string of formatting element which we want to remove from latex_src. includes opening curly brace. ex. \mathrm{
  
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
    print()
    print(sympy_expr)
    zss_tree = sympy_to_zss(sympy_expr)
    print()
    print(zss_tree)
    return zss_tree

def show_image(image):
    plt.imshow(image)
    plt.axis('off')
    plt.show()

data = load_dataset("OleehyO/latex-formulas", "cleaned_formulas", trust_remote_code=True)
df = pd.DataFrame(data['train'][:100])

# show_image(df['image'][0]) # <class 'PIL.JpegImagePlugin.JpegImageFile'>
# print(df['latex_formula'][0]) # string

print()
print("First:")
source_to_zss(r"A_m = 1+m+(1-(-1)^m)\kappa_1 + 2\kappa_2.")
print()