import sympy as sp
from sympy.parsing.latex import parse_latex
from zss import Node, distance
import networkx as nx
import matplotlib.pyplot as plt


def zss_to_nx(node, graph=None, parent=None):
    if graph is None:
        graph = nx.DiGraph()
    graph.add_node(id(node), label=node.label)
    if parent is not None:
        graph.add_edge(id(parent), id(node))
    for child in node.children:
        zss_to_nx(child, graph, node)
    return graph


# Define some complex LaTeX expressions
# expr1 represents our query
latex_expr1 = r"\nabla J(\theta) = \frac{1}{m} \sum_{i=1}^m (h_\theta(x^{(i)}) - y^{(i)}) x^{(i)}"
# expr represents our OCR'd expression from the file
latex_expr2 = r"\nabla J(\Theta) = \frac{1}{m} \sum_{i=1}^m (h_\theta(z^{(i)}) - y^{(i)}) z^{(i)}"

# Convert LaTeX to SymPy
sympy_expr1 = parse_latex(latex_expr1)
sympy_expr2 = parse_latex(latex_expr2)


def sympy_to_zss(expr):
    if isinstance(expr, sp.Symbol) or isinstance(expr, sp.Number):
        return Node(str(expr))
    else:
        node = Node(str(expr.func))
        for arg in expr.args:
            child_node = sympy_to_zss(arg)
            node.addkid(child_node)
        return node


# Convert the SymPy expression to a ZSS tree
zss_tree1 = sympy_to_zss(sympy_expr1)
zss_tree2 = sympy_to_zss(sympy_expr2)
# print(zss_tree1)
# print(zss_tree2)

# Assuming zss_tree1 and zss_tree2 are your ZSS trees
nx_tree1 = zss_to_nx(zss_tree1)
nx_tree2 = zss_to_nx(zss_tree2)


def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos


def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)
    if len(children) != 0:
        dx = width / len(children)
        nextx = xcenter - width/2 - dx/2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                 vert_loc=vert_loc-vert_gap, xcenter=nextx,
                                 pos=pos, parent=root, parsed=parsed)
    return pos


def draw_tree(tree):
    pos = hierarchy_pos(tree, root=list(tree.nodes())
                        [0])  # Specify the root node
    labels = nx.get_node_attributes(tree, 'label')
    nx.draw(tree, pos, labels=labels, with_labels=True,
            node_size=3000, node_color='lightblue', font_size=10)
    plt.show()


# Draw the trees
# draw_tree(nx_tree1)
# draw_tree(nx_tree2)

# Compare ZSS trees
# make update non-zero to see difference in more updated tree vs. not
distance = distance(zss_tree1, zss_tree2, get_children=Node.get_children,
                    insert_cost=lambda node: 10, remove_cost=lambda node: 10, update_cost=lambda a, b: 1)
print(distance)  # Output the tree edit distance
