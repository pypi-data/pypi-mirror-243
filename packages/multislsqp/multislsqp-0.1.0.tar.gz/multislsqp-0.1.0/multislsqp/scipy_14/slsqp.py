"""
This module is a variation on the Sequential Least SQuares 
Programming optimization algorithm (SLSQP) used in scipy.optimize.
This code is compatible with version 1.4.x of SciPy. 
The SLSQP algorithm was originally developed by Dieter Kraft.
See http://www.netlib.org/toms/733
                                 
author     : Rhydian Lewis (rhydianlewis1@gmail.com)                                                                   
date       : 25-10-2023                                                     

"""

import numpy as np
from scipy.optimize.optimize import wrap_function, OptimizeResult, _check_unknown_options, MemoizeJac
from scipy.optimize._slsqp import slsqp

_epsilon = np.sqrt(np.finfo(float).eps)

def approx_jacobian(x, func, epsilon, *args):
    """
    Approximate the Jacobian matrix of a callable function.

    Parameters
    ----------
    x : array_like
        The state vector at which to compute the Jacobian matrix.
    func : callable f(x,*args)
        The vector-valued function.
    epsilon : float
        The perturbation used to determine the partial derivatives.
    args : sequence
        Additional arguments passed to func.

    Returns
    -------
    An array of dimensions ``(lenf, lenx)`` where ``lenf`` is the length
    of the outputs of `func`, and ``lenx`` is the number of elements in
    `x`.

    Notes
    -----
    The approximation is done using forward differences.

    """
    x0 = np.asfarray(x)
    f0 = np.atleast_1d(func(*((x0,)+args)))
    dx = np.zeros(x0.shape)
    
    if x0.ndim==2:
        jac = np.zeros(x0.shape)
        for i in range(x0.shape[1]):
            dx[:,i] = epsilon
            jac[:,i] = ((func(*((x0+dx,)+args)) - f0)/epsilon).flatten()
            dx[:,i] = 0.0
    else:
        jac = np.zeros([len(x0), len(f0)])
        for i in range(len(x0)):
            dx[i] = epsilon
            jac[i] = (func(*((x0+dx,)+args)) - f0)/epsilon
            dx[i] = 0.0
        jac = jac.transpose()

    return jac

def minimise_slsqp(*args,**kwargs):
    opts,data = minimise_slsqp_cmp(*args,**kwargs)
    return opts

def minimise_slsqp_cmp(func, x0, args=(), jac=None, bounds=None,
                    constraints=(),
                    maxiter=100, ftol=1.0E-6, iprint=1, disp=False,
                    eps=_epsilon, callback=None,
                    **unknown_options):

    if not callable(jac) and bool(jac):
        func = MemoizeJac(func)
        jac = func.derivative

    fprime = jac
    iter = maxiter
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
            # approximate Jacobian function.  The factory function is needed
            # to keep a reference to `fun`, see gh-4240.
            def cjac_factory(fun):
                def cjac(x, *args):
                    return approx_jacobian(x, fun, epsilon, *args)
                return cjac
            cjac = cjac_factory(con['fun'])


        # update constraints' dictionary
        cons[ctype] += ({'fun': con['fun'],
                         'jac': cjac,
                         'args': con.get('args', ())}, )

    exit_modes = {-1: "Gradient evaluation required (g & a)",
                   0: "Optimization terminated successfully.",
                   1: "Function evaluation required (f & c)",
                   2: "More equality constraints than independent variables",
                   3: "More than 3*n iterations in LSQ subproblem",
                   4: "Inequality constraints incompatible",
                   5: "Singular matrix E in LSQ subproblem",
                   6: "Singular matrix C in LSQ subproblem",
                   7: "Rank-deficient equality constraint subproblem HFTI",
                   8: "Positive directional derivative for linesearch",
                   9: "Iteration limit exceeded"}

    # Wrap func
    feval, func = wrap_function(func, args)

    # Wrap fprime, if provided, or approx_jacobian if not
    if fprime:
        geval, fprime = wrap_function(fprime, args)
    else:
        geval, fprime = wrap_function(approx_jacobian, (func, epsilon))

    # Transform x0 into an np.array.
    x = np.asfarray(x0)
    xdim = x.ndim
    x = np.atleast_2d(x).copy()
    # n = The number of independent variables
    nbPoint,n = x.shape

    # Set the parameters that SLSQP will need
    # meq, mieq: number of equality and inequality constraints
    meq = sum(map(len, [np.atleast_1d(c['fun'](x, *c['args']))
              for c in cons['eq']]))
    mieq = sum(map(len, [np.atleast_1d(c['fun'](x, *c['args']))
               for c in cons['ineq']]))
    meq,mieq = int(meq/nbPoint),int(mieq/nbPoint)

    # m = The total number of constraints
    m = meq + mieq
    # la = The number of constraints, or 1 if there are no constraints
    la = np.array([1, m]).max()



    # Define the workspaces for SLSQP
    n1 = n + 1
    mineq = m - meq + n1 + n1
    len_w = (3*n1+m)*(n1+1)+(n1-meq+1)*(mineq+2) + 2*mineq+(n1+mineq)*(n1-meq) \
            + 2*meq + n1 + ((n+1)*n)//2 + 2*m + 3*n + 3*n1 + 1
    len_jw = mineq
    w = np.zeros(len_w)
    jw = np.zeros(len_jw)

    # Decompose bounds into xl and xu
    if bounds is None or len(bounds) == 0:
        xl = np.empty(n, dtype=float)
        xu = np.empty(n, dtype=float)
        xl.fill(np.nan)
        xu.fill(np.nan)
    else:
        bnds = np.array(bounds, float)
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
        infbnd = ~np.isfinite(bnds)
        xl[infbnd[:, 0]] = np.nan
        xu[infbnd[:, 1]] = np.nan

    # Clip initial guess to bounds (SLSQP may fail with bounds-infeasible
    # initial point)
    have_bound = np.isfinite(xl)
    x[:,have_bound] = np.clip(x[:,have_bound], xl[have_bound], np.inf)
    have_bound = np.isfinite(xu)
    x[:,have_bound] = np.clip(x[:,have_bound], -np.inf, xu[have_bound])

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
    feval_sum = np.zeros(nbPoint).astype('int8')
    geval_sum = np.zeros(nbPoint).astype('int8')

    # Print the header if iprint >= 2
    if iprint >= 2:
        print("%5s %5s %16s %16s" % ("NIT", "FC", "OBJFUN", "GNORM"))

    First=True
    while True:
        Modearr = np.array(modelst)
        bl_f = (Modearr==0)+(Modearr==1)
        if bl_f.any(): # objective and constraint evaluation required
            _fx_all = func(x)
            feval_sum += bl_f*1

            # ensure that only the necessary function evaluation are updated (to ensure matching with usual scipy implementation)
            if First: fx_all = _fx_all
            else: fx_all[bl_f] = _fx_all[bl_f]

            try:
                fx = np.asarray(fx_all)

            except (TypeError, ValueError):
                raise ValueError("Objective function must return a scalar")
            # Compute the constraints

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

            

        bl_g = (Modearr==0)+(Modearr==-1)
        if bl_g.any(): # gradient evaluation required
            # Compute the derivatives of the objective function
            # For some reason SLSQP wants g dimensioned to n+1
            feval_prev = feval[0]
        
            g_all = fprime(x)

            geval_sum += bl_g*1 # update evaluation of gradient
            feval_sum += bl_g*(feval[0] - feval_prev) # update evaluation of function (only changed when approximate Jacobian used)

            

            # ensure that only the necessary gradients are updated (to ensure matching with usual scipy implementation)
            if First: g = g_all
            else: g[bl_g.flatten()] = g_all[bl_g.flatten()]

            # Compute the normals of the constraints
            if cons['eq']:
                a_eq = np.stack([con['jac'](x, *con['args'])
                               for con in cons['eq']],axis=1)
                # a_eq = np.swapaxes(a_eq,1,2)
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

        g2 = np.concatenate([g,np.zeros([nbPoint,1])],axis=1)

        for xi, _fx, _g,_c,_a, mode, vars in zip(x,fx,g2,c,a,modelst,varlst):
            if not First and abs(mode)!=1:continue
            _call_slsqp(m, meq, xi, xl, xu, _fx, _c, _g, _a, acc, vars[0],mode, *vars[1:])

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

                opt_out = OptimizeResult(x=x[ix,:], fun=fx.flatten()[ix], jac=g2[ix,:-1], nit=int(_var[0]),
                          nfev=feval_sum[ix], njev=geval_sum[ix], status=int(_mode),
                          message=exit_modes[int(_mode)], success=(_mode == 0))
                Res[ix] = opt_out

            if complete.all(): break

        First=False
        
    if xdim<2: Res = Res[0]

    return Res, {'nfev':feval[0],'njev':geval[0]}

def _call_slsqp(*args):
    r = slsqp(*args)
    return args 

