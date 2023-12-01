try:
    from sage_lib.input.structure_handling_tools.AtomPositionLoader import AtomPositionLoader
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.Input.structure_handling_tools.AtomPositionLoader: {str(e)}\n")
    del sys

try:
    from sage_lib.input.structure_handling_tools.AtomPositionOperator import AtomPositionOperator
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.Input.structure_handling_tools.AtomPositionOperator: {str(e)}\n")
    del sys

try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

try:
    import re
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing re: {str(e)}\n")
    del sys

class AtomPositionManager(AtomPositionLoader, AtomPositionOperator):
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        super().__init__(name=name, file_location=file_location)
        self._comment = None
        self._atomCount = None  # N total number of atoms
        self._scaleFactor = None  # scale factor
        self._uniqueAtomLabels = None  # [Fe, N, C, H]
        self._atomCountByType = None  # [n(Fe), n(N), n(C), n(H)]
        self._selectiveDynamics = None  # bool 
        self._atomPositions = None  # np.array(N, 3)
        self._atomicConstraints = None # np.array(N, 3)

        self._atomLabelsList = None  # [Fe, N, N, N, N, C, C, C, C, H]
        self._fullAtomLabelString = None  # FeFeFeNNNNNNNCCCCCCCCCCCCCCCHHHHHHHHHHHHHHHH
        self._atomPositions_tolerance = 1e-2

        self._distance_matrix = None
        
        self._total_charge = None
        self._magnetization = None
        self._total_force = None
        self._E = None
        self._Edisp = None
        self._IRdisplacement = None

    @property
    def distance_matrix(self):
        if self._distance_matrix is not None:
            return self._distance_matrix
        elif self._atomPositions is not None:
            from scipy.spatial.distance import cdist 
            self._distance_matrix = cdist(self._atomPositions, self._atomPositions, 'euclidean')
            return self._distance_matrix
        elif'_atomPositions' not in self.__dict__:
            raise AttributeError("Attribute _atomPositions must be initialized before accessing atomLabelsList.")
        else:
            return None

    @property
    def scaleFactor(self):
        if type(self._scaleFactor) in [int, float, list, np.array]:
            self._scaleFactor = np.array(self._scaleFactor)
            return self._scaleFactor
        elif self._scaleFactor is None: 
            self._scaleFactor = np.array([1])
            return self._scaleFactor
        elif self._scaleFactor is not None:
            return self._scaleFactor
        else:
            return None

    @property
    def atomCount(self):
        if self._atomCount is not None:
            return np.array(self._atomCount)
        elif self._atomPositions is not None: 
            self._atomCount = self._atomPositions.shape[0] 
            return self._atomCount
        elif self._atomLabelsList is not None: 
            self._atomCount = self._atomLabelsList.shape
            return self._atomCount   
        elif'_atomPositions' not in self.__dict__:
            raise AttributeError("Attribute _atomPositions must be initialized before accessing atomLabelsList.")
        else:
            return None

    @property
    def uniqueAtomLabels(self):
        if self._uniqueAtomLabels is not None:
            return self._uniqueAtomLabels
        elif self._atomLabelsList is not None: 
            self._uniqueAtomLabels = list(dict.fromkeys(self._atomLabelsList).keys())
            return np.array(self._uniqueAtomLabels)
        elif'_atomLabelsList' not in self.__dict__:
            raise AttributeError("Attribute _atomLabelsList must be initialized before accessing atomLabelsList.")
        else:
            return None

    @property
    def atomCountByType(self):
        if self._atomCountByType is not None:
            return self._atomCountByType
        elif self._atomLabelsList is not None: 
            atomCountByType, atomLabelByType = {}, []
            for a in self._atomLabelsList:
                if not a in atomCountByType:
                    atomLabelByType.append(1)
                    atomCountByType[a] = len(atomLabelByType)-1
                else:
                    atomLabelByType[atomCountByType[a]] += 1
            self._atomCountByType = np.array(atomLabelByType)
            return self._atomCountByType
        elif'_atomLabelsList' not in self.__dict__:
            raise AttributeError("Attribute _atomLabelsList must be initialized before accessing atomLabelsList.")
        else:
            return None

    @property
    def atomLabelsList(self):
        if '_atomCountByType' not in self.__dict__ or '_uniqueAtomLabels' not in self.__dict__:
            raise AttributeError("Attributes _atomCountByType and _uniqueAtomLabels must be initialized before accessing atomLabelsList.")
        elif self._atomLabelsList is None and not self._atomCountByType is None and not self._uniqueAtomLabels is None: 
            return np.array([label for count, label in zip(self._atomCountByType, self._uniqueAtomLabels) for _ in range(count)])
        else:
            return  self._atomLabelsList 

    @property
    def fullAtomLabelString(self):
        if '_atomCountByType' not in self.__dict__ or '_uniqueAtomLabels' not in self.__dict__:
            raise AttributeError("Attributes _atomCountByType and _uniqueAtomLabels must be initialized before accessing fullAtomLabelString.")
        elif self._fullAtomLabelString is None and not self._atomCountByType is None and not self._uniqueAtomLabels is None: 
            self._fullAtomLabelString = ''.join([label*count for count, label in zip(self._atomCountByType, self._uniqueAtomLabels)])
            return self._fullAtomLabelString
        else:
            return  self._fullAtomLabelString 

    @property
    def atomPositions(self):
        if self._atomPositions is list:
            return np.array(self._atomPositions)
        elif self._atomPositions is None:
            return np.array([]).reshape(0, 3) 
        else:
            return self._atomPositions

    @property
    def atomicConstraints(self):
        if self._atomicConstraints is list:
            return np.array(self._atomicConstraints)
        elif self._atomPositions is not None:
            self._atomicConstraints = np.ones_like(self._atomPositions) 
            return self._atomicConstraints
        else:
            return self._atomicConstraints

        '''
    def calculate_rms_displacement_in_angstrom(atomic_mass_amu, temperature, frequency_au=1.0):
        """
        Calculate the root-mean-square displacement of an atom in a harmonic potential in Ångströms.

        Parameters:
        atomic_mass_amu (float): Atomic mass of the element in atomic mass units (amu).
        temperature (float): Temperature in Kelvin.
        frequency_au (float): Vibrational frequency in atomic units (default is 1.0).

        Returns:
        float: RMS displacement in Ångströms.
        """
        # Constants in atomic units
        k_B_au = 3.1668114e-6  # Boltzmann constant in hartree/Kelvin
        amu_to_au = 1822.888486209  # Conversion from amu to atomic units of mass
        bohr_to_angstrom = 0.529177  # Conversion from Bohr radius to Ångströms

        # Convert mass from amu to atomic units
        mass_au = atomic_mass_amu * amu_to_au

        # Force constant in atomic units
        k_au = mass_au * frequency_au**2

        # RMS displacement in atomic units
        sigma_au = np.sqrt(k_B_au * temperature / k_au)

        # Convert RMS displacement to Ångströms
        sigma_angstrom = sigma_au * bohr_to_angstrom
        
        return sigma_angstrom
        '''
