

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10058006.svg)](https://doi.org/10.5281/zenodo.10058006)

# MultiSLSQP

MultiSLSQP is an extension of the SLSQP algorithm used in scipy.optimize.minimize which supports multiple initial starting points. MultiSLSQP has not altered SciPy's SLSQP update step, but instead allows the functional and gradients for multiple initial guesses to be evaluated simultaneously (through the use of NumPy tensors). This results in fewer number of total evaluations of the function and gradients (Jacobian), thus reducing the time required to obtain solutions. 

MultiSLSQP extremely benefical in scenarios where the functional and/or gradients are expensive to evaluate. It is also useufl in scenarios where there are many local optima in the search space, enabling them to be identified concurrently in a fraction of the time, leading to a better chance of finding the global optima.  

## Installation

MultiSLSQP is avalible as a pip package through pypi and as such can be installed with:

```bash
pip install multislsqp
```

The only requirement is the SciPy package since MultiSLSQP is an extension of it. It is compatible with versions of SciPy above 1.4.x and has been tested up to 1.10.1, but may also work for future versions. 

## Usage

MultiSLSQP works in the same way that scipy.optimize.minimize does (when method='SLSQP')

```python
import numpy as np
from multislsqp import minimise_slsqp

def fn(x):
    # functional and gradient used in SLSQP algorithm
    f = np.sin(x)
    df = np.cos(x)
    return f, df

m = 10 # number of different starting points
x = np.random.uniform(-5,5,size=(m,1))
results = minimise_slsqp(fn,x,jac=True)
for i,result in enumerate(results):
    print('#######################################')
    print('Results from starting point {}'.format(x[i]))
    print()
    print(result)
    print()

```


## Benchmarks

MultiSLSQP has two benchmarks included to assess the improved performance possible with this implementation compared with the original implementation in scipy. These can be run with the following

```python
from multislsqp import run_benchmarks
run_benchmarks()
```

The first benchmark is a 1D example, where 100 starting points are evaluated fir the functional $f(x) = sin(x)$ over the range [-10,10].

The second benchmark is a 5D problem, where evaluation of the functional requires the inversion of a large matrix. The output of the benchmarks should look like the following

```bash

Comparison between SciPy SLSQP and multistart implementation

                           Single              Multi        
        Time              0.077988            0.022575      
   No. func eval            512                  15         
 No. Jacobian eval          438                  13    

Comparison between SciPy SLSQP and multistart implementation

                           Single              Multi        
        Time              11.5874             0.1648  
   No. func eval            251                  3          
 No. Jacobian eval          200                  2       

```

The times quoted above used an Intel Core i7-8750H 2.20 GHz (Dell G5 15 laptop).

## Citation

If you use tee4py in your work, please reference it with the following:

If MultiSLSQP has a significant impact during your research please cite it witht he following:


<pre>
@Misc{multislsqp,
author = "Rhydian lewis",
title = "MultiSLSQP",
howpublished = "\url{https://gitlab.com/RhydianL/multislsqp}",
year = "2023",
DOI = https://zenodo.org/doi/10.5281/zenodo.10058005}




