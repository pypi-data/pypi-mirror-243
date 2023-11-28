import numpy as np

class kernal_functions:

    @staticmethod
    def linear(x):
        z = []
        for val in x:
            z.append(val)
        z = np.array(z)
        return z
    
    @staticmethod
    def quadratic(x):
        z = []
        for val in x:
            z.append(val)
            z.append(val * val)
        z = np.array(z)
        return z
    
    @staticmethod
    def squares(x):
        z = []
        for val in x:
            z.append(val * val)
        z = np.array(z)
        return z