import os
import gmsh
from numpy import square as square
from numpy import sqrt as sqrt
import json

from fiqus.utils.Utils import GmshUtils
from fiqus.utils.Utils import FilesAndFolders as Util
from fiqus.utils.Utils import GeometricFunctions as Func
from fiqus.data import DataFiQuS as dF
from fiqus.data import DataMultipole as dM


class Geometry:
    def __init__(self, data: dF.FDM() = None, geom: dF.FiQuSGeometry() = None, sett: dF.FiQuSSettings() = None,
                 geom_folder: str = None, verbose: bool = False):
        """
        Class to generate geometry
        :param data: FiQuS data model
        :param geom: ROXIE geometry data
        :param sett: settings data model
        :param verbose: If True more information is printed in python console.
        """
        self.data: dF.FDM() = data
        self.geom: dF.FiQuSGeometry() = geom
        self.sett: dF.FiQuSSettings() = sett
        self.geom_folder = geom_folder
        self.verbose: bool = verbose

        self.md = dM.MultipoleData()

        self.gu = GmshUtils(self.geom_folder, self.verbose)
        self.gu.initialize()
        self.occ = gmsh.model.occ

        self.model_file = f"{os.path.join(self.geom_folder, self.data.general.magnet_name)}.brep"
        self.iL, self.iR, self.oL, self.oR, self.iLr, self.iRr, self.oLr, self.oRr = [], [], [], [], [], [], [], []

    def ending_step(self, gui: bool = False):
        if gui:
            self.gu.launch_interactive_GUI()
        else:
            gmsh.clear()
            gmsh.finalize()

    def saveHalfTurnCornerPositions(self):
        json.dump({'iL': self.iL, 'iR': self.iR, 'oL': self.oL, 'oR': self.oR,
                   'iLr': self.iLr, 'iRr': self.iRr, 'oLr': self.oLr, 'oRr': self.oRr},
                  open(f"{os.path.join(self.geom_folder, self.data.general.magnet_name)}.crns", 'w'))

    def saveStrandPositions(self):
        ht_nr = 0
        parser_x, parser_y, blocks, ht = [], [], [], []
        for eo in self.geom.Roxie_Data.coil.electrical_order:
            block = self.geom.Roxie_Data.coil.coils[eo.coil].poles[eo.pole].layers[eo.layer].windings[
                eo.winding].blocks[eo.block]
            for halfTurn_nr, halfTurn in block.half_turns.items():
                ht_nr += 1
                for strand_group_nr, strand_group in halfTurn.strand_groups.items():
                    for strand_nr, strand in strand_group.strand_positions.items():
                        blocks.append(eo.block)
                        ht.append(ht_nr)
                        parser_x.append(strand.x)
                        parser_y.append(strand.y)
        json.dump({'x': parser_x, 'y': parser_y, 'block': blocks, 'ht': ht},
                  open(f"{os.path.join(self.geom_folder, self.data.general.magnet_name)}.strs", 'w'))

    def saveBoundaryRepresentationFile(self):
        self.occ.synchronize()
        gmsh.write(self.model_file)
        gmsh.clear()

    def loadBoundaryRepresentationFile(self):
        gmsh.option.setString('Geometry.OCCTargetUnit', 'M')  # set units to meters
        gmsh.open(self.model_file)

    def saveAuxiliaryFile(self):
        Util.write_data_to_yaml(f"{os.path.join(self.geom_folder, self.data.general.magnet_name)}.aux", self.md.dict())

    def constructIronGeometry(self):
        """
            Generates points, hyper lines, and curve loops for the iron yoke
        """
        iron = self.geom.Roxie_Data.iron
        self.md.geometries.iron.quadrants = {1: dM.Region(), 2: dM.Region(), 3: dM.Region(), 4: dM.Region()}
        quadrants = self.md.geometries.iron.quadrants

        lc = 1e-2
        for point_name, point in iron.key_points.items():
            quadrants[1].points[point_name] = self.occ.addPoint(point.x, point.y, 0, lc)

            if point.x == 0.:
                quadrants[2].points[point_name] = quadrants[1].points[point_name]
            else:
                quadrants[2].points[point_name] = self.occ.copy([(0, quadrants[1].points[point_name])])[0][1]
                self.occ.mirror([(0, quadrants[2].points[point_name])], 1, 0, 0, 0)
            if point.y == 0.:
                quadrants[3].points[point_name] = quadrants[2].points[point_name]
                quadrants[4].points[point_name] = quadrants[1].points[point_name]
            else:
                quadrants[3].points[point_name] = self.occ.copy([(0, quadrants[2].points[point_name])])[0][1]
                self.occ.mirror([(0, quadrants[3].points[point_name])], 0, 1, 0, 0)
                quadrants[4].points[point_name] = self.occ.copy([(0, quadrants[1].points[point_name])])[0][1]
                self.occ.mirror([(0, quadrants[4].points[point_name])], 0, 1, 0, 0)

        mirror_x = [1, -1, -1, 1]
        mirror_y = [1, 1, -1, -1]
        for line_name, line in iron.hyper_lines.items():
            if line.type == 'line':
                for quadrant, qq in quadrants.items():
                    if quadrant == 1:
                        qq.lines[line_name] = self.occ.addLine(qq.points[line.kp1], qq.points[line.kp2])
                    elif quadrant == 2:
                        if iron.key_points[line.kp1].x == 0. and iron.key_points[line.kp2].x == 0.:
                            qq.lines[line_name] = quadrants[1].lines[line_name]
                        else:
                            qq.lines[line_name] = self.occ.addLine(qq.points[line.kp1], qq.points[line.kp2])
                    elif quadrant == 3:
                        if iron.key_points[line.kp1].y == 0. and iron.key_points[line.kp2].y == 0.:
                            qq.lines[line_name] = quadrants[2].lines[line_name]
                        else:
                            qq.lines[line_name] = self.occ.addLine(qq.points[line.kp1], qq.points[line.kp2])
                    else:
                        if iron.key_points[line.kp1].y == 0. and iron.key_points[line.kp2].y == 0.:
                            qq.lines[line_name] = quadrants[1].lines[line_name]
                        else:
                            qq.lines[line_name] = self.occ.addLine(qq.points[line.kp1], qq.points[line.kp2])

            elif line.type == 'arc':
                center = Func.arc_center_from_3_points(
                    iron.key_points[line.kp1], iron.key_points[line.kp3], iron.key_points[line.kp2])
                new_point_name = 'kp' + line_name + '_center'
                quadrants[1].points[new_point_name] = self.occ.addPoint(center[0], center[1], 0)
                # gmsh.model.setEntityName(0, gm.iron.quadrants[1].points[new_point_name], 'iron_' + new_point_name)
                if center[0] == 0.:
                    quadrants[2].points[new_point_name] = quadrants[1].points[new_point_name]
                else:
                    quadrants[2].points[new_point_name] = self.occ.copy([(0, quadrants[1].points[new_point_name])])[0][1]
                    self.occ.mirror([(0, quadrants[2].points[new_point_name])], 1, 0, 0, 0)
                if center[1] == 0.:
                    quadrants[3].points[new_point_name] = quadrants[2].points[new_point_name]
                    quadrants[4].points[new_point_name] = quadrants[1].points[new_point_name]
                else:
                    quadrants[3].points[new_point_name] = self.occ.copy([(0, quadrants[2].points[new_point_name])])[0][1]
                    self.occ.mirror([(0, quadrants[3].points[new_point_name])], 0, 1, 0, 0)
                    quadrants[4].points[new_point_name] = self.occ.copy([(0, quadrants[1].points[new_point_name])])[0][1]
                    self.occ.mirror([(0, quadrants[4].points[new_point_name])], 0, 1, 0, 0)

                for quadrant, qq in quadrants.items():
                    qq.lines[line_name] = self.occ.addCircleArc(
                        qq.points[line.kp1], qq.points[new_point_name], qq.points[line.kp2])

            elif line.type == 'circle':
                pt1 = iron.key_points[line.kp1]
                pt2 = iron.key_points[line.kp2]
                center = [(pt1.x + pt2.x) / 2, (pt1.y + pt2.y) / 2]
                radius = (sqrt(square(pt1.x - center[0]) + square(pt1.y - center[1])) +
                          sqrt(square(pt2.x - center[0]) + square(pt2.y - center[1]))) / 2

                for quadrant, qq in quadrants.items():
                    qq.lines[line_name] = self.occ.addCircle(
                        mirror_x[quadrant - 1] * center[0], mirror_y[quadrant - 1] * center[1], 0, radius)
                    qq.points['kp' + line_name] = len(qq.points) + 1

            else:
                raise ValueError('Hyper line {} not supported'.format(line.type))

        for quadrant, qq in quadrants.items():
            for area_name, area in iron.hyper_areas.items():
                qq.areas[area_name] = dM.Area(loop=self.occ.addCurveLoop([qq.lines[line] for line in area.lines]))
                if (iron.hyper_areas[area_name].material not in self.md.domains.groups_surfaces and
                        iron.hyper_areas[area_name].material != 'BH_air'):
                    self.md.domains.groups_surfaces[iron.hyper_areas[area_name].material] = []

    def constructWedgeGeometry(self):
        """
            Generates points, hyper lines, and curve loops for the wedges
        """
        wedges = self.geom.Roxie_Data.wedges
        for i in wedges:
            kp0_inner = self.occ.addPoint(wedges[i].corrected_center.inner.x, wedges[i].corrected_center.inner.y, 0)
            kp0_outer = self.occ.addPoint(wedges[i].corrected_center.outer.x, wedges[i].corrected_center.outer.y, 0)
            arg = [self.occ.addPoint(wedges[i].corners.iL.x, wedges[i].corners.iL.y, 0),
                   self.occ.addPoint(wedges[i].corners.iR.x, wedges[i].corners.iR.y, 0),
                   self.occ.addPoint(wedges[i].corners.oL.x, wedges[i].corners.oL.y, 0),
                   self.occ.addPoint(wedges[i].corners.oR.x, wedges[i].corners.oR.y, 0)]

            left = self.occ.addLine(arg[0], arg[2])
            right = self.occ.addLine(arg[1], arg[3])
            inner = self.occ.addCircleArc(arg[0], kp0_inner, arg[1])
            outer = self.occ.addCircleArc(arg[2], kp0_outer, arg[3])
            self.md.geometries.wedges.areas[i] = dM.Area(loop=self.occ.addCurveLoop([inner, right, outer, left]))

    def constructCoilGeometry(self):
        """
            Generates points, hyper lines, and curve loops for the coil half-turns
        """
        frac = 1  # self.frac if self.frac else 1
        for coil_nr, coil in self.geom.Roxie_Data.coil.coils.items():
            self.md.geometries.coil.coils[coil_nr] = dM.Pole()
            coils = self.md.geometries.coil.coils[coil_nr]
            for pole_nr, pole in coil.poles.items():
                coils.poles[pole_nr] = dM.Layer()
                poles = coils.poles[pole_nr]
                for layer_nr, layer in pole.layers.items():
                    poles.layers[layer_nr] = dM.Winding()
                    layers = poles.layers[layer_nr]
                    for winding_nr, winding in layer.windings.items():
                        layers.windings[winding_nr] = dM.Block(conductor_name=winding.conductor_name,
                                                               conductors_number=winding.conductors_number)
                        windings = layers.windings[winding_nr]
                        ll = self.sett.Model_Data_GS.conductors[winding.conductor_name].cable.bare_cable_height_mean
                        for block_key, block in winding.blocks.items():
                            windings.blocks[block_key] = dM.BlockData(current_sign=block.current_sign)
                            hts = windings.blocks[block_key].half_turns

                            for halfTurn_nr, halfTurn in block.half_turns.items():
                                ht = str(halfTurn_nr)
                                hts.areas[ht] = dM.Area()
                                hf_current = halfTurn.corners.insulated
                                if halfTurn_nr == 1:
                                    bc = block.block_corners
                                    if (hf_current.iL.y < 0 and block_key == max(winding.blocks.keys())) or \
                                            (hf_current.iL.y > 0 and block_key == min(winding.blocks.keys())):
                                        hts.points[ht + 'i'] = self.occ.addPoint(bc.iR.x, bc.iR.y, 0, ll / frac)
                                        hts.points[ht + 'o'] = self.occ.addPoint(bc.oR.x, bc.oR.y, 0, ll / frac)
                                    else:
                                        hts.points[ht + 'i'] = self.occ.addPoint(bc.iL.x, bc.iL.y, 0, ll / frac)
                                        hts.points[ht + 'o'] = self.occ.addPoint(bc.oL.x, bc.oL.y, 0, ll / frac)
                                    hts.lines[ht + 'r'] = self.occ.addLine(hts.points[ht + 'i'], hts.points[ht + 'o'])

                                if halfTurn_nr == winding.conductors_number:
                                    bc = block.block_corners

                                    if (hf_current.iL.y < 0 and block_key == max(winding.blocks.keys())) or \
                                            (hf_current.iL.y > 0 and block_key == min(winding.blocks.keys())):
                                        hts.points['end_i'] = self.occ.addPoint(bc.iL.x, bc.iL.y, 0, ll/frac)
                                        hts.points['end_o'] = self.occ.addPoint(bc.oL.x, bc.oL.y, 0, ll/frac)
                                    else:
                                        hts.points['end_i'] = self.occ.addPoint(bc.iR.x, bc.iR.y, 0, ll/frac)
                                        hts.points['end_o'] = self.occ.addPoint(bc.oR.x, bc.oR.y, 0, ll/frac)

                                    hts.lines[ht + 'i'] = self.occ.addLine(hts.points['end_i'], hts.points[ht + 'i'])
                                    hts.lines[ht + 'o'] = self.occ.addLine(hts.points['end_o'], hts.points[ht + 'o'])
                                    hts.lines['end'] = self.occ.addLine(hts.points['end_i'], hts.points['end_o'])

                                    # For plotting only
                                    if pole_nr == 1:
                                        self.occ.synchronize()
                                        self.iL.append(list(gmsh.model.getValue(0, hts.points['end_i'], [])[:-1]))
                                        self.oL.append(list(gmsh.model.getValue(0, hts.points['end_o'], [])[:-1]))
                                        # if block_key == 1 or block_key == 3 or block_key == 5 or block_key == 6:
                                        #     radius = np.sqrt(np.square(iL[0] - coil.bore_center.x) +
                                        #                      np.square(iL[1] - coil.bore_center.y))
                                        #     self.ax.add_patch(
                                        #         patches.Circle((coil.bore_center.x, coil.bore_center.y), radius=radius,
                                        #                        color='b', fill=False))
                                        #     radius = np.sqrt(np.square(oL[0] - coil.bore_center.x) +
                                        #                      np.square(oL[1] - coil.bore_center.y))
                                        #     self.ax.add_patch(
                                        #         patches.Circle((coil.bore_center.x, coil.bore_center.y), radius=radius,
                                        #                        color='c', fill=False))
                                    ################

                                    left = hts.lines['end']
                                else:
                                    hf_next = block.half_turns[halfTurn_nr + 1].corners.insulated
                                    next_ht = str(halfTurn_nr + 1)
                                    mid_point_i = [(hf_next.iR.x + hf_current.iL.x) / 2,
                                                   (hf_next.iR.y + hf_current.iL.y) / 2]
                                    mid_point_o = [(hf_next.oR.x + hf_current.oL.x) / 2,
                                                   (hf_next.oR.y + hf_current.oL.y) / 2]
                                    hts.points[next_ht + 'i'] = self.occ.addPoint(mid_point_i[0], mid_point_i[1], 0,
                                                                                  ll / frac)
                                    hts.points[next_ht + 'o'] = self.occ.addPoint(mid_point_o[0], mid_point_o[1], 0,
                                                                                  ll / frac)

                                    hts.lines[ht + 'i'] = \
                                        self.occ.addLine(hts.points[next_ht + 'i'], hts.points[ht + 'i'])
                                    hts.lines[ht + 'o'] = \
                                        self.occ.addLine(hts.points[next_ht + 'o'], hts.points[ht + 'o'])
                                    hts.lines[next_ht + 'r'] = \
                                        self.occ.addLine(hts.points[next_ht + 'i'], hts.points[next_ht + 'o'])
                                    left = hts.lines[next_ht + 'r']

                                    # For plotting only
                                    if pole_nr == 1:
                                        self.occ.synchronize()
                                        self.iL.append(list(gmsh.model.getValue(0, hts.points[next_ht + 'i'], [])[:-1]))
                                        self.oL.append(list(gmsh.model.getValue(0, hts.points[next_ht + 'o'], [])[:-1]))
                                if pole_nr == 1:
                                    self.iR.append(list(gmsh.model.getValue(0, hts.points[ht + 'i'], [])[:-1]))
                                    self.oR.append(list(gmsh.model.getValue(0, hts.points[ht + 'o'], [])[:-1]))
                                    hti = halfTurn.corners.insulated
                                    self.iLr.append([hti.iL.x, hti.iL.y])
                                    self.iRr.append([hti.iR.x, hti.iR.y])
                                    self.oLr.append([hti.oL.x, hti.oL.y])
                                    self.oRr.append([hti.oR.x, hti.oR.y])
                                ################

                                hts.areas[ht].loop = self.occ.addCurveLoop([hts.lines[ht + 'i'],  # inner
                                                                            hts.lines[ht + 'r'],  # right
                                                                            hts.lines[ht + 'o'],  # outer
                                                                            left])  # left

        self.saveHalfTurnCornerPositions()

    def buildDomains(self):
        """
            Generates plane surfaces from the curve loops
        """
        iron = self.geom.Roxie_Data.iron
        gm = self.md.geometries

        for i in iron.key_points:
            gm.iron.max_radius = max(gm.iron.max_radius, max(iron.key_points[i].x, iron.key_points[i].y))

        # Create and build air far field
        radius_in = gm.iron.max_radius * (2.5 if self.data.magnet.geometry.with_iron_yoke else 6)
        gm.air_inf.lines['inner'] = self.occ.addCircle(0., 0., 0., radius_in)
        gm.air_inf.areas['inner'] = dM.Area(loop=self.occ.addCurveLoop([gm.air_inf.lines['inner']]))
        gm.air_inf.areas['inner'].surface = self.occ.addPlaneSurface([self.md.geometries.air_inf.areas['inner'].loop])
        radius_out = gm.iron.max_radius * (3.2 if self.data.magnet.geometry.with_iron_yoke else 8)
        gm.air_inf.lines['outer'] = self.occ.addCircle(0., 0., 0., radius_out)
        gm.air_inf.areas['outer'] = dM.Area(loop=self.occ.addCurveLoop([gm.air_inf.lines['outer']]))
        gm.air_inf.areas['outer'].surface = self.occ.addPlaneSurface([gm.air_inf.areas['outer'].loop,
                                                                      gm.air_inf.areas['inner'].loop])
        self.md.domains.groups_surfaces['air_inf'] = [gm.air_inf.areas['outer'].surface]

        # Build iron yoke domains
        if self.data.magnet.geometry.with_iron_yoke:
            for quadrant, qq in gm.iron.quadrants.items():
                for area_name, area in qq.areas.items():
                    build = True
                    loops = [area.loop]
                    for hole_key, hole in iron.hyper_holes.items():
                        if area_name == hole.areas[1]:
                            loops.append(qq.areas[hole.areas[0]].loop)
                        elif area_name == hole.areas[0]:  # or iron.hyper_areas[area_name].material == 'BH_air':
                            build = False
                    if build:
                        area.surface = self.occ.addPlaneSurface(loops)
                        self.md.domains.groups_surfaces[iron.hyper_areas[area_name].material].append(area.surface)

        # Build coil domains
        for coil_nr, coil in gm.coil.coils.items():
            for pole_nr, pole in coil.poles.items():
                for layer_nr, layer in pole.layers.items():
                    for winding_nr, winding in layer.windings.items():
                        # cable = self.set.Model_Data_GS.conductors[winding.conductor_name].cable
                        # ht_area = cable.bare_cable_height_mean * cable.bare_cable_width
                        for block_key, block in winding.blocks.items():
                            current_sign = '_neg' if block.current_sign < 0 else '_pos'
                            for area_name, area in block.half_turns.areas.items():
                                ht_name = 'block' + str(block_key) + '_ht' + str(area_name) + current_sign
                                # self.conductor_areas[ht_name] = ht_area
                                area.surface = self.occ.addPlaneSurface([area.loop])
                                self.md.domains.groups_surfaces[ht_name] = [area.surface]

        # Build wedges domains
        for wedge_nr, wedge in gm.wedges.areas.items():
            wedge.surface = self.occ.addPlaneSurface([wedge.loop])
            self.md.domains.groups_surfaces['wedge_' + str(wedge_nr)] = [wedge.surface]

    def updateTags(self):
        self.md.geometries.coil.electrical_order = self.geom.Roxie_Data.coil.electrical_order
        for coil_nr, coil in self.geom.Roxie_Data.coil.coils.items():
            self.md.geometries.coil.coils[coil_nr].bore_center = coil.bore_center

        for coil_nr, coil in self.md.geometries.coil.coils.items():
            for pole_nr, pole in coil.poles.items():
                for layer_nr, layer in pole.layers.items():
                    for winding_nr, winding in layer.windings.items():
                        for block_key, block in winding.blocks.items():
                            hts = block.half_turns
                            for ht_nr, ht in hts.areas.items():
                                lines_tags = gmsh.model.getAdjacencies(2, ht.surface)[1]
                                first_tag = int(min(lines_tags))
                                hts.lines[ht_nr + ('i' if ht_nr == '1' else 'r')] = first_tag
                                hts.lines[ht_nr + ('r' if ht_nr == '1' else 'i')] = first_tag + 1
                                hts.lines[ht_nr + 'o'] = first_tag + 2
                                if int(ht_nr) == len(hts.areas):
                                    hts.lines['end'] = first_tag + 3

        lines_tags = gmsh.model.getAdjacencies(2, self.md.geometries.air_inf.areas['outer'].surface)[1]
        self.md.geometries.air_inf.lines['outer'] = int(lines_tags[0])
        self.md.geometries.air_inf.lines['inner'] = int(lines_tags[1])
