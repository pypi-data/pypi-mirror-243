"""Defines different classes to work with thermodynamic averaging
"""

import functools

class AnyQuantity:
    def __mul__(self, other):
        return Term(self) * Term(other)
    def __truediv__(self, other):
        return Term(self) / Term(other)
    def __pow__(self, power):
        if isinstance(power, int):
            # Power logic for raising the quantity to an integer power
            return Term({self: power}) if power != 0 else Term({})
        else:
            raise TypeError("Unsupported operand type for **")

class Concentration(AnyQuantity):

    lammps_unit_convevt = 1

    def __init__(self, atom_type: int):
        self.atom_type = atom_type
    
    @property
    def display_string(self):
        return f'c{self.atom_type}'
    
    @property
    def lammps_display_string(self):
        return f'c{self.atom_type + 1}'
    
    @property
    def lammps_instant_var_code(self):
        lmp_atom_type = self.atom_type + 1
        return (f'# define c{lmp_atom_type} as the variable for the concentration of {lmp_atom_type}th species\n' + 
                f'variable        atoms_type{lmp_atom_type} atom "type == {lmp_atom_type}"\n' +
                f'group           group_type{lmp_atom_type} dynamic all var atoms_type{lmp_atom_type} every 1\n'+
                f'variable        c{lmp_atom_type} equal count(group_type{lmp_atom_type})/atoms\n')
    
    def __eq__(self, other):
        if isinstance(other, Concentration):
            return self.atom_type == other.atom_type
        return False

    def __hash__(self):
        return hash((Concentration, self.atom_type))

    def __repr__(self):
        return f'Concentration({self.atom_type})'


class Pressure(AnyQuantity):

    display_string = 'p'
    lammps_display_string = 'p'
    lammps_unit_convevt = 0.0001
    lammps_instant_var_code = ('# define p as the pressure variable\n'+
                               'compute         press all pressure NULL pair\n'+
                               'variable        p   equal c_press\n')
    # lammps_thermo_in = 'press' # how it is given to the thermo command

    def __eq__(self, other):
        return isinstance(other, Pressure)

    def __hash__(self):
        return hash(Pressure)

    def __repr__(self):
        return 'Pressure()'

class Energy(AnyQuantity):
    
    display_string = 'e'
    lammps_display_string = 'e'
    lammps_unit_convevt = 1
    lammps_instant_var_code = ('# define e as the potential energy variable\n'+
                               'variable        e equal c_thermo_pe/atoms\n')
    
    def __eq__(self, other):
        return isinstance(other, Energy)

    # Define the hash operator
    def __hash__(self):
        return hash(Energy)

    def __repr__(self):
        return 'Energy()'

class Volume(AnyQuantity):
    
    display_string = 'V'
    lammps_display_string = 'v'
    lammps_unit_convevt = 1
    lammps_instant_var_code = ('# define v as the intensive volume variable\n'+
                               'variable        v equal vol/atoms\n')
    
    def __eq__(self, other):
        return isinstance(other, Volume)

    # Define the hash operator
    def __hash__(self):
        return hash(Volume)

    def __repr__(self):
        return 'Volume()'

class Term:
    '''Term is the product of variables in the form of {variable: power}, 
    e.g. {Pressure: 1, Energy: 2} is pE^2.
    '''
    def __init__(self, vars = {}):
        if type(vars) == dict:
            self.vars: dict = vars
        elif type(vars) == Term:
            self.vars: dict = vars.vars
        elif vars is None:
            self.vars = {}
        elif isinstance(vars, AnyQuantity):
            self.vars = {vars: 1}
        elif vars==1:
            vars.vars = {}
        else: raise TypeError('vars should be a dict, quantity, or 1')        

    def __eq__(self, other):
        if isinstance(other, Term):
            return self.vars == other.vars
        return False

    # Define the hash operator
    def __hash__(self):
        return hash( tuple(self.vars.items()) )

    def _repr_short(self):
        l = [] # list of strings
        for v, p in self.vars.items():
            if p == 0:
                continue
            elif p == 1:
                l.append(f'{v.display_string}')
            else:
                l.append(f'{v.display_string}^{p}')
        if not l: l = ['1']
        return '*'.join(l)

    def __repr__(self):
        return f'<Term: {self._repr_short()}>'

    def _sort_term(self) -> None:
        '''Auxiliary function: sort the vars in the order: e, p, c0, c1, ... .
        '''
        custom_order = {**{'e': 0, 'p': 1, 'V': 2}, **{f'c{i}': i+3 for i in range(len(self.vars))}}
        def custom_key(item):
            return custom_order[item[0].display_string]
        self.vars = dict(sorted(self.vars.items(), key=custom_key))

    @property
    @functools.lru_cache
    def lammps_var_name(self) -> str:
        '''Names of the variables will follow this convention.
        For Term({Energy: 2, Pressure: 3, Concentration(1): 1})
        the variable will have the name 'e_2_p_3_c1_1'.
        '''
        self._sort_term()
        lammps_var_name = '_'.join([f'{key.lammps_display_string}_{val}' for key, val in self.vars.items()])
        return lammps_var_name

    @property
    def const_lammps_unit_convert(self) -> str:
        '''returns the constant to converts the output lammps quantity
        '''
        const = 1
        for key, val in self.vars.items():
            const *= key.lammps_unit_convevt**val
        return const

    def __mul__(self, other):
        if isinstance(other, AnyQuantity):
            other = Term({other:1})
        if isinstance(other, Term):
            # Multiplication logic for Terms
            new_vars = dict(self.vars)
            for var, power in other.vars.items():
                if var in new_vars:
                    new_vars[var] += power
                else:
                    new_vars[var] = power
                if new_vars[var] == 0:
                    del new_vars[var]
            return Term(new_vars)
        else:
            raise TypeError("Unsupported operand type for *")

    def __truediv__(self, other):
        if isinstance(other, AnyQuantity):
            other = Term({other:1})
        if isinstance(other, Term):
            # Division logic for Terms
            new_vars = dict(self.vars)
            for var, power in other.vars.items():
                if var in new_vars:
                    new_vars[var] -= power
                else:
                    new_vars[var] = -power
                if new_vars[var] == 0:
                    del new_vars[var]
            return Term(new_vars)
        else:
            raise TypeError("Unsupported operand type for /")

    def __pow__(self, power):
        if isinstance(power, int):
            if power == 0: return Term({})
            # Power logic for Terms
            new_vars = {var: power * p for var, p in self.vars.items()}
            return Term(new_vars)
        else:
            raise TypeError("Unsupported operand type for **")

class TermContainer:
    '''Container for the instances of class Term.
    '''

    def __init__(self, terms: list):
        self.terms = [Term(t) for t in terms]

    @property
    def len(self):
        return len(self.terms)

    def _lammps_pre_define_variables(self):
        '''Predefines lammps variables of power 1 that will be used later.
        '''
        terms_power1 = set()
        for term in self.terms:
            terms_power1.update(set(term.vars.keys()))
        return '\n'.join([term.lammps_instant_var_code for term in terms_power1])

    def lammps_thermo_code(self, batch_size):
        '''Generates lammps thermo code.
        '''
        str_vars = self._lammps_pre_define_variables() + '\n'
        str_fixes = ''
        str_vars_aver = ''
        for i, term in enumerate(self.terms):
            lammps_var_name = term.lammps_var_name
            lammps_equation = '*'.join([f'v_{key.lammps_display_string}^{val}' for key, val in term.vars.items()])
            str_vars += f'variable        {lammps_var_name} equal {lammps_equation}\n'
            # 1000 b/c we want to escape collisions with other fixes
            str_fixes += f'fix            {1000+i} all ave/time 1 {batch_size} {batch_size} v_{lammps_var_name}\n'
            str_vars_aver += f'variable        {lammps_var_name}_ equal f_{1000+i}\n'
        lammps_thermo = {'vars_before_fixes': str_vars, 'fixes': str_fixes, 'vars_after_fixes': str_vars_aver}
        return lammps_thermo

    def __repr__(self):
        term_strs = [t._repr_short() for t in self.terms]
        return f'<TermContainer: [{", ".join(term_strs)}]>'
