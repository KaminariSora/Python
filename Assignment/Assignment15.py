number = int(input("Size : "))
for row in range(0,number) :
    for column in range(number) :
        if row == 0 or row == number-1 or column == 0 or column == number-1:
            print("x", end = "")
        else :
            print(" ",end = "")
    print(" ")