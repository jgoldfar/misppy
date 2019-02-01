# misppy

[![Build Status](https://travis-ci.org/jgoldfar/misppy.svg?branch=master)](https://travis-ci.org/jgoldfar/misppy)
[![Build status](https://ci.appveyor.com/api/projects/status/bi8bs42k3otuyv6n?svg=true)](https://ci.appveyor.com/project/jgoldfar/misppy)


misppy is a package for solving the multiphase inverse Stefan problem
(MISP) in Python.
It utilizes [MISPTools.jl]() for its core routines to give high
performance numerical solution of arbitrary multiphase inverse
stefan problems, directly in Python.

## Installation

To install misppy, use pip:

```
pip install misppy
```

Using misppy requires that Julia is installed and in the path, along
with MISPTools.jl and PyCall.jl.
To install Julia, download a generic binary from [the JuliaLang site](https://julialang.org/downloads/) and add it to your path.
To install Julia packages required for misppy, open up Python
interpreter then run:

```pycon
>>> import misppy
>>> misppy.install()
```

and you're good!
In addition, to improve the performance of your code it is
recommended that you use Numba to JIT compile your derivative functions.
To install Numba, use:

```
pip install numba
```

## General Flow

Import and setup the solvers via the commands:

```py
from misppy import isp
```

The general flow for using the package is to follow exactly as would be done
in Julia, except add `misp.` in front.
Most of the commands will work without any modification.
Thus [the MISPTools.jl documentation](https://github.com/jgoldfar/MISPTools.jl)
are the main in-depth documentation for this package.
Below we will show how to translate these docs to Python code.

## Finite Differences

TBD

## Method of Lines

TBD

### One-dimensional ODEs

```py
from diffeqpy import de

def f(u,p,t):
    return -u

u0 = 0.5
tspan = (0., 1.)
prob = de.ODEProblem(f, u0, tspan)
sol = de.solve(prob)
```

The solution object is the same as the one described
[in the DiffEq tutorials](http://docs.juliadiffeq.org/latest/tutorials/ode_example.html#Step-3:-Analyzing-the-Solution-1)
and in the [solution handling documentation](http://docs.juliadiffeq.org/latest/basics/solution.html)
(note: the array interface is missing).
Thus for example the solution time points are saved in `sol.t` and the solution values are saved in `sol.u`.
Additionally, the interpolation `sol(t)` gives a continuous solution.

We can plot the solution values using matplotlib:

```py
import matplotlib.pyplot as plt
plt.plot(sol.t,sol.u)
plt.show()
```

### Solve commands

TBD

### Compilation with Numba and Julia

When solving a differential equation, it's pertinent that your derivative
function `f` is fast since it occurs in the inner loop of the solver.
We can utilize Numba to JIT compile our derivative functions to improve the
efficiency of the solver:

```py
import numba
numba_f = numba.jit(f)

prob = de.ODEProblem(numba_f, u0, tspan)
sol = de.solve(prob)
```

Additionally, you can directly define the functions in Julia
This will allow for more specialization and could be helpful to increase
the efficiency over the Numba version for repeat or long calls.
This is done via `julia.Main.eval`:

```py
from julia import Main
jul_f = Main.eval("(u,p,t)->-u") # Define the anonymous function in Julia
prob = de.ODEProblem(jul_f, u0, tspan)
sol = de.solve(prob)
```

### In-Place Mutating Form

When dealing with systems of equations, in many cases it's helpful to reduce
memory allocations by using mutating functions.
In misppy, the mutating form adds the mutating vector to the front.
Let's make a fast version of the Lorenz derivative, i.e. mutating and JIT compiled:

```py
def f(du,u,p,t):
    x, y, z = u
    sigma, rho, beta = p
    du[0] = sigma * (y - x)
    du[1] = x * (rho - z) - y
    du[2] = x * y - beta * z

numba_f = numba.jit(f)
u0 = [1.0,0.0,0.0]
tspan = (0., 100.)
p = [10.0,28.0,2.66]
prob = de.ODEProblem(numba_f, u0, tspan, p)
sol = de.solve(prob)
```

or using a Julia function:

```py
jul_f = Main.eval("""
function f(du,u,p,t)
  x, y, z = u
  sigma, rho, beta = p
  du[1] = sigma * (y - x)
  du[2] = x * (rho - z) - y
  du[3] = x * y - beta * z
end""")
u0 = [1.0,0.0,0.0]
tspan = (0., 100.)
p = [10.0,28.0,2.66]
prob = de.ODEProblem(jul_f, u0, tspan, p)
sol = de.solve(prob)
```

## Known Limitations

TBD

## Testing

Unit tests can be run by [`tox`](http://tox.readthedocs.io).

```sh
tox                # test with Python 3.6 and 2.7
tox -e py36        # test only with Python 3.6
```

### Troubleshooting

In case you encounter silent failure from `tox`, try running it with
`-- -s` (e.g., `tox -e py36 -- -s`) where `-s` option (`--capture=no`,
i.e., don't capture stdio) is passed to `py.test`.
It may show an error message `"error initializing LibGit2 module"`.
In this case, setting environment variable `SSL_CERT_FILE` may help;
e.g., try:

```sh
SSL_CERT_FILE=PATH/TO/cert.pem tox -e py36
```

See also: [julia#18693](https://github.com/JuliaLang/julia/issues/18693).
