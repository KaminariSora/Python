box = {
    1: 860,
    2: 15,
    3: 1,
    4: 1,
    5: 3
}

line = 1

while True:
    if line == 1:
        box[5] **= 2
        line = line + 5
    elif line == 2:
        box[3] **= 2
        line = line + 3
    elif line == 3:
        box[2] = box[2] + box[5]
        line = 7
    elif line == 4:
        print(f"Ans A : ", box[3])
        line = 1
    elif line == 5:
        box[4] = box[4] + box[3]
        line = 3
    elif line == 6:
        box[3] += box[4]
        line = 2
    elif line == 7:
        if box[2] > 100:
            line = 9
        else:
            line = 8
    elif line == 8:
        if box[2] > 50:
            line = 4
        else:
            line = 1
    elif line == 9:
        print(f"Ans B: ",box[3])
        line = 10
    elif line == 10:
        break
