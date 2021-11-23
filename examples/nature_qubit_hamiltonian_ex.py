from qiskit_nature.drivers import UnitsType, Molecule
from qiskit_nature.drivers.second_quantization import ElectronicStructureDriverType, ElectronicStructureMoleculeDriver

geometry = [['H', [0., 0., 0.]],
            ['H', [0., 0., 0.735]]]

# geometry = [['O', [0., 0., 0.]],
#             ['H', [0.757, 0.586, 0.]],
#             ['H', [-0.757, 0.586, 0.]]]


basis = 'sto3g'
#basis = '631g'
#basis = 'dzvp2'

molecule = Molecule(geometry=geometry,
                     charge=0, multiplicity=1)
driver = ElectronicStructureMoleculeDriver(molecule, basis=basis, driver_type=ElectronicStructureDriverType.PYSCF)

from qiskit_nature.problems.second_quantization import ElectronicStructureProblem
from qiskit_nature.converters.second_quantization import QubitConverter
from qiskit_nature.mappers.second_quantization import JordanWignerMapper

es_problem = ElectronicStructureProblem(driver)
second_q_op = es_problem.second_q_ops()

fermionic_hamiltonian = second_q_op[0]

qubit_converter = QubitConverter(mapper=JordanWignerMapper())
nature_qubit_op = qubit_converter.convert(fermionic_hamiltonian)
