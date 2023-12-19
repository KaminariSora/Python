#โปรแกรมคำนวน BMI
# BMI = weight(kg) / height * height (m)
weight = int(input("weight (kg): "))
height = int(input("height (cm): "))

height = height/100
bmi = weight / (height**2)

if bmi<=18.0 :
    print("Lower than median")
elif bmi >=18.5 and bmi <= 22.9:
    print("good")
elif bmi >23.0 and bmi >=24.9 :
    print("High weight")

print("BMI = ",bmi)