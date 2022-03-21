# Automatically installing Julia

`qiskit_alt` will query to download and install Julia if it can't find the exectuable. The search and installation for Julia
is done by the Python package [`find_julia, described here`](https://github.com/jlapeyre/find_julia).


Alternatively, you can install Julia as described below.

## Installing Julia manually

You can skip everything below if you allow `qiskit_alt` to install Julia for you.

* Install Julia
    * The [Julia installer `jill.py`](https://github.com/johnnychen94/jill.py) works for most common platforms. `pip install jill`, then `jill install`.
      This [table](https://github.com/johnnychen94/jill.py#about-installation-and-symlink-directories) shows where jill installs
      and symlinks julia on various platforms.
    * [juliaup](https://github.com/JuliaLang/juliaup) for MSWin uses the Windows store. It also works (with improving support) for linux and macos.
    * Download a [prebuilt Julia distribution](https://julialang.org/downloads/)

* To allow `qiskit_alt` to find the julia executable you can do one of
    * Install Julia with [`jill.py`](https://github.com/johnnychen94/jill.py),
      or [juliaup](https://github.com/JuliaLang/juliaup) and `qiskit_alt` will find it, even if it is not in your PATH.
    * Ensure that the julia executable is in your `PATH` environment variable. For example, under
      linux, `jill` makes a symlink to `/home/username/.local/bin/julia`.
      [More information is here](https://julialang.org/downloads/platform/).
    * Set the environment variable `QISKIT_ALT_JULIA_PATH` to the path of your julia executable.
    * Pass the option `julia_path="/path/to/julia/executable"` to the `ensure_init()` when initializing.
      That is: `qiskit_alt.project.ensure_init(julia_path="/path/to/julia/executable", otheopts...)`
