ENV["PYCALL_JL_RUNTIME_PYTHON"] = Sys.which("python")

using ElectronicStructure

## using PyCall will trigger loading pyscf-specific code

using PyCall

using ElectronicStructure: one_electron_integrals,
   MolecularData, PySCF

##  Define geometries: specification of atoms and their positions
##  for various molecules.

geoms = (
    Geometry(Atom(:H, (0., 0., 0.)), Atom(:H, (0., 0., 0.7414))),

    Geometry(Atom(:Li, (0., 0., 0.)), Atom(:H, (0., 0., 1.4))),

    Geometry(Atom(:O, (0., 0., 0.)), Atom(:H, (0.757, 0.586, 0.)),
             Atom(:H, (-0.757, 0.586, 0.)))
)

## Choose one of the geometries
geom = geoms[1]

## Construct specification of electronic structure problem
mol_spec = MolecularSpec(geometry=geom)

## Do calculations and populate MolecularData with results
mol_pyscf = MolecularData(PySCF, mol_spec)

## Create interaction operator from one and two body integrals and constant.
## This does just a bit of manipulation of mol_data; converting space orbitals
## into space-and-spin orbitals.
## This is the same as the operator by the same name in OpenFermion.
iop = InteractionOperator(mol_pyscf; spin_order=:block, index_order=:default)

nothing
