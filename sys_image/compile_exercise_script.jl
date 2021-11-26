import QuantumOps
import ElectronicStructure
import QiskitQuantumInfo

include(joinpath(pkgdir(QuantumOps), "test", "runtests.jl"))
include(joinpath(pkgdir(ElectronicStructure), "test", "runtests.jl"))
include(joinpath(pkgdir(QiskitQuantumInfo), "test", "runtests.jl"))
