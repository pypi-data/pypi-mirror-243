from pydantic import BaseModel
from typing import (List, Literal)


class Winding_gFiQuS(BaseModel):  # Geometry related windings _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    names: List[str] = None  # name to use in gmsh and getdp
    r_wms: List[float] = None  # radius of the middle of the winding
    n_turnss: List[float] = None  # number of turns
    ndpts: List[int] = None  # number of divisions of turn, i.e. number of hexagonal elements for each turn
    ndpt_ins: List[int] = None  # number of divisions of terminals in
    ndpt_outs: List[int] = None  # number of divisions of terminals in
    lps: List[float] = None  # layer pitch
    alphas: List[float] = None  # tilt angle
    wwws: List[float] = None  # winding wire widths (assuming rectangular)
    wwhs: List[float] = None  # winding wire heights (assuming rectangular)


class Winding_s(BaseModel):  # Solution time used windings _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CCT
    """
    currents: List[float] = None  # current in the wire
    sigmas: List[float] = None  # electrical conductivity
    mu_rs: List[float] = None  # relative permeability


class FQPL_g(BaseModel):  # Geometry related fqpls _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    names: List[str] = []  # name to use in gmsh and getdp
    fndpls: List[int] = None  # fqpl number of divisions per length
    fwws: List[float] = None  # fqpl wire widths (assuming rectangular) for theta = 0 this is x dimension
    fwhs: List[float] = None  # fqpl wire heights (assuming rectangular) for theta = 0 this is y dimension
    r_ins: List[float] = None  # radiuses for inner diameter for fqpl (radial (or x direction for theta=0) for placing the fqpl
    r_bs: List[float] = None  # radiuses for bending the fqpl by 180 degrees
    n_sbs: List[int] = None  # number of 'bending segmetns' for the 180 degrees turn
    thetas: List[float] = None  # rotation in deg from x+ axis towards y+ axis about z axis.
    z_starts: List[str] = None  # which air boundary to start at. These is string with either: z_min or z_max key from the Air region.
    z_ends: List[float] = None  # z coordinate of loop end


class FQPL_s(BaseModel):  # Solution time used fqpls _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CCT
    """
    currents: List[float] = []  # current in the wire
    sigmas: List[float] = []  # electrical conductivity
    mu_rs: List[float] = []  # relative permeability


class Former_gFiQuS(BaseModel):  # Geometry related formers _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    names: List[str] = None  # name to use in gmsh and getdp
    r_ins: List[float] = None  # inner radius
    r_outs: List[float] = None  # outer radius
    z_mins: List[float] = None  # extend of former  in negative z direction
    z_maxs: List[float] = None  # extend of former in positive z direction


class Former_s(BaseModel):  # Solution time used formers _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CCT
    """
    sigmas: List[float] = None  # electrical conductivity
    mu_rs: List[float] = None  # relative permeability


class Air_g(BaseModel):  # Geometry related air_region _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    name: str = None  # name to use in gmsh and getdp
    sh_type: str = None  # cylinder or cuboid are possible
    ar: float = None  # if box type is cuboid a is taken as a dimension, if cylinder then r is taken
    z_min: float = None  # extend of air region in negative z direction
    z_max: float = None  # extend of air region in positive z direction


class Air_s(BaseModel):  # Solution time used air _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CCT
    """
    sigma: float = None  # electrical conductivity
    mu_r: float = None  # relative permeability


class GeometryCCTFiQuS(BaseModel):
    """
        Level 2: Class for FiQuS CCT for FiQuS input
    """
    windings: Winding_gFiQuS = Winding_gFiQuS()
    fqpls: FQPL_g = FQPL_g()
    formers: Former_gFiQuS = Former_gFiQuS()
    air: Air_g = Air_g()


class MeshCCT(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    MaxAspectWindings: float = None  # used in transfinite mesh_generators settings to define mesh_generators size along two longer lines of hex elements of windings
    ThresholdSizeMin: float = None  # sets field control of Threshold SizeMin
    ThresholdSizeMax: float = None  # sets field control of Threshold SizeMax
    ThresholdDistMin: float = None  # sets field control of Threshold DistMin
    ThresholdDistMax: float = None  # sets field control of Threshold DistMax


class SolveCCT(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    windings: Winding_s = Winding_s()  # windings solution time _inputs
    fqpls: FQPL_s = FQPL_s()  # fqpls solution time _inputs
    formers: Former_s = Former_s()  # former solution time _inputs
    air: Air_s = Air_s()  # air solution time _inputs
    pro_template: str = None  # file name of .pro template file
    variables: List[str] = None  # Name of variable to post-process by GetDP, like B for magnetic flux density
    volumes: List[str] = None  # Name of volume to post-process by GetDP, line Winding_1
    file_exts: List[str] = None  # Name of file extensions to post-process by GetDP, like .pos


class PostprocCCTFiQuS(BaseModel):
    """
        Class for FiQuS CCT input file
    """
    windings_wwns: List[int] = None  # wires in width direction numbers
    windings_whns: List[int] = None  # wires in height direction numbers
    additional_outputs: List[str] = None  # Name of software specific input files to prepare, like :LEDET3D
    winding_order: List[int] = None
    fqpl_export_trim_tol: List[float] = None  # this multiplier times winding extend gives 'z' coordinate above(below) which hexes are exported for LEDET, length of this list must match number of fqpls
    variables: List[str] = None  # Name of variable to post-process by python Gmsh API, like B for magnetic flux density
    volumes: List[str] = None  # Name of volume to post-process by python Gmsh API, line Winding_1
    file_exts: List[str] = None  # Name of file extensions o post-process by python Gmsh API, like .pos


class CCTDM(BaseModel):
    """
        Level 1: Class for FiQuS CCT
    """
    type: Literal['CCT_straight'] = "CCT_straight"
    geometry: GeometryCCTFiQuS = GeometryCCTFiQuS()
    mesh: MeshCCT = MeshCCT()
    solve: SolveCCT = SolveCCT()
    postproc: PostprocCCTFiQuS = PostprocCCTFiQuS()
