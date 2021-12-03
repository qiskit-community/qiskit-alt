# qiskit_alt

## ATTENTION

This package is NOT part of Qiskit. You can find the [Qiskit repositories here](https://github.com/Qiskit).
And here is [how to install Qiskit](https://qiskit.org/documentation/getting_started.html).

`qiskit_alt` is an experimental package.

## qiskit_alt

This Python package uses a backend written in Julia to implement high performance features for
standard Qiskit. This package is a proof of concept with little high-level code.

### Demonstration

* There are a few demos in this [demonstration benchmark notebook](./demos/qiskit_alt_demo.ipynb)

* The [benchmark code](./bench/) is a good place to get an idea of what qiskit_alt can do.

### Installation/configuration notes

`qisit_alt` uses [pyjulia](https://pyjulia.readthedocs.io/en/latest/index.html) to communicate with Julia. It is advisable
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
    * Write the path to the julia exectuable in `./qiskit_alt/julia_path.py`
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
  Julia executable. If an incompatible system image is loaded, julia will crash.

* Do `python -m venv ./env`, which creates a virtual environment for python packages needed to run `qiskit_alt`.
  You can use whatever name you like in place of the directory `./env`.

* Activate the environment using the file required for your shell. For example
  `source ./env/bin/activate` for bash.

* Install required python packages with `pip install -r requirements.txt`. Or install them one by one.
  pip will clone `qiskit-terra` which takes relatively a long time.

* Install `qiskit_alt` in editable mode, `pip install -e .`

* You may need to start python and do `import julia` and `julia.install()` after pip-installing `pyjulia`.

* You need to do one of the following
    * `ssh-keyscan github.ibm.com >> ~/.ssh/known_hosts`
    * Set this environment variable `export JULIA_SSH_NO_VERIFY_HOSTS=github.ibm.com`

* The Julia packages are installed the first time you run `import qiskit_alt` from Python. If this fails,
  see the log file qiskit_alt.log and the manual steps below.

*  To speed up loading and reduce delays due to just-in-time compilation, you can precompile `qiskit_alt` as follows.
`import qiskit_alt`, `qiskit_alt.compile_qiskit_alt()`. This takes five to ten minutes. The new Julia system image will be found
the next time you import `qiskit_alt`. However, if you don't pre-compile, jit delays are relatively small for `qiskit_alt`.
**AS NOTED ABOVE**, you have to rename or delete the system image in `./sys_image/sys_quantum.so` if you later want to use
a different version or location of Julia.

### Manual steps

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
    has been installed. In this case, the [standard procudure for downloading and installing Julia packages](https://pkgdocs.julialang.org/v1/environments/)
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

#### Julia packages

* The Julia repos [`QuantumOps.jl`](https://github.ibm.com/IBM-Q-Software/QuantumOps.jl) and [`ElectronicStructure.jl`](https://github.ibm.com/IBM-Q-Software/ElectronicStructure.jl),
and [`QiskitQuantumInfo.jl`](https://github.ibm.com/IBM-Q-Software/QiskitQuantumInfo.jl),
are not registered in the General Registry, but rather in [`QuantumRegistry`](https://github.ibm.com/IBM-Q-Software/QuantumRegistry) which contains just
a handful of packages for this project.

#### Communication between Python and Julia

* We are currently using `pyjulia` to call Julia from Python, and it's dependency `PyCall.jl`. The latter
is also used to call Python from Julia.

* An alternative Python package is `juliacall`. This may have some advantages and we may use it in the future.

* An alternative is to create a C-compatible interface on the Julia side and then call it using using Python
methods for calling dynamically linked libraries. We have not yet explored this.

<!--  LocalWords:  qiskit backend qisit pyjulia pypi julia cd venv env txt repo
 -->
<!--  LocalWords:  precompile terra executables toml cli url QuantumRegistry jl
 -->
<!--  LocalWords:  jit toplevel sys PYCALL repl linux NUM pyscf repos PyCall
 -->
<!--  LocalWords:  QuantumOps ElectronicStructure QiskitQuantumInfo juliacall
 -->
