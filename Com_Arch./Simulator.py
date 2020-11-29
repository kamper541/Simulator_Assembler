out = []
address = []

##---------------2's converter
def twosCom_decBin(dec, digit):
    if dec>=0:
            bin1 = bin(dec).split("0b")[1]
            while len(bin1)<digit :
                    bin1 = '0'+bin1
            return bin1
    else:
            bin1 = -1*dec
            return bin(dec-pow(2,digit)).split("0b")[1]

def twosCom_binDec(bin, digit):
    while len(bin)<digit :
            bin = '0'+bin
    if bin[0] == '0':
            return int(bin, 2)
    else:
            return -1 * (int(''.join('1' if x == '0' else '0' for x in bin), 2) + 1)

def binaryToDecimal(binary):
  
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal

##---------------ดึงไฟล์ machine code
with open('machine_code_6.txt','r')as file:
    con = file.read().split('\n')
    
    if not(con[-1]):
        del con[-1]
        
    for i in con:
        out.append(int(i))

##---------------กำหนด address
for i in range (len(out)):
    address.append(out[i])

binary = []

##---------------ค่าที่ติดลบ ทำเป็น 2's
for i in range (len(address)):
    if(address[i] < 0):
#        print(twosCom_decBin(address[i] , 16))
        binary.append(twosCom_decBin(address[i] , 16))
        
    else:
        binary.append(bin(address[i])[2:])

##---------------เติม 0 ให้ครบ
for i in range (len(binary)):
    if(len(binary[i]) != 25):
        add = 25 - len(binary[i])
        binary[i] = '0'*add + binary[i]
#print(binary)

##---------------init reg กับ mem
reg = [0] * 20
memory = []

for i in range (len(address)):
    memory.append(address[i])

for i in range (25):
    memory.append(0)

##---------------check op code ว่าคือ function ไหน เริ่มการรันโค้ด
i = 0
#while i < len(binary):
#print(len(binary))
while i < len(binary):
    print(f'pc[{i}]:')
    print('Memory:')
    ##---------------display memory reg
    for j in range (len(memory)):
        print(f'\tmemory[ {j} ]:', memory[j])

    print('Register:')

    for j in range (len(reg)):
        print(f'\tregister[ {j} ]:' , reg[j])
        
    print('\n\n')
    ##---------------จำแนกชนิดของ โค้ด
    if(binary[i][:3] == '000'):
#        print('Radd')
        regA = binary[i][3:6]
        regB = binary[i][6:9]
        regdst = binary[i][22:]
        reg[binaryToDecimal(int(regdst))] = reg[binaryToDecimal(int(regA))] + reg[binaryToDecimal(int(regB))]
        i = i + 1
    elif(binary[i][:3] == '001'):
#        print('Rnand')
        regA = binary[i][3:6]
        regB = binary[i][6:9]
        regdst = binary[i][22:]
        #just test--------------------------------added
        z = []
        ans = ''
        AA = twosCom_decBin(reg[binaryToDecimal(int(regA))] , 3)
        BB = twosCom_decBin(reg[binaryToDecimal(int(regB))] , 3)
        for b in range (3):
            if(AA[b] == '1' and BB[b] == '1'):
                z.append('0')
            elif(AA[b] == '1' and BB[b] == '0'):
                z.append('1')
            elif(AA[b] == '0' and BB[b] == '1'):
                z.append('1')
            elif(AA[b] == '0' and BB[b] == '0'):
                z.append('1')
                
        for b in range (3):
            ans += z[b]
        print(ans)
        reg[binaryToDecimal(int(regdst))] = int(binaryToDecimal(int(ans)))
        #test--------------------------------------added
#        reg[binaryToDecimal(int(regdst))] = int(not (reg[binaryToDecimal(int(regA))] and reg[binaryToDecimal(int(regB))]))
        i = i + 1
    elif(binary[i][:3] == '010'):
#           print('lw')
        regA = binary[i][3:6]
        regB = binary[i][6:9]
        offset = binary[i][9:]
#           print(offset)
        try:
            reg[binaryToDecimal(int(regB))] = memory[reg[binaryToDecimal(int(regA))] + binaryToDecimal(int(offset))]
        except:
            print('exit(0)')
            break
#           print('======', reg[binaryToDecimal(int(regA))]
#           + binaryToDecimal(int(offset)))
#           reg[binaryToDecimal] = reg[regA] + offset
#        print(regA , regB , offset)
        i = i + 1
    elif(binary[i][:3] == '011'):
#        print('sw')
        regA = binary[i][3:6]
        regB = binary[i][6:9]
        offset = binary[i][9:]
#        print(binaryToDecimal(int(offset)) , binaryToDecimal(int(regA)) , binaryToDecimal(int(regB)))
        try:
            memory[binaryToDecimal(int(offset)) + reg[binaryToDecimal(int(regA))]] = reg[binaryToDecimal(int(regB))]
            i = i + 1
        except:
            print('exit(0)')
            break
    elif(binary[i][:3] == '100'):
        regA = binary[i][3:6]
        regB = binary[i][6:9]
        offset = binary[i][9:]
        try:
            if(reg[binaryToDecimal(int(regA))] == reg[binaryToDecimal(int(regB))]):
                print(i,1 ,binaryToDecimal(int(offset)))
                i = i + 1 + binaryToDecimal(int(offset))
            else:
                i = binaryToDecimal(int(offset))
        except:
            print('exit(0)')
            break
#        print('BEQ' , regA,regB,offset)
#        print('beq')
    elif(binary[i][:3] == '101'):
#        print('jalr')
        regA = binary[i][3:6]
        regB = binary[i][6:9]
        if(reg[binaryToDecimal(int(regA))] == reg[binaryToDecimal(int(regB))]):
            reg[binaryToDecimal(int(regB))] = i + 1
            i = reg[binaryToDecimal(int(regA))]
        else:
            reg[binaryToDecimal(int(regB))] = i + 1
            i = reg[binaryToDecimal(int(regA))]
    elif(binary[i][:3] == '110'):
#        print('halt')
        print('exit(1)')
        break
    elif(binary[i][:3] == '111'):
#        print('noop')
        i = i + 1
    else:
        print('exit(0)')
        break
