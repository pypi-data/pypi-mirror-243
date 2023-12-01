import os
import getpass
import time
import argparse

from fiqus.utils.Utils import initialize_logger
from fiqus.utils.Utils import FilesAndFolders as Util
from fiqus.utils.Utils import CheckForExceptions as Check
from fiqus.data import DataFiQuS as dF
from fiqus.mains.MainMultipole import MainMultipole
from fiqus.mains.MainCCT import MainCCT
from fiqus.mains.MainPancake3D import MainPancake3D


class MainFiQuS:
    def __init__(self, input_file_path: str = None, model_folder: str = None, verbose: bool = True, fdm=None, GetDP_path=None):
        """
        Main class for working with FiQuS simulations
        :param input_file_path: input file name
        :param verbose: if True, more info is printed in the console
        """
        self.time_stamp = time.strftime("%Y-%m-%d-%H-%M-%S")

        self.start_folder = os.getcwd()
        self.wrk_folder = model_folder

        # Intialize logger
        self.logger = initialize_logger(
            verbose=verbose, time_stamp=self.time_stamp, work_folder=self.wrk_folder
        )

        self.verbose = verbose
        if self.verbose:
            Util.print_welcome_graphics()

        # Load yaml input file
        if not fdm:
            self.fdm = Util.read_data_from_yaml(input_file_path, dF.FDM)
        else:
            self.fdm = fdm

        # Check for input errors
        Check.check_inputs(self.fdm.run)

        # Initialize Main object
        if self.fdm.magnet.type == 'CCT_straight':
            self.main_magnet = MainCCT(fdm=self.fdm, verbose=verbose)

        elif self.fdm.magnet.type == 'multipole':
            # Load settings
            self.sdm = Util.read_data_from_yaml(f'{input_file_path[:-5]}.set', dF.FiQuSSettings)

            self.main_magnet = MainMultipole(fdm=self.fdm, sdm=self.sdm, rgd_path=f'{input_file_path[:-5]}.geom',
                                             verbose=verbose)

        elif self.fdm.magnet.type == 'Pancake3D':
            self.main_magnet = MainPancake3D(fdm=self.fdm, verbose=verbose)
        else:
            raise ValueError(f'FiQuS does not support magnet type: {self.fdm.magnet.type}!')

        # Load user paths for executables and additional files
        user_name = getpass.getuser()
        if verbose:
            print(f'FiQuS is running on machine with user name: {user_name}')
        if user_name in ['root', 'MP-WIN-02$']:
            user_name = 'SYSTEM'
        path_to_settings_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests", f"settings.{user_name}.yaml")
        if verbose:
            print(f'FiQuS is using settings file: {path_to_settings_file}')
        if GetDP_path:
            self.main_magnet.settings = {'GetDP_path': GetDP_path}
            self.main_magnet.GetDP_path = GetDP_path
        else:
            self.main_magnet.settings = Util.read_data_from_yaml(path_to_settings_file, dict)
            self.main_magnet.GetDP_path = self.main_magnet.settings['GetDP_path']

        # Save Model/Geometry/Mesh/Solution folder paths
        Util.prep_folder(self.wrk_folder)
        self.save_folders()

        # Build magnet
        self.summary = dict.fromkeys(['SJ', 'SICN', 'SIGE', 'Gamma', 'nodes', 'solution_time', 'overall_error', 'minimum_diff', 'maximum_diff'])
        self.build_magnet()

    def save_folders(self):
        def _check_and_generate_path(folder_type: str = None):
            if folder_type == "Geometry":
                folder = self.wrk_folder
            elif folder_type == "Mesh":
                folder = self.main_magnet.geom_folder
            elif folder_type == "Solution":
                folder = self.main_magnet.mesh_folder
            else:
                raise Exception("Incompatible type.")

            if getattr(self.fdm.run, folder_type.lower()) is None:
                # folder_key is not given, so it is computed
                folder_key = Util.compute_folder_key(
                    folder_type=folder_type,
                    folder=folder,
                    overwrite=self.fdm.run.overwrite,
                )
            else:
                # folder_key is given
                folder_key = getattr(self.fdm.run, folder_type.lower())

            required_folder = folder_type in required_folders
            if self.fdm.run.overwrite and folder_type == (
                required_folders[0] if required_folders else None
            ):
                Check.check_overwrite_conditions(
                    folder_type=folder_type, folder=folder, folder_key=folder_key
                )
            return Util.get_folder_path(
                folder_type=folder_type,
                folder=folder,
                folder_key=folder_key,
                overwrite=self.fdm.run.overwrite,
                required_folder=required_folder,
            )

        if self.fdm.run.type == "start_from_yaml":
            required_folders = ["Geometry", "Mesh", "Solution"]
        elif self.fdm.run.type == "geometry_and_mesh":
            required_folders = ["Geometry", "Mesh"]
        elif self.fdm.run.type == "mesh_and_solve_with_post_process_python":
            required_folders = ["Mesh", "Solution"]
        elif self.fdm.run.type in ["solve_with_post_process_python", "solve_only"]:
            required_folders = ["Solution"]
        elif self.fdm.run.type == "geometry_only":
            required_folders = (
                []
                if self.fdm.run.geometry and not self.fdm.run.overwrite
                else ["Geometry"]
            )
        elif self.fdm.run.type == "mesh_only":
            required_folders = (
                [] if self.fdm.run.mesh and not self.fdm.run.overwrite else ["Mesh"]
            )
        else:  # post_process_getdp_only or post_process_python_only or plot_python
            required_folders = []

        fdm = self.main_magnet.fdm.magnet
        self.main_magnet.geom_folder = _check_and_generate_path(folder_type='Geometry')
        Util.write_data_to_yaml(os.path.join(self.main_magnet.geom_folder, 'geometry.yaml'), fdm.geometry.dict(by_alias=True))
        if not self.fdm.run.type == 'geometry_only':
            self.main_magnet.mesh_folder = _check_and_generate_path(folder_type='Mesh')
            Util.write_data_to_yaml(os.path.join(self.main_magnet.mesh_folder, 'mesh.yaml'), fdm.mesh.dict(by_alias=True))
        if not (self.fdm.run.type == 'geometry_only' or self.fdm.run.type == 'mesh_only'):
            self.main_magnet.solution_folder = _check_and_generate_path(folder_type='Solution')
            Util.write_data_to_yaml(os.path.join(self.main_magnet.solution_folder, 'solve.yaml'), fdm.solve.dict(by_alias=True))
            Util.write_data_to_yaml(os.path.join(self.main_magnet.solution_folder, 'postproc.yaml'), fdm.postproc.dict(by_alias=True))

    def build_magnet(self):
        if self.fdm.run.type == 'start_from_yaml':  # needs 3 files (yaml, set, geom)
            self.main_magnet.generate_geometry()
            self.main_magnet.pre_process()
            self.main_magnet.load_geometry()
            for key, value in self.main_magnet.mesh().items():
                self.summary[key] = value
            self.summary['solution_time'] = self.main_magnet.solve_and_postprocess_getdp()
            for key, value in self.main_magnet.post_process_python(gui=self.main_magnet.fdm.run.launch_gui).items():
                self.summary[key] = value
        elif self.fdm.run.type == 'geometry_only':
            if len(os.listdir(self.main_magnet.geom_folder)) == 1:
                self.main_magnet.generate_geometry()  # needs 3 files (yaml, set, geom)
                self.main_magnet.pre_process(gui=self.main_magnet.fdm.run.launch_gui)
            else:
                self.main_magnet.load_geometry(gui=self.main_magnet.fdm.run.launch_gui)  # needs 2 files (yaml, brep)
        elif self.fdm.run.type == 'mesh_and_solve_with_post_process_python':  # needs 5 files (yaml, strs/map2d, set, brep, aux)
            self.main_magnet.load_geometry()
            for key, value in self.main_magnet.mesh().items():
                self.summary[key] = value
            self.summary['solution_time'] = self.main_magnet.solve_and_postprocess_getdp()
            for key, value in self.main_magnet.post_process_python(gui=self.main_magnet.fdm.run.launch_gui).items():
                self.summary[key] = value
        elif self.fdm.run.type == 'mesh_only':
            if len(os.listdir(self.main_magnet.mesh_folder)) == 1:
                self.main_magnet.load_geometry()  # needs 3 files (yaml, brep, aux)
                for key, value in self.main_magnet.mesh(gui=self.main_magnet.fdm.run.launch_gui).items():
                    self.summary[key] = value
            else:
                self.main_magnet.load_mesh(gui=self.main_magnet.fdm.run.launch_gui)  # needs 2 files (yaml, msh)
        elif self.fdm.run.type == 'solve_with_post_process_python':  # needs 5 files (yaml, strs/map2d, set, msh, reg)
            self.summary['solution_time'] = self.main_magnet.solve_and_postprocess_getdp()
            for key, value in self.main_magnet.post_process_python(gui=self.main_magnet.fdm.run.launch_gui).items():
                self.summary[key] = value
        elif self.fdm.run.type == 'solve_only':  # needs 5 files (yaml, strs/map2d, set, msh, reg)
            self.summary['solution_time'] = self.main_magnet.solve_and_postprocess_getdp(gui=self.main_magnet.fdm.run.launch_gui)
        elif self.fdm.run.type == 'post_process_getdp_only':
            self.main_magnet.post_process_getdp(gui=self.main_magnet.fdm.run.launch_gui)
        elif self.fdm.run.type == 'post_process_python_only':
            for key, value in self.main_magnet.post_process_python(gui=self.main_magnet.fdm.run.launch_gui).items():
                self.summary[key] = value
        elif self.fdm.run.type == 'plot_python':
            self.main_magnet.plot_python()
        os.chdir(self.start_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="FiQuS",
        description="Finite Elements Quench Simulator",
        epilog="steam-team@cern.ch",
    )
    parser.add_argument(
        "--in",
        dest="full_path_input",
        type=str,
        help="Full path to FiQuS input yaml file",
    )
    parser.add_argument(
        "--out", dest="output_path", type=str, help="Full path to FiQuS output folder"
    )
    parser.add_argument(
        "--getdp", dest="GetDP_path", type=str, help="Full path to GetDP executable"
    )
    args = parser.parse_args()
    # print(args.full_path_input)
    # print(args.output_path)
    # print(args.GetDP_path)
    MainFiQuS(
        input_file_path=args.full_path_input,
        model_folder=args.output_path,
        GetDP_path=args.GetDP_path,
    )
    print("FiQuS run completed")