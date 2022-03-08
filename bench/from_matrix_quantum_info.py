# Benchmark qiskit.quantum_info transforming an operator from the computational- to the Pauli basis.
import timeit

def make_setup_code(nqubits):
    return f"""
from qiskit.quantum_info import SparsePauliOp
from qiskit.quantum_info import Operator
import numpy as np

m = np.random.rand(2**{nqubits}, 2**{nqubits})
"""

def run_one(nqubits, num_repetitions):
    setup_code = make_setup_code(nqubits)
    bench_code = "SparsePauliOp.from_operator(Operator(m))"
    time = timeit.timeit(stmt=bench_code, setup=setup_code, number=num_repetitions)
    t = 1000 * time / num_repetitions
    print(f"nqubits={nqubits}, {t:0.2f}", "ms")
    return t

pyqk_times = []

for nqubits, num_repetitions in ((2, 50), (3, 50), (4, 10), (5, 10), (6, 5),
                                 (7, 1), (8, 1)):
    t = run_one(nqubits, num_repetitions)
    pyqk_times.append(t)
