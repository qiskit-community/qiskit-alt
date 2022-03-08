import os
from ._julia_project import project
project.ensure_init()

Main = project.simple_import("Main")
QuantumOps = project.simple_import("QuantumOps")
QiskitQuantumInfo = project.simple_import("QiskitQuantumInfo")
from .pauli_operators import jlSparsePauliOp

# TODO: This could probably be moved to QiskitQuantumInfo.jl
#Main.include(os.path.join(julia_src_dir, 'electronic_structure.jl'))
Main.include(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'electronic_structure.jl'))

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
    return Main.qiskit_geometry_to_Geometry(qiskit_geometry)


def fermionic_hamiltonian(geometry, basis):
    """
    Given a qiskit-nature molecular geometry specification and basis set, return
    the electronic Hamiltonian as a QuantumOps.FermiSum.

    The integrals are computed by pyscf.
    """
    jlgeometry = Geometry(geometry) # Convert Python geometry spec to ElectronicStructure.Geometry
    fermi_op = Main.fermionic_hamiltonian(jlgeometry, basis)
    return fermi_op


def jordan_wigner(fermi_op):
    """
    Compute the Jordan-Wigner transform of a QuantumOps.FermiSum representing a Fermionic Hamiltonian.
    Return a qiskit.SparsePauliOp.
    """
    pauli_op = QuantumOps.jordan_wigner(fermi_op)
    spop_jl = QiskitQuantumInfo.SparsePauliOp(pauli_op) # Convert to QiskitQuantumInfo.SparsePauliOp
    spop = jlSparsePauliOp(spop_jl)  # Convert to qisit.quantum_info.SparsePauliOp
    return spop
