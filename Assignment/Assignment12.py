last = int(input("last-row : "))

for row in range(1,last) :
    for column in range(1,row+1) :
        print(column,end='')
    print(" ")