def check(arr, var):
    for a in arr:
        for v in var:
            if a == v:
                return True
    return False

def sp(term):
    count = 0
    n = len(term)-1
    count2 = []
    for i in range(2, len(term)-1):
        if term[i] == '(':
            count += 1
        if term[i] == ')':
            count -= 1
        if count == 0 and term[i] == ',':
            count2.append(i)

    term = term[:n]
    str2 = []
    if len(count2) > 0:
        str2.append(term[2:count2[0]])
        for i in range(1, len(count2)):
            str2.append(term[count2[i-1] + 1: count2[i]])
        str2.append(term[count2[len(count2) - 1] + 1: n])
    else:
        str2.append(term[2:n])
    return str2

def find(s, s1):
    part = []
    start_index = 0
    while True:
        index = s.find(s1, start_index)
        if index == -1:
            break
        part.append(index)
        start_index = index + len(s1)
    return part

def rep(term, s1, s2):
    part = find(term, s1)
    part_ex = []
    for j in range(len(part)):
        p = term[:part[j]] + s2 + term[part[j] + len(s1):]
        part_ex.append(p)
    return part_ex

#
def check2(term, rule, var):
    rules = []
    rule = rule.replace(' ', '')
    rules += rule.split("->")
    # for i in range(len(rules)):
    #     rules[i] = rules[i].strip()
    count = 0
    for i in range(len(term)-1):
        if term[i] == rules[0][0]:
            count += 1
    j = -1
    str2 = []
    for t in range(count):
        cnt = -1
        for i in range(len(term)):
            if term[i] == rules[0][0] and j < i and cnt < 0:
                j = i
                cnt = 0
            if term[i] == '(' and cnt >= 0:
                cnt += 1
            if term[i] == ')' and cnt >= 0:
                cnt -= 1
                if cnt == 0:
                    str2.append(term[j: i+1])
                    cnt = -1
    # print(str2)

    str2_ex = []
    st = []
    for s in str2:
        st.append(sp(s))
    # print(st)

    s = rules[0]
    check_rule = sp(s)
    # print(check_rule)

    for t in range(len(st)):
        s = rules[1]
        if check(s, var):
            if len(check_rule) > 1:
                if check_rule[0] == check_rule[1]:
                    if st[t][0] == st[t][1]:
                        s = s.replace(var[0], st[t][0])
                    else:
                        s = '' #str2[t]
                else:
                    for i in range(len(var)):
                        s = s.replace(check_rule[i], st[t][i])

            else:
                for i in range(len(var)):
                    s = s.replace(check_rule[i], st[t][i])
        str2_ex.append(s)
    # print(str2_ex)
    s_final = []
    for i in range(len(st)):
        if str2_ex[i] != '':
            s = rep(term, str2[i], str2_ex[i])
            s_final += s
    s_final = list(set(s_final))
    s_final = [x for x in s_final if x != '']
    # print(term)
    # print(s_final)
    return s_final

# check2("g(g(t, t), h(t))", "h(x) -> f", ['x'])
# check2("g(g(t, t), g(t, t))", "g(x, x) -> h(h(x)))", ['x'])
# check2("h(h(h(h(t))))", "g(x, x) -> h(h(x)))", ['x'])
# check2("g(g(t, t), h(t))", "g(x,y) -> g(h(x), y)", ['x', 'y'])

def valu(rule, variables):
    part = []
    for i in range(len(rule)):
        for v in variables:
            if rule[i] == v:
                part.append(v)
    part = list(set(part))
    return part

def main():
    """
    n = 2
    Variables: x,t,y
    Start: g(g(t, t), h(t))
    Rules:
    g(x,y) -> g(h(x), y)
    h(t) -> f
    """
    n = int(input("n: "))

    variable = input("Variables: ")
    variable = variable.replace(' ', '')
    variables = []
    variables += variable.split(",")

    term = input("Start: ")
    term = term.replace(' ', '')
    print("Rules: ")
    rules = []
    while True:
        rule = input()
        if rule == "":
            break
        rules.append(rule)

    xx = []
    xx.append(term)
    print('Original term: ' + term)
    # print(len(xx))
    # for j in range(len(xx)):
    # print(xx[0])
    # check2('f(t,z)', 'f(x,y) -> f(y,x)', ['x', 'y'])
    # part = valu(rules[0], variables)
    # check2(xx[0], rules[0], part)
    # print(rules[1])
    # part = valu(rules[1], variables)
    # print(rules[1])
    # print(part)
    # check2(xx[0], rules[1], part)
    for i in range(n):
        print("Step {}: ".format(i+1))
        st = []
        for j in range(len(xx)):
            for rule in rules:
                part = valu(rule, variables)
                # print(part)
                s = check2(xx[j], rule, part)
                st += s
        # print(st)
        st = list(set(st))
        # print(st)
        for s in st:
            print(s)
        xx = st
    # print(st)

if __name__ == "__main__":
    main()



