import sys
import re
from tabulate import tabulate

inMulcom = False

inLineCom = False

FA_state = 'p'

cyk = [[]]

startstate = "S"

grammar = [{}, {}]

grammar[0] = {
    startstate: ["NpVp", "MulcomEmulcom", "ComMulcom", "LinecomCom", "SCom"],
    "Vp": ["VpPp", "XNp", "eats"],
    "Pp": ["YNp"],
    "Np": ["DetZ", "she"],
    "X": ["eats"],
    "Y": ["with"],
    "Z": ["fish", "fork"],
    "Det": ["a"],
    "Emulcom": ["ComMulcom", "ComEmulcom"],
    "Linecom": ["LinecomCom"],
    "Com": ["ComCom"]
}

grammar[1] = {
    startstate: ["NpVp", "MulcomEmulcom", "ComMulcom", "LinecomCom", "SCom"],
    "Vp": ["VpPp", "XNp", "eats"],
    "Pp": ["YNp"],
    "Np": ["DetZ", "she"],
    "X": ["eats"],
    "Y": ["with"],
    "Z": ["fish", "fork"],
    "Det": ["a"],
    "Emulcom": ["ComMulcom", "ComEmulcom"],
    "Linecom": ["LinecomCom"],
    "Com": ["ComCom"]
}

Error = 0

Errors = ["Syntax", "Naming"]


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


def getCombinations(verticals, diagonals, order=0):
    combinations = list()
    # Find Combinations
    for vert_states, diag_states in zip(verticals, diagonals):
        # Test for all vertical and diagonal combinations
        for vert_state in vert_states:
            for diag_state in diag_states:
                current_state = vert_state + diag_state
                for prev_state, next_states in grammar[order].items():
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


def makeCYKTable(line, order=0):
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
        for key, value in grammar[order].items():
            if word in value:
                cyk[0][i].append(key)
        if (inMulcom and not ('"""' in word or "'''" in word)) or (inLineCom):
            if i == 0:
                cyk[0][i].append(startstate)
            cyk[0][i].append("Com")
        # If line is not in the next state, line is a variable -> check for variable validity
        # Also Check for comments, multiline comments, string, and num
        if len(cyk[0][i]) == 0:
            if (('"""' in word[:4] and '"""' in word[-4:]) or ("'''" in word[:4] and "'''" in word[-4:])) and len(word) >= 6:
                cyk[0][i].append(startstate)
                cyk[0][i].append("Mulcom")
            elif '"""' in word[:4] or "'''" in word[:4]:
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
                print(word)
                Error = 1
                return [[[]]]

    # Make CYK Table for line
    # offset and position
    for offset in range(1, len(line)):
        # Add line to table
        cyk.append([])
        # iterate for each position in line minus the offset (next lines are 1 shorter than the last)
        for position in range(len(line) - offset):
            verticals, diagonals = getCompSets(offset, position)
            cyk[-1].append(getCombinations(verticals, diagonals, order=order))
    Error = 0
    return cyk


def outputTable(Table, line):
    tab = [[', '.join(y) for y in x] for x in Table]
    print(tabulate(tab, line, tablefmt="fancy_grid", showindex="always"))


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
        re.split('([^\w\'\"])', line) for line in ori if line]
    contents = [[word for word in line if word and word != ' ']
                for line in contents]
    f.close()
    return contents, ori


def checkFile(file, readTable=False):
    if readTable == False:
        for i, line in enumerate(file):
            if not checkValid(line):
                return False, i
        return True, None
    else:
        for i, line in enumerate(file):
            if not checkValid(line, readTable=True):
                return False, i
        return True, None


def getIdxLine(lines, list, minline):
    for i, line in enumerate(lines):
        if i >= minline and all(word in line for word in list):
            return i
    return -1


if __name__ == "__main__":
    if len(sys.argv) != 1:
        for i, args in enumerate(sys.argv[1:]):
            file, ori = readFile(args)
            print(file)
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
