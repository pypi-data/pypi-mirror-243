import os
import timeit
import logging
import subprocess
import re

import gmsh

from fiqus.utils.Utils import FilesAndFolders
from fiqus.utils.Utils import GmshUtils
from fiqus.data.RegionsModelFiQuS import RegionsModel
from fiqus.pro_assemblers.ProAssembler import ASS_PRO as ass_pro
from fiqus.mains.MainPancake3D import Base
from fiqus.data.DataFiQuSPancake3D import Pancake3DGeometry, Pancake3DMesh
from fiqus.parsers.ParserRES import ParserRES

logger = logging.getLogger(__name__)


class Solve(Base):
    """
    Main class to run GetDP for Pancake3D.

    :param fdm: FiQuS data model
    :param GetDP_path: Settings for GetDP
    :type GetDP_path: dict
    """

    def __init__(
        self,
        fdm,
        GetDP_path: str = None,
        geom_folder=None,
        mesh_folder=None,
        solution_folder=None,
    ) -> None:
        super().__init__(fdm, geom_folder, mesh_folder, solution_folder)

        self.GetDP_path = GetDP_path  # Some settings for GetDP
        # check for init from res file option
        if self.dm.magnet.solve.initFromPrevious:
            self.res_file_path = os.path.join(
                self.mesh_folder,
                f"Solution_{self.dm.magnet.solve.initFromPrevious}",
                self.magnet_name + ".res",
            )

            if not os.path.isfile(self.res_file_path):
                raise ValueError(f"Res file {self.res_file_path} does not exist.")
            else:
                if self.dm.run.type not in ["solve_only", "solve_with_post_process_python"]:
                    raise ValueError(
                        f"Run type should be solve only for init from res file option."
                    )

                if self.dm.magnet.solve.type == "weaklyCoupled":
                    _no_of_previous_solutions = 2
                else:
                    _no_of_previous_solutions = 1

                logger.info(
                    f"Initializing from previous solution {self.res_file_path}."
                )

                # parse given res file
                parsed_init_res = ParserRES(self.res_file_path)

                # remove all but no_of_previous_solutions
                parsed_init_res.solution["time_real"] = parsed_init_res.solution[
                    "time_real"
                ][-_no_of_previous_solutions:]
                parsed_init_res.solution["time_imag"] = parsed_init_res.solution[
                    "time_imag"
                ][-_no_of_previous_solutions:]
                parsed_init_res.solution["time_step"] = parsed_init_res.solution[
                    "time_step"
                ][-_no_of_previous_solutions:]
                parsed_init_res.solution["dof_data"] = parsed_init_res.solution[
                    "dof_data"
                ][-_no_of_previous_solutions:]
                parsed_init_res.solution["solution"] = parsed_init_res.solution[
                    "solution"
                ][-_no_of_previous_solutions:]

                self.res_file_without_previous_solutions = os.path.join(
                    self.solution_folder, self.magnet_name + ".res"
                )
                ParserRES(self.res_file_without_previous_solutions, parsed_init_res)

        # Create pro file:
        self.ap = ass_pro(os.path.join(self.solution_folder, self.magnet_name))

        # Start GMSH:
        self.gu = GmshUtils(self.mesh_folder)
        self.gu.initialize()

        # Read regions model:
        self.rm = FilesAndFolders.read_data_from_yaml(self.regions_file, RegionsModel)

        # Check if the geometry data and mesh data has not been altered after they are
        # created:
        previousGeo = FilesAndFolders.read_data_from_yaml(
            self.geometry_data_file, Pancake3DGeometry
        )
        previousMesh = FilesAndFolders.read_data_from_yaml(
            self.mesh_data_file, Pancake3DMesh
        )

        if previousGeo.dict() != self.geo.dict():
            raise ValueError(
                "Geometry data has been changed. Please regenerate the geometry or load"
                " the previous geometry data."
            )
        elif previousMesh.dict() != self.mesh.dict():
            raise ValueError(
                "Mesh data has been changed. Please regenerate the mesh or load the"
                " previous mesh data."
            )

    def assemble_pro(self):
        logger.info(f"Assembling pro file ({self.pro_file}) has been started.")
        start_time = timeit.default_timer()

        self.ap.assemble_combined_pro(
            template=self.solve.proTemplate,
            rm=self.rm,
            dm=self.dm,
        )

        logger.info(
            f"Assembling pro file ({self.pro_file}) has been finished in"
            f" {timeit.default_timer() - start_time:.2f} s."
        )

    def run_getdp(self, solve=True, postOperation=True):
        logger.info("Solving Pancake3D magnet has been started.")
        start_time = timeit.default_timer()

        getdpArguments = ["-v2", "-mat_mumps_cntl_1", "0", "-verbose", "6"]

        if self.dm.magnet.solve.initFromPrevious:
            getdpArguments.extend(
                ["-restart", "-res", str(self.res_file_without_previous_solutions)]
            )

        # Add solve argument
        if solve:
            getdpArguments.extend(["-solve", f"RESOLUTION_{self.solve.type}"])

        # Add post operation argument
        if postOperation:
            posStringList = ["-pos"]
            if solve is False:
                # Quantities to be saved:
                if self.dm.magnet.solve.save is not None:
                    for quantity in self.dm.magnet.solve.save:
                        posStringList.append(f"{quantity.getdpPostOperationName}")

                if self.dm.magnet.postproc is not None:
                    if self.dm.magnet.postproc.timeSeriesPlots is not None:
                        # Post-operations for Python post-processing:
                        for timeSeriesPlot in self.dm.magnet.postproc.timeSeriesPlots:
                            posStringList.append(
                                f"POSTOP_timeSeriesPlot_{timeSeriesPlot.quantity}"
                            )

                    if self.dm.magnet.postproc.magneticFieldOnCutPlane is not None:
                        # Post-operations for Python post-processing:
                        posStringList.append("POSTOP_magneticFieldOnCutPlaneVector")
                        posStringList.append("POSTOP_magneticFieldOnCutPlaneMagnitude")

            else:
                posStringList.append("POSTOP_dummy")
            getdpArguments.extend(posStringList)

        # Add mesh argument
        getdpArguments.extend(["-msh", f"{self.mesh_file}"])

        # Add pre-processing argument
        getdpArguments.extend(["-pre", f"RESOLUTION_{self.solve.type}"])

        getdp_binary = self.GetDP_path

        getdpProcess = subprocess.Popen(
            [getdp_binary, self.pro_file] + getdpArguments,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        with getdpProcess.stdout:
            for line in iter(getdpProcess.stdout.readline, b""):
                line = line.decode("utf-8").rstrip()
                line = line.split("\r")[-1]
                if "Info" in line:
                    parsedLine = re.sub(r"Info\s*:\s*", "", line)
                    logger.info(parsedLine)
                elif "Warning" in line:
                    parsedLine = re.sub(r"Warning\s*:\s*", "", line)
                    if "Unknown" not in parsedLine:
                        logger.warning(parsedLine)
                elif "Error" in line:
                    parsedLine = re.sub(r"Error\s*:\s*", "", line)
                    logger.error(parsedLine)
                    logger.error("Solving Pancake3D magnet has failed.")
                    raise Exception(parsedLine)
                elif "Critical" in line:
                    parsedLine = re.sub(r"Critical\s*:\s*", "", line)
                    if "Quench started!" in parsedLine:
                        logger.critical(r" _____ _  ___        ____ ")
                        logger.critical(r"|  ___(_)/ _ \ _   _/ ___| ")
                        logger.critical(r"| |_  | | | | | | | \___ \ ")
                        logger.critical(r"|  _| | | |_| | |_| |___) |")
                        logger.critical(r"|_|   |_|\__\_\\__,_|____/ ")
                        logger.critical("")
                        logger.critical("The coil has been quenched!")
                    else:
                        logger.critical(parsedLine)
                # else:
                #     logger.info(line)

        getdpProcess.wait()

        logger.info(
            "Solving Pancake3D magnet has been finished in"
            f" {timeit.default_timer() - start_time:.2f} s."
        )

        if self.solve_gui:
            gmsh.option.setNumber("Geometry.Volumes", 0)
            gmsh.option.setNumber("Geometry.Surfaces", 0)
            gmsh.option.setNumber("Geometry.Curves", 0)
            gmsh.option.setNumber("Geometry.Points", 0)
            posFiles = [
                fileName
                for fileName in os.listdir(self.solution_folder)
                if fileName.endswith(".pos")
            ]
            for posFile in posFiles:
                gmsh.open(os.path.join(self.solution_folder, posFile))
            self.gu.launch_interactive_GUI()
        else:
            gmsh.clear()
            gmsh.finalize()
