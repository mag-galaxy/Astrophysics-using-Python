import numpy as np

a = np.array([0.0, 1.0, 2.0])
b = np.array([-1.0, 0.0, 3.0])
print(f'a = {a}')
print(f'b = {b}')

c = np.cross(a, b)
print('c = a X b')
print(f'c = {c}')