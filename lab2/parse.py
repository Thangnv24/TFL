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
    index = 0

    def parse_star():
        nonlocal index
        subtree = parse_parentheses()
        while index < len(token_list) and token_list[index] == '*':
            index += 1
            subtree = Node('*', subtree)
        return subtree

    def parse_parentheses():
        nonlocal index
        if index < len(token_list):
            token = token_list[index]
            index += 1
            if token == '(':
                subtree = parse_all()
                assert token_list[index] == ')'
                index += 1
                return subtree
            else:
                return Node(token)
        else:
            return None

    def parse_concat():
        nonlocal index
        subtree = parse_star()
        while index < len(token_list) and token_list[index] not in '|)':
            subtree = Node('.', subtree, parse_concat())
        return subtree

    def parse_all():
        nonlocal index
        subtree = parse_concat()
        if index < len(token_list) and token_list[index] == '|':
            index += 1
            subtree = Node('|', subtree, parse_all())
        return subtree


    token_list = list(regex)
    # return parse_star()
    # return parse_concat()
    # return parse_regex()
    return parse_all()


# regex = 'ab*c|de(fg)*'
# # regex = '(((bb|b)*|(ab|ca)*)|(bcab|acc)**)c'
#
# root = parse_regex(regex)
#
# print("Tree: '{}':".format(regex))
# root.print_node()
