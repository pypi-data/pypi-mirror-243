from pydantic import BaseModel
from typing import (List, Literal)


class Threshold(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    SizeMin: float = None
    SizeMax: float = None
    DistMin: float = None
    DistMax: float = None


class GeometryMultipole(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    with_iron_yoke: bool = None


class MeshMultipole(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    default_mesh: bool = None
    mesh_iron: Threshold = Threshold()
    mesh_coil: Threshold = Threshold()
    MeshSizeMin: float = None  # sets gmsh Mesh.MeshSizeMin
    MeshSizeMax: float = None  # sets gmsh Mesh.MeshSizeMax
    MeshSizeFromCurvature: float = None  # sets gmsh Mesh.MeshSizeFromCurvature
    Algorithm: int = None  # sets gmsh Mesh.Algorithm
    AngleToleranceFacetOverlap: float = None  # sets gmsh Mesh.AngleToleranceFacetOverlap
    ElementOrder: int = None  # sets gmsh Mesh.ElementOrder
    Optimize: int = None  # sets gmsh Mesh.Optimize


class SolveMultipoleFiQuS(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    I_initial: List[float] = None
    pro_template: str = None  # file name of .pro template file


class PostProcMultipole(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    compare_to_ROXIE: str = None
    plot_all: str = None
    variables: List[str] = None  # Name of variables to post-process, like "b" for magnetic flux density
    volumes: List[str] = None  # Name of domains to post-process, like "powered"
    file_exts: List[str] = None  # Name of file extensions to output to, like "pos"
    additional_outputs: List[str] = None  # Name of software specific input files to prepare, like "LEDET3D"


class MPDM(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    type: Literal['multipole'] = 'multipole'
    geometry: GeometryMultipole = GeometryMultipole()
    mesh: MeshMultipole = MeshMultipole()
    solve: SolveMultipoleFiQuS = SolveMultipoleFiQuS()
    postproc: PostProcMultipole = PostProcMultipole()
