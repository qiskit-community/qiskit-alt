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

* [Motivations](#motivations)
    * [The Problem with Python](#the-problem-with-python) a case study
    * [Dynamic Python Julia interface](#dynamic-python-julia-interface)
    * [Caveats](#caveats)

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

* [Development](./Development.md) link to another document in the `qiskit_alt` repo.

## qiskit_alt

This Python package uses a backend written in Julia to implement high performance features for
standard Qiskit. This package is a proof of concept with little high-level code.

## Motivations

I judge it highly probable that Julia provides a uniquely high-productivity environment for developing high-performance
Qiskit features. By high-productivity, I mean higher than Python. By high-performance, I mean
competitive with C or Rust. I base the judgment both on the nature of Julia and of Qiskit. In particular,
Qiskit is built around a large number of complicated pure-Python types, rather than thin wrappers around
standard numerical code. In the following, I present a selection of individual pieces of evidence to back up the judgment,
omitting some of the most important because they require a longer discussion.
However, the overall argument is inevitably rather polemical. The only way to test the judgment is through
experiments, such as this package.

* Julia is developed largely by applied mathematicians. It is dedicated to correct, performant, technical, computing.
But the developers are committed to providing a complete ecosystem, as expected of any ambitious modern language.
A successful full-stack [web framework](https://github.com/GenieFramework/Genie.jl)
is written in Julia.

* Julia is a dynamic language. It is as well suited as Python, I would argue better suited, for rapidly
exploring ideas. This project shows that experimenting with writing Qiskit functionality in Julia,
and exposing it via a Python package, can be done quickly and fruitfully.

* Idiomatic, straightforward, Julia code executes as fast as statically compiled languages.
In addition Julia offers many opportunities for further optimization without leaving the language;
For instance, using macros such as `@inbounds`, `@simd`, `@avx`, `@threads`, and specialized data
types.

* Native data structures are the same or similar to those in languages such as C++ and Rust.
    * Ideas developed in Julia may be ported to these languages and vice-versa. For instance, to
     Qiskit modules written in C++ or Rust.
    * Interfaces between Julia and these languages are straightforward and highly efficient.

* Julia is fully committed to a single, coherent, type system in all aspects of the language.

### The Problem with Python

A case study

* A large amount of Qiskit development effort is expended working around the fact that Python lacks the
features above. An example is the following sequence (and several issues linked within). The issue
involved trying to write both efficient and generic code in a hot location.
    * [Using a numpy integer type as an index for a QuantumRegister fails #3929](https://github.com/Qiskit/qiskit-terra/issues/3929)
    16 comments
    * [Allow numbers.Integral instead of only built-in int for QuantumRegister index #4591](https://github.com/Qiskit/qiskit-terra/pull/4591)
    25 comments, 25 commits.
    * [Performance regression in circuit construction because of type checking #4791](https://github.com/Qiskit/qiskit-terra/issues/4791)
    3 comments
    * [Fixed #4791: Explicity checked for several int types #4810](https://github.com/Qiskit/qiskit-terra/pull/4810)
    1 comment

    The solution was to enumerate possible types and take a small performance hit. Presumably, if further numpy derivatives
    need to be supported, we could weigh the benefit of supporting them vs the cost of adding more checks to the list.
    In contrast, in Julia,
    * Regarding different types of integers, `Int64`, `Int32`, etc.; one would, idiomatically, with little consideration,
      use a parametric type, possibly constrained by the supertype `Integer`.
    * Standard Julia arrays and all kinds of exotic arrays use the same set of integer types, so the issue of supporting
      different numerical packages, GPUs, AD, etc. in this context would not arise.
    * because of compilation and inlining, the check would take, rather than microseconds, strictly no time; it would be elided.
    * So, compared to the Python solution, the code would be far more generic, take far less engineering effort (none), and be
    far more efficient.

    I see similar issues arise over and over in Qiskit development. The productivity gain in developing Qiskit algorithms
    in Julia rather than Python would be, by my rough, not-quite-semi-quantitative, estimate, about ten times. I mean
    medium scale development. Larger than the Jordan-Wigner implementation below, but less than reproducing all of Qiskit.
    It would be interesting, but very difficult, to try to support this estimate with evidence. I think a better approach
    is to carry out experiments such as qiskit_alt.

### Dynamic Python Julia interface

* There are a few good options for using Python and Julia together. The approach here uses
pyjulia, which offers the Python module `julia`. This allows mixing Julia and Python modules
dynamically and rapidly with no interface code required. Conversions of data types is handled
by pyjulia. You can call existing Julia modules or define them from Python. For example,
```python
In [1]  from julia import Main
In [2]: Main.eval("""
    ...: module Foo
    ...:     calc(array, num) = array .+ num
    ...: end""");
In [3]: Main.Foo.calc([1, 2, 3], 4)
Out[3]: array([5, 6, 7], dtype=int64)
```
Here, we have defined a function `calc` in a  Julia module `Foo`.
The input Python list is converted to a Julia array. And the returned Julia array is converted to
a numpy array. Here is an example of how we convert a user defined type from Julia to Python.
```python
def jlPauliList(pauli_list):
    """
    Convert a QiskitQuantumInfo.PauliList to a qiskit.quantum_info.PauliList
    """
    return PauliList.from_symplectic(pauli_list.z, pauli_list.x)
```

### Caveats

* Julia is neither purely interpreted nor traditionally statically compiled. What it "is" evolves;
just-ahead-of-time compiled is a useful description.
But, it doesn't have all the advantages of a language that is largely committed to one (Python) or the other (Rust) model.
In the past, the JIT (or JAOT) penalty was typically large and there weren't a lot of good ways to mitigate it.
The situation today is much, much, improved on several fronts. But, it is still an issue.
At the moment
    * The JIT penalty for qiskit_alt is not great (for someone who started using Julia in 2015).
    First, about 8 seconds to import `qiskit_alt`. Then there are various delays
    for compiling code paths. There are large Julia dependencies that might be attractive, but that incur larger JIT penalties. One
    would have to weigh the consequences of adopting them.
    * But, the penalty is not static, rather it is improving. Ongoing developments include switching to the interpreter;
    more fine-grained optimization and code specialization levels; techniques to avoid cache-invalidations in the method table,
    a huge source of compilation cost.
    * One can reduce the start-up penalty by loading on demand. The [current system](https://github.com/JuliaPackaging/Requires.jl)
    is ok, but a bit ad-hoc and limited. There is talk about improving it, which should require only ordinary engineering effort.
    In fact, we use it to get around a hard dependency on `pyscf`, but I will likely make `pyscf` a hard dependency.
    * One can make a fully AOT-compiled system image. Currently, we can build this locally in `qiskit_alt` in less than five minutes.
    The basic tooling is there, and improving, but could be more polished.
    We are rolling-our own functions and scripts. How robust it is, is a crucial
    question. During development, currently, you *cannot* use the system image. The compiled-in package cannot be replaced dynamically.
    For development, we instead rely on [Revise](./Development.md).

* Julia is not magic, performance-pixie-dust. This should go without saying, but the misconception is encountered frequently enough to
be dangerous to projects. I have seen a relatively small amount of not-to-obscure numba code easily outperform a Julia package.
Using Julia effectively requires learning
some [basic guidelines](https://docs.julialang.org/en/v1/manual/performance-tips/). They are not really difficult to learn and
to employ, but are not optional. So, a good Julia project requires a certain amount of Julia culture. Is it more than that required
for a quality Python project? I think likely not, but it is an important question.

* Julia does not (yet) have multiple inheritance. More generally, understanding how to best use multiple dispatch, traits, various macro-based embellishments
to the type system is perhaps not as mature as the understanding of design in Python.
However, some of the [most ancient (9 years old), large packages](https://github.com/JuliaStats/Distributions.jl)
have weathered the changes relatively well and are still widely used.

* The key creator of Julia, Jeff Bezanson, can tell you [What's bad about Julia](https://www.youtube.com/watch?v=TPuJsgyu87U) in 2019.
This covers the points above and many others.

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

* Do `python -m venv ./env`, which creates a virtual environment for python packages needed to run `qiskit_alt`.
  You can use whatever name you like in place of the directory `./env`.

* Activate the environment using the file required for your shell. For example
  `source ./env/bin/activate` for bash.

* Install required python packages with `pip install -r requirements.txt`. Or install them one by one.
  pip will clone `qiskit-terra` which takes relatively a long time.

* Install `qiskit_alt` in editable mode, `pip install -e .`

* You may need to start python and do `import julia` and `julia.install()` after pip-installing `julia`.

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
One detail that is a bit out of the ordinary is that (only temporarily) the development version of qiskit-terra is used.
`pip` will clone the whole repo, which takes several minutes.


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

### Troubleshooting

* To get the most recent Julia packages, try some of
    * Delete `Manifest.toml` and `./sys_image/Manifest.toml`.
    * Start with a fresh clone of `qiskit_alt`.
    * Start Julia at the command line. And do `Pkg.update()`.

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
