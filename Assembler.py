# mem inst, wrt, add, add/val, math inst, wrt, add/val
# [0b0000, 0b0, 0b00000, 0b00000000, 0b000, 0b0, 0b00000000]

asm = open(input("Program >> ")).read().split("\n")

instructions = []
for com in asm:
    split = com.split(" ")
    inst = split[0]
    instO = [0b0, 0b0, 0b0, 0b0, 0b0, 0b0, 0b0]
    
    if inst == "LodA":
        instO = [0b1000, 0b0, int(split[1]), 0b0, 0b0, 0b0, 0b0]
    elif inst == "LodB":
        instO = [0b0100, 0b0, int(split[1]), 0b0, 0b0, 0b0, 0b0]
    elif inst == "LdAB":
        instO = [0b1100, 0b0, int(split[1]), int(split[2]), 0b0, 0b0, 0b0]
    elif inst == "RedC":
        instO = [0b0010, 0b1, int(split[1]), 0b0, 0b0, 0b0, 0b0]
    elif inst == "WtRC":
        instO = [0b1010, 0b0, 0b0, int(split[1]), 0b0, 0b0, 0b0]
    elif inst == "WrtR":
        instO = [0b0110, 0b1, int(split[1]), int(split[2]), 0b0, 0b0, 0b0]
    elif inst == "WrtA":
        instO = [0b1110, 0b0, 0b0, int(split[1]), 0b0, 0b0, 0b0]
    elif inst == "WrtB":
        instO = [0b0001, 0b0, 0b0, int(split[1]), 0b0, 0b0, 0b0]
    elif inst == "LdRA":
        instO = [0b1001, 0b0, 0b0, 0b0, 0b0, 0b0, 0b0]
    elif inst == "LDRB":
        instO = [0b0101, 0b0, 0b0, 0b0, 0b0, 0b0, 0b0]
    elif inst == "WtCR":
        instO = [0b1101, 0b0, int(split[1]), 0b0, 0b0, 0b0, 0b0]
    elif inst == "WrRR":
        instO = [0b0011, 0b1, int(split[1]), int(split[2]), 0b0, 0b0, 0b0]
    elif inst == "Disp":
        instO = [0b1011, 0b0, 0b0, 0b0, 0b0, 0b0, 0b0]
    elif inst == "Outp":
        instO = [0b0111, 0b0, 0b0, 0b0, 0b0, 0b0, 0b0]
    elif inst == "Inpt":
        instO = [0b1111, 0b0, 0b0, 0b0, 0b0, 0b0, 0b0]
    elif inst == "Add":
        if len(split) == 1:
            instO = [0b0, 0b0, 0b0, 0b0, 0b100, 0b0, 0b0]
        else:
            instO = [0b0, 0b0, 0b0, 0b0, 0b100, 0b1, int(split[1])]
    elif inst == "Not":
        if len(split) == 1:
            instO = [0b0, 0b0, 0b0, 0b0, 0b010, 0b0, 0b0]
        else:
            instO = [0b0, 0b0, 0b0, 0b0, 0b010, 0b1, int(split[1])]
    elif inst == "Sub":
        if len(split) == 1:
            instO = [0b0, 0b0, 0b0, 0b0, 0b110, 0b0, 0b0]
        else:
            instO = [0b0, 0b0, 0b0, 0b0, 0b110, 0b1, int(split[1])]
    elif inst == "SftL":
        if len(split) == 1:
            instO = [0b0, 0b0, 0b0, 0b0, 0b001, 0b0, 0b0]
        else:
            instO = [0b0, 0b0, 0b0, 0b0, 0b001, 0b1, int(split[1])]
    elif inst == "Jump":
        instO = [0b0, 0b0, 0b0, 0b0, 0b101, 0b0, int(split[1])]
    elif inst == "JmIZ":
        instO = [0b0, 0b0, 0b0, 0b0, 0b011, 0b0, int(split[1])]
    elif inst == "Halt":
        instO = [0b0, 0b0, 0b0, 0b0, 0b111, 0b0, 0b0]
    
    instructions.append(instO)

finalBin = ""
for inst in instructions:
    line = f"{inst[0]} {inst[1]} {inst[2]} {inst[3]} {inst[4]} {inst[5]} {inst[6]}\n"
    finalBin += line
finalBin = finalBin[:-1]

with open(input("Output >> "), 'w') as out:
            out.write(finalBin)
