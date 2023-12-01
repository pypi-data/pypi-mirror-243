import os
import sys
import time

from fiqus.data.DataFiQuSPancake3D import (
    Pancake3DGeometry,
    Pancake3DMesh,
    Pancake3DSolve,
    Pancake3DPostprocess,
)

if len(sys.argv) == 3:
    sys.path.insert(0, os.path.join(os.getcwd(), "steam-fiqus-dev"))


class Base:
    """
    Base class for geometry, mesh, and solution classes. It is created to avoid code
    duplication and to make the code more readable. Moreover, it guarantees that
    all the classes have the same fundamental methods and attributes.
    """

    def __init__(
        self,
        fdm,
        geom_folder=None,
        mesh_folder=None,
        solution_folder=None,
    ) -> None:
        """
        Define the fundamental attributes of the class.

        :param fdm: fiqus data model
        :param geom_folder: folder where the geometry related files are stored
        :type geom_folder: str
        :param mesh_folder: folder where the mesh related files are stored
        :type mesh_folder: str
        :param solution_folder: folder where the solution related files are stored
        :type solution_folder: str
        """

        self.magnet_name = fdm.general.magnet_name
        self.geom_folder = geom_folder
        self.mesh_folder = mesh_folder
        self.solution_folder = solution_folder

        self.dm = fdm  # Data model
        self.geo: Pancake3DGeometry = fdm.magnet.geometry  # Geometry data
        self.mesh: Pancake3DMesh = fdm.magnet.mesh  # Mesh data
        self.solve: Pancake3DSolve = fdm.magnet.solve  # Solve data
        self.pp: Pancake3DPostprocess = fdm.magnet.postproc  # Postprocess data

        self.geo_gui = False
        self.mesh_gui = False
        self.solve_gui = False
        self.python_postprocess_gui = False

        if fdm.run.launch_gui:
            if fdm.run.type == "start_from_yaml":
                self.python_postprocess_gui = True
            elif fdm.run.type == "geometry_only":
                self.geo_gui = True
            elif fdm.run.type == "mesh_only":
                self.mesh_gui = True
            elif fdm.run.type == "geometry_and_mesh":
                self.mesh_gui = True
            elif fdm.run.type == "solve_only":
                self.solve_gui = True
            elif fdm.run.type == "post_process_getdp_only":
                self.solve_gui = True
            elif fdm.run.type == "solve_with_post_process_python":
                self.python_postprocess_gui = True
            elif fdm.run.type == "post_process_python_only":
                self.python_postprocess_gui = True

        # Geometry related files:
        if self.geom_folder is not None:
            self.brep_file = os.path.join(self.geom_folder, f"{self.magnet_name}.brep")
            self.vi_file = os.path.join(self.geom_folder, f"{self.magnet_name}.vi")
            self.geometry_data_file = os.path.join(self.geom_folder, "geometry.yaml")

        # Mesh related files:
        if self.mesh_folder is not None:
            self.mesh_file = os.path.join(self.mesh_folder, f"{self.magnet_name}.msh")
            self.regions_file = os.path.join(
                self.mesh_folder, f"{self.magnet_name}.regions"
            )
            self.mesh_data_file = os.path.join(self.mesh_folder, "mesh.yaml")
        # Solution related files:
        if self.solution_folder is not None:
            self.pro_file = os.path.join(
                self.solution_folder, f"{self.magnet_name}.pro"
            )


from fiqus.geom_generators.GeometryPancake3D import Geometry
from fiqus.mesh_generators.MeshPancake3D import Mesh
from fiqus.getdp_runners.RunGetdpPancake3D import Solve
from fiqus.post_processors.PostProcessPancake3D import Postprocess


class MainPancake3D:
    """
    The main class for working with simulations for high-temperature superconductor
    pancake coil magnets.

    Geometry can be created and saved as a BREP file. Parameters like the number of
    turns, tape dimensions, contact layer thicknesses, and other dimensions can be
    specified. Contact layers can be modeled as two-dimensional shells or three-dimensional
    volumes. Moreover, multiple pancakes can be stacked on top of each other.

    Using the BREP file created, a mesh can be generated and saved as an MSH file.
    Winding mesh can be structured, and parameters like, azimuthal number of elements
    per turn, axial number of elements, and radial number of elements per turn can be
    specified for each pancake coil. The appropriate regions will be assigned to the
    relevant volumes accordingly so that finite element simulations can be done.

    Using the mesh files, GetDP can be used to analyze Pancake3D coils.

    :param fdm: FiQuS data model
    """

    def __init__(self, fdm, verbose):
        self.fdm = fdm
        self.GetDP_path = None

        self.geom_folder = None
        self.mesh_folder = None
        self.solution_folder = None

    def generate_geometry(self, gui=False):
        """
        Generates the geometry of the magnet and save it as a BREP file. Moreover, a
        text file with the extension VI (volume information file) is generated, which
        stores the names of the volume tags in JSON format.
        """
        geometry = Geometry(
            self.fdm,
            self.geom_folder,
            self.mesh_folder,
            self.solution_folder,
        )

        geometry.generate_geometry()
        geometry.generate_vi_file()

        self.model_file = geometry.brep_file

    def load_geometry(self, gui=False):
        """
        Loads the previously generated geometry from the BREP file.
        """
        geometry = Geometry(
            self.fdm,
            self.geom_folder,
            self.mesh_folder,
            self.solution_folder,
        )

        geometry.load_geometry()
        self.model_file = geometry.brep_file

    def pre_process(self, gui=False):
        pass

    def mesh(self, gui=False):
        """
        Generates the mesh of the magnet, creates the physical regions, and saves it as
        an MSH file. Moreover, a text file with the extension REGIONS is generated,
        which stores the names and tags of the physical regions in YAML format.
        """
        mesh = Mesh(
            self.fdm,
            self.geom_folder,
            self.mesh_folder,
            self.solution_folder,
        )

        mesh.generate_mesh()
        mesh.generate_regions()
        mesh.generate_mesh_file()

        self.model_file = mesh.mesh_file

        return {"gamma": 0}  # to be modified with mesh_parameters (see multipole)

    def load_mesh(self, gui=False):
        """
        Loads the previously generated mesh from the MSH file.
        """
        mesh = Mesh(
            self.fdm,
            self.geom_folder,
            self.mesh_folder,
            self.solution_folder,
        )
        mesh.load_mesh()

        self.model_file = mesh.mesh_file

    def solve_and_postprocess_getdp(self, gui=False):
        """
        Simulates the Pancake3D magnet with GetDP using the created mesh file and post
        processes the results.
        """
        solve = Solve(
            self.fdm,
            self.GetDP_path,
            self.geom_folder,
            self.mesh_folder,
            self.solution_folder,
        )
        solve.assemble_pro()

        start_time = time.time()
        solve.run_getdp(solve=True, postOperation=True)

        return time.time() - start_time

    def post_process_getdp(self, gui=False):
        solve = Solve(
            self.fdm,
            self.GetDP_path,
            self.geom_folder,
            self.mesh_folder,
            self.solution_folder,
        )
        solve.assemble_pro()

        start_time = time.time()
        solve.run_getdp(solve=False, postOperation=True)

        return time.time() - start_time

    def post_process_python(self, gui=False):
        """
        To be written.
        """
        postprocess = Postprocess(
            self.fdm,
            self.geom_folder,
            self.mesh_folder,
            self.solution_folder,
        )

        if self.fdm.magnet.postproc is not None:
            if self.fdm.magnet.postproc.timeSeriesPlots is not None:
                postprocess.plotTimeSeriesPlots()
            if self.fdm.magnet.postproc.magneticFieldOnCutPlane is not None:
                postprocess.plotMagneticFieldOnCutPlane()

        return {"overall_error": 0}

    def plot_python(self):
        pass
