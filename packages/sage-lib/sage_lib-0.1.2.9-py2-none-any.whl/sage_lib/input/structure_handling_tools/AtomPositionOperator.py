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

class AtomPositionOperator:
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        super().__init__(name=name, file_location=file_location)
        
    def convert_to_periodic(self):
        return PeriodicSystem(**self.attributes)
    
    def convert_to_non_periodic(self):
        return NonPeriodicSystem(**self.attributes)

    def distance(self, r1, r2): return np.linalg.norm(r1, r2)

    def move_atom(self, atom_index:int, displacement:np.array):
        self._atomPositions[atom_index,:] += displacement
        self._distance_matrix = None
        self._atomPositions_fractional = None

    def set_atomPositions(self, new_atomPositions:np.array):
        self._atomPositions = new_atomPositions
        self._distance_matrix = None
        self._atomPositions_fractional = None

    def remove_atom(self, atom_index: int):
        """Remove an atom at the given index."""
        self._atomicConstraints = np.delete(self.atomicConstraints, atom_index, axis=0)
        self._atomPositions = np.delete(self.atomPositions, atom_index, axis=0)
        self._atomPositions_fractional = np.delete(self._atomPositions_fractional, atom_index, axis=0)
        self._atomLabelsList = np.delete(self.atomLabelsList, atom_index)
        self._total_charge = np.delete(self.total_charge, atom_index) if self._total_charge is not None else self._total_charge
        self._magnetization = np.delete(self.magnetization, atom_index) if self._magnetization is not None else self._magnetization
        self._total_force = np.delete(self.total_force, atom_index) if self._total_force is not None else self._total_force
        self._atomCount -= 1
        self._atomCountByType = None
        self._fullAtomLabelString = None
        self._uniqueAtomLabels = None

        if self._distance_matrix is not None:
            self._distance_matrix = np.delete(self._distance_matrix, var, axis=0)  # Eliminar fila
            self._distance_matrix = np.delete(self._distance_matrix, var, axis=1)  # Eliminar columna

    def add_atom(self, atomLabels: str, atomPosition: np.array, atomicConstraints: np.array = np.array([1, 1, 1])) -> bool:
        """
        Adds an atom to the AtomContainer.

        :param atomLabels: Label for the new atom.
        :param atomPosition: Position of the new atom as a numpy array.
        :param atomicConstraints: Atomic constraints as a numpy array (defaults to [1,1,1]).
        """
        # Add to atomPositions
        self._atomPositions = np.atleast_2d(atomPosition) if self.atomPositions is None else np.vstack([self.atomPositions, atomPosition])

        # Add to atomLabelsList
        self._atomLabelsList = np.array([atomLabels]) if self.atomLabelsList is None else np.append(self.atomLabelsList, atomLabels)

        # Add to atomicConstraints
        self._atomicConstraints = np.vstack([self.atomicConstraints, atomicConstraints]) if self.atomicConstraints is not None else np.atleast_2d(atomicConstraints)

        # Increment atomCount
        self._atomCount = 1 if self._atomCount is None else self._atomCount + 1

        # Reset dependent attributes
        self._reset_dependent_attributes()

        # Group elements and positions
        self.group_elements_and_positions()
        return True

    def _reset_dependent_attributes(self):
        """
        Resets dependent attributes to None.
        """
        attributes_to_reset = ['_total_charge', '_magnetization', '_total_force', '_atomPositions_fractional', 
                               '_atomCountByType', '_fullAtomLabelString', '_uniqueAtomLabels', '_distance_matrix']
        for attr in attributes_to_reset:
            setattr(self, attr, None)

    def find_n_closest_neighbors(self, position, n):
        """Find the n closest neighbors to a given atom."""
        #distance_matrix = self.distanceamtrix
        #distances = distance_matrix[atom_index]
        
        # Sort the distances and get the indices of the n closest neighbors.
        # We exclude the first index because it's the atom itself (distance=0).
        distances = [self.distance( position, a) for a in self.atomPositions ]
        closest_indices = np.argsort( distances )[:n]
        
        # Get the labels and positions of the closest neighbors.
        closest_labels = [self._atomLabelsList[i] for i in closest_indices]
        closest_distance = [ distances[i] for i in closest_indices]
        
        return closest_indices, closest_labels, closest_distance

    def compare_chemical_environments(self, distances1, labels1, distances2, labels2, label_weights=None, distance_decay=1.0):
        """
        Compare two chemical environments and return a similarity score.

        Parameters:
        - distances1, distances2: List of distances to the atoms in the environments.
        - labels1, labels2: List of labels indicating the type of each atom in the environments.
        - label_weights: Dictionary assigning weights to each type of atom label. If None, all weights are set to 1.
        - distance_decay: A decay factor for the influence of distance in the similarity score.

        Returns:
        - float: A similarity score. Lower values indicate more similar environments.
        """
        if label_weights is None:
            label_weights = {label: 1.0 for label in set(labels1 + labels2)}
        
        # Initialize similarity score
        similarity_score = 0.0

        for d1, l1 in zip(distances1, labels1):
            min_diff = float('inf')
            for d2, l2 in zip(distances2, labels2):
                if l1 == l2:
                    diff = np.abs(d1 - d2)
                    min_diff = min(min_diff, diff)
            
            if min_diff != float('inf'):
                weight = label_weights.get(l1, 1.0)
                similarity_score += weight * np.exp(-distance_decay * min_diff)

        return similarity_score

    def get_plane(self, atom1, atom2, atom3):
        v1 = self.atomPositions[atom1, :] - self.atomPositions[atom2, :]
        v2 = self.atomPositions[atom2, :] - self.atomPositions[atom3, :]
        # | i        j     k   | #
        # | v1x    v1y    v1z  | #
        # | v2x    v2y    v2z  | #
        return np.array([   v1[1]*v2[2]-v1[2]*v2[1],
                            v1[2]*v2[0]-v1[0]*v2[2],
                            v1[0]*v2[1]-v1[1]*v2[0], ])

    def get_dihedric(self, atom1, atom2, atom3, atom4):
        p1 = self.get_plane(atom1, atom2, atom3)
        p2 = self.get_plane(atom2, atom3, atom4)
        '''
     ****         xxx
        ****    xxx
          ****xxxfilename
            xxx***
          xxx   *****
        xxx (P2)   ***** (P1)
        '''
        return self.get_vector_angle(p1, p2)

    def get_angle(self, atom1, atom2, atom3):
        v1 = self.atomPositions[atom1, :] - self.atomPositions[atom2, :]
        v2 = self.atomPositions[atom2, :] - self.atomPositions[atom3, :]

        return self.get_vector_angle(v1, v2)

    def get_vector_angle(self, v1, v2):
        '''
        1.     The get_vector_angle function takes two vectors as input. These vectors represent the direction and magnitude of an angle between the vectors.
        2.     The function calculates the angle between the vectors using the arccosine function.
        3.     The angle returned is a unit vector in the direction of the angle.
        '''
        unit_vector_1 = v1 / np.linalg.norm(v1)
        unit_vector_2 = v2 / np.linalg.norm(v2)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        angle = np.arccos(dot_product)

        return angle

    def rotation_matrix(self, axis, phi):
        """Create a rotation matrix given an axis and an angle phi."""
        axis = normalize(axis)
        a = np.cos(phi / 2)
        b, c, d = -axis * np.sin(phi / 2)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                         [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                         [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

    def rotate_atoms(self, atoms, axis, phi):
        """
        Rotate a set of atoms around an axis by an angle phi.

        :param atoms: A Nx3 matrix of atomic coordinates.
        :param axis: A 3D vector representing the rotation axis.
        :param phi: The rotation angle in radians.
        :return: The rotated Nx3 matrix of atomic coordinates.
        """
        # Create the rotation matrix
        R = self.rotation_matrix(axis, phi)
        # Apply the rotation matrix to each row (atom) in the atoms matrix
        return np.dot(atoms, R.T)

    def group_elements_and_positions(self, atomLabelsList:list=None, atomPositions:list=None):
        # Verificar que la longitud de element_labels coincide con el número de filas en position_matrix
        atomLabelsList = atomLabelsList if atomLabelsList is not None else self.atomLabelsList
        atomPositions = atomPositions if atomPositions is not None else self.atomPositions

        # Crear un diccionario para almacenar los índices de cada tipo de elemento
        element_indices = {}
        for i, label in enumerate(atomLabelsList):
            if label not in element_indices:
                element_indices[label] = []
            element_indices[label].append(i)

        # Crear una nueva lista de etiquetas y una nueva matriz de posiciones
        atomLabelsList_new = []
        atomPositions_new = []
        uniqueAtomLabels_new = element_indices.keys()
        for label in element_indices:
            atomLabelsList_new.extend([label] * len(element_indices[label]))
            atomPositions_new.extend(atomPositions[element_indices[label]])

        self._atomLabelsList = atomLabelsList_new
        self._atomPositions = np.array(atomPositions_new)
        self._uniqueAtomLabels = None  # [Fe, N, C, H]
        self._atomCountByType = None  # [n(Fe), n(N), n(C), n(H)]
        self._fullAtomLabelString = None  # FeFeFeNNNNNNNCCCCCCCCCCCCCCCHHHHHHHHHHHHHHHH

        return True

    def atomLabelFilter(self, ID, v=False):  
        return np.array([ True if n in ID else False for n in self.atomLabelsList])

    def rattle(self, stdev:float=0.001, seed:float=None, rng:float=None):
        """Randomly displace atoms.

        This method adds random displacements to the atomic positions,
        taking a possible constraint into account.  The random numbers are
        drawn from a normal distribution of standard deviation stdev.

        For a parallel calculation, it is important to use the same
        seed on all processors!  """

        if seed is not None and rng is not None:
            raise ValueError('Please do not provide both seed and rng.')

        if rng is None:
            if seed is None:
                seed = 42
            rng = np.random.RandomState(seed)

        self.set_atomPositions(self.atomPositions +
                           rng.normal(scale=stdev, size=self.atomPositions.shape))


    def introduce_vacancy(self, atom_index: int, tolerance_z=4, verbosity:bool=False):
        """
        Introduce a vacancy by removing an atom.
        """
        # Remove the atom at the specified index
        removed_atom_position = self.atomPositions[atom_index]
        removed_atom_label = self.atomLabelsList[atom_index]
        self.remove_atom(atom_index)

        if self.is_surface:
            opposite_atom_index = self.find_opposite_atom(removed_atom_position, removed_atom_label, tolerance_z=tolerance_z)
            if opposite_atom_index is not None:
                self.remove_atom(opposite_atom_index)

        if verbosity: print( f'Vacancy {removed_atom_label} generated.')

    def introduce_interstitial(self, new_atom_label:str, new_atom_position:np.array, verbosity:bool=False):
        """
        Introduce a self-interstitial defect.
        
        A self-interstitial is a type of point defect where an extra atom is added to an interstitial site.
        This method adds an atom to a specified interstitial position and updates the associated metadata.
        """ 
        self.add_atom(atomLabels=new_atom_label, atomPosition=new_atom_position)

        if verbosity: print( f'Interstitial {new_atom_label} at {removed_atom_position}.')

    def introduce_substitutional_impurity(self, atom_index:int, new_atom_label: str, verbosity:bool=False):
        """
        Introduce a substitutional impurity.
        
        A substitutional impurity is a type of point defect where an atom is replaced by an atom of a different type.
        This method modifies the type of atom at the specified index to a new type.
        """
        # Remove the atom at the specified index
        removed_atom_position = self.atomPositions[atom_index]
        removed_atom_label = self.atomLabelsList[atom_index]
        self.remove_atom(atom_index)
        self.add_atom(atomLabels=new_atom_label, atomPosition=removed_atom_position)

        if verbosity: print( f'Substitution {removed_atom_label} >> {new_atom_label} at {removed_atom_position}.')
        # Update _atomCountByType here similar to introduce_vacancy
