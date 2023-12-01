import scipy
from multislsqp._version import __version__

__author__  = 'Rhydian Lewis <rhydian.lewis@swansea.ac.uk>'

__all__ = ['minimise_slsqp', 'minimise_slsqp_cmp','run_benchmark_1D', 'run_benchmark_multiD', 'run_benchmarks', 'scipy_version']

_scipy_version = scipy.__version__.split('.')
scipy_version = list(map(int,_scipy_version))   

if scipy_version[0] != 1:
    raise Exception('This version of MultiSLSQP is only compatible with the first major release of SciPy')

if scipy_version[1]==4:
    from multislsqp.scipy_14 import minimise_slsqp, minimise_slsqp_cmp
elif scipy_version[1]==5:
    from multislsqp.scipy_15 import minimise_slsqp, minimise_slsqp_cmp
elif scipy_version[1] in [6,7]:
    from multislsqp.scipy_16 import minimise_slsqp, minimise_slsqp_cmp
elif scipy_version[1] in [8,9,10]:
    from multislsqp.scipy_18 import minimise_slsqp, minimise_slsqp_cmp       
elif scipy_version[1] >10:
    print('Warning: MultiSLSQP is known to work for versions up to and including 1.10.x')
    print('You are currently using version {} of scipy, which means this code may not work as expected.'.format(scipy.__version__))
    from multislsqp.scipy_18 import minimise_slsqp, minimise_slsqp_cmp               
else:
    raise Exception('This version of MultiSLSQP is not compatible with version {} of SciPy'.format(scipy.__version__))

from multislsqp.benchmarks import run_benchmark_1D, run_benchmark_multiD, run_benchmarks