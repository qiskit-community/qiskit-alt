### Resources

* [Incorporating Julia Into Python Programs](https://www.peterbaumgartner.com/blog/incorporating-julia-into-python-programs/)

### Development environment

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
Indeed making changes to the `QuantumOps` source   
