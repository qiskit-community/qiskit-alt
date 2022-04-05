# Benchmark qiskit_alt transforming an operator from the computational- to the Pauli basis.
import qiskit_alt
qiskit_alt.project.ensure_init()

import timeit

Main = qiskit_alt.project.julia.Main

def make_setup_code(nqubits):
    return f"""
import qiskit_alt
from qiskit_alt.pauli_operators import PauliSum_to_SparsePauliOp
QuantumOps = qiskit_alt.project.simple_import("QuantumOps")
import numpy as np
Main = qiskit_alt.project.julia.Main

m = np.random.rand(2**{nqubits}, 2**{nqubits})
"""

def run_one(nqubits, num_repetitions):
    setup_code = make_setup_code(nqubits)
    if qiskit_alt.project._calljulia_name == 'juliacall':
        bench_code = "PauliSum_to_SparsePauliOp(QuantumOps.PauliSum(Main.convert(Main.Matrix, m)))"
    else:
        bench_code = "PauliSum_to_SparsePauliOp(QuantumOps.PauliSum(m))"
    time = timeit.timeit(stmt=bench_code, setup=setup_code, number=num_repetitions)
    t = 1000 * time / num_repetitions
    print(f"nqubits={nqubits}, {t:0.2f}", "ms")
    return t


def run_benchmarks():
    qk_alt_times = []

    for nqubits, num_repetitions in ((2, 50), (3, 50), (4, 10), (5, 10), (6, 10),
                                     (7, 10),
                                     (8, 3)):
        t = run_one(nqubits, num_repetitions)
        qk_alt_times.append(t)
    return qk_alt_times


if __name__ == '__main__':
    qk_alt_times = run_benchmarks()
