from pynput import keyboard
import time, random

# gets the pressed key
def on_press(key):
    global inBus
    try:
        inBus = ord(key.char)
    except AttributeError:
        pass


# goes when a key is released
def on_release(key):
    global inBus
    inBus = 0
    if not running:
        # Stop listener
        return False


# gets and returns the correct address
def Read(add: str, regValue: int=0) -> int:
    if add[0] == "<":
        number = int(add[1:-1])
        if number == 0: return ram[regValue]
        return ram[number]
    elif add == "ACC": return accumulator
    return int(add)


# gets and returns the correct address
def Write(add: str, writeVal: int, regValue: int=0) -> None:
    global ram, accumulator
    writeVal = max(writeVal, 0)
    if add[0] == "<":
        number = int(add[1:-1])
        if number == 0: ram[regValue] = writeVal
        else: ram[number] = writeVal
    elif add == "ACC": accumulator = writeVal
    else: ram[int(add)] = writeVal


# the program
program = open(input(">> ")).read().split("\n")

# stuff for the processed program
jumpPoints = {}
code = []

# getting the jump points
lineNumber = 0
for l in program:
    line = l.split(";")[0].strip()
    if line:
        if line[0] == ".":
            jumpPoints[line[1:-1]] = lineNumber
        else: lineNumber += 1

# processing the program into a computer readable form
lineNumber = 0
for l in program:
    line = l.split(";")[0].strip()
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

# printing the code
for line in code:
    print(line)


# getting key inputs
running = True
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

# the registers
readRegA = 0
readRegB = 0
writeReg = 0

inBus = 0

# memory
ram = [0 for i in range(32)]
letterDisplay = []
accumulator = 0
stack = []

# screen stuff
screenBuffer = [[0 for i in range(31)] for i in range(31)]
screen = [[0 for i in range(31)] for i in range(31)]
screenRefresh = True

# running the program
lineNumber = 0
while running:
    # getting the next line
    lineNumber += 1
    line = code[lineNumber - 1]
    ram[1] = lineNumber - 1
    #time.sleep(0.25)
    #print(f"{lineNumber}: {line}")
    #print(accumulator)
    
    insts = line.split(" ")

    # processing the line and running it
    if insts[0] == "LodI": Write(insts[2], int(insts[1]), writeReg)
    if insts[0] == "LodA": readRegA = int(insts[1])
    if insts[0] == "LodB": readRegB = int(insts[1])
    if insts[0] == "LodW": writeReg = int(insts[1])
    if insts[0] == "Add" : Write(insts[3], Read(insts[1], readRegA) + Read(insts[2], readRegB), writeReg)
    if insts[0] == "Sub" : Write(insts[3], Read(insts[1], readRegA) - Read(insts[2], readRegB), writeReg)
    if insts[0] == "SubL": Write(insts[3], Read(insts[2], readRegB) - Read(insts[1], readRegA), writeReg)
    if insts[0] == "WrtW": writeReg = Read(insts[1], readRegB)
    if insts[0] == "WrtA": readRegA = Read(insts[1], readRegB)
    if insts[0] == "WrtB": readRegB = Read(insts[1], readRegB)
    if insts[0] == "Jump": lineNumber = Read(insts[1], readRegB)
    if insts[0] == "JmpZ" and accumulator == 0: lineNumber = Read(insts[1], readRegB)
    if insts[0] == "JmpE" and accumulator == Read(insts[1], readRegB): lineNumber = int(insts[2])
    if insts[0] == "JmpG" and accumulator >  Read(insts[1], readRegB): lineNumber = int(insts[2])
    if insts[0] == "JmpL" and accumulator <  Read(insts[1], readRegB): lineNumber = int(insts[2])
    if insts[0] == "Wrte": Write(insts[2], Read(insts[1], readRegB), writeReg)
    if insts[0] == "Outp": print(Read(insts[1], readRegB))  # no longer an instruction on the actual computer (but will still be on this emulated version)
    if insts[0] == "SftR": Write(insts[2], Read(insts[1], readRegA) >> 1, writeReg)
    if insts[0] == "Pop" :  # deleting empty values will cause an error here but not on the actual computer
        Write(insts[1], stack[0], writeReg)
        del stack[0]
    if insts[0] == "Push": stack.insert(0, Read(insts[1], readRegB))  # the actual computer has a limit of 16 values before it will start deleting older ones
    if insts[0] == "Not" : Write(insts[2], ~Read(insts[1], readRegA), writeReg)
    if insts[0] == "NotB": Write(insts[2], ~Read(insts[1], readRegB), writeReg)
    if insts[0] == "RefT": screenRefresh = True
    if insts[0] == "RefF": screenRefresh = False
    if insts[0] == "Refr":
        screen = screenBuffer
        time.sleep(0.5)
    if insts[0] == "Plot":
        try:  # works the same way on the mc computer
            screenBuffer[Read(insts[2], readRegB)-1][Read(insts[1], readRegA)-1] = accumulator  # [y][x] instruction is x, y
        except IndexError:
            pass
    if insts[0] == "Cler": screenBuffer = [[0 for i in range(31)] for i in range(31)]
    if insts[0] == "PshT": letterDisplay.insert(0, Read(insts[1], readRegB))
    if insts[0] == "ClrT": letterDisplay = []

    # not real instructions on the computer
    if insts[0] == "Inpt": Write(insts[1], inBus, writeReg)
    if insts[0] == "Rand": Write(insts[1], random.randint(0, 255), writeReg)
    
    # refreshing the screen
    if screenRefresh: screen = screenBuffer
    
    # rendering the screen, and text
    #"""
    if insts[0] == "Refr":
        abc = list(" abcdefghijklmnopqrstuvwxyz")
        print("".join([abc[char] for char in letterDisplay[::-1]]))
        print("++" + "--"*31 + "++")
        for row in screenBuffer[::-1]:
            print("||", end='')
            for value in row:
                char = "  "
                if value: char="##"
                print(char, end='')
            print("||")
        print("++" + "--"*31 + "++")
    #"""

    # ending the program
    if line == "END": running = False

    #time.sleep(4)

print(ram)
