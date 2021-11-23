# qiskit_alt
Components of Qiskit written in Julia

This Python package uses a backend written in Julia to implement high performance features for
standard Qiskit.

* We are currently using `pyjulia` to call Julia from Python, and it's dependency `PyCall.jl`. The latter
is also used to call Python from Julia.

* An alternative Python package is `juliacall`. This may have some advantages and we may use it in the future.

* An alternative is to create a C-compatible interface on the Julia side and then call it using using Python
methods for calling dynamically linked libraries. We have not yet explored this.

### Demonstration

A demonstration of computing a qubit Hamiltonian representing the electronic structure of a molecule starting with
the description of the molecule is provided. The following demo has been superceded by
this [demonstration benchmark notebook](./demos/qiskit_alt_demo.ipynb)

In the following benchmark the Julia version runs about 60 times faster
than the equivalent calculation in qiskit-nature.

First you need to install the python and Julia components.
Then, to run the example, enable the python environment and run the script "./examples/qubit_hamiltonian_ex.py".
The version using only qiskit-nature is in the script "./examples/nature_qubit_hamiltonian_ex.py".
Here are the timings.

```
> ipython
Python 3.9.7 (default, Oct 10 2021, 15:13:22) 

In [1]: %time %run examples/nature_qubit_hamiltonian_ex.py
CPU times: user 1min 10s, sys: 8.08 s, total: 1min 18s
Wall time: 47.2 s

In [2]: %timeit %run examples/qubit_hamiltonian_ex.py
  Activating project at `~/myrepos/quantum_repos/qiskit_alt`
773 ms ± 64.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

* The latter time uses `%timeit`, which hides the compilation time of the Julia version. This can be mitigated by
distributing a pre-compiled system image.

* This package is in very early stages of development. There are no other high-level demonstrations available.

* The phase of the Pauli operators is computed incorrectly. But, correcting this will have a negligible impact on performance.

* The efficiency of the qiskit-nature version could be improved by a more efficient implementation of Fermi operators. The
  efficiency of this package, qiskit_alt, could be improved by reducing the amount of copying. EDIT:
  of the 773ms above, about 2.5ms are spent translating the result of the JW transform through two different representations
  and then copying buffers to a Python object.

* The benchmark above used the "631g" basis. If we instead use the "dzvp2" basis, then the qiskit_alt computation of the Pauli Hamiltonian
  finishes in 18s. The qiskit-nature computation finishes in 5730s.

### Installation/configuration notes

* Python side: This package is developed using an environment created via `python -m venv ./env`. It may be compatible with
other management systems.

* The path to the Julia binary is hardcoded in `./qiskit_alt/activate_julia.py`

* The Julia package requirements are handled using the standard `Project.toml` file. This seems to work when using
`pyjulia` to call Julia from Python. At the moment you need to start Julia and to `Pkg.activate(".")` and `Pkg.instantiate()`. This
only has to be done once. There is a way to install the required Julia packages via python, but we have
not done this. 

* The Julia repos `QuantumOps` and `ElectronicStructure` are not registered. You need to install the master branch of each

* An attempt has been made to make requirements.txt useful. But it is not complete. In particuar `pip list`
  and `pip list --not-required` both seem to erroneously omit some required pacakges and to erroneously include
  some dependencies of installed packages.

* We sometimes use this incantation at the top of Julia code `ENV["PYCALL_JL_RUNTIME_PYTHON"] = Sys.which("python")` to get the correct python
interpreter. Note that the built-in Julia shell and Julia `Sys` report different paths for python. In particular the Julia shell
does not inherit the path from the system shell from which Julia was invoked.

```julia
shell> type python   # This is the Julia repl shell
python is /usr/sbin/python

shell> which python
/usr/sbin/python

julia> Sys.which("python")
"/home/lapeyre/myrepos/quantum_repos/qiskit_alt/env/bin/python"
```

* One way to enable Julia threads (on linux, and maybe other platforms) is by setting an environment variable.
For example `export JULIA_NUM_THREADS=4`. You can check that the threads are available like this.
```python
In [1]: from qiskit_alt import Main  # You could just as well import `Base`

In [2]: Main.Threads.nthreads()
Out[2]: 12
```

### Required packages

Eventually, we should construct a proper requirements.txt file and whatever other manifest and configuration files are necessary.
Until then, we collect a list of installed packages here. Again, to be clear, this is installed in a virtual environment
with `python -m venv ./env`. Most or all of the actions below assume that we have activated the environment. If a package
is listed with no comment, then it was installed via `pip install packagename`.

#### Python

* *qiskit-terra* A development version was needed. We git-cloned the qiskit-terra repo to the toplevel of the qiskit_alt
  repo and entered the directory and did `pip install -e .` (or something like that).

* *qiskit-nature*

* *julia* this is the pypi name of the pyjulia package.

* *pyscf*

#### Julia

* The Julia repos [`QuantumOps.jl`](https://github.com/jlapeyre/QuantumOps.jl) and [`ElectronicStructure.jl`](https://github.com/jlapeyre/ElectronicStructure.jl),
and [`QiskitQuantumInfo.jl`](https://github.com/jlapeyre/QiskitQuantumInfo.jl),
are not registered. You need to install the master branch of each

