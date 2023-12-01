from pydantic import BaseModel
from typing import List


class Terminal(BaseModel):
    vol_st: List[int] = None  # volume number for terminal in for straightening
    surf_st: List[int] = None  # surface number for terminal in for straightening
    vol_et: List[int] = None  # volume number for terminal in for extending
    surf_et: List[int] = None  # surface number for terminal in for extending
    lc_st: List[List[List[int]]] = None  # line connections for straightening terminals
    lc_et: List[List[List[int]]] = None  # line connections for extending terminals
    z_air: float = None
    z_add: float = None
    ndpterms: List[int] = None  # number of divisions per terminal


class Winding(BaseModel):
    names: List[str] = None  # name to use in gmsh and getdp
    t_in: Terminal = Terminal()     # Terminal in
    t_out: Terminal = Terminal()    # Terminal in


class WindingsInformation(BaseModel):
    magnet_name: str = None
    windings_avg_length: float = None
    windings: Winding = Winding()
    w_names: List[str] = None
    f_names: List[str] = None
    formers: List[str] = None
    air: str = None


class SpliterBrep(BaseModel):  # Brep file model splitter data
    magnet_name: str = None
    file_name: str = None           # full file name for the brep file
    vol_firsts: List[int] = None    # list of first volumes for the partitioned model
    vol_lasts: List[int] = None      # list of last volumes for the partitioned model
