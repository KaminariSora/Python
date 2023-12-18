#โปรแกรมคำนวน BMI
# BMI = weight(kg) / height * height (m)
weight = int(input("weight (kg): "))
height = int(input("height (cm): "))

height = height/100
bmi = weight / (height**2)

print("BMI = ",bmi)