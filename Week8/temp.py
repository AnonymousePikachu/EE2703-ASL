%%cython --annotate

import numpy as np

# solves Ax = b and returns x
def solve_2(double complex[:, :] A, double complex[:] b):
    cdef Py_ssize_t n = A.shape[0] # number of unknowns
    
    cdef Py_ssize_t i, j
    
    # augmented matrix
    cdef double complex[:, :] B = np.concatenate(
            (A, np.expand_dims(b, axis=1)), axis=1
        )
    
    cdef Py_ssize_t k, max_k
    cdef double complex temp, ratio
    
    # bring B to row echelon form
    for i in range(0, n): # loop through diagonal elements
        # implement partial pivoting
        # find the maximum absolute value in this column
        max_k = i
        
        for k in range(i + 1, n):
            if abs(B[k, i]) > abs(B[max_k, i]):
                max_k = k
                
        if B[max_k, i] == 0:
            raise ZeroDivisionError("unsolvable matrix")
                
        # swap rows so that the maximum value is our new pivot
        for j in range(0, n + 1):
            temp = B[i, j]
            B[i, j] = B[max_k, j]
            B[max_k, j] = temp
        
        # reduce the values below
        for j in range(i + 1, n): # loop through rows below
            ratio = B[j, i] / B[i, i]
            
            for k in range(i, n + 1):
                B[j, k] = B[j, k] - ratio * B[i, k]
        
    # now find the variables
    for i in range(n - 1, -1, -1): # loop up the matrix
        B[i, n] = B[i, n] / B[i, i]
        for j in range(0, i):
            B[j, n] = B[j, n] - B[i, n] * B[j, i]
        
    return B[0:n,n]