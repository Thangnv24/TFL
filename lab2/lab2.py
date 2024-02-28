import aci as ai
import parse as pa
import ssnf as sf

def optimize(regex):
    regex = regex.replace(' ', '')
    tree = pa.parse_regex(regex)
    # tree.print_node()
    # print()
    tree = sf.ssnf(tree)
    tree = ai.aci(tree)
    str = ai.back_tracking(tree)
    return str

def main():
    # regex = input()
    print("Regex optimized: ")
    str = optimize('(((bb|b)*|(ab|ca)*)|(bcab|acc)**)c')
    print(str)
    file_path = "tests.txt"

    lines = []

    with open(file_path, "r") as file:
        for line in file:
            lines.append(line.strip())
    if '' in lines:
        lines.remove('')

    mess = ""
    for line in lines:
        mess += line
        mess += '\nRegex optimized: '
        s = optimize(line)
        mess += s
        mess += '\n'

    f = open("result.txt", "w")
    f.write(mess)
    f.close()


if __name__ == "__main__":
    main()
