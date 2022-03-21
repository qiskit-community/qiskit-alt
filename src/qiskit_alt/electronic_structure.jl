# ENV["PYCALL_JL_RUNTIME_PYTHON"] = Sys.which("python") or ''

#using PyCall
using ElectronicStructure: Atom, Geometry, MolecularSpec,
    InteractionOperator, MolecularData

# using ElectronicStructurePySCF: PySCF

using QuantumOps: FermiSum

"""
    qiskit_geometry_to_Geometry(geometry::Matrix)

Convert a geometry specification that originated in Python in the qiskit-nature format to
an `ElectronicStructure.Geometry` object. pyjulia will have translated the python input to
a `Matrix`.

# Example from python:
```python
In [1]: geometry = [['O', [0., 0., 0.]],
   ...:             ['H', [0.757, 0.586, 0.]],
   ...:             ['H', [-0.757, 0.586, 0.]]]

In [2]: Main.qiskit_geometry_to_Geometry(geometry)
Out[2]: <PyCall.jlwrap Geometry{Float64}(Atom{Float64}[Atom{Float64}(:O, (0.0, 0.0, 0.0)), Atom{Float64}(:H, (0.757, 0.586, 0.0)), Atom{Float64}(:H, (-0.757, 0.586, 0.0))])>
```
"""
function qiskit_geometry_to_Geometry(geometry::Matrix)
    (num_atoms, num_components_per_atom) = size(geometry)
    if num_components_per_atom != 2
        throw(ArgumentError("Expecting two elements to specify geometry of a single Atom. Got ", num_components_per_atom))
    end
    atoms = []
    for atom_in in eachrow(geometry)
        element_symbol = atom_in[1]
        coords = atom_in[2]
        atom = Atom(Symbol(element_symbol), (coords...,))
        push!(atoms, atom)
    end
    return Geometry(atoms...)
end

function fermionic_hamiltonian(geometry::Geometry, basis)
    # Construct the specification of the electronic structure problem.
    mol_spec = MolecularSpec(geometry=geometry, basis=basis)

    # Do calculations using `PySCF` and populate a `MolecularData` object with results.
    # `mol_pyscf` holds a constant, a rank-two tensor, and a rank-four tensor.
    mol_pyscf = MolecularData(PySCF, mol_spec);
    iop = InteractionOperator(mol_pyscf);
    return FermiSum(iop)
end


# Not useful. Just call jordan_wigner(fermi_op) directly
# function qubit_hamiltonian(fermi_op)
#     pauli_op = jordan_wigner(fermi_op)
#     return pauli_op
# end

# function qubit_hamiltonian(geometry::Geometry, basis)
#     fermi_op = fermionic_hamiltonian(geometry::Geometry, basis)
#     pauli_op = jordan_wigner(fermi_op)
#     return pauli_op
# end
