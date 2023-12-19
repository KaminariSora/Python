temp = input("Temperature : ")

degree = temp[:-1]
unit = temp[-1].upper()

if unit == "C":
    result = ((9*float(degree))/5) + 32
    print("result is ",result," F")
elif unit == "F" :
    result = (float(degree) - 32) * 5/9
    print("result is ",result, " C")
else :
    print("wrong temperature")