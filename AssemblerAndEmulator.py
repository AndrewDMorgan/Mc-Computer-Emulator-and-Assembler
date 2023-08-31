
# the program
program = [
    ".Main",
    "   LodI 212 <1>  ; loading 212 into ram at 1",
    "Jump Main"
]

# stuff for the processed program
jumpPoints = {}
code = []

# processing the program into a computer readable form
lineNumber = 0
for line in program:
    if line:
        if line[0] == ".":
            jumpPoints[line[1:]] = lineNumber
        else:
            lineNumber += 1
            instruction = line.split(";")[0].strip()
            headerCorrected = ""
            for word in instruction.split(" "):
                if word in jumpPoints:
                    headerCorrected += str(jumpPoints[word])
                else:
                    headerCorrected += word
                headerCorrected += " "
            code.append(headerCorrected[:-1])

print(code)

# the registers
readRegA = 0
readRegB = 0
wrtieReg = 0

# the ram
ram = [0 for i in range(32)]

# the stack
stack = []

# screen stuff
screenBuffer = [[0 for i in range(31)] for i in range(31)]
screen = [[0 for i in range(31)] for i in range(31)]

screenRefresh = True
