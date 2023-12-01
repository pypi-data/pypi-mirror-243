"""Defines `class` ``FittingErrors``

"""


class QuantityDeviations:
    """Contains errors for a single quantity"""
    def __init__(self, mad=None, rmsd=None, maxad=None):
        self.mad = mad
        self.rmsd = rmsd
        self.maxad = maxad

    def __repr__(self):
        return f"QuantityDeviations(mad={self.mad}, rmsd={self.rmsd}, maxad={self.maxad})"    

class FittingErrors:
    """
    Container for five QuantityDeviations instances related to energy, energy per atom, forces, stress, and stress in eV.

    Attributes
    ----------
    energy : QuantityDeviations
        QuantityDeviations instance representing deviations related to energy.

    energy_per_atom : QuantityDeviations
        QuantityDeviations instance representing deviations related to energy per atom.

    forces : QuantityDeviations
        QuantityDeviations instance representing deviations related to forces.

    stress : QuantityDeviations
        QuantityDeviations instance representing deviations related to stress.

    stress_ev : QuantityDeviations
        QuantityDeviations instance representing deviations related to stress measured in eV.
    """

    def __init__(self, energy=None, energy_per_atom=None, forces=None, stress=None, stress_ev=None):
        self.energy = energy if energy else QuantityDeviations()
        self.energy_per_atom = energy_per_atom if energy_per_atom else QuantityDeviations()
        self.forces = forces if forces else QuantityDeviations()
        self.stress = stress if stress else QuantityDeviations()
        self.stress_ev = stress_ev if stress_ev else QuantityDeviations()

    def __repr__(self):
        return (
            f"FittingErrors("
            f"energy={self.energy}, "
            f"energy_per_atom={self.energy_per_atom}, "
            f"forces={self.forces}, "
            f"stress={self.stress}, "
            f"stress_ev={self.stress_ev}"
            ")"
        )
