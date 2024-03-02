import math

pi = math.pi

#degree
theta = 45.0

#radian
theta_rad = theta * (pi / 180.0)

sin_theta = math.sin (theta_rad)

print (f'theta in degree = {theta} deg')
print (f'theta in radian = {theta_rad} rad')
print (f'sin(theta) = sin({theta} degree) = sin({theta_rad} rad) = {sin_theta}')