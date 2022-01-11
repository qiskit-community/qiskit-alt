# Automatically installing Julia

`qiskit_alt` will query to download and install Julia if it can't find the exectuable. Alternatively, you can install Julia as described below.

To manage the Julia installation and Julia packages, `qiskit_alt` uses [`julia_project`](https://github.com/jlapeyre/julia_project) and
[`find_julia`](https://github.com/jlapeyre/find_julia).


## Installing Julia manually

You can skip everything below if you allow `qiskit_alt` to install Julia for you.

* Install Julia
    * The [Julia installer `jill.py`](https://github.com/johnnychen94/jill.py) works for most common platforms. `pip install jill`, then `jill install`.
      This [table](https://github.com/johnnychen94/jill.py#about-installation-and-symlink-directories) shows where jill installs
      and symlinks julia on various platforms.
    * [juliaup](https://github.com/JuliaLang/juliaup) for MSWin uses the Windows store.
    * Download a [prebuilt Julia distribution](https://julialang.org/downloads/)

* To allow `qiskit_alt` to find the julia executable you can do one of
    * Install Julia with [`jill.py`](https://github.com/johnnychen94/jill.py), and `qiskit_alt` will find it,
      even if it is not in your PATH.
    * Ensure that the julia executable is in your `PATH` environment variable. For example, under
      linux, `jill` makes a symlink to `/home/username/.local/bin/julia`.
      [More information is here](https://julialang.org/downloads/platform/).
    * Unpack, move, or symlink the julia installation to the toplevel of this `qiskit_alt` package.
      For example `jill` installs to `/home/username/packages/julias/julia-1.7/` under linux, so you
      could make a symlink `julia -> /home/username/packages/julias/julia-1.7/`.
      `qiskit_alt` will search for the executable at `qiskit_alt/julia/bin/julia`.
