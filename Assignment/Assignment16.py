import random

MyNumber = random.randrange(1,7)
i = 1
print("Correct answer is ",MyNumber)

while True :
    i+=1
    answer = int(input("Guess your number : "))
    if (answer == MyNumber) or i == 3:
        print("end Program")
        break
    elif answer > MyNumber :
        print("Lower than that.")
        continue
    elif answer < MyNumber :
        print("Higher than that.")
        continue
    elif answer < 0 :
        print("Wrong Input")
        continue