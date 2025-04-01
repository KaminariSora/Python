box = {
    1: 1,
    2: 0,
    3: 2,
    4: 14,
    5: 3,
    6: 12000
}

while(box[4] < box[6]):
    # Line 1
    box[2] = box[1] + box[2]
    # print(box[2])

    # Line 2
    box[4] = box[3] + box[4]
    # print(box[4])

    # Line 3
    box[6] = box[6] - box[5]
    # print(box[6])

    if(box[4] == box[6]):
        # Line 7
        print(f"Ans A: ",box[4])
        print(f"Ans B: ",box[6])
    elif(box[4] > box[6]):
        # Line 5
        print(f"Ans A: ",box[2])
        print(f"Ans B: ",box[4])
    elif(box[4] < box[6]):
        print(f"Box[4] :",box[4])
        print(f"Box[6] :",box[6])