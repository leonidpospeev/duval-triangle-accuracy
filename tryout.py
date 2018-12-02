import numpy as np

p = np.array([[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]])
p[2] = [0, 0, 0]
print(p)