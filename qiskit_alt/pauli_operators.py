import os
from .activate_julia import julia

from julia import QuantumOps
from julia import QiskitQuantumInfo
from julia import Main

from qiskit.quantum_info import Pauli, SparsePauliOp, PauliList

def jlPauli(data):
    if isinstance(data, str):
        data = QiskitQuantumInfo.Pauli(data)
    return Pauli((data.x, data.z, data.phase))

def jlPauliList(pl):
    return PauliList.from_symplectic(pl.z, pl.x)

def jlSparsePauliOp(sp):
    pl = PauliList.from_symplectic(sp.pauli_list.z, sp.pauli_list.x)
    return SparsePauliOp(pl, sp.coeffs)

def PauliSum_to_SparsePauliOp(ps):
    spop_jl = QiskitQuantumInfo.SparsePauliOp(ps) # Convert to QiskitQuantumInfo.SparsePauliOp
    spop = jlSparsePauliOp(spop_jl)  # Convert to qisit.quantum_info.SparsePauliOp
    return spop

