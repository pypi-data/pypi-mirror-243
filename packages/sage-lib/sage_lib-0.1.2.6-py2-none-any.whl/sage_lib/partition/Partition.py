try:
    from sage_lib.partition.partition_builder.BandStructure_builder import BandStructure_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing BandStructure_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.Config_builder import Config_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing Config_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.Crystal_builder import Crystal_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing Crystal_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.CrystalDefect_builder import CrystalDefect_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing CrystalDefect_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.ForceField_builder import ForceField_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing ForceField_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.Molecule_builder import Molecule_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing Molecule_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.PositionEditor_builder import PositionEditor_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing PositionEditor_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.SurfaceStates_builder import SurfaceStates_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing SurfaceStates_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.VacuumStates_builder import VacuumStates_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing VacuumStates_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.PartitionManager import PartitionManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing PartitionManager: {str(e)}\n")
    del sys

try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

class Partition(BandStructure_builder, Config_builder, Crystal_builder, CrystalDefect_builder, ForceField_builder, 
                 Molecule_builder, PositionEditor_builder, SurfaceStates_builder, VacuumStates_builder):
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        super().__init__(name=name, file_location=file_location)

    def generate_variants(self, parameter: str, values:np.array=None, file_location: str = None) -> bool:
        containers = []
        directories = ['' for _ in self.containers]
        parameter = parameter.upper().strip()
        for container_index, container in enumerate(self.containers):
            if parameter.upper() == 'KPOINTS':
                containers += self.handleKPoints(container, values, container_index,  file_location) 
                directories[container_index] = 'KPOINTConvergence'

            elif container.InputFileManager and parameter.upper() in container.InputFileManager.parameters_data:
                containers += self.handleInputFile(container, values, parameter,  container_index, file_location)
                directories[container_index] = f'{parameter}_analysis'

            elif parameter.upper() == 'VACANCY':
                containers += self.handleVacancy(container, values, container_index, file_location)
                directories[container_index] = 'Vacancy'

            elif parameter.upper() == 'BAND_STRUCTURE':
                containers += self.handleBandStruture(container, values, container_index, file_location)
                directories[container_index] = 'band_structure'

            elif parameter.upper() == 'RATTLE':
                containers += self.handleRattle(container, values, container_index, file_location)
                directories[container_index] = 'rattle'

        self.containers = containers
        self.generate_master_script_for_all_containers(directories, file_location if not file_location is None else container.file_location )

'''
path = '/home/akaris/Documents/code/Physics/VASP/v6.2/files/dataset/CoFeNiOOH_jingzhu/bulk_NiFe/rattle'
DP = Partition(path)

DP.readVASPFolder(v=False)
DP.generate_variants('rattle', [ {'N':20, 'std':[0.13]} ] )
'''
