import parse as pa

'''
ssnf
β = ε ⇒ ssnf(β) = ε;
β = a ⇒ ssnf(β) = a;
β = A | B ⇒ ssnf(β) = ssnf(A) | ssnf(B);
β = AB ⇒ ssnf(β) = ssnf(A) ssnf(B);
β = A∗ ⇒ ssnf(β) = ss(A)∗.

ss
β = ε ⇒ ss(β) = ∅;
β = a ⇒ ss(β) = a;
β = A | B ⇒ ss(β) = ss(A) | ss(B);
β = AεBε ⇒ ss(β) = ss(Aε) | ss(Bε);
β = AB ⇒ ss(β) = ssnf(A) ssnf(B);
β = A∗ ⇒ ss(β) = ss(A).
'''

chars = ['*', '|', '.']

def ssnf(node):
    if node.data is None:
        return node
    elif node.data != '.' and node.data != '|' and node.data != '*':
        return pa.Node(node.data)
    elif node.data == '|':
        return pa.Node('|', ssnf(node.left), ssnf(node.right))
    elif node.data == '.':
        return pa.Node('.', ssnf(node.left), ssnf(node.right))
    elif node.data == '*':
        return pa.Node('*', ss(node.left), None)


def ss(node):
    if node.data is None:
        return
    elif node.data != '.' and node.data != '|' and node.data != '*':
        return pa.Node(node.data)
    elif node.data == '|':
        return pa.Node('|', ss(node.left), ss(node.right))
    elif node.data == '.':
        if node.left.data == '*' and node.right.data == '*':
            return pa.Node('|', ss(node.left), ss(node.right))
        else:
            return pa.Node('.', ssnf(node.left), ssnf(node.right))
    elif node.data == '*':
        return ss(node.left)


# regex = '((ab*c|de)**)c**)*bcd (de)*|gh*'
# regex = regex.replace(' ', '')
# root = pa.parse_regex(regex)
# root.print_node()
# print()
# root2 = ssnf(root)
# root2.print_node()
