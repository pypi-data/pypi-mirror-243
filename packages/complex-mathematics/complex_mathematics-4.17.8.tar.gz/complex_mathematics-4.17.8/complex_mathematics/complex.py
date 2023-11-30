import numpy as np
import math

class complex:
  def __init__(self, a, bi):
    self.a = a
    self.bi = bi

  def conjugate(self):
    return np.array([self.a, -self.bi])

  def mod(self):
    return math.sqrt(self.a ** 2 + self.bi ** 2)

  def arg(self):
    return math.atan(self.bi/self.a)

def cmultiply(num1, num2):
  a1 = num1.a
  a2 = num2.a
  bi1 = num1.bi
  bi2 = num2.bi
  a = -(bi1*bi2) + a1*a2
  bi = bi1*a2 + a1*bi2
  return complex(a, bi)