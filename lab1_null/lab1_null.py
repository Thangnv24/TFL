def check(arr, var):
    for a in arr:
        for v in var:
            if a == v:
                return True
    return False

def sp(str):
    count = 0
    n = len(str)-1
    count2 = []
    for i in range(2, len(str)-1):
        if str[i] == '(':
            count += 1
        if str[i] == ')':
            count -= 1
        if count == 0 and str[i] == ',':
            count2.append(i)

    str = str[:n]
    str2 = []
    if len(count2)>0:
        str2.append(str[2:count2[0]])
        for i in range(1, len(count2)):
            str2.append(str[count2[i-1] + 2: count2[i]])
        str2.append(str[count2[len(count2) - 1] + 2: n])
    else:
        str2.append(str[2:n])
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

def rep(str, s1, s2):
    part = find(str, s1)
    part_ex = []
    for j in range(len(part)):
        p = str[:part[j]] + s2 + str[part[j] + len(s1):]
        part_ex.append(p)
    return part_ex

#

def check2(str, rule, var):
    rules = []
    rules += rule.split("->")
    for i in range(len(rules)):
        rules[i] = rules[i].strip()
    count = 0
    for i in range(len(str)-1):
        if str[i] == rules[0][0]:
            count += 1
    j = -1
    str2 = []
    for t in range(count):
        cnt = -1
        for i in range(len(str)):
            if str[i] == rules[0][0] and j < i and cnt < 0:
                j = i
                cnt = 0
            if str[i] == '(' and cnt >= 0:
                cnt += 1
            if str[i] == ')' and cnt >= 0:
                cnt -= 1
                if cnt == 0:
                    str2.append(str[j: i+1])
                    cnt = -1
    # print(str2)

    str2_ex = []
    st = []
    for s in str2:
        st.append(sp(s))
    # print(st)

    check_rule = []
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
                        s = s.replace(var[i], st[t][i])

            else:
                for i in range(len(var)):
                    s = s.replace(var[i], st[t][i])
        str2_ex.append(s)
    # print(str2_ex)
    s_final = []
    for i in range(len(st)):
        s = rep(str, str2[i], str2_ex[i])
        s_final += s
    s_final = list(set(s_final))
    s_final = [x for x in s_final if x != '']
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
    variables = []
    variables += variable.split(",")
    for i in range(len(variables)):
        variables[i] = variables[i].strip()
    print(variables)

    str = input("Start: ")
    print("Rules: ")
    rules = []
    while True:
        rule = input()
        if rule == "":
            break
        rules.append(rule)
    # print(rules)

    xx = []
    xx.append(str)
    print('Original term: ' + str)

    for i in range(n):
        print("Step {}: ".format(i+1))
        st = []
        for j in range(len(xx)):
            for rule in rules:
                part = valu(rule, variables)
                s = check2(xx[j], rule, part)
                st += s
        st = list(set(st))
        for s in st:
            print(s)
        xx = st
    # print(st)

if __name__ == "__main__":
    main()




