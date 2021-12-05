import os
from .activate_julia import julia, julia_src_dir
from julia import Main, QuantumOps, QiskitQuantumInfo
from .pauli_operators import jlSparsePauliOp

# TODO: This could probably be moved to QiskitQuantumInfo.jl
Main.eval('include("' + os.path.join(julia_src_dir, 'electronic_structure.jl') + '")')

def Geometry(qiskit_geometry):
    """
    Convert a geometry specification that originated in Python in the qiskit-nature format to
    an ElectronicStructure.Geometry object. pyjulia will have translated the python input to
    a Matrix.

    .. code:
    In [1]: geometry = [['O', [0., 0., 0.]],
    ...:             ['H', [0.757, 0.586, 0.]],
    ...:             ['H', [-0.757, 0.586, 0.]]]

    In [2]: Geometry(geometry)
    Out[2]: <PyCall.jlwrap Geometry{Float64}(Atom{Float64}[Atom{Float64}(:O, (0.0, 0.0, 0.0)), Atom{Float64}(:H, (0.757, 0.586, 0.0)), Atom{Float64}(:H, (-0.757, 0.586, 0.0))])>
    ```
    """
    return Main.qiskt_geometry_to_Geometry(qiskit_geometry)


# TODO: move these to another file
def fermionic_hamiltonian(geometry, basis):
    jlgeometry = Geometry(geometry) # Convert Python geometry spec to ElectronicStructure.Geometry
    fermi_op = Main.fermionic_hamiltonian(jlgeometry, basis)
    return fermi_op

def jordan_wigner(fermi_op):
    pauli_op = QuantumOps.jordan_wigner(fermi_op)
    spop_jl = QiskitQuantumInfo.SparsePauliOp(pauli_op) # Convert to QiskitQuantumInfo.SparsePauliOp
    spop = jlSparsePauliOp(spop_jl)  # Convert to qisit.quantum_info.SparsePauliOp
    return spop

# TODO: bitrot. this is broken. Easy to fix
# This is only a bit faster than above. The two final conversions are typically relatively very fast.
def qubit_hamiltonian_no_convert(geometry, basis):
    jlgeometry = Geometry(geometry) # Convert Python geometry spec to ElectronicStructure.Geometry
    pauli_op = Main.qubit_hamiltonian(jlgeometry, basis) # Compute Pauli operator as QuantumOps.PauliSum
    return pauli_op
