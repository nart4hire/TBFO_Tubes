import sys
import re
from tabulate import tabulate

inMulcom = False

inLineCom = False

FA_state = 'p'

cyk = [[]]

startstate = "S"

grammar = {
    startstate: ["break", "ReturnANNY", "continue", "MulcomEmulcom", "ComMulcom", "LinecomCom", "SCom", "H0End", "H1EXPR", "H2End", "break", "H3End", "If_funcSUITE1", "H4End", "WH_FSUITE1", "ElseEnd", "ELS_FSUITE1", "ImportH5", "H6H5", "H7H5", "H8H5", "H9End", "H10End", "FO_FSUITE1", "H11End", "H12EXPR", "H12ANNY", "H13Pc", "H14METHOD", "H15End", "ELF_FSUITE1"],
    "SUITE1": ["H12EXPR", "H12ANNY", "break", "H13Pc", "H14METHOD"],
    "EXPR": ["H16Singles", "H17Singles", "H18METHOD", "H19Singles", "H20Pc", "not_funcSingles", "H21ARRG", "H13Pc", "H14METHOD", "True", "False", "None", "H22ANNY", "H23ANNY", "Var", "Str", "Num", "H24EXPR", "H25Pc", "H26zqC", "zqOzqC", "H27zqC", "H28zqC", "H29CClose", "COpenCClose", "H30Pc", "POpenPc", "H31Pc", "H32Pc"],
    "not_func": ["not_funcnot_real", "not"],
    "ARRG": ["H21ARRG", "H26zqC", "zqOzqC", "H27zqC", "H28zqC", "H29CClose", "COpenCClose", "Var", "Str", "Num", "H30Pc", "POpenPc", "H31Pc", "H32Pc", "H13Pc", "H14METHOD"],
    "ARG_DICT": ["H33ARG_DICT", "H34ANNY"],
    "Any_Dict": ["H34ANNY"],
    "ANNY": ["Var", "Str", "Num", "H13Pc", "H14METHOD", "H26zqC", "zqOzqC", "H27zqC", "H28zqC", "H29CClose", "COpenCClose", "H30Pc", "POpenPc", "H31Pc", "H32Pc"],
    "Singles": ["Var", "Str", "Num"],
    "METHOD": ["H13Pc", "H14METHOD"],
    "If_func": ["H3End", "If_funcSUITE1"],
    "INL_IF": ["H35EXPR", "H36ELS_F", "H37EXPR"],
    "INL_FOR": ["H38EXPR", "H39EXPR", "H40ELS_F"],
    "ELF_F": ["H15End", "ELF_FSUITE1"],
    "ELS_F": ["ElseEnd", "ELS_FSUITE1"],
    "WH_F": ["H4End", "WH_FSUITE1"],
    "FO_F": ["H10End", "FO_FSUITE1", "H11End"],
    "is_Func": ["H24EXPR", "H25Pc"],
    "Comma": [","],
    "Import": ["import"],
    "Return": ["return"],
    "DEF_R": ["def"],
    "While": ["while"],
    "For": ["for"],
    "Assign": ["="],
    "Comp": [">", "<", "LegrAssign", "ExclamAssign", "AssignAssign"],
    "Legr": [">", "<"],
    "Exclam": ["!"],
    "OPR": ["+", "-", "/", "DivDiv", "%", "*", "MulMul"],
    "Div": ["/"],
    "Mul": ["*"],
    "POpen": ["("],
    "Pc": [")"],
    "zqC": ["]"],
    "zqO": ["["],
    "COpen": ["{"],
    "CClose": ["}"],
    "Elif": ["elif"],
    "Else": ["else"],
    "If_real": ["if"],
    "End": [":"],
    "Class": ["class"],
    "AS_R": ["as"],
    "From": ["from"],
    "With": ["with"],
    "IN_R": ["in"],
    "not_real": ["not"],
    "is_real": ["is"],
    "Per": ["and", "or"],
    "H0": ["H41Pc"],
    "H1": ["H42Return"],
    "H2": ["ClassH5"],
    "H3": ["If_realEXPR"],
    "H4": ["WhileEXPR"],
    "H5": ["Var"],
    "H6": ["H43AS_R"],
    "H7": ["H44Import"],
    "H8": ["H45AS_R"],
    "H9": ["H46EXPR"],
    "H10": ["ForEXPR"],
    "H11": ["H47EXPR"],
    "H12": ["H5Assign"],
    "H13": ["H48EXPR"],
    "H14": ["H50H49"],
    "H15": ["ElifEXPR"],
    "H16": ["H5OPR"],
    "H17": ["H5Per"],
    "H18": ["H5H49"],
    "H19": ["H5Comp"],
    "H20": ["POpenEXPR"],
    "H21": ["ANNYComma"],
    "H22": ["SinglesIN_R"],
    "H23": ["H51IN_R"],
    "H24": ["H5is_real"],
    "H25": ["POpenis_Func"],
    "H26": ["zqOARRG"],
    "H27": ["zqOINL_FOR"],
    "H28": ["zqOINL_IF"],
    "H29": ["COpenARG_DICT"],
    "H30": ["POpenARRG"],
    "H31": ["POpenINL_FOR"],
    "H32": ["POpenINL_IF"],
    "H33": ["Any_DictComma"],
    "H34": ["SinglesEnd"],
    "H35": ["ANNYIf_real"],
    "H36": ["H35EXPR"],
    "H37": ["INL_IFFor"],
    "H38": ["ANNYFor"],
    "H39": ["INL_FORIf_real"],
    "H40": ["H39EXPR"],
    "H41": ["H52EXPR"],
    "H42": ["H0End"],
    "H43": ["ImportH5"],
    "H44": ["FromH5"],
    "H45": ["H7H5"],
    "H46": ["H53AS_R"],
    "H47": ["EXPRFor"],
    "H48": ["H5POpen"],
    "H49": ["Dot"],
    "H50": ["H13Pc"],
    "H51": ["ForSingles"],
    "H52": ["H54POpen"],
    "H53": ["WithEXPR"],
    "H54": ["DEF_RH5"],
    "Emulcom": ["ComMulcom", "ComEmulcom"],
    "Linecom": ["LinecomCom"],
    "Com": ["ComCom"]
}

Error = 0

Errors = ["Syntax", "Naming", "Outside Primitive"]


def isLetter(unsigned):
    c = ord(unsigned)
    return 65 <= c <= 90 or 97 <= c <= 122


def isNumber(unsigned):
    c = ord(unsigned)
    return 48 <= c <= 57


def DFA(char):
    global FA_state
    if FA_state == 's':
        if isLetter(char) or char == '_':
            FA_state = 'a'
            return True
        else:
            FA_state = 'r'
            return False
    elif FA_state == 'a':
        if isLetter(char) or isNumber(char) or char == '_':
            return True
        else:
            FA_state = 'r'
            return False
    elif FA_state == 'r':
        return False


def checkVar(string):
    global FA_state
    FA_state = 's'
    for char in string:
        Accepted = DFA(char)
    return Accepted


def getCombinations(verticals, diagonals):
    combinations = list()
    # Find Combinations
    for vert_states, diag_states in zip(verticals, diagonals):
        # Test for all vertical and diagonal combinations
        for vert_state in vert_states:
            for diag_state in diag_states:
                current_state = vert_state + diag_state
                for prev_state, next_states in grammar.items():
                    if current_state in next_states and prev_state not in combinations:
                        combinations.append(prev_state)
    return combinations


def getCompSets(offset, position):
    verticals = []
    diagonals = []
    i = 0
    # get vertical and diagonal sets
    while i < len(cyk) - 1:
        # verticals inserted at the beginning and diagonals appended at the end for order of comparison
        verticals.insert(0, cyk[i][position])
        diagonals.append(cyk[i][position + offset])
        offset -= 1
        i += 1
    return verticals, diagonals


def makeCYKTable(line):
    # Make an empty 2d array
    global cyk, Error, inMulcom, inLineCom
    cyk = [[]]
    inLineCom = False
    # Get CNF form of all words in line
    # Iterate through list of words
    for i, word in enumerate(line):
        # Make Empty State List
        cyk[0].append([])
        # If line is the next state return previous state for all matching states
        for key, value in grammar.items():
            if word in value:
                cyk[0][i].append(key)
        if (inMulcom and not ('"""' in word or "'''" in word)) or (inLineCom):
            if i == 0:
                cyk[0][i].append(startstate)
            cyk[0][i].append("Com")
        # If line is not in the next state, line is a variable -> check for variable validity
        # Also Check for comments, multiline comments, string, and num
        if len(cyk[0][i]) == 0:
            if (('"""' in word[: 4] and '"""' in word[-4:]) or ("'''" in word[: 4] and "'''" in word[-4:])) and len(word) >= 6:
                cyk[0][i].append(startstate)
                cyk[0][i].append("Mulcom")
            elif '"""' in word[: 4] or "'''" in word[: 4]:
                if not inMulcom or len(word) == 3:
                    cyk[0][i].append(startstate)
                cyk[0][i].append("Mulcom")
                inMulcom = not inMulcom
            elif '"""' in word[-4:] or "'''" in word[-4:]:
                if inMulcom or len(word) == 3:
                    cyk[0][i].append(startstate)
                cyk[0][i].append("Mulcom")
                inMulcom = not inMulcom
            elif ('#' in word[0]):
                cyk[0][i].append(startstate)
                cyk[0][i].append("Linecom")
                inLineCom = True
            elif ('"' in word[0] and '"' in word[-1]) or ("'" in word[0] and "'" in word[-1]):
                cyk[0][i].append("Str")
            elif all(isNumber(x) for x in word):
                cyk[0][i].append("Num")
            elif checkVar(word):
                cyk[0][i].append("Var")
            else:
                Error = 1
                return [[[]]]
            for key, value in grammar.items():
                for state in cyk[0][i]:
                    if state in value:
                        cyk[0][i].append(key)

    # Make CYK Table for line
    # offset and position
    for offset in range(1, len(line)):
        # Add line to table
        cyk.append([])
        # iterate for each position in line minus the offset (next lines are 1 shorter than the last)
        for position in range(len(line) - offset):
            verticals, diagonals = getCompSets(offset, position)
            cyk[-1].append(getCombinations(verticals, diagonals))
    Error = 0
    return cyk


def outputTable(Table, line):
    tab = [[', '.join(y) for y in x] for x in Table]
    print(tabulate(tab, line, tablefmt="pretty"))


def checkValid(line, readTable=False):
    if readTable == False:
        return startstate in makeCYKTable(line)[-1][-1]
    else:
        Table = makeCYKTable(line)
        outputTable(Table, line)
        return startstate in Table[-1][-1]


def readFile(file):
    f = open(file, 'r')
    ori = f.read().split('\n')
    contents = [
        re.findall('\".+?\"||[\w]+||[\W]+?', line) for line in ori if line]
    contents = [[word for word in line if word and word != ' ']
                for line in contents]
    f.close()
    return contents, ori


def checkFile(file, readTable=False):
    global Error
    Stack = []
    if readTable == False:
        for i, line in enumerate(file):
            if not checkValid(line):
                return False, i
            if (line[0] in "def") and ("def" not in Stack):
                if "if" in Stack:
                    Stack.remove("if")
                if "loop" in Stack:
                    Stack.remove("loop")
                Stack.append("def")
            elif (line[0] in "if") and ("if" not in Stack):
                Stack.append(line[0])
            elif (line[0] in "forwhile") and ("loop" not in Stack):
                Stack.append("loop")
            elif (line[0] in "return") and ("def" not in Stack):
                Error = 2
                return False, i
            elif (line[0] in "elifelse") and ("if" not in Stack):
                Error = 2
                return False, i
            elif (line[0] in "else") and ("if" in Stack):
                Stack.remove("if")
            elif (line[0] in "breakcontinue") and ("loop" not in Stack):
                Error = 2
                return False, i
        return True, None
    else:
        for i, line in enumerate(file):
            if not checkValid(line, readTable=True):
                return False, i
            if (line[0] in "def") and ("def" not in Stack):
                if "if" in Stack:
                    Stack.remove("if")
                if "loop" in Stack:
                    Stack.remove("loop")
                Stack.append("def")
            elif (line[0] in "if") and ("if" not in Stack):
                Stack.append(line[0])
            elif (line[0] in "forwhile") and ("loop" not in Stack):
                Stack.append("loop")
            elif (line[0] in "return") and ("def" not in Stack):
                Error = 2
                return False, i
            elif (line[0] in "elifelse") and ("if" not in Stack):
                Error = 2
                return False, i
            elif (line[0] in "else") and ("if" in Stack):
                Stack.remove("if")
            elif (line[0] in "breakcontinue") and ("loop" not in Stack):
                Error = 2
                return False, i
        return True, None


def getIdxLine(lines, list, minline):
    for i, line in enumerate(lines):
        if i >= minline and all(word in line for word in list):
            return i
    return -1


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[-1] in 'y':
        for i, args in enumerate(sys.argv[1: -1]):
            file, ori = readFile(args)
            if sys.argv[-1] in 'y':
                valid, line = checkFile(file, readTable=True)
            else:
                valid, line = checkFile(file)
            if valid:
                print("File %d" % (i + 1) + " successfully compiled.")
            else:
                x = getIdxLine(ori, file[line], line)
                print("File %d" % (i + 1) + " had a %s error." % Errors[Error])
                print("(Error Located at line: %d, in '%s')" % (x + 1, ori[x]))

    elif len(sys.argv) > 1:
        for i, args in enumerate(sys.argv[1:]):
            file, ori = readFile(args)
            valid, line = checkFile(file)
            if valid:
                print("File %d" % (i + 1) + " successfully compiled.")
            else:
                x = getIdxLine(ori, file[line], line)
                print("File %d" % (i + 1) + " had a %s error." % Errors[Error])
                print("(Error Located at line: %d, in '%s')" % (x + 1, ori[x]))

    else:
        filename = input('Input file name :')
        debug = input('Debug :')
        file, ori = readFile(filename)
        if debug.lower() in 'y':
            valid, line = checkFile(file, readTable=True)
        else:
            valid, line = checkFile(file)
        if valid:
            print("File successfully compiled.")
        else:
            x = getIdxLine(ori, file[line], line)
            print("File had a %s error." % Errors[Error])
            print("(Error Located at line: %d, in '%s')" % (x + 1, ori[x]))
