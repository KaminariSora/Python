box = {
    1: 3,
    2: 1,
    3: 2,
    4: 3,
    5: 5,
    6: 8
}

line = 1

while True:
    if line == 1:
        box[1] = 1 + 1
        line = 9
    elif line == 2:
        box[1] = 2 + 1
        line = 9
    elif line == 3:
        print(f"Ans A : {box[3]}")
        line = 4
    elif line == 4:
        box[1] = 4 + 1
        line = 9
    elif line == 5:
        print(f"Ans B: {box[4]}")
        line = 6
    elif line == 6:
        box[1] = 6 + 1
        line = 11
    elif line == 7:
        print(f"Ans C: {box[5]}")
        line = 8
    elif line == 8:
        break
    elif line == 9:
        box[6] = box[1] + box[2] + box[3] + box[4] + box[5]
        line = 10
    elif line == 10:
        box[1] = box[6]
        line = 11
    elif line == 11:
        line = box[1]
