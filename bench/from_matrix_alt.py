# Benchmark qiskit_alt transforming an operator from the computational- to the Pauli basis.
import timeit

def make_setup_code(nqubits):
    return f"""
from qiskit_alt import QuantumOps, PauliSum_to_SparsePauliOp
import numpy as np

m = np.random.rand(2**{nqubits}, 2**{nqubits})
"""

def run_one(nqubits, num_repetitions):
    setup_code = make_setup_code(nqubits)
    bench_code = "PauliSum_to_SparsePauliOp(QuantumOps.PauliSum(m))"
    time = timeit.timeit(stmt=bench_code, setup=setup_code, number=num_repetitions)
    t = 1000 * time / num_repetitions
    print(f"nqubits={nqubits}, {t:0.2f}", "ms")
    return t

qk_alt_times = []

for nqubits, num_repetitions in ((2, 50), (3, 50), (4, 10), (5, 10), (6, 10),
                                 (7, 10), (8, 10)):
    t = run_one(nqubits, num_repetitions)
    qk_alt_times.append(t)
