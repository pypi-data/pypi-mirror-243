import os
import gmsh
from numpy import square as square
from numpy import sqrt as sqrt

from fiqus.utils.Utils import GmshUtils
from fiqus.utils.Utils import FilesAndFolders as Util
from fiqus.data import DataFiQuS as dF
from fiqus.data import DataMultipole as dM
from fiqus.data.RegionsModelFiQuS import RegionsModel as rM


class Mesh:
    def __init__(self, data: dF.FDM() = None, sett: dF.FiQuSSettings() = None, mesh_folder: str = None,
                 verbose: bool = False):
        """
        Class to generate mesh
        :param data: FiQuS data model
        :param sett: settings data model
        :param verbose: If True more information is printed in python console.
        """
        self.data: dF.FDM() = data
        self.set: dF.FiQuSSettings() = sett
        self.mesh_folder = mesh_folder
        self.verbose: bool = verbose

        self.md = dM.MultipoleData()
        self.rm = rM()

        self.gu = GmshUtils(self.mesh_folder, self.verbose)
        self.gu.initialize()
        self.occ = gmsh.model.occ
        self.mesh = gmsh.model.mesh

        self.brep_iron_curves = {1: set(), 2: set(), 3: set(), 4: set()}
        self.mesh_parameters = dict.fromkeys(['SJ', 'SICN', 'SIGE', 'Gamma', 'nodes'])
        self.geom_folder = os.path.dirname(self.mesh_folder)
        self.model_file = f"{os.path.join(self.mesh_folder, self.data.general.magnet_name)}.msh"

        self.colors = {'wedges': [86, 180, 233],  # sky blue
                       'half_turns_pos': [213, 94, 0],  # vermilion
                       'half_turns_neg': [255, 136, 42],  # light vermilion
                       'air': [240, 228, 66],  # yellow
                       'air_inf': [220, 208, 46],  # dark yellow
                       # yoke
                       'BHiron1': [0, 114, 178],  # blue
                       'BHiron2': [0, 158, 115],  # bluish green
                       'BHiron4': [86, 180, 233],  # sky blue
                       # key
                       'BHiron3': [220, 208, 46],  # dark yellow
                       # [230, 159, 0],  # orange
                       # collar
                       'BHiron5': [204, 121, 167],  # hopbush
                       'BHiron6': [0, 114, 178],  # blue
                       'BHiron7': [204, 121, 167]}  # reddish purple

    def ending_step(self, gui: bool = False):
        if gui:
            self.gu.launch_interactive_GUI()
        else:
            gmsh.clear()
            gmsh.finalize()

    def loadAuxiliaryFile(self):
        self.md = Util.read_data_from_yaml(f"{os.path.join(self.geom_folder, self.data.general.magnet_name)}.aux", dM.MultipoleData)

    def updateAuxiliaryFile(self):
        md2 = Util.read_data_from_yaml(f"{os.path.join(self.geom_folder, self.data.general.magnet_name)}.aux", dM.MultipoleData)
        md2.domains.physical_groups = self.md.domains.physical_groups
        Util.write_data_to_yaml(f"{os.path.join(self.geom_folder, self.data.general.magnet_name)}.aux", md2.dict())

    def saveMeshFile(self):
        gmsh.write(self.model_file)

    def saveRegionFile(self):
        Util.write_data_to_yaml(f"{os.path.join(self.mesh_folder, self.data.general.magnet_name)}.reg", self.rm.dict())

    def getIronCurvesTags(self):
        if self.data.magnet.geometry.with_iron_yoke:
            for quadrant, qq in self.md.geometries.iron.quadrants.items():
                for area_name, area in qq.areas.items():
                    if area.surface:
                        self.brep_iron_curves[quadrant] |= set(gmsh.model.getAdjacencies(2, area.surface)[1])

    def defineMesh(self):
        curves_list = []
        for coil_nr, coil in self.md.geometries.coil.coils.items():
            for pole_nr, pole in coil.poles.items():
                for layer_nr, layer in pole.layers.items():
                    for winding_nr, winding in layer.windings.items():
                        for block_key, block in winding.blocks.items():
                            hts = block.half_turns
                            for i in range(len(hts.areas) - 1):
                                curves_list.append(self.occ.copy([(1, hts.lines[str(i + 1) + 'r'])])[0][1])
                            curves_list.append(self.occ.copy([(1, hts.lines['end'])])[0][1])

        self.occ.synchronize()
        if not self.data.magnet.mesh.default_mesh:
            curve_list_iron = []
            if self.data.magnet.geometry.with_iron_yoke:
                # if self.from_brep:
                for quadrant, qq in self.brep_iron_curves.items():
                    for line in qq:
                        curve_list_iron.append(self.occ.copy([(1, line)])[0][1])
                # else:
                #     for quadrant, qq in self.md.geometry.iron.quadrants.items():
                #         for line_name, line in qq.lines.items():
                #             curve_list_iron.append(self.occ.copy([(1, line)])[0][1])

            size_min = self.data.magnet.mesh.mesh_coil.SizeMin
            size_max = self.data.magnet.mesh.mesh_coil.SizeMax
            dist_min = self.data.magnet.mesh.mesh_coil.DistMin
            dist_max = self.data.magnet.mesh.mesh_coil.DistMax  # iron max_radius

            list_aux_type = "CurvesList"
            list_aux = curve_list_iron
            size_min_aux = self.data.magnet.mesh.mesh_iron.SizeMin
            size_max_aux = self.data.magnet.mesh.mesh_iron.SizeMax
            dist_min_aux = self.data.magnet.mesh.mesh_iron.DistMin
            dist_max_aux = self.data.magnet.mesh.mesh_iron.DistMax

        else:
            min_height = 1.
            for name, cond in self.set.Model_Data_GS.conductors.items():
                min_height = min(min_height, cond.cable.bare_cable_height_mean)

            bore_centers = [self.occ.addPoint(coil.bore_center.x, coil.bore_center.y, 0.)
                            for coil_nr, coil in self.md.geometries.coil.coils.items()]
            point = gmsh.model.getValue(0, self.md.geometries.coil.coils[1].poles[1].layers[1].windings[1].blocks[
                1].half_turns.points['1i'], [])
            min_dist = sqrt(square(point[0] - self.md.geometries.coil.coils[1].bore_center.x) +
                            square(point[1] - self.md.geometries.coil.coils[1].bore_center.y))

            size_min = min_height / 2
            size_max = min_height * 20
            dist_min = min_height * 2
            dist_max = self.md.geometries.iron.max_radius

            list_aux_type = "PointsList"
            list_aux = bore_centers
            size_min_aux = min_height / 2
            size_max_aux = min_height * 20
            dist_min_aux = min_dist
            dist_max_aux = min_dist

        self.occ.synchronize()

        distance_coil = self.mesh.field.add("Distance")
        self.mesh.field.setNumbers(distance_coil, "CurvesList", curves_list)
        self.mesh.field.setNumber(distance_coil, "Sampling", 100)

        threshold = self.mesh.field.add("Threshold")
        self.mesh.field.setNumber(threshold, "InField", distance_coil)
        self.mesh.field.setNumber(threshold, "SizeMin", size_min)
        self.mesh.field.setNumber(threshold, "SizeMax", size_max)
        self.mesh.field.setNumber(threshold, "DistMin", dist_min)
        self.mesh.field.setNumber(threshold, "DistMax", dist_max)

        distance_aux = self.mesh.field.add("Distance")
        self.mesh.field.setNumbers(distance_aux, list_aux_type, list_aux)
        self.mesh.field.setNumber(distance_aux, "Sampling", 100)

        threshold_aux = self.mesh.field.add("Threshold")
        self.mesh.field.setNumber(threshold_aux, "InField", distance_aux)
        self.mesh.field.setNumber(threshold_aux, "SizeMin", size_min_aux)
        self.mesh.field.setNumber(threshold_aux, "SizeMax", size_max_aux)
        self.mesh.field.setNumber(threshold_aux, "DistMin", dist_min_aux)
        self.mesh.field.setNumber(threshold_aux, "DistMax", dist_max_aux)

        background = self.mesh.field.add("Min")
        self.mesh.field.setNumbers(background, "FieldsList", [threshold, threshold_aux] if (
                self.data.magnet.geometry.with_iron_yoke and not self.data.magnet.mesh.default_mesh
                or self.data.magnet.mesh.default_mesh) else [threshold])
        self.mesh.field.setAsBackgroundMesh(background)

    def fragment(self):
        """
            Fragment and group air domains
        """
        holes = []
        for group_name, surfaces in self.md.domains.groups_surfaces.items():
            if group_name != 'air_inf':
                holes.extend([(2, s) for s in surfaces])
        fragmented = self.occ.fragment([(2, self.md.geometries.air_inf.areas['inner'].surface)], holes)[1]
        self.md.domains.groups_surfaces['air'] = []
        existing_domains = [e[0][1] for e in fragmented[1:]]
        for e in fragmented[0]:
            if e[1] not in existing_domains:
                self.md.domains.groups_surfaces['air'].append(e[1])

        self.occ.synchronize()

    def createPhysicalGroups(self):
        """
            Creates physical groups by grouping the mirrored entities according to the Roxie domains
        """
        pg = self.md.domains.physical_groups
        for group_name, surfaces in self.md.domains.groups_surfaces.items():
            pg.surfaces[group_name] = gmsh.model.addPhysicalGroup(2, surfaces)
            gmsh.model.setPhysicalName(2, pg.surfaces[group_name], group_name)
            if group_name[:5] == 'block':
                color = self.colors['half_turns_pos'] if group_name[-3:] == 'pos' else self.colors['half_turns_neg']
            elif group_name[:5] == 'wedge':
                color = self.colors['wedges']
            else:
                color = self.colors[group_name]
            gmsh.model.setColor([(2, i) for i in surfaces], color[0], color[1], color[2])

        pg.curves['air_inf'] = gmsh.model.addPhysicalGroup(1, [self.md.geometries.air_inf.lines['outer']])
        gmsh.model.setPhysicalName(1, pg.curves['air_inf'], 'air_inf')

    def assignRegionsTags(self):
        self.rm.air_far_field.vol.radius_out = float(gmsh.model.getValue(0, gmsh.model.getAdjacencies(
                1, self.md.geometries.air_inf.lines['outer'])[1][0], []).max())
        self.rm.air_far_field.vol.radius_in = float(gmsh.model.getValue(0, gmsh.model.getAdjacencies(
                1, self.md.geometries.air_inf.lines['inner'])[1][0], []).max())

        self.rm.air.vol.name = "Air"
        self.rm.air.vol.number = self.md.domains.physical_groups.surfaces['air']
        self.rm.air_far_field.vol.names = ["AirInf"]
        self.rm.air_far_field.vol.numbers = [self.md.domains.physical_groups.surfaces['air_inf']]
        self.rm.powered.vol.names = []
        self.rm.powered.vol.numbers = []
        self.rm.iron.vol.names = []
        self.rm.iron.vol.numbers = []
        self.rm.induced.vol.names = []
        self.rm.induced.vol.numbers = []
        for group_name, surface in self.md.domains.physical_groups.surfaces.items():
            if group_name[:5] == 'block':
                self.rm.powered.vol.names.append(group_name)
                self.rm.powered.vol.numbers.append(surface)
                #  self.fd.half_turns.cross_sections.append(self.conductor_areas[name])
            elif group_name[:2] == 'BH':
                self.rm.iron.vol.names.append(group_name)
                self.rm.iron.vol.numbers.append(surface)
            elif group_name[:5] == 'wedge':
                self.rm.induced.vol.names.append(group_name)
                self.rm.induced.vol.numbers.append(surface)

        self.rm.air_far_field.surf.name = "Surface_Inf"
        self.rm.air_far_field.surf.number = self.md.domains.physical_groups.curves['air_inf']

    def setMeshOptions(self):
        """
            Meshes the generated domain
        """
        gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
        gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
        gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 0)
        if not self.data.magnet.mesh.default_mesh:
            # gmsh.option.setNumber("Mesh.AngleToleranceFacetOverlap", self.data.one_lab.mesh.AngleToleranceFacetOverlap)
            # gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", self.data.one_lab.mesh.MeshSizeFromCurvature)
            # gmsh.option.setNumber("Mesh.MeshSizeMin", self.data.one_lab.mesh.MeshSizeMin)
            # gmsh.option.setNumber("Mesh.MeshSizeMax", self.data.one_lab.mesh.MeshSizeMax)
            gmsh.option.setNumber("Mesh.Algorithm", self.data.magnet.mesh.Algorithm)
            gmsh.option.setNumber("Mesh.Optimize", self.data.magnet.mesh.Optimize)
            gmsh.option.setNumber("Mesh.ElementOrder", self.data.magnet.mesh.ElementOrder)
        else:
            gmsh.option.setNumber("Mesh.Algorithm", 6)
            gmsh.option.setNumber("Mesh.Optimize", 1)
            gmsh.option.setNumber("Mesh.ElementOrder", 2)

    def generateMesh(self):
        self.mesh.generate(2)
        self.mesh.removeDuplicateNodes()

    def checkMeshQuality(self):
        tags = self.mesh.getElements(2)[1][0]

        self.mesh_parameters['SJ'] = min(self.mesh.getElementQualities(elementTags=tags, qualityName='minSJ'))
        self.mesh_parameters['SICN'] = min(self.mesh.getElementQualities(elementTags=tags, qualityName='minSICN'))
        self.mesh_parameters['SIGE'] = min(self.mesh.getElementQualities(elementTags=tags, qualityName='minSIGE'))
        self.mesh_parameters['Gamma'] = min(self.mesh.getElementQualities(elementTags=tags, qualityName='gamma'))
        self.mesh_parameters['nodes'] = len(self.mesh.getNodes()[0])

        # gmsh.plugin.setNumber("AnalyseMeshQuality", "JacobianDeterminant", 1)
        # gmsh.plugin.setNumber("AnalyseMeshQuality", "CreateView", 100)
        # test = gmsh.plugin.run("AnalyseMeshQuality")
        # test2 = gmsh.view.getModelData(test, test)

        # gmsh.logger.getLastError()
        # gmsh.logger.get()
