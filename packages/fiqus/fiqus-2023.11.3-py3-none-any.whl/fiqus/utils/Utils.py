import sys
import os
import shutil
import numpy as np
from pathlib import Path
from time import sleep
import multiprocessing
import ruamel.yaml
import warnings
import gmsh
import logging


logger = logging.getLogger(__name__)

class LoggingFormatter(logging.Formatter):
    """
    Logging formatter class
    """
    grey = "\x1b[38;20m" # debug level
    white = "\x1b[37;20m" # info level
    yellow = "\x1b[33;20m" # warning level
    red = "\x1b[31;20m" # error level
    bold_red = "\x1b[31;1m" # critical level

    reset = "\x1b[0m"
    format = '%(asctime)s | %(levelname)s | %(message)s'

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: white + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class FilesAndFolders:
    @staticmethod
    def read_data_from_yaml(full_file_path, data_class):
        with open(full_file_path, 'r') as stream:
            yaml = ruamel.yaml.YAML(typ='safe', pure=True)
            yaml_str = yaml.load(stream)
        return data_class(**yaml_str)

    @staticmethod
    def write_data_to_yaml(full_file_path, dict_of_data_class):
        def my_represent_none(self, data):
            return self.represent_scalar('tag:yaml.org,2002:null', 'null')

        yaml = ruamel.yaml.YAML()
        yaml.default_flow_style = False
        yaml.emitter.alt_null = 'Null'
        yaml.representer.add_representer(type(None), my_represent_none)
        with open(full_file_path, 'w') as yaml_file:
            yaml.dump(dict_of_data_class, yaml_file)

    @staticmethod
    def prep_folder(folder_full_path, clear: bool = False):
        if clear:
            if os.path.exists(folder_full_path):
                shutil.rmtree(folder_full_path)  # delete directory
        if not os.path.exists(folder_full_path):
            os.makedirs(folder_full_path)  # make new directory

    @staticmethod
    def get_folder_path(folder_type, folder, ref_nr, overwrite, required_folder):
        if required_folder and not (ref_nr and overwrite):
            last_nr = 0
            for study in [x.parts[-1] for x in Path(folder).iterdir() if x.is_dir()]:
                last_nr = max(int(study[study.find('_') + 1:]), last_nr)
            if overwrite and required_folder and last_nr > 0:
                run_nr = str(last_nr)
            else:
                run_nr = str(last_nr + 1)
        else:
            run_nr = str(ref_nr)

        folder_path = os.path.join(folder, folder_type + '_' + run_nr)
        FilesAndFolders.prep_folder(folder_path, overwrite and required_folder)
        return folder_path

    @staticmethod
    def get_folder_path(folder_type, folder, folder_key, overwrite, required_folder):
        if required_folder and not (folder_key and overwrite):
            all_dirs = [x.parts[-1] for x in Path(folder).iterdir() if x.is_dir()]
            all_relevant_dirs = [x for x in all_dirs if x.startswith(f"{folder_type}_{folder_key}")]
            if f"{folder_type}_{folder_key}" in all_relevant_dirs:
                new_folder_key = f"{folder_key}_{len(all_relevant_dirs) + 1}"
                folder_key = new_folder_key

        folder_path = os.path.join(folder, folder_type + '_' + str(folder_key))
        # Disable the line below to avoid deleating volder
        FilesAndFolders.prep_folder(folder_path, overwrite and required_folder)
        return folder_path

    @staticmethod
    def compute_folder_key(folder_type, folder, overwrite):
        # Find all the directories in the folder
        all_dirs = [x.parts[-1] for x in Path(folder).iterdir() if x.is_dir()]

        # Find all the directiories that start with the folder_type (e.g. geometry, mesh, solution)
        # Then combine them into a single string with a custom seperator (se@p)
        # Seperators are used to guarantee the directories can be split later
        all_relevant_dirs = " se@p ".join([x for x in all_dirs if x.startswith(f"{folder_type}_")])
        all_relevant_dirs = f"{all_relevant_dirs} se@p "

        # Find all the integer keys in the relevant directories
        integers_in_relevant_dirs = re.findall(rf'{folder_type}_(\d+) se@p ', all_relevant_dirs)

        if integers_in_relevant_dirs is None:
            # If there are no integers in the relevant directories, set the key to 1
            folder_key = 1
        else:
            # Make a list of integers out of the integers in the relevant directories
            integers_in_relevant_dirs = [int(x) for x in integers_in_relevant_dirs]

            # Sort the integers in the relevant directories
            integers_in_relevant_dirs.sort()

            if overwrite:
                # If overwrite is true, set the key to the largest integer in the
                # so that the folder with the largest integer key is overwritten
                if len(integers_in_relevant_dirs) == 0:
                    folder_key = 1
                else:
                    folder_key = max(integers_in_relevant_dirs)
            else:
                # If overwrite is false, then find the smallest integer key that is not
                # in the list of integers in the relevant directories
                folder_key = 1
                for i in integers_in_relevant_dirs:
                    if folder_key < i:
                        break
                    folder_key += 1
        
        return folder_key

    @staticmethod
    def print_welcome_graphics():
        print(r"  _____ _  ___        ____ ")
        print(r"|  ___(_)/ _ \ _   _/ ___| ")
        print(r"| |_  | | | | | | | \___ \ ")
        print(r"|  _| | | |_| | |_| |___) |")
        print(r"|_|   |_|\__\_\\__,_|____/ ")
        print("")


class CheckForExceptions:
    @staticmethod
    def check_inputs(run):  # RunFiQuS()
        if run.type == 'start_from_yaml':
            if run.geometry and not run.overwrite:
                warnings.warn("Warning: Geometry folder is needed only if it has to be overwritten. Ignoring it...")
            if run.solution or run.mesh:
                warnings.warn("Warning: Mesh and Solution folders are not needed. Ignoring them...")
        elif run.type == 'geometry_only':
            if run.solution or run.mesh:
                warnings.warn("Warning: Mesh and Solution folders are not needed. Ignoring them...")
        elif run.type == 'mesh_and_solve_with_post_process':
            if not run.geometry:
                raise Exception('Full path to Geometry not provided. '
                                'Insert options -> reference_files -> geometry.')
            if run.mesh and not run.overwrite:
                warnings.warn("Warning: Mesh folder is needed only if it has to be overwritten. Ignoring it...")
            if run.solution:
                warnings.warn("Warning: Solution folder is not needed. Ignoring it...")
        elif run.type == 'mesh_only':
            if not run.geometry:
                raise Exception('Full path to Mesh not provided. '
                                'Insert options -> reference_files -> geometry.')
            if run.solution:
                warnings.warn("Warning: Solution folder is not needed. Ignoring it...")
        elif run.type == 'solve_with_post_process':
            if not run.mesh or not run.geometry:
                raise Exception('Full path to Mesh not provided. '
                                'Insert options -> reference_files -> geometry and mesh.')
            if run.solution and not run.overwrite:
                warnings.warn("Warning: Solution folder is needed only if it has to be overwritten. Ignoring it...")
        elif run.type == 'solve_only':
            if not run.mesh or not run.geometry:
                raise Exception('Full path to Mesh not provided. '
                                'Insert options -> reference_files -> geometry and mesh.')
            if run.solution and not run.overwrite:
                warnings.warn("Warning: Solution folder is needed only if it has to be overwritten. Ignoring it...")
        elif run.type == 'post_process_only':
            if not run.mesh or not run.geometry or not run.solution:
                raise Exception('Full path to Solution not provided. '
                                'Insert options -> reference_files -> geometry, mesh, and solution.')

    @staticmethod
    def check_overwrite_conditions(folder_type, folder, folder_key):
        if folder_key:
            if not os.path.exists(os.path.join(folder, folder_type + '_' + str(folder_key))):
                warnings.warn(
                    f'The folder {folder_type}_{folder_key} does not exist. Creating it...')
        else:
            warnings.warn(
                f'Reference number of the folder {folder_type} not provided. '
                f'Overwriting the latest {folder_type} folder...')


class GeometricFunctions:

    @staticmethod
    def centroid(X, Y):
        """
            Computes the centroid coordinates of a non-self-intersecting closed polygon
            :param X: list of X coordinate of the vertices
            :param Y: list of y coordinate of the vertices
        """
        sum_A, sum_Cx, sum_Cy = 0, 0, 0
        for i in range(len(X)):
            index = i + 1 if i != len(X) - 1 else 0
            A = X[i] * Y[index] - X[index] * Y[i]
            sum_Cx += (X[i] + X[index]) * A
            sum_Cy += (Y[i] + Y[index]) * A
            sum_A += A
        factor = 1 / (3 * sum_A)
        return [factor * sum_Cx, factor * sum_Cy]

    @staticmethod
    def arc_center_from_3_points(a, b, c):
        """
            Computes the center coordinates of an arc passing through three points
            :param a: DataRoxieParser.Coord class object of one arc point
            :param b: DataRoxieParser.Coord class object of one arc point
            :param c: DataRoxieParser.Coord class object of one arc point
        """
        ab = [a.x - b.x, a.y - b.y]
        ac = [a.x - c.x, a.y - c.y]
        sac = [a.x * a.x - c.x * c.x, a.y * a.y - c.y * c.y]
        sba = [b.x * b.x - a.x * a.x, b.y * b.y - a.y * a.y]
        yy = (sac[0] * ab[0] + sac[1] * ab[0] + sba[0] * ac[0] + sba[1] * ac[0]) / \
             (2 * ((c.y - a.y) * ab[0] - (b.y - a.y) * ac[0]))
        xx = (sac[0] * ab[1] + sac[1] * ab[1] + sba[0] * ac[1] + sba[1] * ac[1]) / \
             (2 * ((c.x - a.x) * ab[1] - (b.x - a.x) * ac[1]))
        return [-xx, -yy]


class GmshUtils:

    def __init__(self, model_name=None, verbose=True):
        self.model_name = model_name
        self.verbose = verbose

    @staticmethod
    def initialize():
        if not gmsh.is_initialized():
            gmsh.initialize(sys.argv)
            num_threads = multiprocessing.cpu_count()
            gmsh.option.setNumber('General.NumThreads', num_threads)  # enable multithreading (this seems to be only for meshing)
            gmsh.option.setNumber('Mesh.MaxNumThreads1D', num_threads)
            gmsh.option.setNumber('Mesh.MaxNumThreads2D', num_threads)
            gmsh.option.setNumber('Mesh.MaxNumThreads3D', num_threads)

            gmsh.option.setNumber('Geometry.ToleranceBoolean', 0.0000001)
            gmsh.option.setNumber('General.Terminal', 1)
            # gmsh.model.add(self.model_name)

    def check_for_event(self):  # pragma: no cover
        action = gmsh.onelab.getString("ONELAB/Action")
        if len(action) and action[0] == "check":
            gmsh.onelab.setString("ONELAB/Action", [""])
            if self.verbose:
                print("-------------------check----------------")
            gmsh.fltk.update()
            gmsh.graphics.draw()
        if len(action) and action[0] == "compute":
            gmsh.onelab.setString("ONELAB/Action", [""])
            if self.verbose:
                print("-------------------compute----------------")
            gmsh.onelab.setChanged("Gmsh", 0)
            gmsh.onelab.setChanged("GetDP", 0)
            gmsh.fltk.update()
            gmsh.graphics.draw()
        return True

    def launch_interactive_GUI(self, close_after=-1):  # pragma: no cover
        gmsh.fltk.initialize()
        while gmsh.fltk.isAvailable() and self.check_for_event():
            gmsh.fltk.wait()
            if close_after >= 0:
                sleep(close_after)
                gmsh.fltk.finalize()
        gmsh.finalize()


class RoxieParsers:
    def __init__(self, conductor, block, xyCorner):
        self.conductor = conductor
        self.block = block
        self.xyCorner = xyCorner

    @staticmethod
    def parseMap2d(map2dFile: Path, headerLines: int = 1):
        """
            Generates array-stream of values of map2dFile
            :param map2dFile: path of map2dFile containing the content to parse
            :param headerLines: which index the header line is at - will start to read after that
        """
        # Open map2dfile
        fileContent = open(map2dFile, "r").read()
        # Split content of file in rows
        fileContentByRow = fileContent.split("\n")
        # Create array-matrix to fill in with the values of the file
        output_matrix = np.array([[None for x in range(10)] for y in range(headerLines + 1, len(fileContentByRow) - 1)],
                                 dtype=float)

        # Assign values to the matrix row by row
        for index, rowContent in enumerate(fileContentByRow):
            if index > headerLines and rowContent:  # without header
                row = rowContent.split()
                output_array = np.array([])  # create temp. array
                output_array = np.append(output_array, int(row[0]))  # strands to groups
                output_array = np.append(output_array, int(row[1]))  # strands to halfturn
                output_array = np.append(output_array, float(row[2]))  # idx
                output_array = np.append(output_array, float(row[3]) / 1e3)  # x_strands in [m]
                output_array = np.append(output_array, float(row[4]) / 1e3)  # y_strands in [m]
                output_array = np.append(output_array, float(row[5]))  # Bx
                output_array = np.append(output_array, float(row[6]))  # By
                output_array = np.append(output_array, float(row[7]) / 1e6)  # Area in [m^2]
                output_array = np.append(output_array, float(row[8]))  # I_strands
                output_array = np.append(output_array, float(row[9]))  # fill factor
                output_matrix[index - headerLines - 1] = output_array  # assign into matrix
        return output_matrix

    @staticmethod
    def parseCond2d(cond2dFile: Path):
        """
            Read input file and return list of ConductorPosition objects

            # input: fileName
            # output: conductorPositionsList

        """
        # conductorStartKeyword = "CONDUCTOR POSITION IN THE CROSS-SECTION"
        blockStartKeyword = "BLOCK POSITION IN THE CROSS-SECTION"

        fileContent = open(cond2dFile, "r").read()

        # separate rows
        fileContentByRow = fileContent.split("\n")

        # Find block definition
        for i in range(len(fileContentByRow)):
            if blockStartKeyword in fileContentByRow[i]:
                startOfBlockDefinitionIndex = i

        # separate part of the data with conductor position information
        conductorPositions = fileContentByRow[5:startOfBlockDefinitionIndex - 2]

        # drop every 5th row
        conductorPositionsFourVertices = list(conductorPositions)
        del conductorPositionsFourVertices[4::5]

        # arrange data in a list of lists
        outputConductorPositions = []
        for row in conductorPositionsFourVertices:
            rowSplitStr = row.split(',')
            rowSplitFloat = [float(elem) for elem in rowSplitStr]
            outputConductorPositions.append(rowSplitFloat)

        # arrange data from list to numpy.array
        outputConductorPositionsMatrix = np.array(outputConductorPositions)

        # input: outputConductorPositions
        # output: conductorPositionsList
        conductorPositionsList = []
        for i in range(0, len(outputConductorPositions), 4):
            out = outputConductorPositions[i]
            conductor = int(out[1])
            block = int(out[2])
            xyCorner = outputConductorPositionsMatrix[i:i + 4, 4:6]
            conductorPositionsList.append(RoxieParsers(conductor, block, xyCorner))

        return conductorPositionsList

def initialize_logger(verbose: bool = True, work_folder: str = None, time_stamp: str = None):
    logger = logging.getLogger()

    if verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    for handler in logger.handlers:
        logger.handlers.remove(handler)
        handler.close()
    
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(LoggingFormatter())
    logger.addHandler(stdout_handler)

    FilesAndFolders.prep_folder(work_folder)
    FilesAndFolders.prep_folder(os.path.join(work_folder, "logs"))
    file_handler = logging.FileHandler(os.path.join(work_folder, "logs", f"{time_stamp}.FiQuS.log"))
    file_handler.setLevel(logging.INFO)
    fileFormatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler.setFormatter(fileFormatter)
    logger.addHandler(file_handler)

    errorsAndWarnings_file_handler = logging.FileHandler(os.path.join(work_folder, "logs", f"ERRORS_WARNINGS_{time_stamp}.FiQuS.log"))
    errorsAndWarnings_file_handler.setLevel(logging.WARNING)
    errorsAndWarnings_file_handler.setFormatter(fileFormatter)
    logger.addHandler(errorsAndWarnings_file_handler)

    return logger
