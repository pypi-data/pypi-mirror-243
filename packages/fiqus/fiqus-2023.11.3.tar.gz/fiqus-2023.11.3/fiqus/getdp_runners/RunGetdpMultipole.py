import os
import pathlib

import gmsh

from fiqus.pro_assemblers.ProAssembler import ASS_PRO as aP
from fiqus.utils.Utils import GmshUtils
from fiqus.utils.Utils import FilesAndFolders as Util
from fiqus.data import DataFiQuS as dF
from fiqus.data.RegionsModelFiQuS import RegionsModel as rM


class AssignNaming:
    def __init__(self, data: dF.FDM() = None):
        """
        Class to assign naming convention
        :param data: FiQuS data model
        """
        self.data: dF.FDM() = data

        self.naming_conv = {'omega': 'Omega', 'boundary': 'Bd_', 'powered': '_p', 'induced': '_i', 'air': '_a',
                            'air_far_field': '_aff', 'iron': '_bh', 'conducting': '_c', 'terms': 'Terms'}
        self.data.magnet.postproc.volumes = \
            [self.naming_conv['omega'] + self.naming_conv[var] if not var == 'omega'
             else self.naming_conv['omega'] for var in self.data.magnet.postproc.volumes]


class RunGetdpMultipole:
    def __init__(self, data: AssignNaming = None, sett: dF.FiQuSSettings() = None, solution_folder: str = None,
                 settings: dict = None, verbose: bool = False):
        """
        Class to solve pro file
        :param data: FiQuS data model
        :param sett: settings data model
        :param verbose: If True more information is printed in python console.
        """
        self.data: dF.FDM() = data.data
        self.naming_conv: dict = data.naming_conv
        self.set: dF.FiQuSSettings() = sett
        self.solution_folder = solution_folder
        self.settings = settings
        self.verbose: bool = verbose

        self.rm = rM()

        self.gu = GmshUtils(self.solution_folder, self.verbose)
        self.gu.initialize()
        self.occ = gmsh.model.occ
        self.mesh = gmsh.model.mesh

        self.brep_iron_curves = {1: set(), 2: set(), 3: set(), 4: set()}
        self.mesh_folder = os.path.dirname(self.solution_folder)
        self.model_file = os.path.join(self.solution_folder, 'Center_line.csv')

        self.II = (self.set.Model_Data_GS.general_parameters.I_ref[0] if self.data.magnet.postproc.compare_to_ROXIE
                   else self.data.magnet.solve.I_initial[0])

    def loadRegionFile(self):
        self.rm = Util.read_data_from_yaml(f"{os.path.join(self.mesh_folder, self.data.general.magnet_name)}.reg", rM)

    def assemblePro(self):
        self.rm.powered.vol.currents = []
        for name in self.rm.powered.vol.names:
            if name[-3:] == 'pos':
                self.rm.powered.vol.currents.append(self.II)
            else:
                self.rm.powered.vol.currents.append(-self.II)

        ap = aP(file_base_path=os.path.join(self.solution_folder, self.data.general.magnet_name),
                naming_conv=self.naming_conv)
        BH_curves_path = os.path.join(pathlib.Path(os.path.dirname(__file__)).parent, 'pro_material_functions', 'ironBHcurves.pro')
        ap.assemble_combined_pro(template=self.data.magnet.solve.pro_template, rm=self.rm, dm=self.data.magnet, BH_curves_path=BH_curves_path)

    def solve_and_postprocess(self):
        command = "-solve -v2 -pos"
        self._run(command=command)

    def postprocess(self):
        command = "-v2 -pos"
        self._run(command=command)

    def _run(self, command):
        gmsh.onelab.run(f"{self.data.general.magnet_name}",
                        f"{self.settings['GetDP_path']} "
                        f"{os.path.join(self.solution_folder, self.data.general.magnet_name)}.pro "
                        f"{command} -msh {os.path.join(self.mesh_folder, self.data.general.magnet_name)}.msh")
        gmsh.onelab.setChanged("GetDP", 0)
        # view_tag = gmsh.view.getTags()  # this should be b
        # # # v = "View[" + str(gmsh.view.getIndex('b')) + "]"
        # gmsh.view.write(view_tag, f"{os.path.join(self.solution_folder, self.data.general.magnet_name)}-view.msh")

    def ending_step(self, gui: bool = False):
        if gui:
            self.gu.launch_interactive_GUI()
        else:
            gmsh.clear()
            gmsh.finalize()
