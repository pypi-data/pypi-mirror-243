from typing import Union, Literal
import functools


class Msd:

    def __init__(self, atom_type = None):
        # Because we are doing GCMC simulations, we compute msd for all atoms
        # If we try computing it species by species, the task will have incorrect formulation

        # TODO: check for correctness of atom_type
        self.atom_type = atom_type

    @property
    def display_atom_type(self):
        return f'{self.atom_type}' if self.atom_type is not None else 'all'
    
    @property
    def lammps_compute_group(self):
        return f'group_type_{self.atom_type}' if self.atom_type is not None else 'all'
    

    @property
    def display_string(self):
        return f'msd_{self.display_atom_type}'

    @property
    def lammps_var_name(self):
        return f'msd_{self.display_atom_type}'
    
    @property
    def lammps_compute_code(self):
        return f'compute {self.lammps_var_name} {self.lammps_compute_group} msd com yes' 
    
    def __eq__(self, other):
        return isinstance(other, Msd)
    
    def __hash__(self):
        return hash(Msd)

    def __repr__(self):
        if self.atom_type:
            return f'Msd()'
        else:
            return f'Msd({self.atom_type})'


class KineticContainer:
    """The current version of Container only works with Msd classes. 
    But can be possibly customized for computation of other kinetic properties.
    """
    def __init__(self, terms):
        self.terms = terms
    
    def __len__(self):
        return len(self.terms)

    def lammps_kinetic_code(self, batch_size):
        '''Generates lammps kinetic code.
        '''
        str_computes = ''
        # output will be defined later in the lammps.py module
        for term in self.terms:
            str_computes += term.lammps_compute_code
            str_computes += '\n'

        str_vars_after_fixes = ''
        # output will be defined later in the lammps.py module
        for term in self.terms:
            str_vars_after_fixes += f'variable        {term.lammps_var_name}_ equal c_{term.lammps_var_name}[4]\n'

        return {'computes': str_computes, 'vars_after_fixes': str_vars_after_fixes}
