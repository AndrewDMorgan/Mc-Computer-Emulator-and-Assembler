# mem inst, wrt, add, add/val, math inst, wrt, add/val
# [0b0000, 0b0, 0b00000, 0b00000000, 0b000, 0b0, 0b00000000]

asm = [
    "WrtA 24",
    "WrtB 9",
    "Add",
    "Outp",
    "Halt"
]

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

ram = ['0b0' for i in range(31)]
dsp = [['0b0' for x in range(15)] for y in range(15)]
regA = '0b0'
regB = '0b0'
regC = '0b0'
outBus = '0b0'
inBus = '0b0'

line = 0
running = True

while running:
    instruction = instructions[line]
    memInst = instruction[0]
    writeMem = instruction[1]
    address1 = instruction[2]
    addValue = instruction[3]
    
    opInst = instruction[4]
    writeOp = instruction[5]
    addValueOp = instruction[6]
    
    # memory stuffs
    if memInst == 0b1000:  # ram -> reg A
        regA = ram[int(address1)]
    elif memInst == 0b0100:  # ram -> reg B
        regB = ram[int(address1)]
    elif memInst == 0b1100:  # ram -> reg A and regB
        regA = ram[int(address1)]
        regB = ram[int(addValue)]
    elif memInst == 0b0010:  # reg C -> ram
        ram[int(address1)] = regC
    elif memInst == 0b1010:  # value -> ram[reg C]
        ram[int(regC, 2)] = bin(addValue)
    elif memInst == 0b0110:  # value -> ram
        ram[int(address1)] = bin(addValue)
    elif memInst == 0b1110:  # value -> reg A
        regA = bin(addValue)
    elif memInst == 0b0001:  # value -> reg B
        regB = bin(addValue)
    elif memInst == 0b1001:  # ram[reg C] -> regA
        regA = ram[int(regC, 2)]
    elif memInst == 0b0101:  # ram[reg C] -> regB
        regB = ram[int(regC, 2)]
    elif memInst == 0b1101:  # ram -> ram[reg C]
        ram[int(regC, 2)] = ram[int(address1)]
    elif memInst == 0b0011:  # ram -> ram
        ram[int(address1)] = ram[int(addValue)]
    elif memInst == 0b1011:  # reg C -> dsp[reg A, reg B]
        if int(regC, 2) > 0:
            dsp[int(regA, 2)][int(regB, 2)] = 0b1
        else:
            dsp[int(regA, 2)][int(regB, 2)] = 0b0
    elif memInst == 0b0111:  # reg C -> output bus
        outBus = regC
    elif memInst == 0b1111:  # input bus -> reg C
        regC = inBus
    
    # math/operations
    if opInst == 0b111:  # hault
        running = False
    elif opInst == 0b011:  # conditional jump if reg C == 0
        if regC == 0:
            line = int(str(addValueOp)[:-1], 2) - 1
    elif opInst == 0b101:  # jump
        line = int(str(addValueOp)[:-1], 2) - 1
    elif opInst == 0b001:  # bit shift left
        regC = bin(int(regA, 2) << 1)
        if writeOp:
            ram[int(addValueOp)] = regC
    elif opInst == 0b110:  # subtraction
        regC = bin(int(regA, 2) - int(regB, 2))
        if writeOp:
            ram[int(addValueOp)] = regC
    elif opInst == 0b010:  # not
        regC = bin(0b11111111 - int(regA, 2))
        if writeOp:
            ram[int(addValueOp)] = regC
    elif opInst == 0b100:  # addition
        regC = bin(int(regA, 2) + int(regB, 2))
        if writeOp:
            ram[int(addValueOp)] = regC
    
    # clamping the output of regC
    regC = bin(max(min(int(regC, 2), 255), 0))
    
    line += 1

print(int(outBus, 2))

for y in range(15):
    for x in range(15):
        value = int(dsp[y][x], 2)
        if value > 0:
            print("##", end='')
        else:
            print("  ", end='')
    print("")

