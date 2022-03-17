# Benchmark qiskit_alt creating a SparsePauliOp from a list of strings.
import sys
import qiskit_alt
qiskit_alt.project.ensure_init()

import random
from timeit import timeit

Main = qiskit_alt.project.julia.Main

QuantumOps = qiskit_alt.project.simple_import("QuantumOps")
from qiskit_alt.pauli_operators import PauliSum_to_SparsePauliOp

random.seed(123)

def rand_label(k, n):
    return ["".join(random.choices("IXYZ", k=k)) for _ in range(n)]

qkalt_times = []

for k in (10, 100):
    for n in (10, 100, 1000, 5000, 10_000, 100_000):
        label = rand_label(k, n)
        if qiskit_alt.project._calljulia_name == 'juliacall':
            label = Main.pyconvert_list(Main.String, label)
        PauliSum_to_SparsePauliOp(QuantumOps.PauliSum(label))
        number = 20
        t = timeit(lambda: PauliSum_to_SparsePauliOp(QuantumOps.PauliSum(label)), number=number)
        t = t * 1000 / number
        qkalt_times.append(t)
        print(f'k={k}, n={n}, {t} ms')

qkalt_times
