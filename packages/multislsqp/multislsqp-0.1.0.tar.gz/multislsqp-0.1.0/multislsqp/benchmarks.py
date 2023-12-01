import numpy as np
from multislsqp.utils import runner,create_x_seed as create_x

# ============================================================================
# 1D examples

def fn1_all(x):
    return np.sin(x), np.cos(x)

def run_benchmark_1D(m=100,repeat=5):
    '''
    m - number of different inital guesses to evaluate
    repeat - number of times to repeat the analysis to average out the results
    '''    
    bounds = [(-10,10)]
    x = create_x(m,bounds)
    f_dict = {'fun':fn1_all,'jac':True}
    print()
    same = runner(x,f_dict,bounds=bounds,repeat=repeat)
    assert same==True

# ============================================================================
# multi dimension example

def _matrices(ndim,matsize=500):
    np.random.seed(101) # ensure its the same random matrix every time the function is called
    vec1 = np.random.uniform(0,1,size=(ndim,matsize))
    mat = np.random.uniform(0,1,size=(matsize,matsize))
    vec2 = np.random.uniform(0,1,size=(matsize,1))
    return vec1,mat,vec2

def func(x, matsize=500):
    if x.ndim==2: ndim = x.shape[1] 
    else : ndim = len(x)

    vec1,mat,vec2 = _matrices(ndim,matsize)

    mat_inv = np.linalg.inv(mat)
    a = np.matmul(mat_inv,vec2)
    a = np.matmul(vec1,a)
    f = np.matmul(x,a)
    return f

def dfunc(x, matsize=500):
    if x.ndim==2: ndim = x.shape[1] 
    else : ndim = len(x)

    vec1,mat,vec2 = _matrices(ndim,matsize)

    mat_inv = np.linalg.inv(mat)
    a = np.matmul(mat_inv,vec2)
    a = np.matmul(vec1,a)

    if x.ndim==2: df = np.repeat(a,x.shape[0],axis=1).T
    else: df = a.flatten()
    return df

def run_benchmark_multiD(m=100,N=5,repeat=3,matsize=600):
    '''
    m - number of different inital guesses to evaluate
    N - dimension of the problem
    repeat - number of times to repeat the analysis to average out the results
    matsize - size of the matrix which needs to be inverted (matsize x matsize)
    '''
    bounds = [(-3,3)]*N
    x = create_x(m,bounds)
    f_dict = {'fun':func,'jac':dfunc,'args':(matsize,)}
    print()
    same = runner(x,f_dict,bounds=bounds,repeat=repeat)
    assert same==True

def run_benchmarks():
    run_benchmark_1D()
    run_benchmark_multiD()