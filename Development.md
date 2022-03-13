# Notes for Developers

Most of what is written here is generic to Julia. A bit is generic to Julia within Python.

* [Resources](#resources)

* [Development environment](#development-environment)

    * [Details](#details)

* [Revise](#revise) Automatically compiling code into a live session.

* [Example Development Session](#example-development-session)

* [Making a subdirectory for examples](#making-a-subdirectory-for-examples)

* [Troubleshooting](./README.md#troubleshooting)

### Resources

* [Incorporating Julia Into Python Programs](https://www.peterbaumgartner.com/blog/incorporating-julia-into-python-programs/) discusses using pyjulia and Docker.

* [Performance Tips](https://docs.julialang.org/en/v1/manual/performance-tips/). Essential reading for
scientific projects in Julia. It is largely about avoiding big performance blunders. For example an array of these
```julia
struct TypeA
   x::Integer
end
```
will always have pointers to `TypeA` because each element could hold, for example, an `Int64` or an `Int32`, even if
all are in fact `Int64`. The compiler can't tell from the type information.
So `a = [TypeA(1), TypeA(42)]` will be an array of generic `TypeA` even though each element (thus far) is a 64 bit integer.
Pushing `TypeA(Int32(1))` to `a` is allowed.
On the other hand, if I define
```julia
struct TypeB{T<:Integer}
   x::T
end
```
then `a = [TypeB(1), TypeB(42)]` will be an array of `TypeB{Int64}` and the storage will be implemented as a packed array
of 64 bit integers. Trying to push a `TypeB(Int32(1))` to `a` will throw an error.
So the performance tips are largely not complicated optimizations, but rather idiomatic coding habits to avoid
performance penalties.

### Development environment

Before describing a workflow, we explain how to use the package manager.
Here are three ways (there are more):

* From the Julia REPL:
```julia
julia> import Pkg
julia> Pkg.activate(".")
julia> Pkg.status()
julia> Pkg.add("APackage")
julia> Pkg.rm("APackage")
julia> Pkg.develop(path="/path/to/package/source/tree/")

```
* From the package manager REPL. Enter the jula repl and hit `]`.
```julia
(@v1.7) pkg> activate "."
(@v1.7) pkg> status
(@v1.7) pkg> add APackage
(@v1.7) pkg> develop /path/to/package/source/tree/
```

* From Python. Do `from qiskit_alt import Pkg`. Then the syntax is the same as from the Julia REPL.

The following enables a workflow, which is explained in more detail further below.

* clone `qiskit_alt`
* clone the packages in the [QuantumRegistry](https://github.com/Qiskit-Extensions/QuantumRegistry).
`QuantumOps`, `ElectronicStructure`, `ElectronicStructurePySCF`, and `QiskitQuantumInfo`.
You can do this in one of two ways.
    * Clone them via `Pkg.develop("QuantumOps")`. This looks up the url in your registries and clones to `~/.julia/dev/`.
      It also writes the path to the downloaded tree to the `Manifest.toml` of your current project, so that your project
      loads the package from the development tree.
    * Clone them manually into a directory of your choice. For each one, you have to
      do `Pkg.develop(path="/path/to/source/Package")` after activating the `qiskit_alt` project.
      I prefer this second method because `~/.julia/dev/` becomes cluttered. But the first method is simpler.

* If you chose the second option above, start the Julia REPL,
and enter the package manager mode with `]`.
Then do `dev ~/path/to/QuantumOps`.
Repeat this for each package you want to develop.

* Start ipython. Before doing `import qiskit_alt`, enable the magics listed in the section [Revise](#revise).

Now you can edit the source in the cloned Julia packages and the changes will be reflected in your ipython REPL without restarting.
To revert to the production environment, enter `free QuantumOps`, etc. at the Julia package manager prompt.

When a package is "developed", `qiskit_alt` will use the editable version in `~/path/to/QuantumOps`.
When the package is "freed", `qiskit_alt` will use the immutable versions stored in your local package depot:
```shell
> ls ~/.julia/packages/QuantumOps/
I1StV oJT7c TdAEP VCfDa  wv1sy
```
Each subdirectory contains an immutable snapshot or version of the package identified with a uuid.
Your `Manifest.toml` includes these uuids, for all packages, including in the standard library.
So it can be used to reproduce an environment with exactly these immutable versions of packages.

#### Details

* A [Registry](https://pkgdocs.julialang.org/v1/registries/) is a directory structure that associates package UUIDS
with package metadata, such as a package name, available versions, and download url. These registries are stored
in `~/.julia/registries/`. When Julia resolves package requirements for a project, it refers to these registries.
The[General Registry](https://github.com/JuliaRegistries/General) contains thousands of packages.
We add to this our own [QuantumRegistry](https://github.com/Qiskit-Extensions/QuantumRegistry).
A package is identified by its UUID. You can use this to distinguish packages with the same name.
If you type `julia> Pkg.add("MyPackage")`. Julia looks for a package by that name in your registries.

* A Julia [project](https://pkgdocs.julialang.org/v1/environments/)
may be specified by a `Project.toml` file. It contains data on required packages and version
ranges, as well as other information. It does *not* record from where a package was downloaded.
When we refer to the `qiskit_alt` project, we mean the Julia project specified by the top level `Project.toml` file.
There is a another project specified by `./sys_image/Project.toml`. This is the project,
a different set of packages, instantiated when compiling a system image for `qiskit_alt`.
If you activate a project say, via `Pkg.activate(".")`, then `Pkg.add` and `Pkg.rm` modify `Project.toml`.

* The `Manifest.toml` file associated with a `Project.toml` records how your system has instantiated
the project. It records a package dependency graph with metadata including download url.
For each package, a SHA hash of the read-only directory containing the source is included in `Manifest.toml`.
This corresponds, roughly to a package version. When you "develop" and "free" a package, it's url is changed
in `Manifest.toml`. We don't keep `Manifest.toml` under VCS. It is always safe to delete it. It will
be rebuilt from the `Project.toml` and the registries.

The Julia packages backing qiskit_alt are registered in this registry
[https://github.com/Qiskit-Extensions/QuantumRegistry](https://github.com/Qiskit-Extensions/QuantumRegistry).
The registered packages themselves are also on `github.com`.
While developing, we want our `Manifest.toml` to point to local editable source trees rather than
copies of immutable sources trees that have been downloaded. When developing Python, you typically
restart frequently because you are working with precompiled components.
Julia currently recompiles quite a bit on restart (Julia caches some parts of the compilation
in `.ji` files. And there are plans to
[cache native code](https://github.com/JuliaLang/julia/issues/30488).
But for now, it is recompiled.)
One way around this is to recompile code snippets into a running session with
[`Revise.jl`](https://github.com/timholy/Revise.jl).

* [`Revise.jl`](https://github.com/timholy/Revise.jl). `Revise` monitors source files. When you edit and
save a file, a diff is made and the changed code is evaluated in the appropriate scope.
The change is available immediately at the REPL without restarting the runtime.

We need to change the location of the Julia packages, for example `QuantumOps.jl` from the ibm server to a local source tree.

* To tell the active project to load a package from a development source tree, use `dev(elop)`.
Use `free` to return to an immuatable copy downloaded from a registry url.
Assuming you have a local clone of `QuantumOps.jl`, you can do the following.
```julia
julia>  # hit ']' to enter package management mode
(v1.7) pkg> activate .
  Activating project at `~/myrepos/quantum_repos/qiskit_alt`

(qiskit_alt) pkg> dev /home/username/quantum_repos/QuantumOps
   Resolving package versions...
    Updating `~/myrepos/quantum_repos/qiskit_alt/Project.toml`
  [d0cc4389] ~ QuantumOps v0.1.1 ⇒ v0.1.1 `~/quantum_repos/QuantumOps`
    Updating `~/myrepos/quantum_repos/qiskit_alt/Manifest.toml`
  [d0cc4389] ~ QuantumOps v0.1.1 ⇒ v0.1.1 `~/quantum_repos/QuantumOps`

(qiskit_alt) pkg> free QuantumOps
   Resolving package versions...
    Updating `~/myrepos/quantum_repos/qiskit_alt/Project.toml`
  [d0cc4389] ~ QuantumOps v0.1.1 `~/quantum_repos/QuantumOps` ⇒ v0.1.1
    Updating `~/myrepos/quantum_repos/qiskit_alt/Manifest.toml`
  [d0cc4389] ~ QuantumOps v0.1.1 `~/quantum_repos/QuantumOps` ⇒ v0.1.1
```

### Revise

From the link above, [Incorporating Julia Into Python Programs](https://www.peterbaumgartner.com/blog/incorporating-julia-into-python-programs/),
I find the following
```python
In [1]: %config JuliaMagics.revise = True

In [2]: %load_ext julia.magic
Initializing Julia interpreter. This may take some time...

In [3]: from qiskit_alt import QuantumOps, Main
  Activating project at `~/myrepos/quantum_repos/qiskit_alt`
```

Indeed changes to the `QuantumOps` source are reflected immediately at the ipython REPL.
For example, a variable `foo = 1` added to `src/QuantumOps.jl` is visible
in ipython as `QuantumOps.foo`.

I'd like to find a way to enable `Revise` without using magics. I have not yet discovered this.

### Example Development Session

* Install the [`LocalRegsitry`](https://github.com/GunnarFarneback/LocalRegistry.jl) package to manage our registry.

```julia
# julia repl prompt
julia> 

# Hit `;` to enter shell mode and check our current directory. It is qiskit_alt
shell> pwd
/home/lapeyre/myrepos/quantum_repos/qiskit_alt

# Hit backspace to return to julia repl mode.
# Hit `]` to enter package management mode
# And add the package `LocalRegistry` to your main environment so it is always avaiable.
(@v1.7) pkg> add LocalRegistry

* Change the qiskit_alt project to "develop" `ElectronicStructure` like this:

# Activate the current project described `Project.toml` in the echoed directory.
(@v1.7) pkg> activate .
  Activating project at `~/myrepos/quantum_repos/qiskit_alt`

(qiskit_alt) pkg> status ElectronicStructure
      Status `~/myrepos/quantum_repos/qiskit_alt/Project.toml`
  [f7ec468b] ElectronicStructure v0.1.4

# "develop" ElectronicStructure from the url given in the registry
# This clones the repo and enters the path to the clone in the qiskit_alt project.
(qiskit_alt) pkg> dev ElectronicStructure
     Cloning git-repo `https://github.com/Qiskit-Extensions/ElectronicStructure.jl.git`
   Resolving package versions...
    Updating `~/myrepos/quantum_repos/qiskit_alt/Project.toml`
  [f7ec468b] ~ ElectronicStructure v0.1.4 ⇒ v0.1.4 `~/.julia/dev/ElectronicStructure`
    Updating `~/myrepos/quantum_repos/qiskit_alt/Manifest.toml`
  [f7ec468b] ~ ElectronicStructure v0.1.4 ⇒ v0.1.4 `~/.julia/dev/ElectronicStructure`
```

Now, start `qiskit_alt`. The following method automatically avoids loading
any custom sytem image in `./sys_image`, which is necessary. It also probably avoids
the julia installation found by the `julia_project` package and the julia exectuable found
on your path.
```
In [1]: %config JuliaMagics.revise = True

In [2]: %load_ext julia.magic
Initializing Julia interpreter. This may take some time...

In [3]: import qiskit_alt
  Activating project at `~/myrepos/quantum_repos/qiskit_alt`

In [4]: from qiskit_alt import ElectronicStructure

# In `~/.julia/dev/ElectronicStructure/src/ElectronicStructure.jl` add a line `foo = 1` and save the file.
# `qiskit_alt` sees the change

In [5]: ElectronicStructure.foo
Out[5]: 1

# Change the line to `foo = 2` and save, and see the change reflected

In [6]: ElectronicStructure.foo
Out[6]: 2
```

* Make the changes you want to `~/.julia/dev/ElectronicStructure/`; we will just leave `foo = 2`.
* In the `Project.toml` file in `~/.julia/dev/ElectronicStructure/` we bump the version to `v0.1.5`.
* Commit the changes to `ElectronicStructure`.
* push the commit to `ElectronicStructure` upstream. Make a PR if you are working from a fork.
* you can tag the commit, and/or make a github release, but the Julia package manager does not care.
* Return to the Julia session, or start a new one, and do (after activating if needed)
```julia
julia> using LocalRegistry

julia> register("ElectronicStructure", registry="QuantumRegistry")
```
This should register the new version v0.1.5 in the local copy of `QuantumRegistry`,
commit the changes, and push the registry upstream. If you are working from a fork of
the registry, you may need to open a PR to the main repo.

* free `ElectronicStructure`.
```julia
(qiskit_alt) pkg> free ElectronicStructure
   Resolving package versions...
    Updating git-repo `https://github.com/Qiskit-Extensions/ElectronicStructure.jl.git`
   Installed ElectronicStructure ─ v0.1.5
    Updating `~/myrepos/quantum_repos/qiskit_alt/Project.toml`
  [f7ec468b] ~ ElectronicStructure v0.1.4 `~/.julia/dev/ElectronicStructure` ⇒ v0.1.5
    Updating `~/myrepos/quantum_repos/qiskit_alt/Manifest.toml`
  [f7ec468b] ~ ElectronicStructure v0.1.4 `~/.julia/dev/ElectronicStructure` ⇒ v0.1.5
Precompiling project...
  4 dependencies successfully precompiled in 10 seconds (98 already precompiled)

(qiskit_alt) pkg> status ElectronicStructure
      Status `~/myrepos/quantum_repos/qiskit_alt/Project.toml`
  [f7ec468b] ElectronicStructure v0.1.5
```
This should remove the reference to our local clone from `Manifest.toml`. And download the new version
of `ElectronicStructure` that we just pushed from the location given in `QuantumRegistry`.
If necessary, you may want change `Project.toml` in the qiskit_alt top level to require
the new version of `ElectronicStructure`.

* Delete `./sys_image/sys_qiskit_alt.so` if it exists; it is out of date.
* Start ipython and verify the changes.
```python
In [1]: from qiskit_alt import ElectronicStructure
  Activating project at `~/myrepos/quantum_repos/qiskit_alt`

In [2]: ElectronicStructure.foo
Out[2]: 2
```
* Run `qiskit_alt.compile_qiskit_alt()` if you like to generate a new system image.

Alternatively, you can do all of the steps above from `ipython`. For example (with output edited)
```python
In [1]: import qiskit_alt
  Activating project at `~/myrepos/quantum_repos/qiskit_alt`

In [2]: from qiskit_alt import julia

In [3]: from julia import Pkg

In [4]: Pkg.status()
      Status `~/myrepos/quantum_repos/qiskit_alt/Project.toml`
  [f7ec468b] ElectronicStructure v0.1.5 `~/quantum_repos/ElectronicStructure`
  [14ae0224] ElectronicStructurePySCF v0.1.0
  [438e738f] PyCall v1.92.5
  [8d55b643] QiskitQuantumInfo v0.1.0
  [d0cc4389] QuantumOps v0.1.1
  [295af30f] Revise v3.1.20
  [8603256b] ZChop v0.3.10

In [5]: Pkg.activate()  # activate your main Julia environment
  Activating project at `~/.julia/environments/v1.7`

In [6]: Pkg.status()
      Status `~/.julia/environments/v1.7/Project.toml`
  [6e4b80f9] BenchmarkTools v1.0.0
  [861a8166] Combinatorics v1.0.2
  ...

In [7]: Pkg.add("LocalRegistry")  # add LocalRegsitry to the main environment
    Updating registry at `~/.julia/registries/QuantumRegistry`
    Updating git-repo `https://github.com/Qiskit-Extensions/QuantumRegistry.git`
    Updating registry at `~/.julia/registries/General.toml`
   Resolving package versions...
  No Changes to `~/.julia/environments/v1.7/Project.toml`
  No Changes to `~/.julia/environments/v1.7/Manifest.toml`

In [9]: Pkg.activate(".")  # activate qiskit_alt environment again
  Activating project at `~/myrepos/quantum_repos/qiskit_alt`

# Here we use a previously cloned copy rather than the default location `~/.julia/dev`
In [10]: Pkg.develop(path="/home/lapeyre/quantum_repos/ElectronicStructure")

In [13]: from julia import LocalRegistry

# Register a package version
In [14]: LocalRegistry.register("ElectronicStructure", registry="QuantumRegistry")

# Return to using the version in the registries
In [15]: Pkg.free("ElectronicStructure")
```

### Making a subdirectory for examples

You may want to include a subdirectory for examples or tutorials. Or you may want them in a separate repo.
A new Julia environment should be defined in a `Project.toml` file. That is, you have files
`./examples/ex1.py`, etc. and also `./examples/Project.toml`.
You can create `Project.toml` by cd'ing into `./examples` and doing `Pkg.activate(".")`.
You populate the project by doing `Pkg.add("somepackage")`.
When you run the examples, activate the project somehow, from Julia or Python.
By default, only the packages in your main user-wide project, e.g. `@v1.7` and
those in `./examples/Project.toml` will be available.
If you want to develop the examples together with the main package, say `qiskit_alt` (or others),
then "develop" that package: Activate the examples project, then do `Pkg.develop(path="/path/to/dev/qiskit_alt")`.


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
