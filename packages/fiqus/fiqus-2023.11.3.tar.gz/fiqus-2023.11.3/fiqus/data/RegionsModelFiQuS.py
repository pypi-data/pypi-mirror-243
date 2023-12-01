from pydantic import BaseModel
from typing import (List, Dict)


class Region(BaseModel):
    name: str = None
    number: int = None


class Regions(BaseModel):
    names: List[str] = None
    numbers: List[int] = None


class TwoParBoundaryRegions(BaseModel):
    names: List[List[str]] = None
    numbers: List[List[int]] = None
    values: List[List[float]] = None


class OneParBoundaryRegions(BaseModel):
    names: List[List[str]] = None
    numbers: List[List[int]] = None
    value: List[float] = None


class PoweredRegions(BaseModel):
    names: List[str] = None
    numbers: List[int] = None
    currents: List[float] = None
    sigmas: List[float] = None
    mu_rs: List[float] = None


class InducedRegions(BaseModel):
    names: List[str] = None
    numbers: List[int] = None
    sigmas: List[float] = None
    mu_rs: List[float] = None


class InsulatorRegions(BaseModel):
    names: List[str] = None
    numbers: List[int] = None
    sigmas: List[float] = None
    mu_rs: List[float] = None


class IronRegions(BaseModel):
    names: List[str] = None
    numbers: List[int] = None
    sigmas: List[float] = None
    mu_rs: List[float] = None


class AirRegion(BaseModel):
    name: str = None
    number: int = None
    sigma: float = None
    mu_r: float = None


class AirFarFieldRegions(BaseModel):
    names: List[str] = None
    numbers: List[int] = None
    radius_in: float = None
    radius_out: float = None


class NonPermeableSourceRegion(BaseModel):
    name: str = None
    number: int = None
    sigma: float = None
    mu_r: float = None


class SourceFreeRegion(BaseModel):
    name: str = None
    number: int = None
    sigma: float = None
    mu_r: float = None


class Powered(BaseModel):
    vol: PoweredRegions = PoweredRegions()  # volume region
    vol_in: Region = Region()  # input terminal volume region
    vol_out: Region = Region()  # input terminal volume region
    conductors: Dict[str, List[str]] = {}  # conductor types
    surf: Regions = Regions()  # surface region
    surf_th: Regions = Regions()  # surface region
    surf_in: Regions = Regions()  # input terminal surface region
    surf_out: Regions = Regions()  # output terminal surface region
    cochain: Regions = Regions()  # winding cochain (cut)
    curve: Regions = Regions()  # powered volumes lines


class Induced(BaseModel):
    vol: InducedRegions = InducedRegions()  # volume region
    surf_in: Regions = Regions()  # input terminal surface region
    surf_out: Regions = Regions()  # output terminal surface region
    cochain: Regions = Regions()  # winding cochain (cut)


class Insulator(BaseModel):
    vol: InsulatorRegions = InsulatorRegions()  # volume region
    surf: Regions = Regions()  # surface region
    curve: Regions = Regions()  # curve region


class Iron(BaseModel):
    vol: IronRegions = IronRegions()  # volume region
    surf: Regions = Regions()  # surface region


class Air(BaseModel):
    vol: AirRegion = AirRegion()  # volume region
    surf: Region = Region()  # surface region
    line: Region = Region()    # line region
    point: Regions = Regions()    # point region
    cochain: Regions = Regions()  # air cochain (cut)


class AirFarField(BaseModel):
    vol: AirFarFieldRegions = AirFarFieldRegions()  # volume region
    surf: Region = Region()  # surface region


class NonPermeableSource(BaseModel):
    vol: NonPermeableSourceRegion = NonPermeableSourceRegion()  # volume region
    surf: Region = Region()  # surface region


class SourceFree(BaseModel):
    vol: SourceFreeRegion = SourceFreeRegion()  # volume region
    surf: Region = Region()  # surface region


class RobinCondition(BaseModel):
    bc: TwoParBoundaryRegions = TwoParBoundaryRegions()
    groups: Dict[str, List[int]] = {}


class NeumannCondition(BaseModel):
    bc: OneParBoundaryRegions = OneParBoundaryRegions()
    groups: Dict[str, List[int]] = {}


class DirichletCondition(BaseModel):
    bc: OneParBoundaryRegions = OneParBoundaryRegions()
    groups: Dict[str, List[int]] = {}


class ThermalBoundaryConditions(BaseModel):
    temperature: DirichletCondition = DirichletCondition()
    heat_flux: NeumannCondition = NeumannCondition()
    cooling: RobinCondition = RobinCondition()


class SymmetryBoundaryConditions(BaseModel):
    normal_free: Region = Region()
    tangential_free: Region = Region()


class BoundaryConditions(BaseModel):
    thermal: ThermalBoundaryConditions = ThermalBoundaryConditions()
    symmetry: SymmetryBoundaryConditions = SymmetryBoundaryConditions()


class InsulationType(BaseModel):
    layers_number: List[int] = []
    thin_shells: List[List[int]] = []
    layers_material: List[List[str]] = []
    thicknesses: List[List[float]] = []


class ThinShell(BaseModel):
    groups: Dict[str, List[int]] = {}
    mid_turns_layers_poles: List[int] = None
    second_group_is_next: Dict[str, List[int]] = {}
    normals_directed: Dict[str, List[int]] = {}
    insulation_types: InsulationType = InsulationType()
    quench_heaters: InsulationType = InsulationType()


class RegionsModel(BaseModel):
    powered: Powered = Powered()
    induced: Induced = Induced()
    insulator: Insulator = Insulator()
    iron: Iron = Iron()
    air: Air = Air()
    air_far_field: AirFarField = AirFarField()
    thin_shells: ThinShell = ThinShell()
    boundaries: BoundaryConditions = BoundaryConditions()


# if __name__ == "__main__":
#     write = True
#     read = False
#
#     def read_regions(regions_file_name):
#         with open(regions_file_name, 'r') as stream:
#             yaml_str = ruamel.yaml.safe_load(stream)
#         return RegionsModel(**yaml_str)
#
#     def flist(x):
#         retval = ruamel.yaml.comments.CommentedSeq(x)
#         retval.fa.set_flow_style()  # fa -> format attribute
#         return retval
#
#     if write:
#         model = RegionsModel()
#         model.powered.vol = [1, 2]
#         data_dict = model.dict()
#         yaml = ruamel.yaml.YAML()
#         yaml.default_flow_style = False
#         yaml.emitter.alt_null = 'Null'
#
#         def my_represent_none(self, data):
#             return self.represent_scalar('tag:yaml.org,2002:null', 'null')
#
#         yaml.representer.add_representer(type(None), my_represent_none)
#         with open('cct_regions_empty.yaml', 'w') as yaml_file:
#             yaml.dump(model.dict(), yaml_file)
#     if read:
#         regions_file_name = 'cct1_regions_manual.yaml'
#         regions = read_regions(regions_file_name)
