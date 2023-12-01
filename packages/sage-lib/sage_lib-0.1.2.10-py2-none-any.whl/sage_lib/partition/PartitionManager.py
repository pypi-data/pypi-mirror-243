try:
    from sage_lib.master.FileManager import FileManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing FileManager: {str(e)}\n")
    del sys

try:
    from sage_lib.single_run.SingleRun import SingleRun
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing SingleRun: {str(e)}\n")
    del sys

try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

try:
    import os 
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing os: {str(e)}\n")
    del sys

try:
    import copy
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing copy: {str(e)}\n")
    del sys

try:
    import re
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing re: {str(e)}\n")
    del sys

class PartitionManager(FileManager): # el nombre no deberia incluir la palabra DFT tieneu qe ser ma general
    """
    A class for partitioning and managing data files for simulations.

    This class extends FileManager and provides functionalities for handling 
    different types of simulation data, applying operations to it, and organizing the results.

    Attributes:
        file_location (str): The file path where the data files are located.
        containers (list): A list of containers to hold various data structures.
    """
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        """
        Initialize the DataPartition instance.

        Parameters:
            file_location (str, optional): Location of the files to be managed.
            name (str, optional): Name of the partition.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(name=name, file_location=file_location)
        self._containers = []

    def add_container(self, container: object):
        """
        Add a new container to the list of containers.

        Parameters:
            container (object): The container object to be added.
        """
        self.containers.append(container)

    def remove_container(self, container: object):
        """
        Remove a container from the list of containers.

        Parameters:
            container (object): The container object to be removed.
        """
        self.containers.remove(container)

    def empty_container(self):
        """
        Empty the list of containers.
        """
        self.containers = []

    def filter_conteiners(self, filter_class:str, value:float) -> bool:
        mask = np.ones_like(containers)
        for container_index, container in enumerate(self.containers):
            if filter_class.lower() == 'fmax':
                if np.any(container.AtomPositionManager.atomPositions > value):
                    mask[container_index] = 0

        self.containers = self.containers[mask]
        return True 

    def readConfigSetup(self, file_location:str=None, source='VASP', v=False):
        file_location = file_location if type(file_location) == str else self.file_location
        
        DFT_SR = self.readVASPFolder(file_location=file_location, add_container=False, v=v)
        DFT_SR.InputFileManager.set_LDAU( DFT_SR.AtomPositionManager.uniqueAtomLabels )

        for c_i, container in enumerate(self.containers):
            container.InputFileManager = DFT_SR.InputFileManager
            container.KPointsManager = DFT_SR.KPointsManager
            container.PotentialManager = DFT_SR.PotentialManager
            container.BashScriptManager = DFT_SR.BashScriptManager
            container.vdw_kernel_Handler = DFT_SR.vdw_kernel_Handler
            container.WaveFileManager = DFT_SR.WaveFileManager
            container.ChargeFileManager = DFT_SR.ChargeFileManager

    def readVASPSubFolder(self, file_location:str=None, v=False):
        file_location = file_location if type(file_location) == str else self.file_location
                
        for root, dirs, files in os.walk(file_location):
            DFT_SR = self.readVASPFolder(file_location=root, add_container=True, v=v)
            if v: print(root, dirs, files)

    def readVASPFolder(self, file_location:str=None, add_container:bool=True, v=False):
        file_location = file_location if type(file_location) == str else self.file_location

        SR = SingleRun(file_location)
        SR.readVASPDirectory()        
        if add_container and SR.AtomPositionManager is not None: 
            self.add_container(container=SR)

        return SR

    def exportVaspPartition(self, file_location:str=None, label:str='fixed'): 
        for c_i, container in enumerate(self.containers):

            if label == 'enumerate':
                container.exportVASP(file_location=file_location+f'/{c_i:03d}')
            if label == 'fixed':
                container.exportVASP(file_location=file_location)

    def read_configXYZ(self, file_location:str=None, verbose:bool=False):
        file_location = file_location if type(file_location) == str else self.file_location

        lines =list(self.read_file(file_location,strip=False))
        container = []

        for i, line in enumerate(lines):
            print(i, line)
            if line.strip().isdigit():
                num_atoms = int(line.strip())
                if num_atoms > 0:
                    DFT_SR = DFTSingleRun(file_location)
                    DFT_SR.AtomPositionManager = PeriodicSystem()
                    DFT_SR.AtomPositionManager.read_configXYZ(lines=lines[i:i+num_atoms+2])

                    container.append(DFT_SR)

        self._containers += container
        return container

    def export_configXYZ(self, file_location:str=None, verbose:bool=False):
        file_location  = file_location if file_location else self.file_location+'_config.xyz'
        with open(file_location, 'w'):pass # Create an empty file
        for container_index, container in enumerate(self.containers):
            if container.OutFileManager is not None:    
                container.OutFileManager.export_configXYZ(file_location=file_location, save_to_file='a', verbose=False)

        if verbose:
            print(f"XYZ content has been saved to {file_location}")

        return True
    
    def _is_redundant(self, containers:list=None, new_container:object=None):
        """
        Checks if the new configuration is redundant within the existing configurations.

        Parameters:
        - configurations (list): List of existing configurations.
        - new_config (object): New configuration to check.

        Returns:
        - bool: True if redundant, False otherwise.
        """
        containers = containers if containers is not None else self.containers
        return any(np.array_equal(conteiner.atomPositions, new_container.atomPositions) for conteiner in containers)

    def summary(self, ) -> str:
        text_str = ''
        text_str += f'{self.file_location}\n'
        text_str += f'> Conteiners : { len(self.containers) }\n'
        return text_str
    
    def copy_and_update_container(self, container, sub_directory: str, file_location=None):
        container_copy = copy.deepcopy(container)
        container_copy.file_location = f'{container.file_location}{sub_directory}' if file_location is None else file_location
        return container_copy

    def generate_execution_script_for_each_container(self, directories: list = None, file_location: str = None):
        self.create_directories_for_path(file_location)
        script_content = self.generate_script_content('RUNscript.sh', directories)
        self.write_script_to_file(script_content, f"{file_location}/execution_script_for_each_container.py")

    def generate_master_script_for_all_containers(self, directories: list = None, file_location: str = None):
        self.create_directories_for_path(file_location)
        script_content = self.generate_script_content('execution_script_for_each_container.py', directories)
        self.write_script_to_file(script_content, f"{file_location}/master_script_for_all_containers.py")

    def generate_script_content(self, script_name: str, directories: list = None) -> str:
        directories_str = "\n".join([f"    '{directory}'," for directory in directories])
        return f'''#!/usr/bin/env python3
import os
import subprocess

original_directory = os.getcwd()

directories = [
{directories_str}
]

for directory in directories:
    os.chdir(directory)
    subprocess.run(['chmod', '+x', '{script_name}'])
    subprocess.run(['sbatch', '{script_name}'])
    os.chdir(original_directory)
'''

    def write_script_to_file(self, script_content: str, file_path: str):
        with open(file_path, "w") as f:
            f.write(script_content)




'''
DP.exportVaspPartition()

print(DP.containers[0].AtomPositionManager.pbc)
DP.generateDFTVariants('band_structure', values=[{'points':20, 'special_points':'GMLCXG'}])
DP.exportVaspPartition()


path = '/home/akaris/Documents/code/Physics/VASP/v6.1/files/POSCAR/Cristals/test/files'
DP = DFTPartition(path)
DP.readVASPSubFolder(v=False)
DP.readConfigSetup('/home/akaris/Documents/code/Physics/VASP/v6.1/files/POSCAR/Cristals/test/config')
DP.generate_execution_script_for_each_container([ f'{n:03d}'for n, c in enumerate(DP.containers) ], '/home/akaris/Documents/code/Physics/VASP/v6.1/files/POSCAR/Cristals/test/calcs')

#DP.read_configXYZ()

'''




'''
DP.export_configXYZ()

path = '/home/akaris/Documents/code/Physics/VASP/v6.1/files/dataset/CoFeNiOOH_jingzhu/surf_CoFe_4H_4OH/MAG'

DP = DFTPartition(path)

DP.readVASPFolder(v=True)

DP.generateDFTVariants('Vacancy', [1], is_surface=True)
#DP.generateDFTVariants('KPOINTS', [[n,n,1] for n in range(1, 15)] ) 


path = '/home/akaris/Documents/code/Physics/VASP/v6.1/files/dataset/CoFeNiOOH_jingzhu/surf_CoFe_4H_4OH/MAG'
DP = DFTPartition(path)
DP.readVASPFolder(v=True)
DP.generateDFTVariants('NUPDOWN', [n for n in range(0, 10, 1)] )
DP.writePartition()

path = '/home/akaris/DocumeEENnts/code/Physics/VASP/v6.1/files/POSCAR/Cristals/NiOOH/*OH surface with Fe(HS)'
path = '/home/akaris/Documents/code/Physics/VASP/v6.1/files/POSCAR/Cristals/NiOOH/*OH surface for pure NiOOH'
#DP = DFTPartition('/home/akaris/Documents/code/Physics/VASP/v6.1/files/bulk_optimization/Pt/parametros/ENCUT_optimization_252525_FCC')
DP = DFTPartition(path)
#DP.readVASPSubFolder(v=True)
DP.readVASPFolder(v=True)

#DP.generateDFTVariants('Vacancy', [1], is_surface=True)
#DP.generateDFTVariants('KPOINTS', [[n,n,1] for n in range(1, 15)] )    
DP.generateDFTVariants('ENCUT', [n for n in range(200, 1100, 45)] )

DP.writePartition()

DP.generateDFTVariants('ENCUT', [ E for E in range(400,700,30)] )
print( DP.summary() )

print( DP.containers[0].AtomPositionManager.summary() )
'''

