import parse as pa
import ssnf as sf

def back_tracking(node):
    if node is None:
        return ""

    a = back_tracking(node.left)
    b = back_tracking(node.right) if node.right else ""

    if node.data == '.':
        if node.left.data == '|':
            a = '(' + a + ')'
        if node.right and node.right.data == '|':
            b = '(' + b + ')'
        return a + b

    elif node.data == '*':
        if node.left.data == '|' or node.left.data == '.':
            return '(' + a + ')*'
        return a + '*'

    elif node.data == '|':
        if a in b:
            return b
        else:
            return a + '|' + b
    else:
        return node.data

def aci(node):
    if node is None:
        return None

    if node.data != '|':
        node.left = aci(node.left)
        node.right = aci(node.right)
        return pa.Node(back_tracking(node))

    else:
        node.left = aci(node.left)
        node.right = aci(node.right)

        a = node.left.data
        b = node.right.data

        if a and b not in sf.chars and a > b:
            node.left, node.right = node.right, node.left

        if a == '|':
            node = pa.Node(node.data, aci(node.left), aci(node.right))

        if b == '|':
            node = pa.Node(node.data, aci(node.left), aci(node.right))
            s1 = node.right.left.data
            s2 = node.left.data
            if s1 not in sf.chars:
                if s1 < s2:
                    node.left, node.right.left = node.right.left, node.left

        return node

# regex = '((b|cc)|(cc|cb))**(cc|a**)cca(b**|c)'
# regex = '(aacb|bcca)((b|b)|(a|bc))b**b**'
# regex = '(((bb|b)*|(ab|ca)*)|ac(bcab|acc)**)c'
# regex = regex.replace(' ', '')
# print(regex)
# tree = pa.parse_regex(regex)
# tree.print_node()
# print()
# tree2 = sf.ssnf(tree)
# tree3 = aci(tree2)
# print(back_tracking(tree3))
