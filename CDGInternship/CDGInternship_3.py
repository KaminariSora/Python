box = {
    1: 0,
    2: 1,
    3: 2
}

line =1

if line == 1:
    # line 1
    box[2] = box[2]+3
elif line == 2:
    # line 2
    line = box[3]
elif line == 3:
    # line 3
    box[3] = box[3]+3
elif line == 4:
    # line 4
    box[1] = box[1]+6
