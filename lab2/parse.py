class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def print_node(self):
        if self is not None:
            print(self.data, end=' ')

            if self.left:
                self.left.print_node()

            if self.right:
                self.right.print_node()

def parse_regex(regex):
    def check_char(token_list):
        if token_list[0] != '|' and token_list[0] != 'ε' and token_list[0] != '*' and token_list[0] != ')':
            return True
        else:
            return False

    def parse_token(token_list, expected):
        if token_list[0] == expected:
            del token_list[0]
            return True
        else:
            return False

    def parse_char(token_list):
        if parse_token(token_list, '('):
            # get the subexpression
            x = parse_all(token_list)
            # remove the closing parenthesis
            parse_token(token_list, ')')
            return x
        else:
            x = token_list[0]
            if type(x) != type('') or x == 'end': return None
            token_list[0:1] = []
            return Node(x, None, None)

    def parse_star(token_list):
        a = parse_char(token_list)
        if parse_token(token_list, '*'):
            subtree = a
            while token_list[0] == '*':
                helper = Node('*', subtree, None)
                subtree = helper
                token_list[0:1] = []
            return Node('*', subtree, None)
        else:
            return a

    def parse_concat(token_list):
        a = parse_star(token_list)
        if check_char(token_list):
            b = parse_concat(token_list)
            return Node('.', a, b)
        else:
            return a

    def parse_all(token_list):
        a = parse_concat(token_list)
        if parse_token(token_list, '|'):
            b = parse_all(token_list)
            return Node('|', a, b)
        else:
            return a

    token_list = list(regex)
    token_list.append('ε')
    return parse_all(token_list)

# regex = '(a|b|a(a*|c*)*)*|(a|b|c)*'
# regex = 'ab*c|de(fg)*'
# # regex = '(((bb|b)*|(ab|ca)*)|(bcab|acc)**)c'
#
# root = parse_regex(regex)
#
# # print("Tree: '{}':".format(regex))
# root.print_node()
