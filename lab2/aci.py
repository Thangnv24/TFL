import parse as pa
import ssnf as sf

def rotate(node):
    if node.data == None:
        return
    temp = node.left
    node.left = node.right
    node.right = temp


def aci(node):
    op = ['|', '.', '*']
    if node is None:
        return
    elif node.data != '|':
        # Recursively process child branches
        node.left = aci(node.left)
        node.right = aci(node.right)
        return pa.Node(back_tracking(node), None, None)
    else:
        # operator '|'
        node.left = aci(node.left)
        node.right = aci(node.right)

        left = node.left.data
        right = node.right.data

        # Check idempotency: A | A -> A
        if left == right:
            return node.left

        # Sort branch order if both are characters
        if left not in op and right not in op:
            if left > right:
                rotate(node)

        # Check if the child branch is '|'
        if left == '|':
            node = pa.Node(node.data, aci(node.left), aci(node.right))

        if right == '|':
            node = pa.Node(node.data, aci(node.left), aci(node.right))
            right = node.right.left.data
            left = node.left.data
            if right not in op:
                if left > right:
                    temp = node.left
                    node.left = node.right.left
                    node.right.left = temp
            node = pa.Node(node.data, aci(node.left), aci(node.right))

        return node

def back_tracking(node):
    s = ""
    if node.left != None:
        left = back_tracking(node.left)
        right = None
        if node.right != None:
            right = back_tracking(node.right)
        if node.data == '.':
            if node.left.data == '|':
                s = '(' + left + ')' + right
                if node.right.data == '|':
                    s = '(' + left + ')' + '(' + right + ')'
                node = pa.Node(s, None, None)
                return s
            if node.right.data == '|':
                s = left + '(' + right + ')'
                node = pa.Node(s, None, None)
                return s
            else:
                s = left + right
                node = pa.Node(s, None, None)
                return s
        elif node.data == '*':
            if node.left.data == '|' or node.left.data == '.':
                s = "(" + left + ")" + "*"
            else:
                s = left + "*"
            node = pa.Node(s, None, None)
            return s
        elif node.data == '|':
            if left in right:
                s = right
            else:
                s = left + '|' + right
            node = pa.Node(s, None, None)
            return s
        else:
            return node.data
    else:
        return str(node.data)

# regex = '((b|cc)|(cc|cb))**(cc|a**)cca(b**|c)'
# regex = '(aacb|bcca)((b|b)|(a|bc))b**b**'
# regex = '(((bb|b)*|(ab|ca)*)|ac(bcab|acc)**)c'
# regex = regex.replace(' ', '')
# print(regex)
# node = pa.parse_regex(regex)
# node.print_node()
# print()
# node2 = sf.ssnf(node)
# node3 = aci(node2)
# print(back_tracking(node3))
