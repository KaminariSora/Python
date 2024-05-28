from cmath import sqrt
from scipy.stats import t
import math

t_value = (-0.8-0.12)/(2.84/math.sqrt(328))
print("t-test : ",t_value)

T = t.cdf(t_value, 100 - 1)
print("Result for p-value : ",T)

C = t.ppf(1, 100 - 1)
print("Critical value : ",C)