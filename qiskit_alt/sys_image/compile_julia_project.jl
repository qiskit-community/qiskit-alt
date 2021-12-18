using PackageCompiler
using Libdl: Libdl

packages = [:PyCall, :QuantumOps, :ElectronicStructure, :QiskitQuantumInfo]

sysimage_path = "sys_julia_project." * Libdl.dlext

create_sysimage(packages; sysimage_path=sysimage_path,
                precompile_execution_file="compile_exercise_script.jl")
