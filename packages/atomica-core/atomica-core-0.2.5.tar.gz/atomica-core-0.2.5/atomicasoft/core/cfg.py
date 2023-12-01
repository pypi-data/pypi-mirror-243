"""Defines `class` ``Cfg``

This module defines `class` ``Cfg`` ---
a class describing a configuration.

Also defines some functions working with configurations, see below.
"""

import numpy as np, copy, re

from . import ptable

class Cfg:
    """Class describing a configuration

    ``cell`` is zero to three vectors of the supercell,
    is always of type ``numpy.ndarray`` of size 0x3, 1x3, 2x3 or 3x3.
    ``cell = None`` makes an empty, 0x3 cell.

    ``pos`` is zero or more coordinates of atoms,
    is always of type ``numpy.ndarray`` of size nx3, where n is the number of atoms
    ``pos = None`` makes an empty, 0x3 position list.

    ``types`` is ``None`` if types are not prescribed or
    a ``numpy.ndarray`` with atomic numbers of size n, where n is the number of atoms.
    """

    _is_safe_to_serialize = True

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, new_pos):
        self._pos = np.array(new_pos)

    @property
    def cell(self):
        return self._cell

    @cell.setter
    def cell(self, new_cell):
        self._cell = np.array(new_cell)

    @property
    def types(self):
        return self._types

    @types.setter
    def types(self, new_types):
        if type(new_types) is np.ndarray:
            self._types = new_types
        elif type(new_types) is str:
            self._types = np.repeat(ptable.NUMBERS[new_types], len(self._pos))
        elif type(new_types) is int:
            self._types = np.repeat(new_types, len(self._pos))
        elif new_types is None:
            self._types = None
        else:
            try:
                new_types = list(new_types)
            except TypeError:
                raise TypeError('unknown format for atomic types')
            assert len(new_types) == len(self._pos) or len(new_types) == 0, 'number of types and positions should be the same'
            if len(new_types) == 0:
                self._types = None
            elif isinstance(new_types[0], str):
                self._types = np.array([ptable.NUMBERS[t] for t in new_types])
            elif isinstance(new_types[0], int) or isinstance(new_types[0], np.integer):
                self._types = np.array([t for t in new_types])
            else:
                raise TypeError('unknown format for atomic types')

    def __init__(self, cell = None, pos = None, types = None):
        if cell is None or len(cell) == 0: cell = np.zeros((0, 3))
        self._cell = np.array(cell)
        assert (len(self.cell.shape) == 2 and self.cell.shape[1] == 3 and self.cell.shape[0] <= 3)

        if pos is None or len(pos) == 0: pos = np.zeros((0, 3))
        self._pos = np.array(pos)
        assert (len(self.pos.shape) == 2 and self.pos.shape[1] == 3)

        self.types = types

        assert (self._types is None or (len(self.types.shape) == 1 and len(self.types) == len(self.pos)))

    @property
    def n_atoms(self):
        return len(self._pos)

    @property
    def species(self):
        return ["'" + ptable.ELEMENTS[t] + "'" for t in self._types]
    @species.setter
    def species(self, new_species):
        self.types = new_species

    def Deform(self, matr) -> None:
        """
        Deform the cell together with the atoms (i.e., multiplies ``cell`` and ``pos`` by ``matr`` on the right)
        """

        self.cell = np.dot(self.cell, matr)
        self._pos = np.dot(self._pos, matr)

    def ReflectInsideCell(self) -> None:
        """
        Use periodic boundary conditions to reflect the atoms so that all are inside the cell
        """

        if len(self.cell) == 3:
            inv_cell = np.linalg.inv(self.cell)
            self._pos = np.array([np.dot(np.mod(np.dot(x, inv_cell), 1.0), self.cell) for x in self.pos])
        else:
            cell = self.cell
            cell_size = len(cell)
            cell = np.pad(cell, ((0, 3 - cell_size), (0, 0)))  # make it square
            u, d, vh = np.linalg.svd(cell, full_matrices=False)
            dinv = [1 / d[i] for i in range(cell_size)] + [0.0 for i in range(cell_size, 3)]
            dorth = [0.0 for i in range(cell_size)] + [1.0 for i in range(cell_size, 3)]
            inv_cell = np.dot(np.transpose(vh), np.dot(np.diag(dinv), np.transpose(u)))
            orth_cell = np.dot(np.transpose(vh), np.dot(np.diag(dorth), np.transpose(u)))
            self._pos = np.array(
                [np.dot(np.mod(np.dot(x, inv_cell), 1.0), cell) + np.dot(x, orth_cell) for x in self.pos])

    def __eq__(self, other) -> np.ndarray:
        return np.array_equal(self.cell, other.cell) and np.array_equal(self.pos, other.pos) \
               and np.array_equal(self.types, other.types)

    def __repr__(self):
        size = len(self._pos)
        if size == 0:
            if len(self.cell) == 0:
                return 'Cfg()'
            return f'Cfg(cell = {self.cell.tolist()})'
        if size < 140:
            details = [f'pos = {self.pos.tolist()}']
            if self.types is not None:
                type_strs = self.species
                details.append(f'types = [{", ".join(type_strs)}]')
            return f'Cfg(cell = {self.cell.tolist()}, {", ".join(details)})'
        else:
            details = [f'{size} atoms']
            return f'<Cfg object, cell = {self.cell.tolist()}, {", ".join(details)}>'


def LammpsDatafile(cfg: Cfg, velocities = None, types = None):
    """
    Write Lammps Datafile based on the configuration.
    LammpsDatafile is currently implemented only for all-periodic conditions.
    """

    assert len(cfg.cell) == 3, 'LammpsDatafile is currently implemented only for all-periodic conditions'
    orig_cfg = cfg
    cfg = copy.copy(orig_cfg)
    is_diagonal = np.count_nonzero(cfg.cell - np.diag(np.diagonal(cfg.cell))) == 0

    # make cell lower-triangular
    if not is_diagonal:
        q, r = np.linalg.qr(np.transpose(cfg.cell), 'complete')
        cfg.Deform(q)
        cfg.cell[0, 1] = cfg.cell[0, 2] = cfg.cell[1, 2] = 0
        for i in [0,1,2]:
            if cfg.cell[i,i]<0:
                for j in [0,1,2]:
                    cfg.cell[i,j] = -cfg.cell[i,j]

    # reflect all the coordinates inside the cell
    cfg.ReflectInsideCell()

    cfg_types = cfg.types
    if cfg_types is None:
        cfg_types = np.array([0 for i in range(len(cfg.pos))])

    if types is None:
        types = np.unique(cfg_types)
    type_map = dict((t, i) for i, t in enumerate(types))

    if velocities is not None:
        velocity_str = '\n'.join(
        [f'{1+i} {v[0]} {v[1]} {v[2]}' for i,v in enumerate(velocities)])
        velocity_str = f'''

Velocities

{velocity_str}'''
    else:
        velocity_str = ''

    atom_str = '\n'.join(
        [f'{1+i} {1 + type_map[cfg_types[i]]} {cfg.pos[i][0]} {cfg.pos[i][1]} {cfg.pos[i][2]}' for i in range(len(cfg.pos))])
    return f"""\
# Atomica-produced lammps datafile

{len(cfg.pos)} atoms
{len(types)} atom types

0.0 {cfg.cell[0][0]} xlo xhi
0.0 {cfg.cell[1][1]} ylo yhi
0.0 {cfg.cell[2][2]} zlo zhi
{cfg.cell[1][0]} {cfg.cell[2][0]} {cfg.cell[2][1]} xy xz yz

Atoms

{atom_str}{velocity_str}
"""

def ReadLammpsDatafile(stream, species = None):
    types = None
    pos = None
    velocities = None

    f = stream
    if isinstance(f, str):
        f = open(stream, 'r')

    l = f.readline()
    # skipping the comment section
    while l.strip(): l = f.readline()

    # number of atoms, etc
    n_atoms = None
    n_atom_types = None
    l = f.readline()
    while l.strip():
        m = re.match('\\s*(\\d+)\\s+atoms', l)
        if(m):
            n_atoms = int(m.group(1))
        m = re.match('\\s*(\\d+)\\s+atom\\s+types', l)
        if(m):
            n_atom_types = int(m.group(1))
        l = f.readline()

    # cell
    cell = np.zeros((3,3))
    l = f.readline()
    while l.strip():
        m = re.match('\\s*([\\d\\.eE+-]+)\\s+([\\d\\.eE+-]+)\\s+xlo\\s+xhi', l)
        if(m):
            cell[0][0] = float(m.group(2)) - float(m.group(1))
        m = re.match('\\s*([\\d\\.eE+-]+)\\s+([\\d\\.eE+-]+)\\s+ylo\\s+yhi', l)
        if(m):
            cell[1][1] = float(m.group(2)) - float(m.group(1))
        m = re.match('\\s*([\\d\\.eE+-]+)\\s+([\\d\\.eE+-]+)\\s+zlo\\s+zhi', l)
        if(m):
            cell[2][2] = float(m.group(2)) - float(m.group(1))
        m = re.match('\\s*([\\d\\.eE+-]+)\\s+([\\d\\.eE+-]+)\\s+([\\d\\.eE+-]+)\\s+xy\\s+xz\\s+yz', l)
        if(m):
            cell[1][0] = float(m.group(1))
            cell[2][0] = float(m.group(2))
            cell[2][1] = float(m.group(3))
        l = f.readline()

    # header: Masses, Atoms, Velocities
    l = f.readline()
    while l.strip():
        if re.match('Masses\\s', l):
            # skip this block
            while l.strip(): l = f.readline()
            # now l is empty
            while not l.strip(): l = f.readline()
            # now l has masses
            while l.strip(): l = f.readline()
            while not l.strip(): l = f.readline()

        if re.match('Atoms\\s', l):
            while l.strip(): l = f.readline()
            l = f.readline()
            types = np.zeros( (n_atoms,), dtype = int)
            pos = np.zeros( (n_atoms,3))
            while l.strip():
                nums = l.strip().split()
                id = int(nums[0]) - 1
                types[id] = int(nums[1]) - 1
                pos[id] = (float(nums[2]), float(nums[3]), float(nums[4]))
                l = f.readline()

        if re.match('Velocities\\s', l):
            while l.strip(): l = f.readline()
            l = f.readline()
            velocities = np.zeros( (n_atoms,3))
            while l.strip():
                nums = l.strip().split()
                id = int(nums[0]) - 1
                velocities[id] = (float(nums[1]), float(nums[2]), float(nums[3 ]))
                l = f.readline()

        l = f.readline()

    # mapping atomic types
    if species is not None:
        if type(species) is not list and not isinstance(species, np.ndarray):
            species = [species]
        if isinstance(species[0], str):
            species = [ptable.NUMBERS[s] for s in species]
        types = [species[t] for t in types]        

    return Cfg(cell = cell, pos = pos, types = types), velocities

def VaspPoscar(cfg: Cfg, unique_types: list):
    """
    Write Vasp Poscar based on the configuration.
    The elements will go in the order prescribed by unique_types
    """

    assert len(cfg.cell) == 3, 'VaspPoscar is currently implemented only for all-periodic conditions'

    # converting to all-numbers
    unique_types = [t if isinstance(t, int) else ptable.NUMBERS[t] for t in unique_types]
    unique_count = [0 for t in unique_types]
    if len(unique_types) != len(np.unique(unique_types)):
        raise ValueError(f'Repeated elements in {unique_types}')
    cfg_types = cfg.types
    out_pos = []
    for i,t in enumerate(unique_types):
        for j in range(len(cfg_types)):
            if cfg_types[j] == t:
                out_pos.append(list(cfg.pos[j]))
                unique_count[i] += 1
    if len(out_pos) != len(cfg_types):
        raise ValueError(f'configuration has other types than {unique_types}')
    
    out_pos = '\n'.join([f'{p[0]} {p[1]} {p[2]}' for p in out_pos])

    return f"""\
Atomica-produced POSCAR
1.0
{cfg.cell[0][0]} {cfg.cell[0][1]} {cfg.cell[0][2]}
{cfg.cell[1][0]} {cfg.cell[1][1]} {cfg.cell[1][2]}
{cfg.cell[2][0]} {cfg.cell[2][1]} {cfg.cell[2][2]}
{' '.join([ptable.ELEMENTS[t] for t in unique_types])}
 {' '.join([str(c) for c in unique_count])}
Cartesian
{out_pos}
"""
