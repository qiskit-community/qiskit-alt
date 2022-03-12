# qiskit_alt

## qiskit_alt

This Python package uses a backend written in Julia to implement high performance features for
standard Qiskit. This package is a proof of concept with little high-level code.

Installing and managing Julia and its packages is automated. So you don't need to learn anything about Julia
to get started.

The highlights thus far are in [benchmark code](./bench/), which is
presented in the [demonstration benchmark notebook](./demos/qiskit_alt_demo.ipynb).

The main application-level demonstration is computing a qubit Hamiltonian as a `qiskit.quantum_info.SparsePauliOp`
from a Python list specifiying the molecule geometry in the same format as that used by `qiskit_nature`.

* The Jordan-Wigner transform in qiskit_alt is 30 or so times faster than in qiskit-nature.
* Computing a Fermionic Hamiltonian from pyscf integrals is several times faster, with the factor increasing
  with the problem size.
* Converting an operator from the computational basis, as a numpy matrix, to the Pauli basis, as a `qiskit.quantum_info.SparsePauliOp`,
  is many times faster with the factor increasing rapidly in the number of qubits.

### Table of contents

* [Motivations](./Motivations.md)

* [Demonstration](#demonstration)
    * [Zapata demo of Jordan-Wigner transformation in Julia](https://www.youtube.com/watch?v=-6VfSgPXe4s&list=PLP8iPy9hna6Tl2UHTrm4jnIYrLkIcAROR); The
      same thing as the main demonstration in qiskit_alt.

* [Installation and configuration notes](#installation-and-configuration-notes)

    * [Compilation](#compilation) Compiling a system image to eliminate compilation at run time.

    * [Using qiskit_alt](#using-qiskit_alt) First steps.

    * [Manual Steps](#manual-steps) Details of automatic installation.

* [Julia Packages](#julia-packages) Julia packages that qiskit_alt depends on.

* [Troubleshooting](#troubleshooting)

* [Communication between Python and Julia](#communication-between-python-and-julia) Options for the language interface.

* [Development](./Development.md). Instructions for developing qiskit_alt.


## Demonstration

* There are a few demos in this [demonstration benchmark notebook](./demos/qiskit_alt_demo.ipynb)

* The [benchmark code](./bench/) is a good place to get an idea of what qiskit_alt can do.

* Here are [some demonstration notebooks](https://github.ibm.com/John-Lapeyre/QuantumDemos) of the Julia packages behind `qiskit_alt`.

* [Zapata demo of Jordan-Wigner transformation in Julia](https://www.youtube.com/watch?v=-6VfSgPXe4s&list=PLP8iPy9hna6Tl2UHTrm4jnIYrLkIcAROR); The
  same thing as the main demonstration in qiskit_alt. This is from JuliaCon 2020.

## Installation and Configuration Notes

### Basic

* `qiskit_alt` is available on pypi: `pip install qiskit_alt`

* Complete installation by running `import qiskit_alt` followed by `qiskit_alt.project.ensure_init()`. See [`julia_project`](https://github.com/jlapeyre/julia_project)
  for more information.

    * If no Julia executable is found, `jill.py` will be used to download and install it. It is *not* necessary
      to add the installation path or symlink path to your search PATH to use julia from qiskit_alt.
      Before offering to install Julia, `qiskit_alt` will search for julia as [described here](./Install_Julia.md).

    * The Julia packages are installed the first time you run `qiskit_alt.project.ensure_init()` from Python. If this fails,
      see the log file qiskit_alt.log and the [manual steps](#manual-steps) below.

* Check that the installation is not completely broken by running benchmark scripts, with the string "alt" in the name:
```sh
python ./bench/run_all_bench.py
```


### More installation details

* `qiskit_alt` depends on the following two packages. It is probably not necessary to read about them to install `qiskit_alt`, but might help.

    * [pyjulia](https://pyjulia.readthedocs.io/en/latest/index.html) is used to communicate with Julia.
      The [installation notes](https://pyjulia.readthedocs.io/en/latest/installation.html) may be useful.

    * [`julia_project`](https://github.com/jlapeyre/julia_project) for managing Julia dependencies.

*  This package is developed in a virtual environment.
   The following instructions assume you are using a virtual environment.
   But, this is not necessary. Nor is it necessary to install `qiskit_alt` in editable mode.

* The installation is interactive. How to do a non-interactive installation with environment variables is
  described below.

* Clone this repository (qiskit_alt) with git and cd to the top level.

* You may allow `qiskit_alt` to download and install Julia for you, using [`jill.py`](https://github.com/johnnychen94/jill.py).
  Otherwise you can follow instructions for [installing Julia manually](./Install_Julia.md).

* Do `python -m venv ./env`, which creates a virtual environment for python packages needed to run `qiskit_alt`.
  You can use whatever name you like in place of the directory `./env`.

* Activate the environment using the file required for your shell. For example
  `source ./env/bin/activate` for bash.

* Install `qiskit_alt`. Optionally in editable mode, i.e. `pip install -e .`

* Install whatever other packages you want. For example `pip install ipython`.

* Configuring installation with environment variables. If you set these environment variables, you will not be prompted
  during installation.
    * Set `QISKIT_ALT_JULIA_PATH` to the path to a Julia executable (in a Julia installation). This variable takes
      precedence over other methods of specifying the path to the executable.
    * Set `QISKIT_ALT_INSTALL_JULIA` to `y` or `n` to confirm or disallow installing julia via `jill.py`.
    * Set `QISKIT_ALT_COMPILE` to `y` or `n`  to confirm or disallow compiling a system image after installing Julia packages


* `qiskit_alt.project.update()` will delete `Manifest.toml` files; upgrade packages; rebuild the manifest; delete compiled system images.
  If you call `update()` while running a compiled system image, you should exit Python and start again before compiling


### Compilation

*  To speed up loading and reduce delays due to just-in-time compilation, you can compile a system image for `qiskit_alt` as follows.
```python
[1]: import qiskit_alt

In [2]: qiskit_alt.project.ensure_init()

In [3]: qiskit_alt.project.compile()
```
Compilation takes about four minutes. The new Julia system image will be found  the next time you import `qiskit_alt`.

* `import qiskit_alt` takes about 8.5s before compilation, and 1.4s after compilation.

* The code is "exercised" during compilation by running the test suites of some of the included packages. Code paths
that are exercised during compilation will suffer no delay in the future, just like statically compiled libraries.
More test suites and exercise scripts can be included in the compilation.
And more Julia code can be moved from `qiskit_alt` into compiled modules.

* "compilation" has different meanings in Julia. Code is always precompiled and cached in a `.ji` file.
What happens during precompilation is described [here](https://julialang.org/blog/2021/01/precompile_tutorial/).
But, this is not the kind of compilation we are considering here.

## Using qiskit_alt

This is a very brief introduction.

* The pyjulia interface is exposed via the `julia` module. However you should *not* do `import julia` before `import qiskit_alt`,
and `qiskit_alt.project.ensure_init()`.
This is because `import julia` will circumvent the facilities described above for choosing the julia executable and the
compiled system image.

* Julia modules are loaded like this.
```python
import qiskit_alt
qiskit_alt.project.ensure_init()
Main = qiskit_alt.project.julia.Main
```

`import qiskit_alt`; `import julia`; `from julia import PkgName`.
After this, all functions and symbols in `PkgName` are available.
You can do, for example
```python
In [1]: import qiskit_alt

In [2]: qiskit_alt.project.ensure_init()

In [3]: julia= qiskit_alt.project.julia

In [4]: julia.Main.cosd(90)
Out[4]: 0.0

In [5]: from julia import QuantumOps

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

This was a brief, low-level view of how `qiskit_alt` works.
The overhead of calling a julia function via `pyjulia` is about 200 micro-seconds.
This in part determines the scale for useful higher-level functions.
Converting types between Julia and Python is also costly.
There are ways to avoid copying, which we have not yet explored.

### Managing Julia packages

* Available Julia modules are those in the standard library and those listed in [Project.toml](./Project.toml).
You can add more packages (and record them in `Project.toml`) by doing `import julia`, `julia.Pkg.add("PackageName")`.
You can also do the same by avoiding Python and using the julia cli.

### Manual Steps

The installation should be as simple as the steps above. But, here is a more detailed account of what happens.
It may be useful in case the automated installation fails.

* How to set up the Python virtual environment and install from `requirements.txt` may be found in several places online.

* Downloading and/or loading Julia components is done in `./qiskit_alt/_julia_project.py`, which uses
 the Python package [`julia_project`](https://github.com/jlapeyre/julia_project)

    * If a compiled Julia system image is found in `./sys_image/`, then it is loaded. Otherwise the standard
      image that ships with Julia is used.
    * The file `Manifest.toml` is created by Julia when first installing packages. If it is missing, it is assumed that nothing
      has been installed. In this case, the [standard procedure for downloading and installing Julia packages](https://pkgdocs.julialang.org/v1/environments/)
     is followed.
    * Most of the Julia packages needed are not registered in the General Registry (This is the counterpart to registering a Python
      package with pypi). They are registered in a registry that will be added to your private Julia installation via the `Pkg` cli command:
      `registry add git@github.ibm.com:John-Lapeyre/QuantumRegistry.git`. You can also add the registry by hand from Julia. A less desirable, but
      workable solution, if the registry fails to install, is to install each package listed in `Project.toml` at the Julia `Pkg` cli or function interface. For
      example `import Pkg; Pkg.add(url="git@github.ibm.com:John-Lapeyre/QuantumOps.jl.git")`.
    * After the registry `QuantumRegistry` is installed, the Julia project is `activate`d, `resolve`d, and `instantiate`d.
      You can also do each of these steps by hand.


## Julia Packages

* The Julia repos [`QuantumOps.jl`](https://github.ibm.com/John-Lapeyre/QuantumOps.jl) and
[`ElectronicStructure.jl`](https://github.ibm.com/John-Lapeyre/ElectronicStructure.jl) and
[`ElectronicStructurePySCF.jl`](https://github.ibm.com/John-Lapeyre/ElectronicStructurePySCF.jl) and
[`QiskitQuantumInfo.jl`](https://github.ibm.com/John-Lapeyre/QiskitQuantumInfo.jl)
are not registered in the General Registry, but rather in [`QuantumRegistry`](https://github.ibm.com/John-Lapeyre/QuantumRegistry) which contains just
a handful of packages for this project.

## Testing

In addtion to the code in the `bench` directory, there are test directories with just a few tests
in them. They can be run for example via `pytest ./test`. The juliacall tests are in a separate
folder because they can't be run in the same process as pyjulia tests.

## Troubleshooting

#### Upgrading Julia packages

* You can call `qiskit_alt.project.update()` or try the manual steps below.

* FIXME: outdated. To get the most recent Julia packages, try some of
    * Delete `Manifest.toml` and `./sys_image/Manifest.toml`.
    * Start Julia at the command line. And do `Pkg.update()`.
    * In python, do `from qiskit_alt import julia; from julia import Pkg; Pkg.update()`.
    * Start with a fresh clone of `qiskit_alt`.

### Errors

* `empty intersection between ElectronicStructure@0.1.1 and project compatibility 0.1.2-*`,
   where the package name and version may vary.
*  Solution: Try [Upgrading Julia packages](#upgrading-julia-packages).

* NOTE: The following error no longer occurs.
`Segmentation fault in expression starting at /home/lapeyre/.julia/packages/ElectronicStructure/FMdUn/src/pyscf.jl:10`.
 This may occur when compiling a system image with `qiskit_alt.project.compile()` after starting `qiskit_alt` with
 a previously compiled system image.
* Solution: Delete sysetm images in `./sys_image/` and restart python.

* `Exception 'ArgumentError' occurred while calling julia code: const PyCall = Base.require(Base.PkgId(Base.UUID("438e738f-606a-5dbb-bf0a-cddfbfd45ab0"), "PyCall"))`.
   This may happen when you try `import qiskit_alt`,  but `PyCall` has not yet been installed for the julia version corresponding to the
    executable found when starting the import of `qiskit_alt`.

* Solution. Try `import julia; julia.install(julia="/path/to/julia")` where the path to the julia executable is the same
 that you chose for `qiskit_alt`. Alternatively, start julia, and do `Pkg.add("PyCall")`. For example, if you have symlinked
 a julia installation to `qiskit_alt/julia/`, then you would start julia from the `qiskit_alt` toplevel as `./julia/bin/julia`,
 and type `Pkg.add("PyCall")`.
 NEW: This installation should happen automatically the first time you run `import qiskit_alt`.

#### Errors when trying to import Python packages from your Python virtual environment via Julia and PyCall

If you activate your Python virtual environment in which you have installed a pacakge, say qiskit,
you may still find that Julia is unable to import it via `PyCall`. In this case,
setting an environment variable will probably do the trick:
```shell
shell> source . env/bin/activate.sh
shell> julia
julia> ENV["PYCALL_JL_RUNTIME_PYTHON"] = Sys.which("python")
julia> import PyCall
julia> PyCall.pyimport("qiskit")
```
If you don't set `ENV["PYCALL_JL_RUNTIME_PYTHON"]` then `pyimport` will fail with an error.
The error messages from `PyCall` will insist that, one way or another, you need to rebuild
`PyCall` via `Pkg.build("PyCall")`. The documentation to `PyCall` is clear on this
as well. Of course, would mean that building `PyCall` in one Julia/Python project
may break it in another, completely separate project. However, as far as I can
tell, setting the environment variable is enough.
Note that you call also set `PYCALL_JL_RUNTIME_PYTHON` from your shell before starting julia.

### Errors related to the compiled custom system image

* You may want to delete the images in `./sys_image/` and build a new one, if compiling repeatedly.
  But, this is normally not necessary.

* If you allow `qiskit_alt` to search your PATH for julia, rather than specifying the location as described above, *and*
if `julia` on your path is a script that loads a custom system image, .i.e. `/path/to/julia -J /path/to/custom-sys-image.so`,
then `qiskit_alt.project.compile()` will likely fail with an error. None of the usual installation methods will create
such a script, so it is not normally something to be concerned about. If in doubt, check the file `qiskit_alt.log`.
However it is not uncommon for people to put a script named "julia" in their path that
runs julia with a custom system image. This is why we must support alternative methods for finding
the executable.


### Communication between Python and Julia

* We are currently using `pyjulia` to call Julia from Python, and its dependency `PyCall.jl`. The latter
is also used to call Python from Julia.

* An alternative Python package is `juliacall`. This may have some advantages and we may use it in the future.

* An alternative is to create a C-compatible interface on the Julia side and then call it using using Python
methods for calling dynamically linked libraries. We have not yet explored this.


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
