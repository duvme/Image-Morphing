# Image-Morphing

import numpy as np

# (a)
a = np.random.exponential(scale=1, size=1000)
print(np.mean(a[:10]), np.mean(a[:100]), np.mean(a[:1000]), np.mean(a[:10000]), np.mean(a[:100000]), np.mean(a))

# (b)
b = np.random.exponential(scale=1/0.5, size=1000)
print(np.mean(b[:10]), np.mean(b[:100]), np.mean(b[:1000]), np.mean(b[:10000]), np.mean(b[:100000]), np.mean(b))

# (c)
c = [1 if i >= 1 else 0 for i in a]
print(np.mean(c[:10]), np.mean(c[:100]), np.mean(c[:1000]), np.mean(c[:10000]), np.mean(c[:100000]), np.mean(c))

# (d)
d = [1 if i >= 2 else 0 for i in b]
print(np.mean(d[:10]), np.mean(d[:100]), np.mean(d[:1000]), np.mean(d[:10000]), np.mean(d[:100000]), np.mean(d))

# (e)
e_1 = []
for i, j in zip(a, c):
    if j:
        e_1.append(i)
print(np.mean(e_1))

e_05 = []
for i, j in zip(b, d):
    if j:
        e_05.append(i)
print(np.mean(e_05))

