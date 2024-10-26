def check_func(term, var):
    funcs = ''
    term = term.replace(' ', '')
    term = term.replace(',', '')
    chars = []
    chars += var
    chars += ')'
    for i in range(len(term)):
        if term[i] not in chars:
            funcs += term[i]

    return funcs

def check(arr, var):
    for a in arr:
        for v in var:
            if a == v:
                return True
    return False

def split_vars(term):
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

def split_vars2(term, var):
    s = []
    for i in range(len(term)):
        for v in var:
            if term[i] == v:
                s += v
    return s

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

def replace_var(term, s1, s2):
    part = find(term, s1)
    part_ex = []
    for j in range(len(part)):
        p = term[:part[j]] + s2 + term[part[j] + len(s1):]
        part_ex.append(p)
    return part_ex

def check2(term, rule, var):
    rules = []
    rule = rule.replace(' ', '')
    rules += rule.split("->")
    count = 0
    for i in range(len(term)-1):
        if term[i] == rules[0][0]:
            count += 1
    j = -1
    func_old = []
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
                    func_old.append(term[j: i+1])
                    cnt = -1
    # print(func_old)

    s = rules[0]
    s_rule = check_func(s, var)
    check_rule = split_vars2(s, var)
    func_old_checked = []
    for f in func_old:
        f_checked = check_func(f, var)
        if f_checked.find(s_rule) == 0:
            func_old_checked.append(f)

    # print(func_old_checked)

    func_new = []
    sts = []
    for s in func_old_checked:
        cnt1 = s.find(s_rule)
        cnt2 = 0
        count = 1
        for i in range(cnt1 + 2, len(s)):
            if s[i] == '(':
                count += 1
            if s[i] == ')':
                count -= 1
                if count == 0:
                    cnt2 = i
        str = s[cnt1: cnt2+1]
        sts.append(str)

    # print(sts)
    sts2 = []
    for s in sts:
        cnt1 = len(s_rule)
        cnt2 = 0
        count = 1
        for i in range(cnt1, len(s)):
            if s[i] == '(':
                count += 1
            if s[i] == ')':
                count -= 1
                if count == 0:
                    cnt2 = i
        str = s[cnt1-2: cnt2 + 1]
        sts2.append(str)

    st = []
    for s in sts2:
        st.append(split_vars(s))
    # print(st)

    for t in range(len(st)):
        s = rules[1]
        if check(s, var):
            if len(check_rule) > 1:
                if check_rule[0] == check_rule[1]:
                    if len(st[t]) > 1 and st[t][0] == st[t][1]:
                        s = s.replace(var[0], st[t][0])
                    else:
                        s = '' #str2[t]
                else:
                    for i in range(len(check_rule)):
                        s = s.replace(check_rule[i], st[t][i])

            else:
                for i in range(len(check_rule)):
                    s = s.replace(check_rule[i], st[t][i])

        func_new.append(s)
    # print(func_old_checked)
    # print(func_new)
    s_final = []
    for i in range(len(st)):
        if func_new[i] != '':
            s = replace_var(term, func_old_checked[i], func_new[i])
            s_final += s

    s_final = list(set(s_final))
    s_final = [x for x in s_final if x != '' and x != term]
    # print(s_final)
    return s_final

# str = 'f(h(h(g(h(x),y))))'
# check2(str, 'h(g(x,y)) -> g(y,x)', ['x', 'y', 't', 'z'])
# str = 'f(t,z)'
# check2(str, 'f(x,y) -> f(y,x)', ['x', 'y', 't', 'z'])

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

if __name__ == "__main__":
    main()
