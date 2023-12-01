import os
import gmsh
import time

from fiqus.utils.Utils import GmshUtils
from fiqus.utils.Utils import FilesAndFolders as Util
from fiqus.data import DataFiQuS as dF
from fiqus.geom_generators.GeometryMultipole import Geometry
from fiqus.mesh_generators.MeshMultipole import Mesh
from fiqus.getdp_runners.RunGetdpMultipole import RunGetdpMultipole
from fiqus.getdp_runners.RunGetdpMultipole import AssignNaming
from fiqus.post_processors.PostProcessMultipole import PostProcess
from fiqus.plotters.PlotPythonMultipole import PlotPythonMultipole


class MainMultipole:
    def __init__(self, fdm: dF.FDM = None, sdm: dF.FiQuSSettings = None, rgd_path: str = None,
                 verbose: bool = None):
        """
        Main class for working with simulations for multipole type magnets
        :param fdm: FiQuS data model
        :param rgd_path: ROXIE geometry data path
        :param sdm: settings data model
        :param verbose: if True, more info is printed in the console
        """
        self.fdm = fdm
        self.sett = sdm
        self.rgd = rgd_path
        self.verbose = verbose

        self.settings = None
        self.geom_folder = None
        self.mesh_folder = None
        self.solution_folder = None
        self.model_file = None

    def generate_geometry(self, gui: bool = False):
        geom = Util.read_data_from_yaml(self.rgd, dF.FiQuSGeometry)
        gg = Geometry(data=self.fdm, geom=geom, sett=self.sett, geom_folder=self.geom_folder, verbose=self.verbose)
        self.model_file = gg.model_file
        gg.saveStrandPositions()
        if self.fdm.magnet.geometry.with_iron_yoke:
            gg.constructIronGeometry()
        gg.constructWedgeGeometry()
        gg.constructCoilGeometry()
        gg.buildDomains()
        gg.saveBoundaryRepresentationFile()
        gg.loadBoundaryRepresentationFile()
        gg.updateTags()
        gg.saveAuxiliaryFile()
        gg.ending_step(gui)

    def load_geometry(self, gui: bool = False):
        gu = GmshUtils(self.geom_folder, self.verbose)
        gu.initialize()
        self.model_file = f"{os.path.join(self.geom_folder, self.fdm.general.magnet_name)}.brep"
        gmsh.option.setString('Geometry.OCCTargetUnit', 'M')  # set units to meters
        gmsh.open(self.model_file)
        if gui:
            gu.launch_interactive_GUI()

    def pre_process(self, gui: bool = False):
        pass

    def mesh(self, gui: bool = False):
        mm = Mesh(data=self.fdm, sett=self.sett, mesh_folder=self.mesh_folder, verbose=self.verbose)
        self.model_file = mm.model_file
        mm.loadAuxiliaryFile()
        mm.getIronCurvesTags()
        mm.defineMesh()
        mm.fragment()
        mm.createPhysicalGroups()
        mm.updateAuxiliaryFile()
        mm.assignRegionsTags()
        mm.saveRegionFile()
        mm.setMeshOptions()
        mm.generateMesh()
        mm.checkMeshQuality()
        mm.saveMeshFile()
        mm.ending_step(gui)
        return mm.mesh_parameters

    def load_mesh(self, gui: bool = False):
        gu = GmshUtils(self.geom_folder, self.verbose)
        gu.initialize()
        self.model_file = f"{os.path.join(self.mesh_folder, self.fdm.general.magnet_name)}.msh"
        gmsh.open(self.model_file)
        if gui:
            gu.launch_interactive_GUI()

    def solve_and_postprocess_getdp(self, gui: bool = False):
        an = AssignNaming(data=self.fdm)
        rg = RunGetdpMultipole(data=an, sett=self.sett, solution_folder=self.solution_folder, settings=self.settings,
                               verbose=self.verbose)
        self.model_file = rg.model_file
        rg.loadRegionFile()
        rg.assemblePro()
        start_time = time.time()
        rg.solve_and_postprocess()
        rg.ending_step(gui)
        return time.time() - start_time

    def post_process_getdp(self, gui: bool = False):
        an = AssignNaming(data=self.fdm)
        rg = RunGetdpMultipole(data=an, sett=self.sett, solution_folder=self.solution_folder, settings=self.settings,
                               verbose=self.verbose)
        self.model_file = rg.model_file
        rg.loadRegionFile()
        rg.assemblePro()
        rg.postprocess()
        rg.ending_step(gui)

    def post_process_python(self, gui: bool = False):
        if self.fdm.run.type == 'post_process_python_only':
            an = AssignNaming(data=self.fdm)
            data = an.data
        else:
            data = self.fdm
        pp = PostProcess(data=data, sett=self.sett, solution_folder=self.solution_folder, verbose=self.verbose)
        self.model_file = pp.model_file
        pp.loadStrandPositions()
        if self.fdm.magnet.postproc.plot_all:
            pp.loadHalfTurnCornerPositions()
        pp.postProcess()
        pp.ending_step(gui)
        return pp.postprocess_parameters

    def plot_python(self):
        os.chdir(self.solution_folder)
        p = PlotPythonMultipole(self.fdm)
        p.dummy_plot_func()