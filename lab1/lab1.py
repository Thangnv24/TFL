import sys

va1 = []
va2 = []
def isin(arr, func):
    for f in arr:
        if f == func:
            return True
    return False

def formSMT(str, v):
    var1 = []
    splitt = []
    cou = []
    for j in v:
        if not isin(str, j):
            cou.append(0)
        else:
            for i in range(len(str)-1):
                if str[i] == j[0] and str[i+1] == '*':
                    cou.append(i-4)
    cou.append(len(str)-1)
    th = 1
    for i in range(len(cou)):
        if cou[i] != 0:
            splitt.append(str[0: cou[i]])
            break
    for i in range (0, len(cou) - 1):
        if cou[i] == 0:
            splitt.append('0')
            th+=1
        else:
            while cou[th] ==0:
                th+=1
            splitt.append(str[cou[i]+4: cou[th]])
            th+=1

    print(cou)
    print(str)
    print(splitt)

    part = []
    part1 = []
    count = 0
    for i in  range(len(splitt[0])):
        if splitt[0][i] == '+':
            s = splitt[0][count: i-2]
            part.append(s)
            count = i + 2
    part.append(splitt[0][count: len(splitt[0])])

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
    if len(part1)>1:
        str2 += ")"
    var1.append(str2)
    part = []
    for i in range(1, len(splitt)):
        p = splitt[i].split("*")
        part.append(p)

    str2 = ""
    for i in range(0, len(part)):
        if len(part[i]) > 2:
            str2 += '(* '
            for j in range(1, len(part[i])):
                str2 += part[i][j]+" "

            str2 += ')'
        elif len(part[i]) ==1:
            str2 = part[i][0]
        elif len(part[i]) == 2:
            str2 = part[i][1]
        var1.append(str2)
    return var1

def main():
    example = ""
    for line in sys.stdin:
        if len(line) == 1:
            break
        example += line

    example = example[:len(example) - 1]
    mess = "(set-logic QF_NIA)\n"

    inqs = []
    inq = ""
    parts = []
    funcs = []
    amounts = []
    variables = []
    coefcounter = 0
    coefs = []
    smtinqs = []

    # find the list of variables
    for i in range(len(example) - 1):
        if example[i + 1] == '(' and not isin(funcs, example[i]):
            funcs.append(example[i])
        elif example[i] != ')' and (example[i - 1] == '(' or example[i + 1] == ')') and not isin(variables, example[
            i]) and not isin(funcs, example[i]):
            variables.append(example[i])

    # break the message into pairs of expressions(biểu thức)
    for s in example:
        if s == '\n':
            inqs.append(inq)
            inq = ""
            continue
        inq += s
    inqs.append(inq)

    for s in inqs:
        parts.append(s.split("->"))

    scheme = []

    # translation into Skim language
    for t in parts:
        for f in t:
            for i in range(len(f)):
                if f[i] == ',':
                    f = f[:i] + f[i + 1:]
                if isin(funcs, f[i]) and f[i + 1] == '(':
                    f = f[:i] + '(' + f[i] + ' ' + f[i + 2:]
            scheme.append(f.replace("  ", " "))

    #
    # counting the number of variables accepted by each function and creating a list of coefficients
    for f in funcs:
        left = 0
        right = 0
        foundf = False
        founda = False
        amount = 0
        for s in scheme:
            if founda:
                break
            for i in s:
                if i == f:
                    foundf = True
                if foundf:
                    if left == right and i == ' ':
                        amount += 1
                    if i == '(':
                        left += 1
                    if i == ')':
                        right += 1
                    if right - left == 1:
                        founda = True
                        break
        amount += 1
        amounts.append(amount)
        coeff = []
        for i in range(amount):
            coeff.append("t" + str(coefcounter))
            coefcounter += 1
        coefs.append(coeff)

    # объявление переменных для z3
    for i in coefs:
        for j in i:
            mess += "(declare-fun " + j + " () Int)\n"

    print("Функции и их коэффициенты (последний свободный):")
    for i in range(len(funcs)):
        print(funcs[i], coefs[i])

    print("\nПеременные:")
    print(variables)

    # 
    for s in scheme:
        ready = False
        while not ready:
            for j in range(len(funcs)):
                for i in range(len(s)):
                    if i < len(s) and s[i] == funcs[j]:
                        s = s[:i] + coefs[j][len(coefs[j]) - 1] + ' + ' + s[i + 1 + len(funcs[j]):]
                        i += 3 + len(coefs[j][len(coefs[j]) - 1])
                        varamount = 0
                        left = 0
                        right = 0
                        part = ""
                        while i < len(s) and varamount != len(coefs[j]) - 1:
                            part += s[i]
                            if s[i] == '(':
                                left += 1
                            if s[i] == ')':
                                right += 1
                                if left != 0 and left == right:
                                    varamount += 1
                                    if varamount == len(coefs[j]) - 1:
                                        s = s[:i - len(part) + 1] + part + "*" + coefs[j][varamount - 1] + s[i + 1:]
                                        i += len(part) - 5 + len(coefs[j][varamount - 1])
                                    else:
                                        s = s[:i - len(part) + 1] + part + "*" + coefs[j][varamount - 1] + " + " + s[
                                                                                                                   i + 1:]
                                        i += len(part) - 4 + len(coefs[j][varamount - 1])  # -1
                                    part = ""
                                    left = 0
                                    right = 0
                            if i < len(s) and left == right and isin(variables, s[i]):
                                varamount += 1
                                if varamount != len(coefs[j]) - 1:
                                    s = s[:i] + s[i] + "*" + coefs[j][varamount - 1] + " +" + s[i + 1:]
                                else:
                                    s = s[:i] + s[i] + "*" + coefs[j][varamount - 1] + s[i + 1:]
                                i += 1 + len(coefs[j][varamount - 1])
                            i += 1
            ready = True
            for f in funcs:
                for i in s:
                    if i == f:
                        ready = False
                        break
        smtinqs.append(s)

    for i in range(len(smtinqs)):
        if smtinqs[i][0] == '(' and smtinqs[i][len(smtinqs[i]) - 1] == ')':
            smtinqs[i] = smtinqs[i][1:len(smtinqs[i]) - 1]

    normal_ineqs = []

    # 
    for s in smtinqs:
        while isin(s, '('):
            for i in range(len(s)):
                summands = []
                part = ""
                if i < len(s) and s[i] == '(':
                    start = i
                    i += 1
                    while s[i] != ')':
                        if s[i] == '(':
                            break
                        if s[i] == ' ':
                            if part != "":
                                summands.append(part)
                            part = ""
                            i += 1
                            continue
                        if s[i] != '+':
                            part += s[i]
                        i += 1
                    if part != "":
                        summands.append(part)
                        i += 1
                        end = i
                        i += 1
                        multi = ""
                        while i < len(s) and s[i] != ' ' and s[i] != ')':
                            multi += s[i]
                            i += 1
                        end += len(multi) + 1
                        result = ""
                        for k in range(len(summands) - 1):
                            result += summands[k] + "*" + multi + " + "
                        result += summands[len(summands) - 1] + "*" + multi
                        s = s[:start] + result[:len(result)] + s[end:]
        normal_ineqs.append(s)

    va1 = formSMT(normal_ineqs[0], variables)
    va2 = formSMT(normal_ineqs[1], variables)

    print(va1)
    print(va2)

    mess += "\n"
    minx = min(len(va1), len(va2))
    for i in range(minx):
        mess += "(assert (>= " + va1[i] + " " + va2[i]+ ")\n\n"
    if len(va1) == minx:
        for i in range(minx, len(va2)):
            mess += "(assert (>= 0 "+ va2[i] + ")\n\n"

    if len(va2) == minx:
        for i in range(minx, len(va1)):
            mess += "(assert (>= "+ va1[i] + " 0" + ")\n\n"

    mess += "(assert (and "
    for i in range(len(coefs)):
        for j in range(len(coefs[i]) - 1):
            mess += "(>= " + coefs[i][j] + " 1) "
        mess += "(>= " + coefs[i][len(coefs[i]) - 1] + " 0)"
        if i != len(coefs) - 1:
            mess += " "
    mess += "))\n\n"
    mess += "(assert (or "
    for i in range(minx):
        mess += "(>= " + va1[i] + " " + va2[i]+ ") "
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

    # print(mess)

if __name__ == '__main__':
    print('Пример ввода: f(g(x, y)) -> g(x, y)\n'
          'Когда поступает пустая строка, ввод считается завершенным')
    main()


# ['a1* + a4*a0* + x*a2*a0* + y*a3*a0*', ' a4* + x*a2* + y*a3*']
# ['a1* + a4*a0* + x*a2*a0* + y*a3*a0*', ' a7* + x*a5* + y*a6*']
