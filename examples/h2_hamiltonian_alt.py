import qiskit_alt
geometry = [['H', [0., 0., 0.]], ['H', [0., 0., 0.7414]]]
#basis = 'sto3g'
basis = '631++g'

fermi_op = qiskit_alt.fermionic_hamiltonian(geometry, basis)
pauli_op = qiskit_alt.qubit_hamiltonian(fermi_op)

#basis = '631g'
#basis = 'dzvp'

# Too big
#basis = 'dzp'
#basis = 'dzvp2'

#code = "qiskit_alt.qubit_hamiltonian_no_convert(geometry, basis)"
#pauli_op = qiskit_alt.qubit_hamiltonian_no_convert(geometry, basis)


