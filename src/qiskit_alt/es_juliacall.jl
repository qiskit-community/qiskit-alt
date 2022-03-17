#import PythonCall
using PythonCall: @pyconvert, PyList

using ElectronicStructure: Atom, Geometry, MolecularSpec,
    InteractionOperator, MolecularData

function qiskit_geometry_to_Geometry(geometry::PyList)
    if length(first(geometry)) != 2
        throw(ArgumentError("Expecting two elements to specify geometry of a single Atom. Got ",
                            length(first(geometry))))
    end
    cgeometry = []
    for atom in geometry
        (element_symbol, coords) = (atom...,)
        push!(cgeometry, (Symbol(element_symbol) , @pyconvert(Tuple, coords)))
    end
    return Geometry((Atom(x...) for x in cgeometry)...)
end
