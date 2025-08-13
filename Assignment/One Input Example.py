import math
x1 = [1.0, 2.0, 3.0, 4.0, 5.0]
y = [2.0, 4.0, 7.0, 6.0, 9.0]
w1 = 0.0
b = 0.0
alpla = 0.05

def gradient(w1, b, x1, y):
    n = len(x1)
    del_w1 = 0.0
    del_b = 0.0
    for i in range(n):
        del_w1 += (w1*x1[i]-y[i])* x1[i]
        del_b += (w1*x1[i] + b - y[i])
    
    del_w1 = (2/n) * del_w1
    del_b = (2/n) * del_b

    return del_w1, del_b
del_w1, del_b = gradient(w1, b, x1, y)

while abs(del_w1) > 0.0001 or (abs(del_b) > 0.0001):
    w1_new = w1 - alpla * del_w1
    b_new = b - alpla * del_b
    print("w1_old = ",format(w1,'.6f'), "del_w1 = ", format(del_w1, '.6f'), "w1_new = ", format(w1_new, '.6f'))
    print("b_old = ", format(b, '.6f'), "del_b = ", format(del_b, '.6f'), "b_new = ", format(b_new, '.6f'))
    w1 = w1_new
    b = b_new
    del_w1, del_b = gradient(w1, b, x1, y)