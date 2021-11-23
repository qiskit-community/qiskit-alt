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


from os.path import dirname
toplevel = dirname(dirname(__file__))
julia_dir = toplevel + "/julia"

Main.eval('include("' + julia_dir + '/electronic_structure.jl")')


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

def qubit_hamiltonian(geometry, basis):
    jlgeometry = Geometry(geometry) # Convert Python geometry spec to ElectronicStructure
    pauli_op = Main.qubit_hamiltonian(jlgeometry, basis) # Compute Pauli operator as QuantumOps.PauliSum
    spop_jl = QiskitQuantumInfo.SparsePauliOp(pauli_op) # Convert to QiskitQuantumInfo.SparsePauliOp
    spop = jlSparsePauliOp(spop_jl)  # Convert to qisit.quantum_info.SparsePauliOp
    return spop

