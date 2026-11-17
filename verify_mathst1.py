#!/usr/bin/env python3
"""Independent rank/nullity and matrix-product anchors for Mathematics T1."""
import numpy as np
def close(x,y): return abs(x-y)<1e-10
A=np.array([[1,2,3,4],[2,3,4,5],[3,4,5,6],[4,5,6,7]],dtype=float)
assert np.linalg.matrix_rank(A)==2
assert A.shape[1]-np.linalg.matrix_rank(A)==2
I=np.eye(4)
assert np.linalg.matrix_rank(I@I)==4
H=np.array([[.5,.5],[.5,.5]])
assert np.allclose(H@H,H) and np.linalg.matrix_rank(H)==1
assert close(float(np.trace(H)),1.0)
C=np.eye(4)-np.ones((4,4))/4
assert np.allclose(C@C,C) and np.linalg.matrix_rank(C)==3
assert close(float(np.trace(C)),3.0)
S=np.array([[0,1,2],[-1,0,3],[-2,-3,0]],dtype=float)
assert np.linalg.matrix_rank(S)==2
print("Mathematics T1 matrix anchors: PASS")
