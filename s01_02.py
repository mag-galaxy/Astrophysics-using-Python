import math
pi = math.pi

def cal_factorial(a):
    answer = 1
    for i in range(1, a+1):
            answer *= i
    return answer

result = 0
x = 45 * (pi / 180)
for i in range(10):
    term = math.pow(-1, i) * math.pow(x, 2*i+1) / cal_factorial(2*i+1)
    result += term

print('x = 45 * pi / 180')
print(f'f(x) = {result}')