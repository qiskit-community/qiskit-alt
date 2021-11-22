import qiskit_alt

def do_jw_problem():
#    qiskit_alt.Main.eval('include("examples/jw_example.jl")')
    qiskit_alt.Main.eval('include("jw_example.jl")')
    pauli_op = qiskit_alt.Main.eval("pauli_op")
    spop_jl = qiskit_alt.QiskitQuantumInfo.SparsePauliOp(pauli_op)
    spop = qiskit_alt.jlSparsePauliOp(spop_jl)
    return spop
