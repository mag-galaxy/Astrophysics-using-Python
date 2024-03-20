import numpy
import scipy
import scipy.integrate

def curve(x):
  y = numpy.exp(-(x**2))
  return y

x0 = float('-inf')
x1 = float('inf')

result = scipy.integrate.quad(curve, x0, x1)
print(f'integ. of exp(-x^2) from negative infinity to positive infinity = {result[0]} +/- {result[1]}')
