max,min = 0, 9999

while True :
    number = int(input("number : "))
    if number < 0 :
        break
    if number > max :
        max = number
    if number < max :
        min = number
    
print("max : ",max)
print("min : ",min)