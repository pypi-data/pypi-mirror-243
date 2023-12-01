from pydantic import BaseModel, Field
from typing import (Dict, List, Union, Literal, Optional)
from fiqus.data.DataRoxieParser import RoxieData
from fiqus.data.DataFiQuSMultipole import MPDM
from fiqus.data.DataFiQuSCCT import CCTDM
from fiqus.data.DataFiQuSPancake3D import Pancake3D


class MonoFiQuS(BaseModel):
    """
        Rutherford cable type
    """
    type: Literal['Mono']
    bare_cable_width: float = None
    bare_cable_height_mean: float = None


class RibbonFiQuS(BaseModel):
    """
        Rutherford cable type
    """
    type: Literal['Ribbon']
    bare_cable_width: float = None
    bare_cable_height_mean: float = None


class RutherfordFiQuS(BaseModel):
    """
        Rutherford cable type
    """
    type: Literal['Rutherford']
    bare_cable_width: float = None
    bare_cable_height_mean: float = None


class ConductorFiQuS(BaseModel):
    """
        Class for conductor type
    """
    cable: Union[RutherfordFiQuS, RibbonFiQuS, MonoFiQuS] = {'type': 'Rutherford'}


class GeneralSetting(BaseModel):
    """
        Class for general information on the case study
    """
    I_ref: List[float] = None


class ModelDataSetting(BaseModel):
    """
        Class for model data
    """
    general_parameters: GeneralSetting = GeneralSetting()
    conductors: Dict[str, ConductorFiQuS] = {}

#######################################################################################################################


class FiQuSGeometry(BaseModel):
    """
        Class for Roxie data
    """
    Roxie_Data: RoxieData = RoxieData()


class FiQuSSettings(BaseModel):
    """
        Class for FiQuS model
    """
    Model_Data_GS: ModelDataSetting = ModelDataSetting()


class RunFiQuS(BaseModel):
    """
        Class for FiQuS run
    """
    type: Literal["start_from_yaml", "mesh_only", "geometry_only", "geometry_and_mesh", "pre_process_only", "mesh_and_solve_with_post_process_python", "solve_with_post_process_python", "solve_only", "post_process_getdp_only", "post_process_python_only", "post_process"] = Field(default="start_from_yaml", title="Run Type of FiQuS", description="FiQuS allows you to run the model in different ways. The run type can be specified here. For example, you can just create the geometry and mesh or just solve the model with previous mesh, etc.")
    geometry: Union[str, int] = Field(default=None, title="Geometry Folder Key", description="This key will be appended to the geometry folder.")
    mesh: Union[str, int] = Field(default=None, title="Mesh Folder Key", description="This key will be appended to the mesh folder.")
    solution: Union[str, int] = Field(default=None, title="Solution Folder Key", description="This key will be appended to the solution folder.")
    launch_gui: bool = Field(default=True, title="Launch GUI", description="If True, the GUI will be launched after the run.")
    overwrite: bool = Field(default=False, title="Overwrite", description="If True, the existing folders will be overwritten, otherwise new folders will be created.")
    comments: str = Field(default="", title="Comments", description="Comments for the run. These comments will be saved in the run_log.csv file.")


class GeneralFiQuS(BaseModel):
    """
        Class for FiQuS general
    """
    magnet_name: str = None


class EnergyExtraction(BaseModel):
    """
        Level 3: Class for FiQuS
    """
    t_trigger: float = None
    R_EE: float = None
    power_R_EE: float = None
    L: float = None
    C: float = None


class QuenchHeaters(BaseModel):
    """
        Level 3: Class for FiQuS
    """
    N_strips: int = None
    t_trigger: List[float] = None
    U0: List[float] = None
    C: List[float] = None
    R_warm: List[float] = None
    w: List[float] = None
    h: List[float] = None
    h_ins: List[List[float]] = []
    type_ins: List[List[str]] = []
    h_ground_ins: List[List[float]] = []
    type_ground_ins: List[List[str]] = []
    l: List[float] = None
    l_copper: List[float] = None
    l_stainless_steel: List[float] = None
    ids: List[int] = None
    turns: List[int] = None
    turns_sides: List[str] = None


class Cliq(BaseModel):
    """
        Level 3: Class for FiQuS
    """
    t_trigger: float = None
    current_direction: List[int] = None
    sym_factor: int = None
    N_units: int = None
    U0: float = None
    C: float = None
    R: float = None
    L: float = None
    I0: float = None


class Circuit(BaseModel):
    """
        Level 2: Class for FiQuS
    """
    R_circuit: float = None
    L_circuit: float = None
    R_parallel: float = None


class PowerSupply(BaseModel):
    """
        Level 2: Class for FiQuS
    """
    I_initial: float = None
    t_off: float = None
    t_control_LUT: List[float] = Field(None, title="Time Values for Current Source", description="This list of time values will be matched with the current values in I_control_LUT, and then these (t, I) points will be connected with straight lines.")
    I_control_LUT: List[float] = Field(None, title="Current Values for Current Source" ,description="This list of current values will be matched with the time values in t_control_LUT, and then these (t, I) points will be connected with straight lines.")
    R_crowbar: float = None
    Ud_crowbar: float = None


class QuenchProtection(BaseModel):
    """
        Level 2: Class for FiQuS
    """
    energy_extraction:  EnergyExtraction = EnergyExtraction()
    quench_heaters: QuenchHeaters = QuenchHeaters()
    cliq: Cliq = Cliq()


class FDM(BaseModel):
    """
        Class for FiQuS
    """
    general: GeneralFiQuS = GeneralFiQuS()
    run: RunFiQuS = RunFiQuS()
    magnet: Union[MPDM, CCTDM, Pancake3D] = Field(default=MPDM(), discriminator='type')
    power_supply: PowerSupply = PowerSupply()
