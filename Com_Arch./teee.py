x = '001'
y = '100'
z = []
ans = ''
for b in range (len(x)):
    if(x[b] == '1' and y[b] == '1'):
        z.append('0')
    elif(x[b] == '1' and y[b] == '0'):
        z.append('1')
    elif(x[b] == '0' and y[b] == '1'):
        z.append('1')
    elif(x[b] == '0' and y[b] == '0'):
        z.append('1')
        
for b in range (len(z)):
    ans += z[b]
print(ans)
