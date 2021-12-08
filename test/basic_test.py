import pytest
import qiskit_alt
from qiskit_alt import Main
#from qiskit_alt import julia

def test_always_passes():
    assert True


def test_import_QuantumOps():
    from qiskit_alt import QuantumOps
    assert True


def test_import_ElectronicStructure():
    from qiskit_alt import ElectronicStructure
    assert True


def test_import_QiskitQuantumInfo():
    from qiskit_alt import QiskitQuantumInfo
    assert True


@pytest.fixture
def conv_geometry():
    geometry = [['H', [0., 0., 0.]], ['H', [0., 0., 0.7414]]]
    # geometry = [['O', [0., 0., 0.]],
    #             ['H', [0.757, 0.586, 0.]],
    #             ['H', [-0.757, 0.586, 0.]]]
    return qiskit_alt.Geometry(geometry)


def test_Geometry_length(conv_geometry):
    assert Main.length(conv_geometry) == 2


def test_Geometry_atom(conv_geometry):
    atom = qiskit_alt.Main.getindex(conv_geometry, 1)
    assert atom.coords == (0.0, 0.0, 0.0)


def test_fermionic_hamiltonian(conv_geometry):
    fermi_op = Main.fermionic_hamiltonian(conv_geometry, "sto3g")
    assert Main.length(fermi_op) == 25
