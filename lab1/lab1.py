import z3
import sys

va1 = []
va2 = []

def check(arr, var):
    for a in arr:
        if a == var:
            return True
    return False

def formSMT(str, v):
    var1 = []
    splitt = []
    cou = []
    for j in v:
        if not check(str, j):
            cou.append(0)
        else:
            for i in range(len(str)-1):
                if str[i] == j and str[i+1] == '*':
                    cou.append(i-3)
    cou.append(len(str))
    cou.sort()
    # print(cou)
    th = 1
    for i in range(len(cou)):
        if cou[i] != 0:
            splitt.append(str[0: cou[i]])
            break
    for i in range (0, len(cou) - 1):
        if cou[i] == 0:
            splitt.append('0')
            th += 1
        else:
            while cou[th] == 0:
                th += 1
            splitt.append(str[cou[i]+3: cou[th]])
            th += 1
    for i in range(len(splitt)):
        for j in range(len(splitt[i])):
            for var in v:
                if j < len(splitt[i]) and splitt[i][j] == '+' and splitt[i][0] == var:
                    splitt[0] += splitt[i][j-1:]
                    splitt[i] = splitt[i][:j-1]
    # print(splitt)
    # print('thang')
    count = []
    for i in range(len(splitt)):
        j = i + 1
        while j < len(splitt):
            for var in v:
                if splitt[i][0] == var and splitt[j][0] == var:
                    splitt[i] += " + " + splitt[j]
                    count.append(splitt[j])
                    splitt[j] = "wrong"

            j+=1

    for j in count:
        splitt.remove("wrong")

    if len(v) > 1:
        if v[0] == splitt[2][0]:
            splitt[1], splitt[2] = splitt[2], splitt[1]

    for i in range(len(splitt)):
        if splitt[i][len(splitt[i]) - 1] == '*':
            splitt[i] = splitt[i][:len(splitt[i]) - 1]
    #//////////////////////////////////////////////

    for i in range(len(splitt)):
        for j in range(len(splitt[i])):
            for var in v:
                if j < len(splitt[i]) and splitt[i][j] == var:
                    if j == 0:
                        splitt[i] = splitt[i][2:]
                    else:
                        splitt[i] = splitt[i][:j] + splitt[i][j+2:]

    for k in range(len(splitt)):
        part = []
        part1 = []
        count = 0
        for i in  range(len(splitt[k])):
            if splitt[k][i] == '+':
                s = splitt[k][count: i-1]
                part.append(s)
                count = i + 2
        part.append(splitt[k][count: len(splitt[k])])
        for l in range(len(part)):
            if part[l][len(part[l]) - 1] == '*':
                part[l] = part[l][:len(part[l]) - 1]

        for i in range(0, len(part)):
            p = part[i].split("*")
            part1.append(p)

        str2 = ""
        if len(part1) > 1:
            str2 += "(+ "

        for i in range(0, len(part1)):
            if len(part1[i]) > 1:
                str2 += '(* '
                for j in range(0, len(part1[i])):
                    str2 += part1[i][j] + " "

                str2 += ')'
            else:
                str2 += part[i] + " "
        if len(part1) > 1:
            str2 += ")"
        var1.append(str2)

    # print(var1 )
    # print('\n')
    return var1

def main():
    inp = ""
    # while True:
    #     line = input()
    #     if len(line) == 0:
    #         break
    #     inp += ' ' + line

    for line in sys.stdin:
        if len(line) == 1:
            break
        inp += line

    inp = inp[:len(inp) - 1]
    print(inp)
    funcs = []
    variables = []

    #
    for i in range(len(inp) - 1):
        if inp[i + 1] == '(' and not check(funcs, inp[i]):
            funcs.append(inp[i])
        elif inp[i] != ')' and (inp[i - 1] == '(' or inp[i + 1] == ')') and not check(variables, inp[i]) and not check(funcs, inp[i]):
            variables.append(inp[i])

    #
    divide = []
    thangs = []
    thang = ""
    for s in inp:
        if s == '\n':
            thangs.append(thang)
            thang = ""
            continue
        thang += s
    thangs.append(thang)

    for s in thangs:
        divide.append(s.split(" -> "))
    # print(divide)
    scheme = []
    for t in divide:
        for f in t:
            for i in range(len(f)):
                if f[i] == ',':
                    f = f[:i] + f[i + 1:]
                if check(funcs, f[i]) and f[i + 1] == '(':
                    f = f[:i] + '(' + f[i] + ' ' + f[i + 2:]
            scheme.append(f.replace("  ", " "))
    print(scheme)
    #
    coefcounter = 0
    coefs = []
    for f in funcs:
        left = 0
        right = 0
        checkleft = False
        checkright = False
        count = 0
        for s in scheme:
            if checkright:
                break
            for i in s:
                if i == f:
                    checkleft = True
                if checkleft:
                    if left == right and i == ' ':
                        count += 1
                    if i == '(':
                        left += 1
                    if i == ')':
                        right += 1
                    if right - left == 1:
                        checkright = True
                        break
        count += 1
        coeff = []
        for i in range(count):
            coeff.append('t' + str(coefcounter))
            coefcounter += 1
        coefs.append(coeff)

    #
    mess = "(set-logic QF_NIA)\n"
    for i in coefs:
        for j in i:
            mess += "(declare-fun " + j + " () Int)\n"

    print("Functions and their coefficients:")
    for i in range(len(funcs)):
        print(funcs[i], coefs[i])

    print("\nVariables:")
    print(variables)

    #
    smt1 = []
    for s in scheme:
        ready = False
        while not ready:
            for j in range(len(funcs)):
                for i in range(len(s)):
                    if i < len(s) and s[i] == funcs[j]:
                        s = s[:i] + coefs[j][len(coefs[j]) - 1] + ' + ' + s[i + 1 + len(funcs[j]):]
                        i += 3 + len(coefs[j][len(coefs[j]) - 1])
                        const = i
                        count = 0
                        left = 0
                        right = 0
                        part = ""
                        while i < len(s) and count != len(coefs[j]) - 1:
                            part += s[i]
                            if s[i] == '(':
                                left += 1
                            if s[i] == ')':
                                right += 1
                                if left != 0 and left == right:
                                    count += 1
                                    if check(variables, s[const]):
                                        part = part[4:]
                                    if count == len(coefs[j]) - 1:
                                        s = s[:i - len(part) + 1] + part + "*" + coefs[j][count - 1] + s[i + 1:]
                                        i += len(part) - 5 + len(coefs[j][count - 1])
                                    else:
                                        s = s[:i - len(part) + 1] + part + "*" + coefs[j][count - 1] + " + " + s[
                                                                                                                   i + 1:]
                                        i += len(part) - 4 + len(coefs[j][count - 1])  # -1
                                    part = ""
                                    left = 0
                                    right = 0
                                    count = 1
                            if i < len(s) and left == right and check(variables, s[i]):
                                count += 1
                                if count != len(coefs[j]) - 1:
                                    s = s[:i] + s[i] + "*" + coefs[j][count - 1] + " +" + s[i + 1:]
                                else:
                                    s = s[:i] + s[i] + "*" + coefs[j][count - 1] + s[i + 1:]
                                i += 1 + len(coefs[j][count - 1])
                            i += 1
            ready = True
            for f in funcs:
                for i in s:
                    if i == f:
                        ready = False
                        break
        smt1.append(s)

    for i in range(len(smt1)):
        if smt1[i][0] == '(' and smt1[i][len(smt1[i]) - 1] == ')':
            smt1[i] = smt1[i][1:len(smt1[i]) - 1]

    #
    smt2 = []
    for s in smt1:
        while check(s, '('):
            for i in range(len(s)):
                v3 = []
                part = ""
                if i < len(s) and s[i] == '(':
                    start = i
                    i += 1
                    while s[i] != ')':
                        if s[i] == '(':
                            break
                        if s[i] == ' ':
                            if part != "":
                                v3.append(part)
                            part = ""
                            i += 1
                            continue
                        if s[i] != '+':
                            part += s[i]
                        i += 1
                    if part != "":
                        v3.append(part)
                        i += 1
                        end = i
                        i += 1
                        multi = ""
                        while i < len(s) and s[i] != ' ' and s[i] != ')':
                            multi += s[i]
                            i += 1
                        end += len(multi) + 1
                        result = ""
                        for k in range(len(v3) - 1):
                            result += v3[k] + "*" + multi + " + "
                        result += v3[len(v3) - 1] + "*" + multi
                        s = s[:start] + result[:len(result)] + s[end:]
        smt2.append(s)
    # print(smt2)

    for i in range(0, len(smt2), 2):
        v1 = formSMT(smt2[i], variables)
        va1.append(v1)
        v2 = formSMT(smt2[i+1], variables)
        va2.append(v2)

    # print(va1)
    # print(va2)
    mess += "\n"
    for k in range(len(va1)):
        mess += ""
        minx = len(va1[k])
        for i in range(minx):
            mess += "(assert (>= " + va1[k][i] + " " + va2[k][i]+ "))\n\n"

    mess += "(assert (and "
    for i in range(len(coefs)):
        for j in range(len(coefs[i]) - 1):
            mess += "(>= " + coefs[i][j] + " 1) "
        mess += "(>= " + coefs[i][len(coefs[i]) - 1] + " 0)"
        if i != len(coefs) - 1:
            mess += " "
    mess += "))\n\n"
    for k in range(len(va1)):
        mess += "(assert (or "
        for i in range(minx):
            mess += "(> " + va1[k][i] + " " + va2[k][i]+ ") "
        mess += "))\n\n"
    mess += "(assert (and "
    for i in range(len(coefs)):
        mess += "(or "
        if len(coefs[i]) > 2:
            mess += "(and "
        for j in range(len(coefs[i]) - 1):
            mess += "(> " + coefs[i][j] + " 1)"
            if j != len(coefs[i]) - 2 or (j == len(coefs[i]) - 2 and len(coefs[i]) == 2):
                mess += " "
        if len(coefs[i]) > 2:
            mess += ") "
        mess += "(> " + coefs[i][len(coefs[i]) - 1] + " 0))"
        if i != len(coefs) - 1:
            mess += " "
    mess += "))\n\n"
    mess += '''(check-sat)
(get-model)
(exit)'''
    f = open("lab1.smt2", "w")
    f.write(mess)
    f.close()
    smt_file = "lab1.smt2"
    s = z3.Solver()
    s.from_file(smt_file)

    result = s.check()

    if result == z3.sat:
        model = s.model()
        for d in model.decls():
            print(f"{d.name()} = {model[d]}")
    elif result == z3.unsat:
        print("Constraints are not satisfied")

if __name__ == '__main__':
    print('Example input: f(g(x, y)) -> g(x, y)\n')
    main()
