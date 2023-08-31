
# the program
program = [
    ".Main",
    "   LodI 212 <1>  ; loading 212 into ram at 1",
    "   Jump End",
    ".End",
    "   END"
]

# stuff for the processed program
jumpPoints = {}
code = []

# getting the jump points
lineNumber = 0
for line in program:
    if line:
        if line[0] == ".":
            jumpPoints[line[1:]] = lineNumber
        else: lineNumber += 1

# processing the program into a computer readable form
lineNumber = 0
for line in program:
    if line:
        if line[0] != ".":
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
letterDisplay = [0 for i in range(16)]

# the stack
stack = []

# screen stuff
screenBuffer = [[0 for i in range(31)] for i in range(31)]
screen = [[0 for i in range(31)] for i in range(31)]
screenRefresh = True

# running the program
lineNumber = 0
running = True
while running:
    # getting the next line
    lineNumber += 1
    line = code[lineNumber - 1]
    
    insts = line.split(" ")

    # processing the line and running it
    if insts[0] == "LodI":
        pass
    if insts[0] == "LodA":
        pass
    if insts[0] == "LodB":
        pass
    if insts[0] == "LodW":
        pass
    if insts[0] == "Add":
        pass
    if insts[0] == "Sub":
        pass
    if insts[0] == "SubL":
        pass
    if insts[0] == "WrtW":
        pass
    if insts[0] == "WrtA":
        pass
    if insts[0] == "WrtB":
        pass
    if insts[0] == "Jump":
        pass
    if insts[0] == "JmpZ":
        pass
    if insts[0] == "JmpE":
        pass
    if insts[0] == "JmpG":
        pass
    if insts[0] == "JmpL":
        pass
    if insts[0] == "Wrte":
        pass
    if insts[0] == "Outp":
        pass
    if insts[0] == "SftR":
        pass
    if insts[0] == "Pop":
        pass
    if insts[0] == "Push":
        pass
    if insts[0] == "Not":
        pass
    if insts[0] == "NotB":
        pass
    if insts[0] == "RefT": screenRefresh = True
    if insts[0] == "RefF": screenRefresh = False
    if insts[0] == "Refr": screen = screenBuffer
    if insts[0] == "Plot":
        pass
    if insts[0] == "Cler":
        pass
    if insts[0] == "PshT":
        pass
    if insts[0] == "ClrT":
        pass
    
    if screenRefresh: screen = screenBuffer

    # ending the program
    if line == "END": running = False

