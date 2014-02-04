import numpy as np

A = np.array([ [1, 2, 3],
               [4, 5, 6] ] )

print A

print A.ndim
print A.shape
print A.itemsize
print A.size

print A[:, 0]
print list(A.flat)

print np.zeros((3, 3, 3))
print np.ones((3, 3, 3))
print np.empty((3, 3, 3))
print np.eye(5, 5)

B = np.random.random((2, 3))
print B

print A + B
print A * B

print np.dot(A, B.T)


# Assignment is not a copy

AA = A
AA[0, 1] = 3
print AA
print A

AA = A.copy()
AA[0, 1] = 4
print AA
print A


# Boolean indexing

AA = np.arange(12).reshape(3,4)
Ind = AA > 4
print Ind

AA[Ind] = 0
print AA
