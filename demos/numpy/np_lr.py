import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return 0.5 * x + 1

x = np.linspace(-10, 10, 21)
y = f(x)

plt.plot(x, y, "ro")
plt.show()

y += 2 * (np.random.rand(y.size) - 0.5)

plt.plot(x, y, "ro")
plt.show()


A = np.vstack([x, np.ones(x.size)]).T

a, b = np.linalg.lstsq(A, y)[0]
print a, b

plt.plot(x, y, "ro", x, a*x + b, "bx")
plt.show()


