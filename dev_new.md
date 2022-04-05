# Working on Julia packages within qiskit_alt

You can start by using qiskit_alt to set up the Julia project for you.
Then we will forget about qiskit_alt for the time being and only develop
a Julia package.

### Optionally install Julia

You can let qiskit-alt install Julia for you.
But, Julia is easy to install (except for those who run into a problem!);
you may want to try it.
If you do install julia yourself, qiskit-alt will use this installation.
To install  Look for either *juliaup* or *jill*.
(Google for *jill python* because there is another non-python version).
For instance to use jill, do this:
```shell
> pip install jill
> jill install
```
This will install julia and try to put it on your command path.

### Install qiskit-alt in development mode

If you are just using qiskit_alt, you can give the command `pip install qiskit_alt`.
You might try this just to explore a bit.
But, since you want to develop qiskit-alt it is better to install it in development mode.

```shell
> git clone https://github.com/Qiskit-Extensions/qiskit-alt
> cd qiskit-alt
```

(Really, a better idea is to go to github and fork qiskit-alt, then pull the repostory to
your machine as instructed)

You typically want to work in a virtual environment that is specific to your development
clone of `qiskit_alt`. So for example in linux (maybe macos too) and
using the standard bash shell, you do (inside the qiskit-alt directory)

```shell
> python -m venv ./venv
> source ./venv/bin/activate  # Activate this environment
```
Just use the command `deactivate` alone to deactivate the environment later.

Alternatively, you may want to use `conda`; i.e. instead of `venv`. Use only one or the other
at a time.
First install conda. Then do something like
```shell
> conda create -n qiskit_alt_env python=3.9
> conda activate qiskit_alt_env
```
I used python 3.9 here because conda installed 3.10 the first time I tried this. Qiskit
is (probably still?) pegged at python 3.9 because it depends on pyscf which also has this
restriction.

Now use this shell with the active virtual environment to run your command line interface or Jupyter notebook, or whatever you are going to use.
I use `ipython` as a cli. It has a few good advantages over `python`. With the virtual
environment active, we do
```shell
> pip install --upgrade pip ipython # upgrade pip to silence complaints
```
Now you can install qiskit-alt in development mode like this
```shell
> pip install -e .
```

Do the first initialization of qiskit-alt.
```python
> ipython
In [1]: import qiskit_alt
In [2]: qiskit_alt.project.ensure_init(compile=False)
In [3]: %run bench/run_all_bench.py  # test some features
```
I explicitly used `compile=False` because we want edit packages, which is not possible if they are
compiled into a system image.


### Develop (that is, work on) a Julia package

You probably only have one version of Julia installed, and it is on your
path, so you can start it by typing `julia` at the shell prompt.
But, it may be that qiskit-alt has installed julia and it is *not* on your
path. (You can try to fix this. I think you may
need to put `~/.local/bin` on your path (`PATH` environment variable) if it is not already. Some OSes
have this on your path already.)
You can also find the path to the julia executable via qiskit-alt like this
```python
import qiskit_alt
qiskit_alt.project.ensure_init()
qiskit_alt.project.julia_path
```
qiskit-alt manages julia dependencies in a *Julia project*, which is similar to
a python virtual environment. You can find the location of the Julia project like this
```python
qiskit_alt.project.project_path
```
If you are using a `venv` virtual environment, this will return a path to the
Julia project that looks something like
```
'/home/quser/qiskit_alt/venv/julia_project/qiskit_alt-1.7.2'.
```
If you are using conda, this will return a path to the
Julia project that looks something like
```
'/home/quser/.conda/envs/qiskit_alt_env/julia_project/qiskit_alt-1.7.2'
```

Start julia from a shell and activate the project and load a Julia package
that is in the project
```julia
julia> using Pkg

julia> Pkg.activate("/home/quser/.conda/envs/qiskit_alt_env/julia_project/qiskit_alt-1.7.2")
   Activating project at `~/.conda/envs/qiskit_alt_env/julia_project/qiskit_alt-1.7.2`

julia> using QuantumOps

julia> rand_op_sum(Pauli, 3, 2)
2x3 PauliSum{Vector{Vector{Pauli}}, Vector{Complex{Int64}}}:
IXY * (1 + 0im)
YYZ * (1 + 0im)
```

You can check the status of QuantumOps like this
```julia
julia> pkg"status QuantumOps"
      Status `~/.conda/envs/qiskit_alt_env/julia_project/qiskit_alt-1.7.2/Project.toml`
  [d0cc4389] QuantumOps v0.1.5
```

The copy of the `QuantumOps` package is read-only (although that's not shown above.)
We need to install an editable copy. So we "develop" the package. This will install
the git repo in a new location where we can edit it.
```julia
julia> pkg"develop QuantumOps"
    Cloning git-repo `https://github.com/Qiskit-Extensions/QuantumOps.jl`
   Resolving package versions...
    Updating `~/.conda/envs/qiskit_alt_env/julia_project/qiskit_alt-1.7.2/Project.toml`
  [d0cc4389] ~ QuantumOps v0.1.5 ⇒ v0.1.5 `~/.julia/dev/QuantumOps`
    Updating `~/.conda/envs/qiskit_alt_env/julia_project/qiskit_alt-1.7.2/Manifest.toml`
  [d0cc4389] ~ QuantumOps v0.1.5 ⇒ v0.1.5 `~/.julia/dev/QuantumOps`

julia> pkg"status  QuantumOps"
      Status `~/.conda/envs/qiskit_alt_env/julia_project/qiskit_alt-1.7.2/Project.toml`
  [d0cc4389] QuantumOps v0.1.5 `~/.julia/dev/QuantumOps`
```
Note that the status now shows the path in `~/.julia/dev/`. This will persist across
sessions until QuantumOps is freed via `Pkg.free()`.

Now exit Julia and start again, loading the package Revise first.
```julia
julia> using Pkg
julia> Pkg.activate("/home/quser/.conda/envs/qiskit_alt_env/julia_project/qiskit_alt-1.7.2");
julia> using Revise; using QuantumOps;
```

Issue #12 is about printing of Pauli terms. Let's investigate.
```julia
julia> t = PauliTerm()
0-factor PauliTerm{Vector{Pauli}, Complex{Int64}}:
 * (1 + 0im)

julia> @which show(stdout, t)
show(io::IO, term::QuantumOps.AbstractTerm) in QuantumOps at /home/quser/.julia/dev/QuantumOps/src/abstract_term.jl:17
```
The function `show` is responsible for displaying. And the function method is called is on line 17 of *abstract_term.jl*.

Let's say we want to print nothing when there are no Pauli operators instead of `* (1 + 0im)`.
The method is [here](https://github.com/Qiskit-Extensions/QuantumOps.jl/blob/d5648bf8779bbe1211bd5c63270bad165384e344/src/abstract_term.jl#L7-L21)
```julia
function Base.show(io::IO, term::AbstractTerm)
    m = length(term)
    print(io, m, "-factor", " ", typeof(term), ":\n")
    _show_abstract_term(io, term)
end
```
Edit the function to read
```julia
function Base.show(io::IO, term::AbstractTerm)
    m = length(term)
    if m == 0
        reuturn nothing
    end
    ...
```
Now return to your Julia session and ask to display the term again, and you
will see it is no longer printed. The package Revise watches the source for changes
and recompiles only the changed code.
```julia
julia> t
0-factor PauliTerm{Vector{Pauli}, Complex{Int64}}:
```
