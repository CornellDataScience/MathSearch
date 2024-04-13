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

def preprocess_latex(latex_src):
  # Get preprocessed LaTeX representation of query
  formatting_elements_to_remove = ["\\\\begin{align*}", "\\\\end{align*}"]
  for elem in formatting_elements_to_remove :
     latex_src = latex_src.replace(elem, "")
  return latex_src

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
print(preprocess_latex(df['latex_formula'][0].replace('\\', '\\\\')))
source_to_zss("A_m = 1+m+(1-(-1)^m)\kappa_1 + 2\kappa_2.")
print()