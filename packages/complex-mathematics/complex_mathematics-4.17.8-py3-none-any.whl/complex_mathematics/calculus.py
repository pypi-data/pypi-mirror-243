import numpy as np

def derivative(coef_):
    derivative = np.zeros(len(coef_)-1)
    for i in range(len(coef_)-1):
        derivative[i] = coef_[i]*(len(coef_)-i-1)
    return derivative