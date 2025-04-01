box = {
    1: 2,
    2: 1001
}

line = 1
# print(box[1])

while True:
    print(f"Line: ",line)
    if line == 1:
        # SKIP - EVEN BOX 1
        if box[1] % 2 == 0:
            line = line+2 # line 3
        else:
            line = line+1 # line 2
    elif line == 2:
        # SKIP - EVEN BOX 1
        if box[1] % 2 == 0:
            line = line+2
        else:
            line = line+1
    elif line == 3:
        box[1] = box[1]+1
        print(box[1])
        line+=1
    elif line == 4:
        # SKIP - EVEN BOX 1
        if box[1] % 2 == 0:
            line = line+2
        else:
            line = line+1
    elif line == 5:
        line = 2
    elif line == 6:
        box[2] -= 1
        line+=1
    elif line == 7:
        # SKIP - EVEN BOX 2 
        if box[2] % 2 ==0:
            line = line+2
        else:
            line = line+1
    elif line == 8:
        line = 10
    elif line == 9:
        line = 1
    elif line == 10:
        if box[1] >= box[2]:
            line = 11
        else:
            line = 1
    elif line == 11:
        print(f"Ans A: ",box[1])
        print(f"Ans B: ",box[2])
        line+=1
    elif line == 12:
        break