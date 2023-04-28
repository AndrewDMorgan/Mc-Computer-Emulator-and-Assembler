

def Bin(val, bits=8):
    return format(val, f"#0{bits+2}b")


instructions = []
coms = open(input("Program >> ")).read().split("\n")
for com in coms:
    instructions.append([int(i) for i in com.split(" ")])

ram = ['0b0' for i in range(32)]  # just pretened you can't use the 0th memory slot
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
    memInst = Bin(instruction[0], 4)
    writeMem = instruction[1]
    address1 = instruction[2]
    addValue = instruction[3]
    
    opInst = Bin(instruction[4], 3)
    writeOp = instruction[5]
    addValueOp = instruction[6]
    
    # memory stuffs
    if memInst == '0b1000':  # ram -> reg A
        regA = ram[int(address1)]
    elif memInst == '0b0100':  # ram -> reg B
        regB = ram[int(address1)]
    elif memInst == '0b1100':  # ram -> reg A and regB
        regA = ram[int(address1)]
        regB = ram[int(addValue)]
    elif memInst == '0b0010':  # reg C -> ram
        ram[int(address1)] = regC
    elif memInst == '0b1010':  # value -> ram[reg C]
        ram[int(regC, 2)] = Bin(addValue)
    elif memInst == '0b0110':  # value -> ram
        ram[int(address1)] = Bin(addValue)
    elif memInst == '0b1110':  # value -> reg A
        regA = Bin(addValue)
    elif memInst == '0b0001':  # value -> reg B
        regB = Bin(addValue)
    elif memInst == '0b1001':  # ram[reg C] -> regA
        regA = ram[int(regC, 2)]
    elif memInst == '0b0101':  # ram[reg C] -> regB
        regB = ram[int(regC, 2)]
    elif memInst == '0b1101':  # ram -> ram[reg C]
        ram[int(regC, 2)] = ram[int(address1)]
    elif memInst == '0b0011':  # ram -> ram
        ram[int(address1)] = ram[int(addValue)]
    elif memInst == '0b1011':  # reg C -> dsp[reg A, reg B]
        if int(regB, 2) in range(1, 17) and int(regA, 2) in range(1, 17):
            if int(regC, 2) > 0:
                dsp[15 - int(regB, 2)][int(regA, 2) - 1] = '0b1'
            else:
                dsp[15 - int(regB, 2)][int(regA, 2) - 1] = '0b0'
        
            print(f"{int(regA, 2)}, {int(regB, 2)}")

            print("--" * 15)
            for y in range(15):
                print("|", end='')
                for x in range(15):
                    value = int(dsp[y][x], 2)
                    if value > 0:
                        print("##", end='')
                    else:
                        print("  ", end='')
                print("|")
            print("--" * 15)
    elif memInst == '0b0111':  # reg C -> output bus
        outBus = regC
        print(f"Out: {int(outBus, 2)}")
    elif memInst == '0b1111':  # input bus -> reg C
        regC = inBus
    
    # math/operations
    if opInst == '0b111':  # hault
        running = False
    elif opInst == '0b011':  # conditional jump if reg C == 0
        if int(regC, 2) == 0:
            line = addValueOp - 2
    elif opInst == '0b101':  # jump
        line = addValueOp - 2
    elif opInst == '0b001':  # bit shift left
        regC = Bin(max(min(int(regA, 2) << 1, 255), 0))
        if writeOp:
            ram[int(addValueOp)] = regC
    elif opInst == '0b110':  # subtraction
        regC = Bin(max(min(int(regA, 2) - int(regB, 2), 255), 0))
        if writeOp:
            ram[int(addValueOp)] = regC
    elif opInst == '0b010':  # not
        regC = Bin(0b11111111 - int(regA, 2))
        if writeOp:
            ram[int(addValueOp)] = regC
    elif opInst == '0b100':  # addition
        regC = Bin(max(min(int(regA, 2) + int(regB, 2), 255), 0))
        if writeOp:
            ram[int(addValueOp)] = regC
    
    #print(f"Inst: {instruction}\nLine: {line}\nReg A: {regA}  Reg B: {regB}  Reg C: {regC}\nRam: {ram}\n")
    #input(">>")
    
    line += 1

