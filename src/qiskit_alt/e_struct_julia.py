import os
from .julia_project import project
project.ensure_init()
from .pauli_operators import jlSparsePauliOp

from . import e_struct_python

Main = project.simple_import("Main")
QuantumOps = project.simple_import("QuantumOps")
QiskitQuantumInfo = project.simple_import("QiskitQuantumInfo")
ElectronicStructure = project.simple_import("ElectronicStructure")


def fermionic_hamiltonian(geometry, basis):
    """
    Given a molecular geometry specification and basis set, return
    the electronic Hamiltonian as a QuantumOps.FermiSum.

    The integrals are computed by pyscf. The geometry spec may be in either qiskit-nature
    format or qiskit_alt format.
    """
    mol_data = e_struct_python.MolecularData.from_specs(geometry=geometry, basis=basis)
    iop = ElectronicStructure.interaction_operator(mol_data.nuclear_repulsion,
                                                   mol_data.one_body_integrals,
                                                   mol_data.two_body_integrals)
    return QuantumOps.FermiSum(iop)


def jordan_wigner(fermi_op):
    """
    Compute the Jordan-Wigner transform of a QuantumOps.FermiSum representing a Fermionic Hamiltonian.
    Return a qiskit.SparsePauliOp.
    """
    pauli_op = QuantumOps.jordan_wigner(fermi_op)
    spop_jl = QiskitQuantumInfo.SparsePauliOp(pauli_op) # Convert to QiskitQuantumInfo.SparsePauliOp
    sparse_pauli = jlSparsePauliOp(spop_jl)  # Convert to qisit.quantum_info.SparsePauliOp
    return sparse_pauli
