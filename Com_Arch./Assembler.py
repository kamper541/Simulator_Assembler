import numpy as np
import math

#with open('dat.txt' , 'r') as file:
#con = file.read().split('\n')
#del con[-1]
#
#for i in con:
#    count += 1
#    arr.append(i.split(','))

out = []
address = []
##---------------ดึงไฟล์ที่เป็น Assembly
with open('code_6.txt' , 'r') as file:
    con = file.read().split('\n')
    
    if not(con[-1]):
        del con[-1]
    
    for i in con:
        out.append(i.split('\t'))

##---------------เปลี่ยนเป็น 2's
def twosCom_decBin(dec, digit):
    if dec>=0:
            bin1 = bin(dec).split("0b")[1]
            while len(bin1)<digit :
                    bin1 = '0'+bin1
            return bin1
    else:
            bin1 = -1*dec
            return bin(dec-pow(2,digit)).split("0b")[1]

label = []
code = []
first = []
second = []
third = []
line = len(out)

##---------------setค่าแต่บรรทัด
for i in range (len(out)):
    for j in range (len(out[i])):
        if(j == 0):
            label.append(out[i][j])
        elif(j == 1):
            code.append(out[i][j])
        elif(j == 2):
            first.append(out[i][j])
        elif(j == 3):
            second.append(out[i][j])
        else:
            third.append(out[i][j])
            
labelin = dict()
addr = dict()
value = dict()

##---------------เก็บ label
for i in range (line):
    if(label[i] != ''):
        labelin.update({label[i] : f'address[{i}]'})
        value.update({f'address[{i}]' : i})
    else:
        labelin.update({f'{int(i)}': f'address[{i}]'})

##---------------fill ค่าไปใน address
for i in range (line):
    if(code[i] == '.fill'):
        try:
            addr.update({f'address[{i}]': int(first[i])})
        except:
            index = 0
            for j in range (line):
                if(first[i] == label[j]):
                    index = int(j)
            
            addr.update({f'address[{i}]': index})

##---------------กำหนด machine code ของแต่ละคำสั่ง
for i in range (line):
    if(code[i] == 'lw'):
        if(not(third[i].isdecimal())):
#            print(addr.get(labelin.get(third[i])))
            op = 2 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + (int(value.get(labelin.get(third[i]))))
            })
        else:
            op = 2 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + int(third[i])
            })
            
    elif(code[i] == 'add'):
        if(third[i].isdecimal()):
            op = 0 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + (int(third[i]))
            })
        else:
            op = 0 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + (int(addr.get(labelin.get(third[i]))))
            })
            
    elif(code[i] == 'nand'):
        if(third[i].isdecimal()):
            op = 1 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + (int(third[i]))
            })
        else:
            op = 1 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + (int(addr.get(labelin.get(third[i]))))
            })
            
    elif(code[i] == 'beq'):
        if(third[i].isdecimal()):
            op = 4 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + (int(third[i]))
            })
        else:
#            go = third[i]
#            for g in range (len(label)):
#                if(label[g] == go):
#                    go = g
#            go = int(go)
#            save = go + 1 + i
#            go = i - save
#            (int(converted,2)
#            converted = twosCom_decBin(go , 16)
#            print(int(value.get(labelin.get(third[i]))))
            op = 4 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + (int(value.get(labelin.get(third[i]))))
            })
            
    elif(code[i] == 'noop'):
        op = 7 << 22
        addr.update({f'address[{i}]': op})
        
    elif(code[i] == 'halt'):
        op = 6 << 22
        addr.update({f'address[{i}]':op})
        
    elif(code[i] == 'jalr'):
        op = 5 << 22
        addr.update({f'address[{i}]':op
        + (int(first[i]) << 19)
        + (int(second[i]) << 16)
        })
    
    elif(code[i] == 'sw'):
        if(not(third[i].isdecimal())):
        #            print(addr.get(labelin.get(third[i])))
            op = 3 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + (int(value.get(labelin.get(third[i]))))
            })
        else:
            op = 3 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + int(third[i])
            })
    elif(code[i] == '.fill'):
        continue
    else:
        print('exit(0)')
        raise Exception('No such instruction')
       
#for i in range (line):
#    if(isinstance(addr.get(f'address[{i}]') , str)):
#        print(12)
    
            
#for i in range (line):
#    print(addr.get(f'addrๆprint(f'address[{i}] : ' , addr.get(f'address[{i}]'))

##---------------output ไฟล์
for i in range (line):
    print(f'address[{i}]:',addr.get(f'address[{i}]'))

##---------------ใส่ output ไปยัง text
with open('machine_code_6.txt' , 'w') as file:
    for i in range (line):
        con = file.write('%s\n' % (addr.get(f'address[{i}]')))


#for i in range (line):
#    if(code[i] == 'lw'):
#        op = 2 << 22
#        if(third[i].isnumeric()):
#            addr.update({f'addr{i}': op + (int(first[i]) << 19) + (int(second[i]) << 16) + (int(third[i]))})
#        else:
#            if(third[i] != ''):
#                addr.update({f'addr{i}': op +
#                (int(first[i]) << 19) +
#                (int(second[i]) << 16) +
#                (addr.get(labelin.get(third[i])))})
##    elif(code[i] == 'beq'):
##        op = 4 << 22
##        if(third[i].isnumeric()):
##            addr.update({f'addr{i}': op + (int(first[i]) << 19) + (int(second[i]) << 16) + (int(third[i]))})
##        else:
##            if(third[i] != ''):
##                addr.update({f'addr{i}': op +
##                (int(first[i]) << 19) +
##                (int(second[i]) << 16) +
##                (addr.get(labelin.get(third[i])))})
#    elif(code[i] == 'add'):
#        op = 0 << 22
#        addr.update({f'addr{i}': op + (int(first[i]) << 19) + (int(second[i]) << 16) + (int(third[i]))})
