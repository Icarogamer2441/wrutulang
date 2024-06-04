import sys
from random import randint

functions = {}
variables = {"spc": " "}
running_while = [False]

class Executor:
    def __init__(self, code):
        self.code = code

    def execute1(self):
        lines = self.code.split("\n")
        in_func = [False]
        endnum = 0
        funcname = [""]

        for line in lines:
            tokens = line.split() or line.split("\t")

            if tokens:
                token = tokens[0]

                if not in_func[0]:
                    if token == "fnc":
                        funcname[0] = tokens[1]
                        if tokens[2] == "[":
                            endnum += 1
                            in_func[0] = True
                            functions[funcname[0]] = []
                    elif token == "&&" or token == "" or token == "]":
                        pass
                    elif token == "import":
                        with open(f"{tokens[1]}.wru", "r") as fi:
                            Executor(fi.read()).execute1()
                    else:
                        print("Error: You can only create functions outside of an function")
                        sys.exit(1)
                elif in_func[0]:
                    if token == "if" or token == "while":
                        endnum += 1
                        functions[funcname[0]].append(" ".join(tokens))
                    elif token == "]":
                        if endnum < 1:
                            pass
                        else:
                            endnum -= 1
                            functions[funcname[0]].append(" ".join(tokens))
                    elif endnum <= 0:
                        in_func[0] = False
                        endnum = 0
                        functions[funcname[0]].pop()
                    else:
                        functions[funcname[0]].append(" ".join(tokens))
        Executor("\n".join(functions["main"])).execute2()

    def execute2(self):
        lines = self.code.split("\n")
        in_if = [False]
        varname1 = [""]
        operation = [""]
        varname2 = [""]
        ifcode = []
        endnum = 0
        in_while = [False]
        while_code = []

        for line in lines:
            tokens = line.split() or line.split("\t")

            if tokens:
                token = tokens[0]

                if not in_if[0] and not in_while[0]:
                    if token == "showln":
                        if tokens[1] == "\"":
                            if tokens[-1] == "\"":
                                msg = " ".join(tokens[2:len(tokens) - 1])
                                print(msg, end="")
                            else:
                                print("Error: use \" to close an string")
                                sys.exit(1)
                        elif tokens[1] == "\\n":
                            print("\n", end="")
                        elif tokens[1] == "\\spc":
                            print(" ", end="")
                        else:
                            print(variables.get(tokens[1]), end="")
                    elif token == "int":
                        varname = tokens[1]
                        if tokens[2] == ":":
                            value = int(tokens[3])
                            variables[varname] = value
                        else:
                            print("Error: use : to atribute a value to an variable")
                            sys.exit(1)
                    elif token == "string":
                        varname = tokens[1]
                        if tokens[2] == ":":
                            value = " ".join(tokens[3:])
                            variables[varname] = value
                        else:
                            print("Error: use : to atribute a value to an variable")
                            sys.exit(1)
                    elif token == "call":
                        funcname = tokens[1]
                        Executor("\n".join(functions[funcname])).execute2()
                    elif token == "if":
                        varname1[0] = tokens[1]
                        operation[0] = tokens[2]
                        if len(tokens) == 5:
                            varname2[0] = tokens[3]
                            if tokens[4] == "[":
                                in_if[0] = True
                                endnum += 1
                                ifcode = []
                        else:
                            if operation[0] == "[":
                                in_if[0] = True
                                endnum += 1
                                ifcode = []
                    elif token == "bool":
                        varname = tokens[1]
                        if tokens[2] == ":":
                            if tokens[3] == "ok":
                                variables[varname] = 1
                            elif tokens[3] == "no":
                                variables[varname] = 0
                            else:
                                print(f"Error: use 'ok' or 'no' ('ok' = 1 (true). 'no' = 0 (false))")
                        else:
                            print("Error: use : to atribute a value to an variable")
                            sys.exit(1)
                    elif token == "while":
                        if tokens[1] == "[":
                            in_while[0] = True
                            while_code = []
                            endnum += 1
                            running_while[0] = True
                        else:
                            print("Error: use [ to open a while loop")
                            sys.exit(1)
                    elif token == "stop":
                        running_while[0] = False
                    elif token == "mod":
                        varname11 = tokens[1]
                        if tokens[2] == "<":
                            varname22 = tokens[3]
                            variables[varname11] += variables.get(varname22)
                        else:
                            print("Error: use < to modify the second var to the first var")
                            sys.exit(1)
                    elif token == "input":
                        inptype = tokens[1]
                        if inptype == "int":
                            varname = tokens[2]
                            variables[varname] = int(input())
                        elif inptype == "string":
                            varname = tokens[2]
                            variables[varname] = input()
                    elif token == "float":
                        varname = tokens[1]
                        if tokens[2] == ":":
                            value = float(tokens[3])
                            variables[varname] = value
                        else:
                            print("Error: use : to atribute a value to an variable")
                            sys.exit(1)
                    elif token == "rand":
                        varname11 = tokens[1]
                        varname22 = tokens[2]
                        if varname11.isdigit():
                            varname11 = int(varname11)
                            if varname22.isdigit:
                                varname22 = int(varname22)
                                outputvar = tokens[3]
                                variables[outputvar] = randint(varname11, varname22)
                            else:
                                outputvar = tokens[3]
                                variables[outputvar] = randint(varname11, variables.get(varname22))
                        elif varname22.isgidit:
                            varname22 = int(varname22)
                            outputvar = tokens[3]
                            variables[outputvar] = randint(variables.get(varname11), varname22)
                        else:
                            outputvar = tokens[3]
                            variables[outputvar] = randint(variables.get(varname11), variables.get(varname22))
                    elif token == "list":
                        varname = tokens[1]
                        variables[varname] = []
                    elif token == "listapp":
                        listvarname = tokens[1]
                        varname = tokens[2]
                        variables[listvarname].append(variables.get(varname))
                    elif token == "listpop":
                        listvarname = tokens[1]
                        variables[listvarname].pop()
                    elif token == "getlistitem":
                        listvarname = tokens[1]
                        itempos = tokens[2]
                        if tokens[3] == ">":
                            if itempos.isdigit():
                                outputvar = tokens[4]
                                variables[outputvar] = variables.get(listvarname)[int(itempos)]
                            else:
                                outputvar = tokens[4]
                                variables[outputvar] = variables.get(listvarname)[variables.get(itempos)]
                        else:
                            print("Error: use > to reference the output var")
                            sys.exit(1)
                    elif token == "split":
                        varname = tokens[1]
                        listvarname = tokens[2]
                        variables[listvarname] = variables.get(varname).split()
                    elif token == "&&" or token == "" or token == "]":
                        pass
                    elif token == "file":
                        ftype = tokens[1]
                        if ftype == "read":
                            filename = variables.get(tokens[2])
                            with open(filename, "r") as fi:
                                outputvar = tokens[3]
                                variables[outputvar] = fi.read()
                        elif ftype == "write":
                            filename = variables.get(tokens[2])
                            with open(filename, "w") as fi:
                                fi.write(variables.get(tokens[3]))
                        elif ftype == "append":
                            filename = variables.get(tokens[2])
                            with open(filename, "a") as fi:
                                fi.write(variables.get(tokens[3]))
                        else:
                            print("Error: Unknown file interact type. use 'append' or 'read' or 'write'.")
                            sys.exit(1)
                    elif token == "listchar":
                        varname = tokens[1]
                        outputvar = tokens[2]
                        variables[outputvar] = list(variables.get(varname))
                    elif token == "len":
                        varname = tokens[1]
                        outputvar = tokens[2]
                        variables[outputvar] = len(variables.get(varname))
                    elif token == "splitchar":
                        varname = tokens[1]
                        chartosplit = tokens[2]
                        if chartosplit == "\\n":
                            outputvar = tokens[3]
                            variables[outputvar] = variables.get(varname).split("\n")
                        else:
                            outputvar = tokens[3]
                            variables[outputvar] = variables.get(varname).split(chartosplit)
                    elif token == "join":
                        varname11 = tokens[1]
                        varname22 = tokens[2]
                        outputvar = tokens[3]
                        variables[outputvar] = variables.get(varname11) + " " + variables.get(varname22)
                    elif token == "join2":
                        varname11 = tokens[1]
                        varname22 = tokens[2]
                        outputvar = tokens[3]
                        variables[outputvar] = variables.get(varname11) + variables.get(varname22)
                    else:
                        print(f"Error: unknown token: {token}")
                        sys.exit(1)
                elif in_if[0]:
                    if token == "if" or token == "while":
                        endnum += 1
                        ifcode.append(" ".join(tokens))
                    elif token == "]":
                        if endnum > 0:
                            endnum -= 1
                            ifcode.append(" ".join(tokens))
                        else:
                            print("", end="")
                        
                        if endnum < 1:
                            endnum = 0
                            in_if[0] = False
                            ifcode.pop()
                            if operation[0] == "=":
                                if variables.get(varname1[0]) == variables.get(varname2[0]):
                                    Executor("\n".join(ifcode)).execute2()
                            elif operation[0] == "!":
                                if variables.get(varname1[0]) != variables.get(varname2[0]):
                                    Executor("\n".join(ifcode)).execute2()
                            elif operation[0] == ">>":
                                if variables.get(varname1[0]) >= variables.get(varname2[0]):
                                    Executor("\n".join(ifcode)).execute2()
                            elif operation[0] == "<<":
                                if variables.get(varname1[0]) <= variables.get(varname2[0]):
                                    Executor("\n".join(ifcode)).execute2()
                            elif operation[0] == ">":
                                if variables.get(varname1[0]) > variables.get(varname2[0]):
                                    Executor("\n".join(ifcode)).execute2()
                            elif operation[0] == "<":
                                if variables.get(varname1[0]) < variables.get(varname2[0]):
                                    Executor("\n".join(ifcode)).execute2()
                            elif operation[0] == "[":
                                if variables.get(varname1[0]):
                                    Executor("\n".join(ifcode)).execute2()
                            elif operation[0] == "starts":
                                if variables.get(varname1[0]).startswith(varname2[0]):
                                    Executor("\n".join(ifcode)).execute2()
                            elif operation[0] == "ends":
                                if variables.get(varname1[0]).endswith(varname2[0]):
                                    Executor("\n".join(ifcode)).execute2()
                    else:
                        ifcode.append(" ".join(tokens))
                elif in_while[0]:
                    if token == "if" or token == "while":
                        endnum += 1
                        while_code.append(" ".join(tokens))
                    elif token == "]":
                        if endnum > 0:
                            endnum -= 1
                            while_code.append(" ".join(tokens))
                        else:
                            print("", end="")
                        
                        if endnum < 1:
                            endnum = 0
                            in_while[0] = False
                            while running_while[0]:
                                Executor("\n".join(while_code)).execute2()
                    else:
                        while_code.append(" ".join(tokens))

if __name__ == "__main__":
    version = "1.4"
    if len(sys.argv) == 1:
        print(f"Wrutu version {version}")
        print(f"Usage: {sys.argv[0]} <file>")
    else:
        if sys.argv[1].endswith(".wru"):
            with open(sys.argv[1], "r") as f:
                Executor(f.read()).execute1()
        else:
            print("Error: use .wru file extension!")
