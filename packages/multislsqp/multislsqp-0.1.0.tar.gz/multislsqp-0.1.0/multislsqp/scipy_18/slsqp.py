"""
This module is a variation on the Sequential Least SQuares 
Programming optimization algorithm (SLSQP) used in scipy.optimize.
This code is compatible with version 1.{8,9,10}.x of SciPy (and maybe newer versions). 
The SLSQP algorithm was originally developed by Dieter Kraft.
See http://www.netlib.org/toms/733
                                 
author     : Rhydian Lewis (rhydianlewis1@gmail.com)                                                                   
date       : 25-10-2023                                                     

"""

import numpy as np
from scipy.optimize._slsqp import slsqp
from numpy import (zeros, array, linalg, append, asfarray, concatenate, finfo,
                   sqrt, vstack, exp, inf, isfinite, atleast_1d)
from scipy.optimize._optimize import (OptimizeResult, _check_unknown_options,MemoizeJac,
                                     _clip_x_for_func, _check_clip_x)

from scipy.optimize._constraints import old_bound_to_new, _arr_to_scalar

from multislsqp.scipy_18._numdiff import approx_derivative
from multislsqp.scipy_18.optimize import _prepare_scalar_function

_epsilon = sqrt(finfo(float).eps)

def minimise_slsqp(*args,**kwargs):
    opts,data = minimise_slsqp_cmp(*args,**kwargs)
    return opts

def minimise_slsqp_cmp(func, x0, args=(), jac=None, bounds=None,
                    constraints=(),
                    maxiter=100, ftol=1.0E-6, iprint=1, disp=False,
                    eps=_epsilon, callback=None, finite_diff_rel_step=None,
                    **unknown_options):
    """
    Minimize a scalar function of one or more variables using Sequential
    Least Squares Programming (SLSQP).

    Options
    -------
    ftol : float
        Precision goal for the value of f in the stopping criterion.
    eps : float
        Step size used for numerical approximation of the Jacobian.
    disp : bool
        Set to True to print convergence messages. If False,
        `verbosity` is ignored and set to 0.
    maxiter : int
        Maximum number of iterations.
    finite_diff_rel_step : None or array_like, optional
        If `jac in ['2-point', '3-point', 'cs']` the relative step size to
        use for numerical approximation of `jac`. The absolute step
        size is computed as ``h = rel_step * sign(x0) * max(1, abs(x0))``,
        possibly adjusted to fit into the bounds. For ``method='3-point'``
        the sign of `h` is ignored. If None (default) then step is selected
        automatically.
    """

    if jac is True:
        func = MemoizeJac(func)
        jac = func.derivative

    _check_unknown_options(unknown_options)
    iter = maxiter - 1
    acc = ftol
    epsilon = eps

    if not disp:
        iprint = 0

    # Constraints are triaged per type into a dictionary of tuples
    if isinstance(constraints, dict):
        constraints = (constraints, )

    cons = {'eq': (), 'ineq': ()}
    for ic, con in enumerate(constraints):
        # check type
        try:
            ctype = con['type'].lower()
        except KeyError:
            raise KeyError('Constraint %d has no type defined.' % ic)
        except TypeError:
            raise TypeError('Constraints must be defined using a '
                            'dictionary.')
        except AttributeError:
            raise TypeError("Constraint's type must be a string.")
        else:
            if ctype not in ['eq', 'ineq']:
                raise ValueError("Unknown constraint type '%s'." % con['type'])

        # check function
        if 'fun' not in con:
            raise ValueError('Constraint %d has no function defined.' % ic)

        # check Jacobian
        cjac = con.get('jac')
        if cjac is None:
            # approximate Jacobian function. The factory function is needed
            # to keep a reference to `fun`, see gh-4240.
            def cjac_factory(fun):
                def cjac(x, *args):
                    x = _check_clip_x(x, new_bounds)

                    if jac in ['2-point', '3-point', 'cs']:
                        return approx_derivative(fun, x, method=jac, args=args,
                                                 rel_step=finite_diff_rel_step)
                    else:
                        return approx_derivative(fun, x, method='2-point',
                                                 abs_step=epsilon, args=args)

                return cjac
            cjac = cjac_factory(con['fun'])

        # update constraints' dictionary
        cons[ctype] += ({'fun': con['fun'],
                         'jac': cjac,
                         'args': con.get('args', ())}, )

    exit_modes = {-1: "Gradient evaluation required (g & a)",
                   0: "Optimization terminated successfully",
                   1: "Function evaluation required (f & c)",
                   2: "More equality constraints than independent variables",
                   3: "More than 3*n iterations in LSQ subproblem",
                   4: "Inequality constraints incompatible",
                   5: "Singular matrix E in LSQ subproblem",
                   6: "Singular matrix C in LSQ subproblem",
                   7: "Rank-deficient equality constraint subproblem HFTI",
                   8: "Positive directional derivative for linesearch",
                   9: "Iteration limit reached"}

    # Transform x0 into an np.array.
    x = np.asfarray(x0)
    xdim = x.ndim
    x = np.atleast_2d(x).copy()
    
    nbPoint,dim = _x_breakdown(x) # n = The number of independent variables

    # SLSQP is sent 'old-style' bounds, 'new-style' bounds are required by
    # ScalarFunction
    if bounds is None or len(bounds) == 0:
        new_bounds = (-np.inf, np.inf)
    else:
        new_bounds = old_bound_to_new(bounds)

    # clip the initial guess to bounds, otherwise ScalarFunction doesn't work
    x = np.clip(x, new_bounds[0], new_bounds[1])

    # Set the parameters that SLSQP will need
    # meq, mieq: number of equality and inequality constraints
    meq = sum(map(len, [atleast_1d(c['fun'](x, *c['args']))
              for c in cons['eq']]))
    mieq = sum(map(len, [atleast_1d(c['fun'](x, *c['args']))
               for c in cons['ineq']]))
    meq,mieq = int(meq/nbPoint),int(mieq/nbPoint)
    # m = The total number of constraints
    m = meq + mieq
    # la = The number of constraints, or 1 if there are no constraints
    la = array([1, m]).max()
    # n = The number of independent variables
    n = dim

    # Define the workspaces for SLSQP
    n1 = n + 1
    mineq = m - meq + n1 + n1
    len_w = (3*n1+m)*(n1+1)+(n1-meq+1)*(mineq+2) + 2*mineq+(n1+mineq)*(n1-meq) \
            + 2*meq + n1 + ((n+1)*n)//2 + 2*m + 3*n + 3*n1 + 1
    len_jw = mineq
    w = zeros(len_w)
    jw = zeros(len_jw)

    # Decompose bounds into xl and xu
    if bounds is None or len(bounds) == 0:
        xl = np.empty(n, dtype=float)
        xu = np.empty(n, dtype=float)
        xl.fill(np.nan)
        xu.fill(np.nan)
    else:
        bnds = array([(_arr_to_scalar(l), _arr_to_scalar(u))
                      for (l, u) in bounds], float)
        # bnds = array(bounds, float)
        if bnds.shape[0] != n:
            raise IndexError('SLSQP Error: the length of bounds is not '
                             'compatible with that of x0.')

        with np.errstate(invalid='ignore'):
            bnderr = bnds[:, 0] > bnds[:, 1]

        if bnderr.any():
            raise ValueError('SLSQP Error: lb > ub in bounds %s.' %
                             ', '.join(str(b) for b in bnderr))
        xl, xu = bnds[:, 0], bnds[:, 1]

        # Mark infinite bounds with nans; the Fortran code understands this
        infbnd = ~isfinite(bnds)
        xl[infbnd[:, 0]] = np.nan
        xu[infbnd[:, 1]] = np.nan


    # ScalarFunction provides function and gradient evaluation
    sf = _prepare_scalar_function(func, x, jac=jac, args=args, epsilon=eps,
                                  finite_diff_rel_step=finite_diff_rel_step,
                                  bounds=new_bounds)

    # gh11403 SLSQP sometimes exceeds bounds by 1 or 2 ULP, make sure this
    # doesn't get sent to the func/grad evaluator.
    wrapped_fun = _clip_x_for_func(sf.fun, new_bounds)
    wrapped_grad = _clip_x_for_func(sf.grad, new_bounds)


    # Initialize the iteration counter and the mode value
    acc = np.array(acc, float)
    majiter_prev = 0

    # Initialize internal SLSQP state variables
    varlst, modelst = [],[]
    Res, EC = [],[]
    for _ in range(nbPoint):
        varlst.append([np.array(iter, int), #majiter
                       np.zeros(len_w), #w
                       np.zeros(len_jw), #jw
                       np.array(0, float), #alpha
                       np.array(0, float), #f0
                       np.array(0, float), #gs
                       np.array(0, float), #h1
                       np.array(0, float), #h2
                       np.array(0, float), #h3
                       np.array(0, float), #h4
                       np.array(0, float), #t
                       np.array(0, float), #t0
                       np.array(0, float), #tol
                       np.array(0, int), #iexact
                       np.array(0, int), #incons
                       np.array(0, int), #ireset
                       np.array(0, int), #itermx
                       np.array(0, int), #line
                       np.array(0, int), #n1
                       np.array(0, int), #n2
                       np.array(0, int)]) #n3
        modelst.append(np.array(0, int))
        EC.append(None) # exit code
        Res.append(None) # array where results will be added to

    complete = np.zeros(nbPoint)
    feval_sum = sf.nfev*np.ones(nbPoint).astype('int8')
    geval_sum = np.ones(nbPoint).astype('int8')

    # Print the header if iprint >= 2
    if iprint >= 2:
        print("%5s %5s %16s %16s" % ("NIT", "FC", "OBJFUN", "GNORM"))

    # mode is zero on entry, so call objective, constraints and gradients
    # there should be no func evaluations here because it's cached from
    # ScalarFunction
    fx = wrapped_fun(x)
    g = np.concatenate([wrapped_grad(x),np.zeros([nbPoint,1])],axis=1)
    c = _eval_constraint(x, cons)
    a = _eval_con_normals(x, cons, la, n, m, meq, mieq)
    i=0
    while 1:
        # Call SLSQP
        for _x, _fx, _g,_c,_a, mode, vars,_comp in zip(x,fx,g,c,a,modelst,varlst,complete):
            if _comp:continue
            slsqp(m, meq, _x, xl, xu, _fx, _c, _g, _a, acc, vars[0],mode, *vars[1:])
        
        i+=1

        Modearr = np.array(modelst)
        bl_f = (Modearr==1) # boolean array for those which require function evaluation
        bl_g = (Modearr==-1) # boolean array for those which require gradient evaluation
        sf._bl_f = bl_f
        sf._bl_g = bl_g 

        if bl_f.any(): # objective and constraint evaluation required
            feval_prev = sf.nfev
            _fx = wrapped_fun(x)
            fx[bl_f]= _fx[bl_f]

            c = _eval_constraint(x, cons)

            feval_sum += bl_f*(sf.nfev - feval_prev)


        if bl_g.any(): # gradient evaluation required
            feval_prev = sf.nfev
            geval_prev = sf.ngev

            _g = wrapped_grad(x)
            g[bl_g,:-1] = _g[bl_g]

            a = _eval_con_normals(x, cons, la, n, m, meq, mieq)

            geval_sum += bl_g*(sf.ngev - geval_prev) # update evaluation of gradient
            feval_sum += bl_g*(sf.nfev - feval_prev) # update evaluation of function (only changed when approximate Jacobian used)


        # Check if any has terminated
        _complete = (np.abs(modelst) != 1)*1

        complete_new = _complete - complete # Find the indexes which have recently switched to 1
        if complete_new.any():
            complete = _complete
            new_ixs = complete_new.nonzero()[0] # local indexes
            for ix in new_ixs:
                # Save results
                _var = varlst[ix]
                _mode = modelst[ix]

                opt_out = OptimizeResult(x=x[ix,:], fun=fx.flatten()[ix], jac=g[ix,:-1], nit=int(_var[0]),
                          nfev=feval_sum[ix], njev=geval_sum[ix], status=int(_mode),
                          message=exit_modes[int(_mode)], success=(_mode == 0))
                Res[ix] = opt_out

            if complete.all(): break

        # if majiter > majiter_prev:
        #     # call callback if major iteration has incremented
        #     if callback is not None:
        #         callback(np.copy(x))

        #     # Print the status of the current iterate if iprint > 2
        #     if iprint >= 2:
        #         print("%5i %5i % 16.6E % 16.6E" % (majiter, sf.nfev,
        #                                            fx, linalg.norm(g)))

        # majiter_prev = int(majiter)

    # Optimization loop complete. Print status if requested
    # if iprint >= 1:
    #     print(exit_modes[int(mode)] + "    (Exit mode " + str(mode) + ')')
    #     print("            Current function value:", fx)
    #     print("            Iterations:", majiter)
    #     print("            Function evaluations:", sf.nfev)
    #     print("            Gradient evaluations:", sf.ngev)

    if xdim<2: Res = Res[0]
    
    return Res, {'nfev':sf.nfev,'njev':sf.ngev}

def _x_breakdown(x):
    if x.ndim==2:
        nbPoint,dim = x.shape
    else:
        nbPoint,dim = 0, len(x)
    return nbPoint,dim



def _eval_constraint(x, cons):
    nbPoint,n = _x_breakdown(x)
    # Compute constraints

    if cons['eq']:
        c_eq = np.stack([np.array(con['fun'](x, *con['args'])).flatten()
                                for con in cons['eq']], axis=1)
    else:
        c_eq = np.zeros((nbPoint,0))

    if cons['ineq']:
        c_ieq = np.stack([np.array(con['fun'](x, *con['args'])).flatten()
                                for con in cons['ineq']], axis=1)
    else:
        c_ieq = np.zeros((nbPoint,0))

    # Now combine c_eq and c_ieq into a single matrix
    c = np.concatenate((c_eq, c_ieq),axis=1)
    return c
    
def _eval_con_normals(x, cons, la, n, m, meq, mieq):
    nbPoint,n = _x_breakdown(x)
    # Compute the normals of the constraints
    if cons['eq']:
        a_eq = np.stack([con['jac'](x, *con['args'])
                        for con in cons['eq']],axis=1)

    else:  # no equality constraint
        a_eq = np.zeros((nbPoint, meq, n))

    if cons['ineq']:
        a_ieq = np.stack([con['jac'](x, *con['args'])
                        for con in cons['ineq']],axis=1)
    else:  # no inequality constraint
        a_ieq = np.zeros((nbPoint, mieq, n))

    # Now combine a_eq and a_ieq into a single a matrix
    if m == 0:  # no constraints
        a = np.zeros((nbPoint,la, n))
    else:
        a = np.concatenate((a_eq, a_ieq),axis=1)

    a = np.concatenate((a, np.zeros([nbPoint,la, 1])), 2)
    return a
