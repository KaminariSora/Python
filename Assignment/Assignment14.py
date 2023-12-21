number = int(input("Size : "))
for row in range(0,number) :
    for column in range(number) :
        if (row + column)%2 == 0 :
            print("x",end = "")
        else :
            print("o",end="")
    print(" ")