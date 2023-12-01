import os
from pathlib import Path
import gmsh
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines

from fiqus.utils.Utils import GmshUtils
from fiqus.utils.Utils import GeometricFunctions as Func
from fiqus.utils.Utils import RoxieParsers as Pars
from fiqus.data import DataFiQuS as dF


class PostProcess:
    def __init__(self, data: dF.FDM() = None, sett: dF.FiQuSSettings() = None, solution_folder: str = None,
                 verbose: bool = False):
        """
        Class to post process results
        :param data: FiQuS data model
        :param sett: settings data model
        :param verbose: If True more information is printed in python console.
        """
        self.data: dF.FDM() = data
        self.set: dF.FiQuSSettings() = sett
        self.solution_folder = solution_folder
        self.verbose: bool = verbose

        self.gu = GmshUtils(self.solution_folder, self.verbose)
        self.gu.initialize()

        self.brep_iron_curves = {1: set(), 2: set(), 3: set(), 4: set()}
        self.strands = None
        self.crns = None
        self.BB_err_mean = []
        self.BB_err_min = []
        self.BB_err_max = []
        self.postprocess_parameters = dict.fromkeys(['overall_error', 'minimum_diff', 'maximum_diff'])
        self.geom_folder = os.path.dirname(os.path.dirname(self.solution_folder))
        self.model_file = f"{os.path.join(self.solution_folder, self.data.general.magnet_name)}.map2d"

        self.II = (self.set.Model_Data_GS.general_parameters.I_ref[0] if self.data.magnet.postproc.compare_to_ROXIE
                   else self.data.magnet.solve.I_initial[0])

        if self.data.magnet.postproc.plot_all != 'False':
            self.fiqus = None
            self.roxie = None
            plt.figure(1)
            self.ax = plt.axes()
            self.ax.set_xlabel('x [m]')
            self.ax.set_ylabel('y [m]')
            self.ax.set_xlim(0, 0.09)
            self.ax.set_ylim(0, 0.04)

            if self.data.magnet.postproc.compare_to_ROXIE:
                fig2 = plt.figure(2)
                self.ax2 = fig2.add_subplot(projection='3d')
                self.ax2.set_xlabel('x [m]')
                self.ax2.set_ylabel('y [m]')
                self.ax2.set_zlabel('Absolute Error [T]')
                self.fig4 = plt.figure(4)
                self.ax4 = plt.axes()
                self.ax4.set_xlabel('x [cm]')
                self.ax4.set_ylabel('y [cm]')
                self.ax4.set_aspect('equal', 'box')
            fig3 = plt.figure(3)
            self.ax3 = fig3.add_subplot(projection='3d')
            self.ax3.set_xlabel('x [m]')
            self.ax3.set_ylabel('y [m]')
            self.ax3.set_zlabel('norm(B) [T]')

        name = 'b_Omega_p'
        gmsh.open(os.path.join(self.solution_folder, f"{name}.pos"))

    def ending_step(self, gui: bool = False):
        if gui:
            self.gu.launch_interactive_GUI()
        else:
            gmsh.clear()
            gmsh.finalize()

    def loadStrandPositions(self):
        self.strands = json.load(open(f"{os.path.join(self.geom_folder, self.data.general.magnet_name)}.strs"))

    def loadHalfTurnCornerPositions(self):
        self.crns = json.load(open(f"{os.path.join(self.geom_folder, self.data.general.magnet_name)}.crns"))

    def plotHalfTurnGeometry(self):
        for i in range(len(self.crns['iL'])):
            self.ax.add_line(lines.Line2D([self.crns['iL'][i][0], self.crns['iR'][i][0]],
                                          [self.crns['iL'][i][1], self.crns['iR'][i][1]], color='green'))
            self.ax.add_line(lines.Line2D([self.crns['oL'][i][0], self.crns['oR'][i][0]],
                                          [self.crns['oL'][i][1], self.crns['oR'][i][1]], color='green'))
            self.ax.add_line(lines.Line2D([self.crns['oR'][i][0], self.crns['iR'][i][0]],
                                          [self.crns['oR'][i][1], self.crns['iR'][i][1]], color='green'))
            self.ax.add_line(lines.Line2D([self.crns['iL'][i][0], self.crns['oL'][i][0]],
                                          [self.crns['iL'][i][1], self.crns['oL'][i][1]], color='green'))
            cc_fiqus = Func.centroid([self.crns['iL'][i][0], self.crns['iR'][i][0],
                                      self.crns['oR'][i][0], self.crns['oL'][i][0]],
                                     [self.crns['iL'][i][1], self.crns['iR'][i][1],
                                      self.crns['oR'][i][1], self.crns['oL'][i][1]])

            if self.data.magnet.postproc.compare_to_ROXIE:
                self.ax.add_line(lines.Line2D([self.crns['iLr'][i][0], self.crns['iRr'][i][0]],
                                              [self.crns['iLr'][i][1], self.crns['iRr'][i][1]],
                                              color='red', linestyle='dashed'))
                self.ax.add_line(lines.Line2D([self.crns['oLr'][i][0], self.crns['oRr'][i][0]],
                                              [self.crns['oLr'][i][1], self.crns['oRr'][i][1]],
                                              color='red', linestyle='dashed'))
                self.ax.add_line(lines.Line2D([self.crns['oRr'][i][0], self.crns['iRr'][i][0]],
                                              [self.crns['oRr'][i][1], self.crns['iRr'][i][1]],
                                              color='red', linestyle='dashed'))
                self.ax.add_line(lines.Line2D([self.crns['iLr'][i][0], self.crns['oLr'][i][0]],
                                              [self.crns['iLr'][i][1], self.crns['oLr'][i][1]],
                                              color='red', linestyle='dashed'))
                cc_roxie = Func.centroid(
                    [self.crns['iLr'][i][0], self.crns['iRr'][i][0], self.crns['oRr'][i][0], self.crns['oLr'][i][0]],
                    [self.crns['iLr'][i][1], self.crns['iRr'][i][1], self.crns['oRr'][i][1], self.crns['oLr'][i][1]])

        self.fiqus = self.ax.scatter(cc_fiqus[0], cc_fiqus[1], c="green")
        if self.data.magnet.postproc.compare_to_ROXIE:
            self.roxie = self.ax.scatter(cc_roxie[0], cc_roxie[1], edgecolor='r', facecolor='none')

    def postProcess(self):
        def _printState(bb):
            perc = round(bb / blocks_nr * 100)
            print("Info    : [" + f"{' ' if perc < 10 else ''}" + f"{' ' if perc < 100 else ''}" + f"{perc}" +
                  "%] Interpolating within block" + f"{str(bb)}")

        def _fetchRoxieData():
            roxie_x.append(matrix[row, 3])
            roxie_y.append(matrix[row, 4])
            strands_area.append(matrix[row, 7])
            BB_roxie_x.append(matrix[row, 5])
            BB_roxie_y.append(matrix[row, 6])
            BB_roxie.append(np.linalg.norm(np.array([matrix[row, 5], matrix[row, 6]])))

        def _probeFromView():
            BB_x = []
            BB_y = []
            BB = []
            b_list = [b for b, field in enumerate(self.data.magnet.postproc.variables) if field == 'b']
            if not b_list:
                raise Exception("The interpolation of the field at the strands locations can not be executed: "
                                "the field 'b' is not listed in 'post_processors' -> 'variables'")
            b_field_index = 0
            while self.data.magnet.postproc.volumes[b_list[b_field_index]] != 'Omega_p':
                b_field_index += 1
            # self.data.magnet.post_proc.variables.index('b')
            for ss in range(len(strands_x)):
                probe_data = gmsh.view.probe(gmsh.view.getTags()[0] if len(b_list) == 1 else b_list[b_field_index],
                                             strands_x[ss], strands_y[ss], 0)[0]
                BB_x.append(probe_data[0])
                BB_y.append(probe_data[1])
                BB.append(np.linalg.norm(np.array([BB_x[-1], BB_y[-1]])))
            return BB_x, BB_y, BB

        def _updateMap2dFile(blk_nr, ht_nr):
            with open(self.model_file, 'a') as f:
                content = []
                s = row - strands
                for x, y, Bx, By in zip(strands_x, strands_y, BB_strands_x, BB_strands_y):
                    s += 1
                    content.append(f"     {blk_nr}     {ht_nr}      {s}      {x * 1e3:.4f}       "
                                   f"{y * 1e3:.4f}    {Bx:.4f}    {By:.4f}     {1.0}   "
                                   f"{self.II / strands:.2f}  {1.0}\n")
                f.writelines(content)

        def _computeError():
            BB_err = BB_strands - np.array(BB_roxie)
            self.BB_err_mean.append(np.mean(abs(BB_err)))
            self.BB_err_min.append(np.min(abs(BB_err)))
            self.BB_err_min.append(np.max(abs(BB_err)))
            return BB_err

        def _plotData():
            map2d = None
            pos_roxie = None
            if self.data.magnet.postproc.compare_to_ROXIE:
                map2d = self.ax.scatter(roxie_x, roxie_y, edgecolor='black', facecolor='black', s=10)
                corners = conductorPositionsList[c + cond_nr].xyCorner
                for corner in range(len(corners)):
                    self.ax.scatter(corners[corner][0] / 1e3, corners[corner][1] / 1e3, edgecolor='black',
                                    facecolor='black', s=10)
                if flag_contraction:
                    self.ax.scatter([x * (1 - 0.002) for x in parser_x],
                                    [y * (1 - 0.002) for y in parser_y], c='r', s=10)
                else:
                    self.ax.scatter(parser_x, parser_y, c='r', s=10)
                self.ax2.scatter3D(roxie_x, roxie_y, BB_abs_err, c=BB_abs_err, cmap='viridis')  # , vmin=-0.2, vmax=0.2)
                self.ax4.scatter(np.array(roxie_x) * 1e2, np.array(roxie_y) * 1e2, s=1, c=np.array(BB_abs_err) * 1e3, cmap='viridis')
                pos_roxie = self.ax3.scatter3D(roxie_x, roxie_y, BB_roxie, c=BB_roxie, cmap='Reds', vmin=0, vmax=10)
            pos = self.ax3.scatter3D(strands_x, strands_y, BB_strands, c=BB_strands, cmap='Greens', vmin=0, vmax=10)
            return map2d, pos_roxie, pos

        print(f"Info    : {self.data.general.magnet_name} - I n t e r p o l a t i n g . . .")
        print("Info    : Interpolating magnetic flux density ...")

        if self.data.magnet.postproc.compare_to_ROXIE:
            roxie_path = self.data.magnet.postproc.compare_to_ROXIE  # f"C:\\Users\\avitrano\\PycharmProjects\\steam_sdk\\tests\\builders\\model_library\\magnets\\{self.data.general.magnet_name}\\input"
            flag_contraction = False
            # flag_self_field = False
            path_map2d = Path(roxie_path)
            # path_map2d = Path(roxie_path, "MQXA_All_" +
            #                   f"{'WithIron_' if self.data.magnet.geometry.with_iron_yoke else 'NoIron_'}" +
            #                   f"{'WithSelfField' if flag_self_field else 'NoSelfField'}" +
            #                   f"{'' if flag_contraction else '_no_contraction'}" + ".map2d")
            matrix = Pars.parseMap2d(map2dFile=path_map2d)

            if self.data.magnet.postproc.plot_all != 'False':
                path_cond2d = Path(os.path.join(os.path.dirname(roxie_path), self.data.general.magnet_name + ".cond2d"))
                # path_cond2d = Path(os.path.dirname(roxie_path), "MQXA_All_NoIron_NoSelfField" +
                #                    f"{'' if flag_contraction else '_no_contraction'}" + ".cond2d")
                conductorPositionsList = Pars.parseCond2d(path_cond2d)

        with open(self.model_file, 'w') as file:
            file.write("  BL.   COND.    NO.    X-POS/MM     Y-POS/MM    BX/T       BY/T"
                       "      AREA/MM**2 CURRENT FILL FAC.\n\n")

        cond_nr = 0
        row = 0
        c_nr_list = []  # list of conductors per block
        blocks_nr = self.strands['block'][-1]
        blocks, hts = np.array(self.strands['block']), np.array(self.strands['ht'])
        for blk in range(blocks_nr):
            _printState(blk + 1)
            c_nr_list.append(hts[np.where(blocks == blk + 1)[0][-1]] - sum(c_nr_list))
            for c in range(c_nr_list[blk]):
                parser_x, parser_y, roxie_x, roxie_y, strands_area, BB_roxie, BB_roxie_x, BB_roxie_y = \
                    [], [], [], [], [], [], [], []
                strands = 0
                ht = hts[row]
                while ht == c + 1 + cond_nr and row < len(self.strands['x']):
                    parser_x.append(self.strands['x'][row])
                    parser_y.append(self.strands['y'][row])
                    if self.data.magnet.postproc.compare_to_ROXIE:
                        _fetchRoxieData()
                    strands += 1
                    row += 1
                    if row < len(self.strands['x']) - 1:
                        ht = hts[row]

                strands_x = roxie_x if self.data.magnet.postproc.compare_to_ROXIE else parser_x
                strands_y = roxie_y if self.data.magnet.postproc.compare_to_ROXIE else parser_y

                BB_strands_x, BB_strands_y, BB_strands = _probeFromView()

                _updateMap2dFile(blk + 1, c + 1 + cond_nr)

                if self.data.magnet.postproc.compare_to_ROXIE:
                    BB_abs_err = _computeError()

                if self.data.magnet.postproc.plot_all != 'False':  # and (blk == 0 or blk == 1):
                    if self.data.magnet.postproc.compare_to_ROXIE:
                        map2d_strands, scatter3D_pos_roxie, scatter3D_pos = _plotData()
                    else:
                        scatter3D_pos = _plotData()[2]

            cond_nr += c_nr_list[blk]

        if self.data.magnet.postproc.compare_to_ROXIE:
            self.postprocess_parameters['overall_error'] = np.linalg.norm(self.BB_err_mean)
            self.postprocess_parameters['minimum_diff'] = np.min(self.BB_err_mean)
            self.postprocess_parameters['maximum_diff'] = np.max(self.BB_err_mean)

        print(f"Info    : {self.data.general.magnet_name} - E n d   I n t e r p o l a t i n g")

        if self.data.magnet.postproc.plot_all != 'False':
            self.plotHalfTurnGeometry()
            if self.data.magnet.postproc.compare_to_ROXIE:
                cax4 = self.fig4.add_axes([self.ax4.get_position().x1 + 0.02, self.ax4.get_position().y0,
                                           0.02, self.ax4.get_position().height])
                cbar = plt.colorbar(self.ax4.get_children()[2], cax=cax4)
                cbar.ax.set_ylabel('Absolute error [mT]', rotation=270)
                self.ax3.legend([scatter3D_pos, scatter3D_pos_roxie], ['FiQuS', 'ROXIE'], numpoints=1)
                # pickle.dump(fig, open('Bfield.fig.pickle', 'wb'))
                self.ax.legend([self.fiqus, self.roxie, map2d_strands], ['FiQuS', 'ROXIEparser', 'ROXIE'], numpoints=1)

            self.fig4.savefig(f"{os.path.join(self.solution_folder, self.data.general.magnet_name)}.svg", bbox_inches='tight')

            if self.data.magnet.postproc.plot_all == 'True':
                plt.show()

        # os.remove(os.path.join(self.solution_folder, 'b_Omega_p.pos'))
        # os.remove(f"{os.path.join(self.solution_folder, self.data.general.magnet_name)}.pre")
        # os.remove(f"{os.path.join(os.path.dirname(self.solution_folder), self.data.general.magnet_name)}.msh")
