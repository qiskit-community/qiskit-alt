# Benchmark creating a SparsePauliOp from a list of strings using quantum_info

import random
from timeit import timeit

from qiskit.quantum_info import PauliList, SparsePauliOp

random.seed(123)

def rand_label(k, n):
    return ["".join(random.choices("IXYZ", k=k)) for _ in range(n)]

quantum_info_times = []

for k in (10, 100):
    for n in (10, 100, 1000, 5000, 10_000, 100_000):
        label = rand_label(k, n)
        number = 20
        if n >= 10_000:
            number = 1
        t = timeit(lambda: SparsePauliOp(PauliList(label)).simplify(), number=number)
        t = t * 1000 / number
        quantum_info_times.append(t)
        print(f'k={k}, n={n}, {t} ms')

quantum_info_times
