using PackageCompiler

packages = [:PyCall, :QuantumOps, :ElectronicStructure, :QiskitQuantumInfo]

create_sysimage(packages; sysimage_path="sys_qiskit_alt.so",
                precompile_execution_file="compile_exercise_script.jl")
