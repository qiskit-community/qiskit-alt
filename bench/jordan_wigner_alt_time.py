# Benchmark qiskit_alt peforming the Jordan-Wigner transform on a Fermi operator.
import qiskit_alt
qiskit_alt.project.ensure_init()

import timeit

def make_setup_code(basis, geometry):
    return f"""
import qiskit_alt.electronic_structure

h2_geometry = [['H', [0., 0., 0.]], ['H', [0., 0., 0.7414]]]

h2o_geometry = [['O', [0., 0., 0.]],
            ['H', [0.757, 0.586, 0.]],
            ['H', [-0.757, 0.586, 0.]]]

basis = {basis}
fermi_op = qiskit_alt.electronic_structure.fermionic_hamiltonian({geometry}, basis)
qiskit_alt.electronic_structure.jordan_wigner(fermi_op);
"""

def run_one_basis(basis, geometry, num_repetitions):
    setup_code = make_setup_code(basis, geometry)
    bench_code = "qiskit_alt.electronic_structure.jordan_wigner(fermi_op)"
    time = timeit.timeit(stmt=bench_code, setup=setup_code, number=num_repetitions)
    t = 1000 * time / num_repetitions
    print(f"geometry={geometry}, basis={basis} {t:0.2f}", "ms")
    return t

alt_times = []

for basis, geometry, num_repetitions in (("'sto3g'", "h2_geometry", 10), ("'631g'", "h2_geometry", 10),
                                         ("'631++g'", "h2_geometry", 10),
                                         ("'sto3g'", "h2o_geometry", 10), ("'631g'", "h2o_geometry", 5)):
    t = run_one_basis(basis, geometry, num_repetitions)
    alt_times.append(t)

alt_times
