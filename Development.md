### Resources

* [Incorporating Julia Into Python Programs](https://www.peterbaumgartner.com/blog/incorporating-julia-into-python-programs/) discusses using pyjulia and Docker.

### Development environment

The following enables a workflow, which is explained in more detail further below.

* clone `qiskit_alt`
* clone the packages in the [QuantumRegistry](https://github.ibm.com/IBM-Q-Software/QuantumRegistry). `QuantumOps`, `ElectronicStructure`, `QiskitQuantumInfo`.
You can also use the Julia package manager to do this, via `Pkg.develop("QuantumOps")`, it will clone to `~/.julia/dev/` and also make the changes in the next item.
But, I prefer to do the steps separately.
* Start the Julia REPL, enter the package manager mode with `]`. Then do `dev ~/path/to/QuantumOps`. Repeat this for each package you want to develop.
* Start ipython. Before doing `import qiskit_alt`, enable the magics listed in the section [Revise](#revise).

Now you can edit the source in the cloned Julia packages and the changes will be reflected in your ipython REPL without restarting.
To revert to the production environment, enter `free QuantumOps`, etc. at the Julia package manager prompt.

#### Details

The Julia packages backing qiskit_alt are registered in this registry [https://github.ibm.com/IBM-Q-Software/QuantumRegistry](https://github.ibm.com/IBM-Q-Software/QuantumRegistry).
The registered packages are also on `github.ibm.com`. But, we want to develop everything locally. In particular, we want to use

* [`Revise.jl`](https://github.com/timholy/Revise.jl). `Revise` monitors source files. When you edit and
save a file, a diff is made and the changed code is evaluated in the appropriate scope.
   The change is available immediately at the REPL without restarting the runtime.

We need to change the location of the Julia packages, for example `QuantumOps.jl` from the ibm server to a local source tree.
This is done as follows, assuming you have a local clone of `QuantumOps.jl`. Use `dev` to use and develop the local clone.
Use `free` to return to the version in the registries (`QuantumRegistry` in this case.)
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

The changes effected by `dev(elop)` and `free` are recorded only in `Manifest.toml` which is not under git revision
in `qiskit_alt`. Only `Project.toml`, which lists the names and uuids of Julia-package dependencies, is under
revision.

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
