import time

import numpy as np
from scipy.optimize import minimize
from multislsqp import minimise_slsqp, minimise_slsqp_cmp

def compare(seq,para,init_x,verbose=False,strict_compare=False):
    match_all = True
    for key, seq_val in seq.items():
        if not strict_compare:
            if key not in ('fun','jac','message','success','x'):
                continue
        para_val = para[key]

        if type(seq_val) is str:
            match = seq_val==para_val
        else:
            match = np.allclose(seq_val,para_val)

        if not match:
            match_all = False
            print("{} (sequential) is not equal to {} (multistart) for {}".format(seq_val,para_val,key))
            break

    if verbose:
        print('~'*25)
        print("Starting from initial point {}\n".format(", ".join(map(str,init_x))))
        print("Standard scipy SLSQP:")
        print(seq)
        print()
        print("MultiSLSQP:")
        print(para)
        print()
        print('All matching: {}\n'.format(match_all))

    return match_all

def sum_over(opt_res,key):
    if type(opt_res) is not list: opt_res = [opt_res]
    val_sum = 0
    for _opt_res in opt_res:
        val_sum += _opt_res[key]
    return val_sum

def res_str(string,pad=20):
    if type(string) is not string: string = str(string)
    return string.center(pad)

def runner(x,f_dict,bounds=None,constraints=(),repeat=1,verbose=False,strict_compare=False,**kwargs):
    ''' function to compare performance of standard SLSQP and multistart implementation'''
    fn1 = f_dict['fun']
    jac = f_dict.get('jac',True)
    args = f_dict.get('args',())
    tots,totp = 0,0
    xdim = np.array(x).ndim
    for _ in range(repeat):
        # parallel
        st = time.time()
        res_multi,multi_data = minimise_slsqp_cmp(fn1, x, jac=jac,args=args,bounds=bounds,constraints=constraints,**kwargs)
        endp = time.time()-st
        totp+=endp

        # sequential
        if xdim<2:
            st = time.time()
            res_single = minimize(fn1,x,jac=jac,method='SLSQP',args=args,bounds=bounds,constraints=constraints,options=kwargs)
            ends = time.time()-st
            tots+=ends
        else:
            st = time.time()
            res_single = []
            for x_init in x:
                a = minimize(fn1,x_init,jac=jac,args=args,method='SLSQP',bounds=bounds,constraints=constraints,options=kwargs)
                res_single.append(a)
            ends = time.time()-st
            tots+=ends
    tots,totp=tots/repeat,totp/repeat

    if xdim<2:
        match = compare(res_single,res_multi,x,verbose=verbose,strict_compare=strict_compare)

    else:
        match_lst = []
        for i,(seq,para) in enumerate(zip(res_single,res_multi)):
            _match = compare(seq,para,x[i],verbose=verbose,strict_compare=strict_compare)
            match_lst.append(_match)
    
        match = np.all(match_lst)

    if not match: return False

    sum_seq_nfev = sum_over(res_single,'nfev') # number of function evaluations
    sum_seq_njev = sum_over(res_single,'njev') # number of jacobian evaluations

    print("Comparison between SciPy SLSQP and multistart implementation\n")
    print(res_str('') + res_str('Single') + res_str('Multi'))
    print(res_str('Time') + res_str(f"{tots:.6f}") + res_str(f"{totp:.6f}"))
    print(res_str('No. func eval') + res_str(sum_seq_nfev) + res_str(multi_data['nfev']))
    print(res_str('No. Jacobian eval') + res_str(sum_seq_njev) + res_str(multi_data['njev']))
    print()
    

    return True

def create_x_seed(*args,seed=100,**kwargs):
    np.random.seed(seed)
    return create_x(*args,**kwargs)

def create_x(m,bounds=None):
    if bounds is not None:
        _bnds = np.array(bounds)
        d,t = _bnds.shape
        lower,upper = _bnds.T
    else:
        d=1;lower=0;upper=1
    
    x = np.random.uniform(0,1,size=(m,d))
    x = lower + x*(upper - lower)
    return x

def example_run(run_name,ex_name,fnc,args=(),kwargs={}):
    if run_name not in (ex_name,'all'): return
    buff = '\n'+'#'*30+'\n'
    print(buff)
    print('Running {}\n'.format(ex_name))
    r = fnc(*args,**kwargs)
    print(buff)
    return r

def run_minimize(*args,**kwargs):
    a = minimize(*args,method='SLSQP',**kwargs)
    return a