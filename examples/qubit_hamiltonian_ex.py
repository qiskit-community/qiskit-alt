import qiskit_alt

#geometry = [['H', [0., 0., 0.]], ['H', [0., 0., 0.7414]]]

geometry = [['O', [0., 0., 0.]],
            ['H', [0.757, 0.586, 0.]],
            ['H', [-0.757, 0.586, 0.]]]

#basis = 'sto3g'
#basis = '631g'
basis = 'dzvp2'

pauli_op = qiskit_alt.jordan_wigner(geometry, basis)
