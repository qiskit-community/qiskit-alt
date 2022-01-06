using PackageCompiler
using Libdl: Libdl

packages = [:PyCall, :QuantumOps, :ElectronicStructure, :QiskitQuantumInfo]

sysimage_path = joinpath(@__DIR__, "sys_julia_project." * Libdl.dlext)

create_sysimage(packages;
                sysimage_path=sysimage_path,
                precompile_execution_file=joinpath(@__DIR__, "compile_exercise_script.jl"),
                incremental=true,
                project=joinpath(@__DIR__, ".")
                )
