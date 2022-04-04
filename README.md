# qiskit_alt

## qiskit_alt

This Python package uses a backend written in Julia to implement high performance features for
standard Qiskit. This package is a proof of concept with little high-level code.

Installing and managing Julia and its packages is automated. So you don't need to learn anything about Julia
to get started.

### Table of contents

* [Installation and configuration notes](#installation-and-configuration-notes)

    * [Compilation](#compilation) Compiling a system image to eliminate compilation at run time.

    * [Using qiskit_alt](#using-qiskit_alt) First steps.

    * [Manual Steps](#manual-steps) Details of automatic installation.

* [Introduction](#introduction)

* [Motivations](./Motivations.md)

* [Demonstration](#demonstration)
    * [Zapata demo of Jordan-Wigner transformation in Julia](https://www.youtube.com/watch?v=-6VfSgPXe4s&list=PLP8iPy9hna6Tl2UHTrm4jnIYrLkIcAROR); The
      same thing as the main demonstration in qiskit_alt.

* [Julia Packages](#julia-packages) Julia packages that qiskit_alt depends on.

* [Troubleshooting](#troubleshooting)

* [Development](./Development.md). Instructions for developing qiskit_alt.

## Installation and Configuration Notes

### Basic

* `qiskit_alt` is available on pypi

```shell
shell> pip install qiskit_alt
```

* Complete installation by running
```python
import qiskit_alt
qiskit_alt.project.ensure_init()
```

See [`julia_project`](https://github.com/jlapeyre/julia_project) for more options.

* If no Julia executable is found, `jill.py` will be used to download and install it. It is *not* necessary
  to add the installation path or symlink path to your search PATH to use julia from qiskit_alt.
  Before offering to install Julia, `qiskit_alt` will search for julia as [described here](./Install_Julia.md).

* The Julia packages are installed the first time you run `qiskit_alt.project.ensure_init()` from Python. If this fails,
  see the log file qiskit_alt.log. You can open a bug report in the [`qiskit_alt` repo](https://github.com/Qiskit-Extensions/qiskit-alt)

* Check that the installation is not completely broken by running benchmark scripts, with the string "alt" in the name:
```sh
python ./bench/run_all_bench.py
```
Note that the folder `bench` is not included when you install via `pip install qiskit_alt`.
But it can be [downloaded here](./bench/).


### More installation details

* `qiskit_alt` depends on [`pyjulia`](https://pyjulia.readthedocs.io/en/latest/index.html)
   and/or [`juliacall`](https://github.com/cjdoris/PythonCall.jl) for communication between Julia and Python.


*  `pyjulia` and `juliacall` are two packages for communication between Python and Julia. You only need
   to import one of them. But, you won't import them directly.

*  When you initialize with `qiskit_alt.project.ensure_init()` the default communication package is chosen.
   You can also choose explicitly with `qiskit_alt.project.ensure_init(calljula="pyjulia")`
   or `qiskit_alt.project.ensure_init(calljula="juliacall")`

* The installation is interactive. How to do a non-interactive installation with environment variables is
  described below.

* You may allow `qiskit_alt` to download and install Julia for you, using [`jill.py`](https://github.com/johnnychen94/jill.py).
  Otherwise you can follow instructions for [installing Julia with an installation tool](./Install_Julia.md).

* We recommend using a virtual Python environment with `venv` or `conda`. For example `python -m venv ./env`,
  which creates a virtual environment for python packages needed to run `qiskit_alt`.
  You can use whatever name you like in place of the directory `./env`.

* Activate the environment using the file required for your shell. For example
  `source ./env/bin/activate` for `venv` and bash.

* Install `qiskit_alt` with `pip install qiskit_alt`.

* Install whatever other packages you want. For example `pip install ipython`.

* Configuring installation with environment variables. If you set these environment variables, you will not be prompted
  during installation.
    * Set `QISKIT_ALT_JULIA_PATH` to the path to a Julia executable (in a Julia installation). This variable takes
      precedence over other methods of specifying the path to the executable.
    * Set `QISKIT_ALT_INSTALL_JULIA` to `y` or `n` to confirm or disallow installing julia via `jill.py`.
    * Set `QISKIT_ALT_COMPILE` to `y` or `n`  to confirm or disallow compiling a system image after installing Julia packages
    * Set `QISKIT_ALT_DEPOT` to `y` or `n` to force using or not using a Julia "depot" specific to this project.

* `qiskit_alt.project.update()` will delete `Manifest.toml` files; upgrade packages; rebuild the manifest; delete compiled system images.
  If you call `update()` while running a compiled system image, you should exit Python and start again before compiling

* `qiskit_alt.project` is an instance of `JuliaProject` from the package [`julia_project`](https://github.com/jlapeyre/julia_project).
   for managing Julia dependencies in Python projects. See more options at [`julia_project`](https://github.com/jlapeyre/julia_project).

### Compilation

*  We highly recommend compiling a system image for `qiskit_alt` to speed up loading and reduce delays due to just-in-time compilation.
   You will be prompted to install when installing or upgrading. Compilation may also be done at any time as follows.

```python
[1]: import qiskit_alt

In [2]: qiskit_alt.project.ensure_init(use_sys_image=False)

In [3]: qiskit_alt.project.compile()
```
Compilation takes about four minutes. The new Julia system image will be found  the next time you import `qiskit_alt`.
Note that we disabled possibly loading a previously-compiled system image before compiling a new one.
This avoids some possible stability issues.


## Using qiskit_alt

This is a very brief introduction.

* The `pyjulia` interface is exposed via the `julia` module. The `juliacall` module is called `juliacall`.
However you should *not* do `import julia` or `import juliacall` before `import qiskit_alt`,
and `qiskit_alt.project.ensure_init()` (or `qiskit_alt.project.ensure_init(calljulia="pyjulia")` or
  `juliacall` with `qiskit_alt.project.ensure_init(calljulia="juliacall")`)
This is because `import julia` will circumvent the facilities described above for choosing the julia executable and the
compiled system image.


* Julia modules are loaded like this. Note that `qiskit_alt.project.julia` points to either `julia` or `juliacall` depending
on which was chosen.
```python
import qiskit_alt
qiskit_alt.project.ensure_init(calljulia=interface_choice)
Main = qiskit_alt.project.julia.Main
```

`import qiskit_alt`; `import julia`; `from julia import PkgName`.
After this, all functions and symbols in `PkgName` are available.
You can do, for example
```python
In [1]: import qiskit_alt

In [2]: qiskit_alt.project.ensure_init()

In [3]: julia = qiskit_alt.project.julia

In [4]: julia.Main.cosd(90)
Out[4]: 0.0

In [5]: QuantumOps = qiskit_alt.project.simple_import("QuantumOps")

In [6]: pauli_sum = QuantumOps.rand_op_sum(QuantumOps.Pauli, 3, 4); pauli_sum
Out[6]:
<PyCall.jlwrap 4x3 QuantumOps.PauliSum{Vector{Vector{QuantumOps.Paulis.Pauli}}, Vector{Complex{Int64}}}:
IIZ * (1 + 0im)
XYI * (1 + 0im)
YIX * (1 + 0im)
ZIZ * (1 + 0im)>
```

In the last example above, `PauliSum` is a Julia object. The `PauliSum` can be converted to
a Qiskit `SparsePauliOp` like this.
```python
In [7]: from qiskit_alt.pauli_operators import PauliSum_to_SparsePauliOp

In [8]: PauliSum_to_SparsePauliOp(pauli_sum)
Out[8]:
SparsePauliOp(['ZII', 'IYX', 'XIY', 'ZIZ'],
              coeffs=[1.+0.j, 1.+0.j, 1.+0.j, 1.+0.j])
```

## Introduction

The highlights thus far are in [benchmark code](./bench/), which is
presented in the demonstration notebooks.
There is one [demonstration notebook using `pyjulia`](./demos/qiskit_alt_demo.ipynb)
and another [demonstration notebook using `juliacall`](./demos/qiskit_alt_demo_jc.ipynb).

The main application-level demonstration is computing a qubit Hamiltonian as a `qiskit.quantum_info.SparsePauliOp`
from a Python list specifiying the molecule geometry in the same format as that used by `qiskit_nature`.

* The Jordan-Wigner transform in qiskit_alt is 30 or so times faster than in qiskit-nature.
* Computing a Fermionic Hamiltonian from pyscf integrals is several times faster, with the factor increasing
  with the problem size.
* Converting an operator from the computational basis, as a numpy matrix, to the Pauli basis, as a `qiskit.quantum_info.SparsePauliOp`,
  is many times faster with the factor increasing rapidly in the number of qubits.

You might want to skip to [installation instructions](#installation-and-configuration-notes)



## Demonstration

* There are a few demos in this [demonstration benchmark notebook](./demos/qiskit_alt_demo.ipynb)

* The [benchmark code](./bench/) is a good place to get an idea of what qiskit_alt can do.

* Here are [some demonstration notebooks](https://github.com/Qiskit-Extensions/QuantumOpsDemos) of the Julia packages behind `qiskit_alt`.

* [Zapata demo of Jordan-Wigner transformation in Julia](https://www.youtube.com/watch?v=-6VfSgPXe4s&list=PLP8iPy9hna6Tl2UHTrm4jnIYrLkIcAROR); The
  same thing as the main demonstration in qiskit_alt. This is from JuliaCon 2020.


### Managing Julia packages

* Available Julia modules are those in the standard library and those listed in [Project.toml](./Project.toml).
You can add more packages (and record them in `Project.toml`) by doing `qiskit_alt.project.julia.Pkg.add("PackageName")`.
You can also do the same by avoiding Python and using the julia cli.


## Julia Packages

* The Julia repos [`QuantumOps.jl`](https://github.com/Qiskit-Extensions/QuantumOps.jl) and
[`ElectronicStructure.jl`](https://github.com/Qiskit-Extensions/ElectronicStructure.jl) and
[`QiskitQuantumInfo.jl`](https://github.com/Qiskit-Extensions/QiskitQuantumInfo.jl)
are not registered in the General Registry, but rather in [`QuantumRegistry`](https://github.com/Qiskit-Extensions/QuantumRegistry) which contains just
a handful of packages for this project.

## Testing

The test folder is mostly out of date.

#### Testing installation with docker

See [the readme](./docker_tests/README-docker_tests.md).

<!--
In addtion to the code in the `bench` directory, there are test directories with just a few tests
in them. They can be run for example via `pytest ./test`. The juliacall tests are in a separate
folder because they can't be run in the same process as pyjulia tests.
 -->

<!--  LocalWords:  qiskit backend qisit pyjulia pypi julia cd venv env txt repo
 -->
<!--  LocalWords:  precompile terra executables toml cli url QuantumRegistry jl
 -->
<!--  LocalWords:  jit toplevel sys PYCALL repl linux NUM pyscf repos PyCall ji
 -->
<!--  LocalWords:  QuantumOps ElectronicStructure QiskitQuantumInfo juliacall
 -->
<!--  LocalWords:  numpy QuantumRegister Explicity supertype GPUs inlining eval
 -->
<!--  LocalWords:  calc num dtype jill symlink symlinks juliaup MSWin prebuilt
 -->
<!--  LocalWords:  keyscan precompiled precompilation PkgName pauli jlwrap IIY
 -->
<!--  LocalWords:  PauliSum im IYZ ZXI ZYI SparsePauliOp YYI ZZY XYZ YZZ TODO
 -->
<!--  LocalWords:  PackageName Fermionic qubits plugable vis jlPauliList JAOT
 -->
<!--  LocalWords:  PauliList invalidations ok AOT numba Bezanson JuliaCon IIZ
 -->
<!--  LocalWords:  XYI YIX ZIZ ZII IYX XIY
 -->
