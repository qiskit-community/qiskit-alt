import qiskit_alt

# geometry = [['H', [0., 0., 0.]], ['H', [0., 0., 0.7414]]]

geometry = [['O', [0., 0., 0.]],
            ['H', [0.757, 0.586, 0.]],
            ['H', [-0.757, 0.586, 0.]]]

#basis = 'sto3g'
basis = '631g'

pauli_op = qiskit_alt.qubit_hamiltonian(geometry, basis)
