from time import time
import numpy as np

a = np.zeros(int(1e7))
b = a 

at = time()
a = [*a, 1]
at = time() - at
bt = time()
b = np.append(b, 1)
bt = time() - bt

print(f"at: {at}")
print(f"bt: {bt}")

