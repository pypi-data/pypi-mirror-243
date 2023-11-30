try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

try:
    from sage_lib.input.structure_handling_tools.structural_file_readers.CIF import CIF
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.input.structure_handling_tools.structural_file_readers.CIF: {str(e)}\n")
    del sys

try:
    from sage_lib.input.structure_handling_tools.structural_file_readers.PDB import PDB
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.input.structure_handling_tools.structural_file_readers.PDB: {str(e)}\n")
    del sys

try:
    from sage_lib.input.structure_handling_tools.structural_file_readers.POSCAR import POSCAR
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.input.structure_handling_tools.structural_file_readers.POSCAR: {str(e)}\n")
    del sys

try:
    from sage_lib.input.structure_handling_tools.structural_file_readers.XYZ import XYZ
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.input.structure_handling_tools.structural_file_readers.XYZ: {str(e)}\n")
    del sys

try:
    from sage_lib.input.structure_handling_tools.structural_file_readers.SI import SI
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sage_lib.input.structure_handling_tools.structural_file_readers.SI: {str(e)}\n")
    del sys

class AtomPositionLoader(CIF, POSCAR, XYZ, SI, PDB):
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        super().__init__(name=name, file_location=file_location)
        self._comment = None
        self._atomCount = None  # N total number of atoms

'''
a = AtomPositionLoader('/home/akaris/Documents/code/Physics/VASP/v6.2/files/dataset/CoFeNiOOH_jingzhu/bulk_NiFe/POSCAR')
a.read_POSCAR()
#print(AtomPositionLoader.__mro__)
'''