from collections import namedtuple
import functools
import pyscf
import numpy

"""
Pure-Python electronic structure code. This mostly provides an interface to PySCF.
"""


Atom = namedtuple("Atom", "species coords")


def atom(species, coords):
    if len(coords) != 3:
        raise ValueError(f"coords must be a three-tuple of floats. Got {coords}")
    return Atom(species, coords)


def atom_to_pyscf(atom):
    if not isinstance(atom, Atom):
        raise TypeError(f"Expect type `Atom`, got {type(atom)}'")
    return atom.species + " " + " ".join((str(coord) for coord in atom.coords))


Geometry = namedtuple("Geometry", "atoms")


def geometry(*atoms):
    if _is_nature_geometry(atoms[0]):
        return geometry_from_nature(atoms[0])
    if not all(isinstance(atom, Atom) for atom in atoms):
        raise ValueError(f"geometry: all arguments must be of type Atom")
    return Geometry(atoms)


def _is_nature_geometry(geom):
    return (isinstance(geom, list) and
            all((isinstance(g, list) and len(g) == 2 and
                 isinstance(g[0], str) and isinstance(g[1], list) and
                 len(g[1]) == 3) for g in geom)
            )


def geometry_from_nature(geom_list):
    if not _is_nature_geometry(geom_list):
        raise ValueError(f"{geom_list} is not a valid geometry specification")
    return Geometry([Atom(a[0], a[1]) for a in geom_list])


def geometry_to_pyscf(geometry):
    return ";".join((atom_to_pyscf(atom) for atom in geometry.atoms))


class MolecularSpec:
    def __init__(self, _geometry, multiplicity=None, charge=None, basis=None):
        self.geometry = geometry(_geometry)
        self.multiplicity = 1 if multiplicity is None else multiplicity
        self.charge = 0 if charge is None else charge
        self.basis = 'sto-3g' if basis is None else basis # probably should be required


    @property
    def spin(self):
        return self.multiplicity - 1


    def to_pyscf(self):
        pymol = pyscf.gto.Mole(atom=geometry_to_pyscf(self.geometry), basis=self.basis)
        pymol.spin = self.spin
        pymol.charge = self.charge
        pymol.symmetry = False
        pymol.build()
        return pymol


def one_electron_integrals(scf):
    mo_coeff = scf.mo_coeff
    h_core = scf.get_hcore()
    return functools.reduce(numpy.dot, (mo_coeff.T, h_core, mo_coeff))


def two_electron_integrals(pymol, scf):
    two_electron_compressed = pyscf.ao2mo.kernel(pymol, scf.mo_coeff)
    n_orbitals =  scf.mo_coeff.shape[1]
    symmetry_code = 1  # No permutation symmetry
    return pyscf.ao2mo.restore(symmetry_code, two_electron_compressed, n_orbitals)


class MolecularData:
    def __init__(self,
                 spec,
                 nuclear_repulsion,
                 one_body_integrals,
                 two_body_integrals
                 ):
        self.spec = spec
        self.nuclear_repulsion = nuclear_repulsion
        self.one_body_integrals = one_body_integrals
        self.two_body_integrals = two_body_integrals


    @classmethod
    def using_pyscf(cls, mol_spec : MolecularSpec):
        pymol = mol_spec.to_pyscf()
        if pymol.spin != 0:  # from OpenFermion
            scf = pyscf.scf.ROHF(pymol)
        else:
            scf = pyscf.scf.RHF(pymol)

        # Run Hartree-Fock
        verbose = scf.verbose
        scf.verbose = 0
        scf.run()
        scf.verbose = verbose
        one_e_ints = one_electron_integrals(scf)  # Compute one and two body integrals
        two_e_ints = two_electron_integrals(pymol, scf)
        nuclear_repulsion = float(pymol.energy_nuc()) # Compute constant energy, convert from numpy.float64 to float
        return MolecularData(mol_spec, nuclear_repulsion, one_e_ints, two_e_ints)


    @classmethod
    def from_specs(cls, geometry, multiplicity=None, charge=None, basis=None):
        mol_spec = MolecularSpec(geometry, multiplicity=multiplicity, charge=charge, basis=basis)
        return cls.using_pyscf(mol_spec)
