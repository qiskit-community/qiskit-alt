# qiskit_alt

## ATTENTION

This package is NOT part of Qiskit. You can find the [Qiskit repositories here](https://github.com/Qiskit).
And here is [how to install Qiskit](https://qiskit.org/documentation/getting_started.html).

`qiskit_alt` is an experimental package.

The highlights thus far are in [benchmark code](./bench/), which is
presented in the [demonstration benchmark notebook](./demos/qiskit_alt_demo.ipynb).

* The Jordan-Wigner transform in qiskit_alt is 30 or so times faster than in qiskit-nature.
* Computing a Fermionic Hamiltonian from pyscf integrals is several times faster, with the factor increasing
  with the problem size.
* Converting an operator from the computational basis, as a numpy matrix, to the Pauli basis, as a `qiskit.quantum_info.SparsePauliOp`,
  is many times faster with the factor increasing rapidly in the number of qubits.

The benchmarks are interesting, but in a sense, only mark the state of development of the two implementations.
There are more general questions than the significance of these particular performance gains.
For instance, how easy is it to develop a robust Python-Julia package for Qiskit? How complex is it? How plugable is it?
What are the advantages and disadvantages vis-a-vis C++/Rust? To whom and at what level should such a package be exposed?
Can and should fruitful designs be ported to C++ or Rust?, Etc.

* [Motivations](./Motivations.md)

* [Demonstration](#demonstration)
    * [Zapata demo of Jordan-Wigner transformation in Julia](https://www.youtube.com/watch?v=-6VfSgPXe4s&list=PLP8iPy9hna6Tl2UHTrm4jnIYrLkIcAROR); The
      same thing as the main demonstration in qiskit_alt.

* [Installation and configuration notes](#installation-and-configuration-notes)

    * [Compilation](#compilation)

    * [Using qiskit_alt](#using-qiskit_alt)

    * [Manual Steps](#manual-steps)

* [Julia Packages](#julia-packages)

* [Notes](#notes)

* [Communication between Python and Julia](#communication-between-python-and-julia)

* [Troubleshooting](#troubleshooting)

* [Development](./Development.md).

## qiskit_alt

This Python package uses a backend written in Julia to implement high performance features for
standard Qiskit. This package is a proof of concept with little high-level code.

## Demonstration

* There are a few demos in this [demonstration benchmark notebook](./demos/qiskit_alt_demo.ipynb)

* The [benchmark code](./bench/) is a good place to get an idea of what qiskit_alt can do.

* [Zapata demo of Jordan-Wigner transformation in Julia](https://www.youtube.com/watch?v=-6VfSgPXe4s&list=PLP8iPy9hna6Tl2UHTrm4jnIYrLkIcAROR); The
  same thing as the main demonstration in qiskit_alt. This is from JuliaCon 2020.

## Installation and Configuration Notes

`qiskit_alt` uses [pyjulia](https://pyjulia.readthedocs.io/en/latest/index.html) to communicate with Julia. It is advisable
to read the pyjulia [installation notes](https://pyjulia.readthedocs.io/en/latest/installation.html)

`qiskit_alt` is not available on pypi.
This package is developed in a virtual environment. The following instructions assume you are using a virtual environment.

* Clone this repository (qiskit_alt) with git and cd to the top level.

* Install Julia. Some possibilities are
    * The [Julia installer `jill`](https://github.com/johnnychen94/jill.py) works for most common platforms. `pip install jill`, then `jill install`.
      This [table](https://github.com/johnnychen94/jill.py#about-installation-and-symlink-directories) shows where jill installs
      and symlinks julia on various platforms.
    * [juliaup](https://github.com/JuliaLang/juliaup) for MSWin uses the Windows store.
    * Download a [prebuilt Julia distribution](https://julialang.org/downloads/)

* To allow `qiskit_alt` to find the julia executable you can do one of
    * Unpack, move, or symlink the julia installation to the toplevel of this `qiskit_alt` package.
      For example `jill` installs to `/home/username/packages/julias/julia-1.7/` under linux, so you
      could make a symlink `julia -> /home/username/packages/julias/julia-1.7/`.
      `qiskit_alt` will search for the executable at `qiskit_alt/julia/bin/julia`.
    * Write the path to the julia executable in `./qiskit_alt/julia_path.py`
       For example, on a Mac, this might be
      ```python
       julia_path = "/Applications/Julia-1.6.app/Contents/Resources/julia/bin/julia"
       ```
       Specifying the executable path here will override the folder `julia` described in the previous item.
    * Ensure that the julia executable is in your `PATH` environment variable. For example, under
      linux, `jill` makes a symlink to `/home/username/.local/bin/julia`.
      [More information is here](https://julialang.org/downloads/platform/).

* **NOTE** If you have built a Julia system image (see below), then it will be loaded before any of the options above.
  You must rename or delete the system image in `./sys_image/sys_quantum.so` if you want to change the location or version of the
  Julia executable. If an incompatible system image is loaded, julia will crash. It wouldn't take much effort (but some!) to
  detect incompatibilities and issue a user-friendly warning, or error, or take action. In fact, developing a Julia and/or Python
  package for compiling and managing system images might be worthwhile. For the moment, we are rolling our own within qiskit_alt.

* **NOTE** If you allow `qiskit_alt` to search your PATH for julia, rather than specifying the location as described above, *and*
if `julia` on your path is a script that loads a custom system image, .i.e. `/path/to/julia -J /path/to/custom-sys-image.so`,
then `qiskit_alt.compile_qiskit_alt()` will likely fail with an error. None of the usual installation methods will create
such a script, so it is not normally something to be concerned about. If in doubt, check the file `qiskit_alt.log`.

* Do `python -m venv ./env`, which creates a virtual environment for python packages needed to run `qiskit_alt`.
  You can use whatever name you like in place of the directory `./env`.

* Activate the environment using the file required for your shell. For example
  `source ./env/bin/activate` for bash.

* Install required python packages with `pip install -r requirements.txt`. Or install them one by one.

* Install `qiskit_alt` in editable mode, `pip install -e .`

* Start python and do `import julia` and `julia.install(julia="./julia/bin/julia")` replacing
  the path by the path you chose above when installing julia.
  NEW: This step should happen automatically the first time you run `import qiskit_alt`.

* You need to do one of the following
    * `ssh-keyscan github.ibm.com >> ~/.ssh/known_hosts`
    * Set this environment variable `export JULIA_SSH_NO_VERIFY_HOSTS=github.ibm.com`

* The Julia packages are installed the first time you run `import qiskit_alt` from Python. If this fails,
  see the log file qiskit_alt.log and the [manual steps](#manual-steps) below.


### Compilation

*  To speed up loading and reduce delays due to just-in-time compilation, you can compile a system image for `qiskit_alt` as follows.
```python
[1]: import qiskit_alt
  Activating project at `~/myrepos/quantum_repos/qiskit_alt`

In [2]: qiskit_alt.compile_qiskit_alt()
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

* **AS NOTED ABOVE**, you have to rename or delete the system image in `./sys_image/sys_quantum.so` if you later want to use
a different version or location of Julia.

## Using qiskit_alt

This is a very brief introduction.

* The pyjulia interface is exposed via the `julia` module. However you should *not* do `import julia` before `import qiskit_alt`.
This is because `import julia` will circumvent the facilities described above for choosing the julia executable and the
compiled system image.

* Julia modules are loaded like this. `import qiskit_alt`; `import julia`; `from julia import PkgName`. (For convenience
the Julia modules `Main` and `Base` are imported and reexported into and from `qiskit_alt`.)
After this, all functions and symbols in `PkgName` are available.
You can do, for example
```python
In [1]: import qiskit_alt, julia  # qiskit_alt first

In [2]: julia.Main.cosd(90)
Out[2]: 0.0

In [3]: from qiskit_alt import QuantumOps # or from julia import QuantumOps

In [4]: pauli_sum = QuantumOps.rand_op_sum(QuantumOps.Pauli, 3, 4); pauli_sum
Out[4]: 
<PyCall.jlwrap 4x3 QuantumOps.PauliSum{Vector{Vector{QuantumOps.Paulis.Pauli}}, Vector{Complex{Int64}}}:
IIZ * (1 + 0im)
XYI * (1 + 0im)
YIX * (1 + 0im)
ZIZ * (1 + 0im)>
```
In the last example above, `PauliSum` is a Julia object. The `PauliSum` can be converted to
a Qiskit `SparsePauliOp` like this.
```python
In [5]: qiskit_alt.PauliSum_to_SparsePauliOp(pauli_sum)
Out[5]: 
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

* Downloading and/or loading Julia components is done in `./qiskit_alt/activate_julia.py`.

    * If the file  `./qiskit_alt/julia_path.py` exists, then the Julia executable path is read from it. Otherwise the
      standard path for finding executables is used.
    * If a compiled Julia system image is found in `./sys_image/sys_quantum.so`, then it is loaded. Otherwise the standard
      image that ships with Julia is used.
    * The file `Manifest.toml` is created by Julia when first installing packages. If it is missing, it is assumed that nothing
    has been installed. In this case, the [standard procedure for downloading and installing Julia packages](https://pkgdocs.julialang.org/v1/environments/)
     is followed.
    * Most of the Julia packages needed are not registered in the General Registry (This is the counterpart to registering a Python
      package with pypi). They are registered in a registry that will be added to your private Julia installation via the `Pkg` cli command:
      `registry add git@github.ibm.com:IBM-Q-Software/QuantumRegistry.git`. You can also add the registry by hand from Julia. A less desirable, but
      workable solution, if the registry fails to install, is to install each package listed in `Project.toml` at the Julia `Pkg` cli or function interface. For
      example `import Pkg; Pkg.add(url="git@github.ibm.com:IBM-Q-Software/QuantumOps.jl.git")`.
    * After the registry `QuantumRegistry` is installed, the Julia project is `activate`d, `resolve`d, and `instantiate`d.
      You can also do each of these steps by hand.

* Compiling `qiskit_alt`. This is not necessary, but will make `qiskit_alt` load faster and cause fewer jit delays due to compilation at run time.
The Python function `qiskit_alt.compile_qiskit_alt()` will do the equivalent of the following.
Start Julia from a shell at the toplevel of the `qiskit_alt` installation and run the compile script as follows.
```julia
import Pkg
cd("./sys_image")
Pkg.activate(".")
include("compile_quantum.jl")
```

## Julia packages

* The Julia repos [`QuantumOps.jl`](https://github.ibm.com/IBM-Q-Software/QuantumOps.jl) and [`ElectronicStructure.jl`](https://github.ibm.com/IBM-Q-Software/ElectronicStructure.jl),
and [`QiskitQuantumInfo.jl`](https://github.ibm.com/IBM-Q-Software/QiskitQuantumInfo.jl),
are not registered in the General Registry, but rather in [`QuantumRegistry`](https://github.ibm.com/IBM-Q-Software/QuantumRegistry) which contains just
a handful of packages for this project.

### Notes

* We sometimes use this incantation at the top of Julia code `ENV["PYCALL_JL_RUNTIME_PYTHON"] = Sys.which("python")` to get the correct python
interpreter. Note that the built-in Julia shell and Julia `Sys` report different paths for python. In particular the Julia shell
does not inherit the path from the system shell from which Julia was invoked.
```julia
shell> type python   # This is the Julia repl shell
python is /usr/sbin/python

shell> which python
/usr/sbin/python

julia> Sys.which("python")
"/home/username/myrepos/quantum_repos/qiskit_alt/env/bin/python"
```

* One way to enable Julia threads (on linux, and maybe other platforms) is by setting an environment variable.
For example `export JULIA_NUM_THREADS=4`. You can check that the threads are available like this.
```python
In [1]: from qiskit_alt import Main  # You could just as well import `Base`

In [2]: Main.Threads.nthreads()
Out[2]: 12
```

### Communication between Python and Julia

* We are currently using `pyjulia` to call Julia from Python, and its dependency `PyCall.jl`. The latter
is also used to call Python from Julia.

* An alternative Python package is `juliacall`. This may have some advantages and we may use it in the future.

* An alternative is to create a C-compatible interface on the Julia side and then call it using using Python
methods for calling dynamically linked libraries. We have not yet explored this.

## Troubleshooting

#### Upgrading Julia packages
* To get the most recent Julia packages, try some of
    * Delete `Manifest.toml` and `./sys_image/Manifest.toml`.
    * Start Julia at the command line. And do `Pkg.update()`.
    * In python, do `from qiskit_alt import julia; from julia import Pkg; Pkg.update()`.
    * Start with a fresh clone of `qiskit_alt`.

### Errors

* `empty intersection between ElectronicStructure@0.1.1 and project compatibility 0.1.2-*`,
   where the package name and version may vary.
*  Solution: Try [Upgrading Julia packages](#upgrading-julia-packages).

* `Segmentation fault in expression starting at /home/lapeyre/.julia/packages/ElectronicStructure/FMdUn/src/pyscf.jl:10`.
 This may occur when compiling a system image with `qiskit_alt.compile_qiskit_alt()` after starting `qiskit_alt` with
 a previously compiled system image.
* Solution: Delete `./sys_image/sys_quantum.so` and restart python.

* `Exception 'ArgumentError' occurred while calling julia code: const PyCall = Base.require(Base.PkgId(Base.UUID("438e738f-606a-5dbb-bf0a-cddfbfd45ab0"), "PyCall"))`.
   This may happen when you try `import qiskit_alt`,  but `PyCall` has not yet been installed for the julia version corresponding to the
    executable found when starting the import of `qiskit_alt`.
* Solution. Try `import julia; julia.install(julia="/path/to/julia")` where the path to the julia executable is the same
 that you chose for `qiskit_alt`. Alternatively, start julia, and do `Pkg.add("PyCall")`. For example, if you have symlinked
 a julia installation to `qiskit_alt/julia/`, then you would start julia from the `qiskit_alt` toplevel as `./julia/bin/julia`,
 and type `Pkg.add("PyCall")`.
 NEW: This installation should happen automatically the first time you run `import qiskit_alt`.

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
