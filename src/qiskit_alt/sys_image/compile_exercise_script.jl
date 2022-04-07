import QuantumOps
import ElectronicStructure
import QiskitQuantumInfo
import QuantumCircuits

try
    include(joinpath(pkgdir(QuantumCircuits), "test", "runtests.jl"))
catch e
    nothing
end
include(joinpath(pkgdir(QuantumOps), "test", "runtests.jl"))
include(joinpath(pkgdir(ElectronicStructure), "test", "runtests.jl"))
include(joinpath(pkgdir(QiskitQuantumInfo), "test", "runtests.jl"))
