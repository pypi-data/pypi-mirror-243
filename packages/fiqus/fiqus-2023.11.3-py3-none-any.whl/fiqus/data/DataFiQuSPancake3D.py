from pydantic import (
    BaseModel,
    PositiveFloat,
    NonNegativeFloat,
    PositiveInt,
    Field,
    validator,
    root_validator,
)
from typing import List, Literal, Union, Optional
import math
import logging
import os
import csv
import scipy
import matplotlib

logger = logging.getLogger(__name__)


# ======================================================================================
# FUNDAMENTAL CLASSES STARTS ===========================================================
# ======================================================================================
class Pancake3DPosition(BaseModel):
    # 1) User inputs:

    # Optionals:
    x: float = Field(
        default=None,
        title="x coordinate",
        description="x coordinate of the position.",
    )
    y: float = Field(
        default=None,
        title="y coordinate",
        description="y coordinate of the position.",
    )
    z: float = Field(
        default=None,
        title="z coordinate",
        description="z coordinate of the position.",
    )
    turnNumber: PositiveFloat = Field(
        default=None,
        title="Turn Number",
        description="Winding turn number as a position input.",
    )
    whichPancakeCoil: PositiveInt = Field(
        default=None,
        title="Pancake Coil Number",
        description="The first pancake coil is 1, the second is 2, etc.",
    )


# ======================================================================================
# FUNDAMENTAL CLASSES ENDS =============================================================
# ======================================================================================


# ======================================================================================
# GEOMETRY CLASSES STARTS ==============================================================
# ======================================================================================


class Pancake3DGeometryWinding(BaseModel):
    # 1) User inputs:

    # Mandatory:
    r_i: PositiveFloat = Field(
        alias="innerRadius",
        title="Inner Radius",
        description="Inner radius of the winding.",
    )
    t: PositiveFloat = Field(
        alias="thickness",
        title="Winding Thickness",
        description="Thickness of the winding.",
    )
    N: float = Field(
        alias="numberOfTurns",
        ge=3,
        title="Number of Turns",
        description="Number of turns of the winding.",
    )
    h: PositiveFloat = Field(
        alias="height",
        title="Winding Height",
        description="Height/width of the winding.",
    )

    # Optionals:
    name: str = Field(
        default="winding",
        title="Winding Name",
        description="The The name to be used in the mesh..",
        examples=["winding", "myWinding"],
    )
    NofVolPerTurn: int = Field(
        default=2,
        alias="numberOfVolumesPerTurn",
        ge=2,
        title="Number of Volumes Per Turn (Advanced Input)",
        description="The number of volumes per turn (CAD related, not physical).",
    )
    theta_i: float = Field(
        default=0.0,
        alias="startAngle",
        title="Start Angle",
        description="The start angle of the first pancake coil in radians.",
    )

    # 2) To be calculated:
    r_o: PositiveFloat = Field(
        default=None,
        alias="outerRadius",
        description="outer radius of the winding (calculated by FiQuS)",
    )
    turnTol: PositiveFloat = Field(
        default=None,
        alias="turnTolerance",
        description="turn tolerance (CAD related, not physical) (calculated by FiQuS)",
    )
    spt: PositiveFloat = Field(
        default=None,
        alias="sectionsPerTurn",
        description=(
            "sections per turn (CAD related, not physical) (calculated by FiQuS)"
        ),
    )
    totalTapeLength: PositiveFloat = Field(
        default=None,
        description="total length of the winding (calculated by FiQuS)",
    )

    @validator("NofVolPerTurn", allow_reuse=True)
    @classmethod
    def check_NofVolPerTurn(cls, value):
        """
        Checks if the number of volumes per turn is greater than 2.

        :param cls: class
        :type cls: class
        :param value: number of volumes per turn
        :type value: int
        :return: number of volumes per turn
        :rtype: int
        """
        if value < 2:
            raise ValueError("Number of volumes per turn must be greater than 2!")

        return value

    @validator("N", allow_reuse=True)
    @classmethod
    def check_N(cls, value):
        """
        Checks if the number of turns is equal to or greater than 3.

        :param cls: class
        :type cls: class
        :param value: number of turns
        :type value: float
        :return: number of turns
        :rtype: float
        """
        if value < 3:
            raise ValueError("Number of turns must be equal to or greater than 3!")
        return value


class Pancake3DGeometryContactLayer(BaseModel):
    # 1) User inputs:

    # Mandatory:
    tsa: bool = Field(
        alias="thinShellApproximation",
        title="Use Thin Shell Approximation",
        description=(
            "If True, the contact layer will be modeled with 2D shell elements (thin"
            " shell approximation), and if False, the contact layer will be modeled"
            " with 3D elements."
        ),
    )
    t: PositiveFloat = Field(
        alias="thickness",
        title="Contact Layer Thickness",
        description="Thickness of the contact layer.",
    )

    # Optionals:
    name: str = Field(
        default="contactLayer",
        title="Contact Layer Name",
        description="The name to be used in the mesh.",
        examples=["myContactLayer"],
    )


class Pancake3DGeometryTerminal(BaseModel):
    # 1) User inputs:

    # Mandatory:
    name: str = Field(
        title="Terminal Name",
        description="The name to be used in the mesh.",
        examples=["innerTerminal", "outerTeminal"],
    )
    t: PositiveFloat = Field(
        alias="thickness",
        title="Terminal Thickness",
        description="Thickness of the terminal's tube.",
    )  # thickness

    # 2) To be calculated:
    r: PositiveFloat = Field(
        default=None,
        alias="radius",
        description=(
            "inner radius of the inner terminal or outer radius of the outer terminal"
            " (calculated by FiQuS)"
        ),
    )


class Pancake3DGeometryTerminals(BaseModel):
    # 1) User inputs:
    i: Pancake3DGeometryTerminal = Field(alias="inner")
    o: Pancake3DGeometryTerminal = Field(alias="outer")

    # Optionals:
    firstName: str = Field(
        default="firstTerminal", description="name of the first terminal"
    )
    lastName: str = Field(
        default="lastTerminal", description="name of the last terminal"
    )


class Pancake3DGeometryAir(BaseModel):
    # 1) User inputs:

    # Mandatory:
    r: PositiveFloat = Field(
        default=None,
        alias="radius",
        title="Air Radius",
        description="Radius of the air (for cylinder type air).",
    )
    a: PositiveFloat = Field(
        default=None,
        alias="sideLength",
        title="Air Side Length",
        description="Side length of the air (for cuboid type air).",
    )
    margin: PositiveFloat = Field(
        alias="axialMargin",
        title="Axial Margin of the Air",
        description=(
            "Axial margin between the ends of the air and first/last pancake coils."
        ),
    )  # axial margin

    # Optionals:
    name: str = Field(
        default="air",
        title="Air Name",
        description="The name to be used in the mesh.",
        examples=["air", "myAir"],
    )
    type: Literal["cylinder", "cuboid"] = Field(
        default="cylinder",
        title="Air Type",
        description="Air can be a cylinder or cuboid.",
    )
    shellTransformation: bool = Field(
        default=False,
        alias="shellTransformation",
        title="Use Shell Transformation",
        description=(
            "Generate outer shell air to apply shell transformation if True (GetDP"
            " related, not physical)"
        ),
    )
    shellTransformationMultiplier: float = Field(
        default=1.2,
        gt=1,
        alias="shellTransformationMultiplier",
        title="Shell Transformation Multiplier (Advanced Input)",
        description=(
            "multiply the air's outer dimension by this value to get the shell's outer"
            " dimension"
        ),
    )
    cutName: str = Field(
        default="Air-Cut",
        title="Air Cut Name",
        description="name of the cut (cochain) to be used in the mesh",
        examples=["Air-Cut", "myAirCut"],
    )
    shellVolumeName: str = Field(
        default="air-Shell",
        title="Air Shell Volume Name",
        description="name of the shell volume to be used in the mesh",
        examples=["air-Shell", "myAirShell"],
    )
    fragment: bool = Field(
        default=False,
        alias="generateGapAirWithFragment",
        title="Generate Gap Air with Fragment (Advanced Input)",
        description=(
            "generate the gap air with gmsh/model/occ/fragment if true (CAD related,"
            " not physical)"
        ),
    )

    # 2) To be calculated:
    h: PositiveFloat = Field(
        default=None,
        alias="height",
        description="total height of the air (calculated by FiQuS)",
    )
    shellOuterRadius: PositiveFloat = Field(
        default=None,
        description="outer radius of the cylinder shell (calculated by FiQuS)",
    )
    shellSideLength: PositiveFloat = Field(
        default=None,
        description="side length of the cuboid shell (calculated by FiQuS)",
    )

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_and_calculate_air(cls, values):
        """
        Checks if the radius or side length is specified for the air.

        :param cls: class
        :type cls: class
        :param values: dictionary of air
        :type values: dict
        :return: dictionary of air
        :rtype: dict
        """

        # If type is cylinder r must be specified, otherwise a must be specified:
        if values["type"] == "cylinder":
            if values["r"] is None:
                raise ValueError("Radius must be specified for air!")

        elif values["type"] == "cuboid":
            if values["a"] is None:
                raise ValueError("Side length must be specified for air!")

        # Calculate shell transformation
        if values["shellTransformation"]:
            if values["type"] == "cylinder":
                values["shellOuterRadius"] = (
                    values["shellTransformationMultiplier"] * values["r"]
                )
            elif values["type"] == "cuboid":
                values["shellSideLength"] = (
                    values["shellTransformationMultiplier"] * values["a"]
                )

        return values

    @validator("shellTransformationMultiplier", allow_reuse=True)
    @classmethod
    def check_shellTransformationMultiplier(cls, value):
        """
        Checks if the shell transformation multiplier is greater than 1.

        :param cls: class
        :type cls: class
        :param value: shell transformation multiplier
        :type value: float
        :return: shell transformation multiplier
        :rtype: float
        """

        if value <= 1:
            raise ValueError("Shell transformation multiplier must be greater than 1!")

        return value


# ======================================================================================
# GEOMETRY CLASSES ENDS ================================================================
# ======================================================================================


# ======================================================================================
# MESH CLASSES STARTS ==================================================================
# ======================================================================================
class Pancake3DMeshWinding(BaseModel):
    # 1) User inputs:

    # Mandatory:
    axne: Union[List[PositiveInt], PositiveInt] = Field(
        alias="axialNumberOfElements",
        title="Axial Number of Elements",
        description=(
            "The number of axial elements for the whole height of the coil. It can be"
            " either a list of integers to specify the value for each pancake coil"
            " separately or an integer to use the same setting for each pancake coil."
        ),
    )

    ane: Union[List[PositiveInt], PositiveInt] = Field(
        alias="azimuthalNumberOfElementsPerTurn",
        title="Azimuthal Number of Elements Per Turn",
        description=(
            "The number of azimuthal elements per turn of the coil. It can be either a"
            " list of integers to specify the value for each pancake coil separately or"
            " an integer to use the same setting for each pancake coil."
        ),
    )

    rne: Union[List[PositiveInt], PositiveInt] = Field(
        alias="radialNumberOfElementsPerTurn",
        title="Winding Radial Number of Elements Per Turn",
        description=(
            "The number of radial elements per tape of the winding. It can be either a"
            " list of integers to specify the value for each pancake coil separately or"
            " an integer to use the same setting for each pancake coil."
        ),
    )

    # Optionals:
    axbc: Union[List[PositiveFloat], PositiveFloat] = Field(
        default=[1],
        alias="axialDistributionCoefficient",
        title="Axial Bump Coefficients",
        description=(
            "If 1, it won't affect anything. If smaller than 1, elements will get finer"
            " in the axial direction at the ends of the coil. If greater than 1,"
            " elements will get coarser in the axial direction at the ends of the coil."
            " It can be either a list of floats to specify the value for each pancake"
            " coil separately or a float to use the same setting for each pancake coil."
        ),
    )

    elementType: Union[
        List[Literal["tetrahedron", "hexahedron", "prism"]],
        Literal["tetrahedron", "hexahedron", "prism"],
    ] = Field(
        default=["tetrahedron"],
        title="Element Type",
        description=(
            "The element type of windings and contact layers. It can be either a"
            " tetrahedron, hexahedron, or a prism. It can be either a list of strings"
            " to specify the value for each pancake coil separately or a string to use"
            " the same setting for each pancake coil."
        ),
    )


class Pancake3DMeshContactLayer(BaseModel):
    # 1) User inputs:

    # Mandatory:

    rne: List[PositiveInt] = Field(
        alias="radialNumberOfElementsPerTurn",
        title="Contact Layer Radial Number of Elements Per Turn",
        description=(
            "The number of radial elements per tape of the contact layer. It can be"
            " either a list of integers to specify the value for each pancake coil"
            " separately or an integer to use the same setting for each pancake coil."
        ),
    )


class Pancake3DMeshAirAndTerminals(BaseModel):
    # 1) User inputs:

    # Optionals:
    structured: bool = Field(
        default=False,
        title="Structure Mesh",
        description=(
            "If True, the mesh will be structured. If False, the mesh will be"
            " unstructured."
        ),
    )
    radialElementSize: PositiveFloat = Field(
        default=1,
        title="Radial Element Size",
        description=(
            "If structured mesh is used, the radial element size can be set. It is the"
            " radial element size in terms of the winding's radial element size."
        ),
    )


# ======================================================================================
# MESH CLASSES ENDS ====================================================================
# ======================================================================================

# ======================================================================================
# SOLVE CLASSES STARTS =================================================================
# ======================================================================================


class Pancake3DSolveAir(BaseModel):
    # 1) User inputs:

    # Mandatory:
    permeability: PositiveFloat = Field(
        title="Permeability of Air",
        description="Permeability of air.",
    )


class Pancake3DSolveIcVsLength(BaseModel):
    lengthValues: List[float] = Field(
        title="Tape Length Values",
        description="Tape length values that corresponds to criticalCurrentValues.",
    )
    criticalCurrentValues: List[float] = Field(
        title="Critical Current Values",
        description="Critical current values that corresponds to lengthValues.",
    )


class Pancake3DSolveCERNSuperConductorMaterial(BaseModel):
    # 1) User inputs:

    # Mandatory:
    name: Literal["HTSSuperPower"] = Field(
        title="Superconductor Material Name",
        description="Name of the superconductor material.",
    )
    IcAtTinit: Union[PositiveFloat, str, Pancake3DSolveIcVsLength] = Field(
        alias="criticalCurrentAtInitialTemperature",
        title="Critical Current at Initial Temperature",
        description=(
            "Critical current at initial temperature. The critical current value will"
            " change with temperature depending on the superconductor material.\nEither"
            " the same critical current for the whole tape or the critical current with"
            " respect to the tape length can be specified. To specify the same critical"
            " current for the entire tape, just use a scalar. To specify critical"
            " current with respect to the tape length: a CSV file can be used, or"
            " lengthValues and criticalCurrentValues can be given as lists. The data"
            " will be linearly interpolated.\nIf a CSV file is to be used, the input"
            " should be the name of a CSV file (which is in the same folder as the"
            " input file) instead of a scalar. The first column of the CSV file will be"
            " the tape length, and the second column will be the critical current."
        ),
        examples=[230, "IcVSlength.csv"],
    )
    nValue: PositiveFloat = Field(
        default=30,
        alias="N-Value for E-J Power Law",
        description="N-value for E–J power law.",
    )

    # Optionals:
    relativeThickness: float = Field(
        default=None,
        le=1,
        title="Relative Thickness (only for winding)",
        description=(
            "Winding tapes generally consist of more than one material. Therefore, when"
            " materials are given as a list in winding, their relative thickness,"
            " (thickness of the material) / (thickness of the winding), should be"
            " specified."
        ),
    )

    jCriticalScalingNormalToWinding: PositiveFloat = Field(
        default=1,
        title="Critical Current Scaling Normal to Winding",
        description=(
            "Critical current scaling normal to winding, i.e., along the c_axis. "
            " We have Jc_cAxis = scalingFactor * Jc_abPlane."
            " A factor of 1 means no scaling such that the HTS layer is isotropic."
        ),
    )

    electricFieldCriterion: PositiveFloat = Field(
        default=1e-4,
        title="Electric Field Criterion",
        description=(
            "The electric field that defines the critical current density, i.e., the"
            " electric field at which the current density reaches the critical current"
            " density."
        ),
    )

    # 2) To be calculated:
    IcValues: List[float] = Field(
        default=None,
        description=(
            "Critical current values for corresponding tape lengths read from the CSV"
            " file (calculated by FiQuS)."
        ),
    )
    lengthValues: List[float] = Field(
        default=None,
        description=(
            "Tape lengths for corresponding critical current values read from the CSV"
            " file (calculated by FiQuS)."
        ),
    )
    getdpCriticalCurrentDensityFunction: str = Field(
        default=None,
        description=(
            "GetDP function name of the material's critical current density (calculated"
            " by FiQuS)"
        ),
    )

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def assign_getdpFunction(cls, values):
        """ """
        functionNames = {
            "HTSSuperPower": "CFUN_HTS_JcFit_SUPERPOWER_T_B_theta",
        }

        values["getdpCriticalCurrentDensityFunction"] = functionNames[values["name"]]

        return values


class Pancake3DSolveCERNPlating(BaseModel):
    # Mandatory:
    name: Literal["Copper"] = Field(
        title="Material Name",
        description="choices: Copper",
    )

    relativeWidth: float = Field(
        default=0,
        title="Relative width of plating",
        le=1,
        description=(
            "HTS 2G coated conductor are typically plated, usually "
            " using copper. The relative width of the plating is the "
            " width of the plating divided by the width of the tape. "
            " 0 means no plating."
        ),
    )


class Pancake3DSolveCERNNormalMaterial(BaseModel):
    # 1) User inputs:

    # Mandatory:
    name: Literal["Copper", "Hastelloy", "Silver", "Indium", "Stainless Steel"] = Field(
        title="Material Name",
        description="choices: Copper, Hastelloy, Silver, Indium, Stainless Steel",
    )

    # Optionals:
    relativeThickness: float = Field(
        default=None,
        le=1,
        title="Relative Thickness (only for winding)",
        description=(
            "Winding tapes generally consist of more than one material. Therefore, when"
            " materials are given as a list in winding, their relative thickness,"
            " (thickness of the material) / (thickness of the winding), should be"
            " specified."
        ),
    )
    rrr: PositiveFloat = Field(
        default=100,
        alias="residualResistanceRatio",
        title="Residual Resistance Ratio",
        description=(
            "Residual-resistivity ratio (also known as Residual-resistance ratio or"
            " just RRR) is the ratio of the resistivity of a material at reference"
            " temperature and at 0 K."
        ),
    )
    rrrRefT: PositiveFloat = Field(
        default=295,
        alias="residualResistanceRatioReferenceTemperature",
        title="Residual Resistance Ratio Reference Temperature",
        description="Reference temperature for residual resistance ratio",
    )

    # 2) To be calculated:
    resistivityMacroName: str = Field(
        default=None,
        description=(
            "GetDP function name of the material's resistivity (calculated by FiQuS)"
        ),
    )
    thermalConductivityMacroName: str = Field(
        default=None,
        description=(
            "GetDP function name of the material's thermal conductivity (calculated by"
            " FiQuS)"
        ),
    )
    heatCapacityMacroName: str = Field(
        default=None,
        description=(
            "GetDP function name of the material's heat capacity (calculated by FiQuS)"
        ),
    )

    getdpTSAMassResistivityFunction: str = Field(
        default=None,
        description=(
            "GetDP function name of the shell material's mass resistivity (calculated"
            " by FiQuS)"
        ),
    )

    getdpTSAStiffnessResistivityFunction: str = Field(
        default=None,
        description=(
            "GetDP function name of the shell material's stiffness resistivity"
            " (calculated by FiQuS)"
        ),
    )

    getdpTSAMassThermalConductivityFunction: str = Field(
        default=None,
        description=(
            "GetDP function name of the shell material's mass thermal conductivity"
            " (calculated by FiQuS)"
        ),
    )

    getdpTSAStiffnessThermalConductivityFunction: str = Field(
        default=None,
        description=(
            "GetDP function name of the shell material's stiffness thermal conductivity"
            " (calculated by FiQuS)"
        ),
    )

    getdpTSAMassHeatCapacityFunction: str = Field(
        default=None,
        description=(
            "GetDP function name of the shell material's mass heat capacity (calculated"
            " by FiQuS)"
        ),
    )

    getdpTSARHSFunction: str = Field(
        default=None,
        description=(
            "GetDP function name of the shell material's RHS (calculated by FiQuS)"
        ),
    )

    getdpTSATripleFunction: str = Field(
        default=None,
        description=(
            "GetDP function name of the shell material's triple (calculated by FiQuS)"
        ),
    )

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def assign_normal_getdp_functions(cls, values):
        """ """
        resistivityMacroNames = {
            "Copper": "MATERIAL_Resistivity_Copper_T_B",
            "Hastelloy": "MATERIAL_Resistivity_Hastelloy_T",
            "Silver": "MATERIAL_Resistivity_Silver_T_B",
            "Indium": "MATERIAL_Resistivity_Indium_T",
            "Stainless Steel": "MATERIAL_Resistivity_SSteel_T",
        }
        thermalConductivityMacroNames = {
            "Copper": "MATERIAL_ThermalConductivity_Copper_T_B",
            "Hastelloy": "MATERIAL_ThermalConductivity_Hastelloy_T",
            "Silver": "MATERIAL_ThermalConductivity_Silver_T",
            "Indium": "MATERIAL_ThermalConductivity_Indium_T",
            "Stainless Steel": "MATERIAL_ThermalConductivity_SSteel_T",
        }
        heatCapacityMacroNames = {
            "Copper": "MATERIAL_SpecificHeatCapacity_Copper_T",
            "Hastelloy": "MATERIAL_SpecificHeatCapacity_Hastelloy_T",
            "Silver": "MATERIAL_SpecificHeatCapacity_Silver_T",
            "Indium": "MATERIAL_SpecificHeatCapacity_Indium_T",
            "Stainless Steel": "MATERIAL_SpecificHeatCapacity_SSteel_T",
        }

        if values["name"] in resistivityMacroNames:
            values["resistivityMacroName"] = resistivityMacroNames[values["name"]]
        if values["name"] in thermalConductivityMacroNames:
            values["thermalConductivityMacroName"] = thermalConductivityMacroNames[
                values["name"]
            ]
        if values["name"] in heatCapacityMacroNames:
            values["heatCapacityMacroName"] = heatCapacityMacroNames[values["name"]]

        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def assign_TSA_getdp_functions(cls, values):
        resistivityMassFunctionNames = {
            "Indium": "TSA_CFUN_rhoIn_T_constantThickness_mass",
            "Stainless Steel": None,
        }
        resistivityStiffnessFunctionNames = {
            "Indium": "TSA_CFUN_rhoIn_T_constantThickness_stiffness",
            "Stainless Steel": None,
        }
        thermalConductivityMassFunctionNames = {
            "Indium": "TSA_CFUN_kIn_constantThickness_mass",
            "Stainless Steel": "TSA_CFUN_kSteel_T_constantThickness_mass",
        }
        thermalConductivityStiffnessFunctionNames = {
            "Indium": "TSA_CFUN_kIn_constantThickness_stiffness",
            "Stainless Steel": "TSA_CFUN_kSteel_T_constantThickness_stiffness",
        }
        heatCapacityMassFunctionNames = {
            "Indium": "TSA_CFUN_CvIn_constantThickness_mass",
            "Stainless Steel": "TSA_CFUN_CvSteel_T_constantThickness_mass",
        }
        rhsFunctionNames = {
            "Indium": "TSA_CFUN_rhoIn_T_constantThickness_rhs",
            "Stainless Steel": None,
        }
        tripleFunctionNames = {
            "Indium": "TSA_CFUN_rhoIn_T_constantThickness_triple",
            "Stainless Steel": None,
        }

        if values["name"] in resistivityMassFunctionNames:
            values["getdpTSAMassResistivityFunction"] = resistivityMassFunctionNames[
                values["name"]
            ]
        if values["name"] in resistivityStiffnessFunctionNames:
            values[
                "getdpTSAStiffnessResistivityFunction"
            ] = resistivityStiffnessFunctionNames[values["name"]]
        if values["name"] in thermalConductivityMassFunctionNames:
            values[
                "getdpTSAMassThermalConductivityFunction"
            ] = thermalConductivityMassFunctionNames[values["name"]]

        if values["name"] in thermalConductivityStiffnessFunctionNames:
            values[
                "getdpTSAStiffnessThermalConductivityFunction"
            ] = thermalConductivityStiffnessFunctionNames[values["name"]]

        if values["name"] in heatCapacityMassFunctionNames:
            values["getdpTSAMassHeatCapacityFunction"] = heatCapacityMassFunctionNames[
                values["name"]
            ]

        if values["name"] in rhsFunctionNames:
            values["getdpTSARHSFunction"] = rhsFunctionNames[values["name"]]

        if values["name"] in tripleFunctionNames:
            values["getdpTSATripleFunction"] = tripleFunctionNames[values["name"]]

        return values


class Pancake3DSolveMaterial(BaseModel):
    # 1) User inputs:

    # Mandatory:

    # Optionals:
    numberOfThinShellElements: PositiveInt = Field(
        default=1,
        title="Number of Thin Shell Elements (Advanced Input)",
        description=(
            "Number of thin shell elements in the FE formulation (GetDP related, not"
            " physical and only used when TSA is set to True)"
        ),
    )
    resistivity: PositiveFloat = Field(
        default=None,
        title="Resistivity",
        description=(
            "A scalar value. If this is given, material properties won't be used for"
            " resistivity."
        ),
    )
    thermalConductivity: PositiveFloat = Field(
        default=None,
        title="Thermal Conductivity",
        description=(
            "A scalar value. If this is given, material properties won't be used for"
            " thermal conductivity."
        ),
    )
    specificHeatCapacity: PositiveFloat = Field(
        default=None,
        title="Specific Heat Capacity",
        description=(
            "A scalar value. If this is given, material properties won't be used for"
            " specific heat capacity."
        ),
    )
    material: Pancake3DSolveCERNNormalMaterial = Field(
        default=None,
        title="Material",
        description="Material from CERN material library.",
    )

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_if_all_the_material_properties_are_given(cls, values):
        """ """
        if values["material"] is None:
            if not (
                values["resistivity"]
                and values["thermalConductivity"]
                and values["specificHeatCapacity"]
            ):
                raise ValueError(
                    "Resistivity, thermal conductivity, and specific heat capacity must"
                    " be specified if material is not specified!"
                )

        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_if_more_than_one_property_is_given(cls, values):
        """ """
        if values["material"]:
            if values["resistivity"]:
                logger.warning(
                    f"Constant resistivity value ({values['resistivity']}) will be used"
                    f" instead of the nonlinear {values['material'].name}'s"
                    " resistivity!"
                )
            if values["thermalConductivity"]:
                logger.warning(
                    "Constant thermal conductivity value"
                    f" ({values['thermalConductivity']}) will be used instead of the"
                    f" nonlinear {values['material'].name}'s thermal conductivity!"
                )
            if values["specificHeatCapacity"]:
                logger.warning(
                    "Constant specific heat capacity value"
                    f" ({values['specificHeatCapacity']}) will be used instead of the"
                    f" nonlinear {values['material'].name}'s specific heat capacity!"
                )

        return values


class Pancake3DSolveContactLayerMaterial(Pancake3DSolveMaterial):
    resistivity: Union[PositiveFloat, Literal["perfectlyInsulating"]] = Field(
        default=None,
        title="Resistivity",
        description=(
            'A scalar value or "perfectlyInsulating". If "perfectlyInsulating" is'
            " given, the contact layer will be perfectly insulating. If this value is"
            " given, material properties won't be used for resistivity."
        ),
    )


class Pancake3DSolveTerminalMaterialAndBoundaryCondition(Pancake3DSolveMaterial):
    cooling: Literal["adiabatic", "fixedTemperature", "cryocooler"] = Field(
        default="fixedTemperature",
        title="Cooling condition",
        description=(
            "Cooling condition of the terminal. It can be either adiabatic, fixed"
            " temperature, or cryocooler."
        ),
    )


class Pancake3DSolveWindingMaterial(BaseModel):
    # 1) User inputs:

    # Mandatory:

    # Optionals:
    resistivity: PositiveFloat = Field(
        default=None,
        title="Resistivity",
        description=(
            "A scalar value. If this is given, material properties won't be used for"
            " resistivity."
        ),
    )
    thermalConductivity: PositiveFloat = Field(
        default=None,
        title="Thermal Conductivity",
        description=(
            "A scalar value. If this is given, material properties won't be used for"
            " thermal conductivity."
        ),
    )
    specificHeatCapacity: PositiveFloat = Field(
        default=None,
        title="Specific Heat Capacity",
        description=(
            "A scalar value. If this is given, material properties won't be used for"
            " specific heat capacity."
        ),
    )
    minimumPossibleResistivity: NonNegativeFloat = Field(
        default=0,
        title="Minimum Possible Resistivity",
        description=(
            "The resistivity of the winding won't be lower than this value, no matter"
            " what."
        ),
    )
    maximumPossibleResistivity: PositiveFloat = Field(
        default=1,
        title="Maximum Possible Resistivity",
        description=(
            "The resistivity of the winding won't be higher than this value, no matter"
            " what."
        ),
    )
    material: List[
        Union[
            Pancake3DSolveCERNNormalMaterial, Pancake3DSolveCERNSuperConductorMaterial
        ]
    ] = Field(
        default=None,
        title="Winding Material",
        description=(
            "Because generally winding tapes consist of more than one material,"
            " materials should be given as a list of Material dictionaries."
        ),
    )

    plating: Pancake3DSolveCERNPlating = Field(
        default=Pancake3DSolveCERNPlating(name="Copper", relativeWidth=0),
        title="Tape plating",
        description=(
            "The plating of the winding tape. Only copper is supported for now."
            "By default, the tape is not plated."
        ),
    )

    # 2) To be calculated:
    relativeThicknessOfNormalConductor: PositiveFloat = Field(
        default=None,
        description=(
            "(thickness of the normal conductor) / (thickness of the winding)"
            " (calculated by FiQuS)"
        ),
    )
    relativeThicknessOfSuperConductor: PositiveFloat = Field(
        default=None,
        description=(
            "(thickness of the normal conductor) / (thickness of the winding)"
            " (calculated by FiQuS)"
        ),
    )
    normalConductors: List[Pancake3DSolveCERNNormalMaterial] = Field(
        default=None, description="list of normal conductors (calculated by FiQuS)"
    )
    superConductor: Pancake3DSolveCERNSuperConductorMaterial = Field(
        default=None, description="super conductor used (calculated by FiQuS)"
    )

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_if_all_the_material_properties_are_given(cls, values):
        """ """
        if values["material"] is None:
            if not (
                values["resistivity"]
                and values["thermalConductivity"]
                and values["specificHeatCapacity"]
            ):
                raise ValueError(
                    "Resistivity, thermal conductivity, and specific heat capacity must"
                    " be specified if material is not specified!"
                )

        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def calculate_relative_thicknesses(cls, values):
        """ """

        totalNormalConductorThickness = 0
        if values["material"]:
            for material in values["material"]:
                if isinstance(material, Pancake3DSolveCERNNormalMaterial):
                    totalNormalConductorThickness = (
                        totalNormalConductorThickness + material.relativeThickness
                    )

            values["relativeThicknessOfNormalConductor"] = totalNormalConductorThickness
            values["relativeThicknessOfSuperConductor"] = (
                1 - totalNormalConductorThickness
            )

        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def create_normal_and_super_conductor_lists(cls, values):
        """ """
        if values["material"]:
            values["normalConductors"] = []
            values["superConductor"] = None
            for material in values["material"]:
                if isinstance(material, Pancake3DSolveCERNNormalMaterial):
                    values["normalConductors"].append(material)
                else:
                    if values["superConductor"] is not None:
                        raise ValueError("Only one super conductor must be specified!")
                    values["superConductor"] = material

        return values

    @validator("material", allow_reuse=True)
    @classmethod
    def check_material(cls, value):
        """"""
        if value is not None:
            totalRelativeThickness = 0
            for material in value:
                if material.relativeThickness is None:
                    raise ValueError(
                        "Relative thickness must be specified for winding material!"
                    )
                totalRelativeThickness = (
                    totalRelativeThickness + material.relativeThickness
                )

            if not math.isclose(totalRelativeThickness, 1):
                raise ValueError(
                    "Sum of the relative thicknesses of the winding materials must be"
                    " equal to 1!"
                )

        return value

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_if_more_than_one_property_is_given(cls, values):
        """ """
        if values["material"]:
            if values["resistivity"]:
                logger.warning(
                    f"Constant resistivity value ({values['resistivity']}) will be used"
                    " instead of the nonlinear"
                    f" {', '.join([material.name for material in values['material']])}'s"
                    " resistivity!"
                )
            if values["thermalConductivity"]:
                logger.warning(
                    "Constant thermal conductivity value"
                    f" ({values['thermalConductivity']}) will be used instead of the"
                    " nonlinear"
                    f" {', '.join([material.name for material in values['material']])}'s"
                    " thermal conductivity!"
                )
            if values["specificHeatCapacity"]:
                logger.warning(
                    "Constant specific heat capacity value"
                    f" ({values['specificHeatCapacity']}) will be used instead of the"
                    " nonlinear"
                    f" {', '.join([material.name for material in values['material']])}'s"
                    " specific heat capacity!"
                )

        return values


class Pancake3DSolveTolerance(BaseModel):
    # 1) User inputs:

    # Mandatory:
    quantity: Literal[
        "solutionVector",
        "totalResistiveHeating",
        "voltageBetweenTerminals",
        "resistiveHeating",
        "temperature",
        "magnitudeOfCurrentDensity",
        "magnitudeOfMagneticField",
        "axialComponentOfTheMagneticField",
        "currentThroughCoil",
        "magnitudeOfHeatFlux",
        "magneticEnergy",
    ] = Field(
        title="Quantity",
        description="Name of the quantity for tolerance.",
    )
    relative: NonNegativeFloat = Field(
        title="Relative Tolerance",
        description="Relative tolerance for the quantity.",
    )
    absolute: NonNegativeFloat = Field(
        title="Absolute Tolerance", description="Absolute tolerance for the quantity"
    )

    # Optionals:
    position: Pancake3DPosition = Field(
        default=None,
        title="Probing Position of the Quantity",
        description="Probing position of the quantity for tolerance.",
    )
    normType: Literal[
        "L1Norm", "MeanL1Norm", "L2Norm", "MeanL2Norm", "LinfNorm"
    ] = Field(
        default="L2Norm",
        alias="normType",
        title="Norm Type",
        description=(
            "Sometimes, tolerances return a vector instead of a scalar (ex,"
            " solutionVector). Then, the magnitude of the tolerance should be"
            " calculated with a method. Norm type selects this method."
        ),
    )

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_if_position_is_required(clas, values):
        """ """
        positionRequiredQuantities = [
            "resistiveHeating",
            "temperature",
            "magnitudeOfCurrentDensity",
            "magnitudeOfMagneticField",
            "axialComponentOfTheMagneticField",
            "magnitudeOfHeatFlux",
        ]
        if values["quantity"] in positionRequiredQuantities:
            if values["position"] is None:
                raise ValueError(
                    f"Position must be specified for {values['quantity']} tolerance!"
                )
            else:
                coordinatesAreGiven = False
                if (
                    values["position"].x is not None
                    and values["position"].y is not None
                    and values["position"].z is not None
                ):
                    coordinatesAreGiven = True

                turnNumberIsGiven = False
                if values["position"].turnNumber is not None:
                    turnNumberIsGiven = True

                if coordinatesAreGiven and turnNumberIsGiven:
                    raise ValueError(
                        "Either xyz-coordinates or turn number can be specified!"
                    )
                elif turnNumberIsGiven:
                    if (
                        values["position"].x
                        or values["position"].y
                        or values["position"].z
                    ):
                        raise ValueError(
                            "Either turn number or x, y, and z coordinates can be"
                            " specified!"
                        )
                elif coordinatesAreGiven:
                    pass
                else:
                    raise ValueError(
                        "x, y, and z coordinates or turn number must be specified"
                        " for position!"
                    )

        return values

    @validator("quantity", allow_reuse=True)
    @classmethod
    def quantity_specific_warnings(cls, value):
        if value == "totalResistiveHeating":
            logger.warning(
                "Calculation of total resistive heating might be slow for tolerances!"
            )

        return value


class Pancake3DSolveAdaptiveTimeLoopSettings(BaseModel):
    # 1) User inputs:

    # Mandatory:
    initialStep: PositiveFloat = Field(
        default=None,
        alias="initialStep",
        title="Initial Step for Adaptive Time Stepping",
        description="Initial step for adaptive time stepping",
    )
    minimumStep: PositiveFloat = Field(
        default=None,
        alias="minimumStep",
        title="Minimum Step for Adaptive Time Stepping",
        description=(
            "The simulation will be aborted if a finer time step is required than this"
            " minimum step value."
        ),
    )
    maximumStep: PositiveFloat = Field(
        default=None,
        alias="maximumStep",
        description="Bigger steps than this won't be allowed",
    )
    tolerances: List[Pancake3DSolveTolerance] = Field(
        default=None,
        title="Tolerances for Adaptive Time Stepping",
        description=(
            "Time steps will be adjusted so the predicted error of quantities below"
            " will stay in the tolerance range. Tolerances will decide how fine the"
            " time stepping will be."
        ),
    )

    # Optionals:
    integrationMethod: Literal[
        "Euler", "Gear_2", "Gear_3", "Gear_4", "Gear_5", "Gear_6"
    ] = Field(
        default="Euler",
        alias="integrationMethod",
        title="Integration Method",
        description="Integration method for transient analysis",
    )
    breakPoints: List[float] = Field(
        default=[0],
        alias="breakPoints",
        title="Break Points for Adaptive Time Stepping",
        description="Make sure to solve the system for these times.",
    )

    # 2) To be calculated:
    postOperationTolerances: List[Pancake3DSolveTolerance] = Field(
        default=None,
        description="post operation type tolerances (calculated by FiQuS)",
    )
    systemTolerances: List[Pancake3DSolveTolerance] = Field(
        default=None,
        description="system type tolerances (calculated by FiQuS)",
    )

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_time_steps(cls, values):
        """
        Checks if the time steps are consistent.

        :param values: dictionary of time steps
        :type values: dict
        :return: dictionary of time steps
        :rtype: dict
        """

        if values["initialStep"] < values["minimumStep"]:
            raise ValueError(
                "Initial time step cannot be smaller than the minimum time step!"
            )

        if values["initialStep"] > values["maximumStep"]:
            raise ValueError(
                "Initial time step cannot be greater than the maximum time step!"
            )

        if values["minimumStep"] > values["maximumStep"]:
            raise ValueError(
                "Minimum time step cannot be greater than the maximum time step!"
            )

        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def parse_tolerances(cls, values):
        values["postOperationTolerances"] = []
        values["systemTolerances"] = []

        for tolerance in values["tolerances"]:
            if tolerance.quantity == "solutionVector":
                values["systemTolerances"].append(tolerance)
            else:
                values["postOperationTolerances"].append(tolerance)

        return values


class Pancake3DSolveFixedTimeLoopSettings(BaseModel):
    # 1) User inputs:

    # Mandatory:
    step: PositiveFloat = Field(
        default=None,
        title="Step for Fixed Time Stepping",
        description="Time step for fixed time stepping.",
    )


class Pancake3DSolveFixedLoopInterval(BaseModel):
    # 1) User inputs:
    startTime: NonNegativeFloat = Field(
        title="Start Time of the Interval",
        description="Start time of the interval.",
    )
    endTime: NonNegativeFloat = Field(
        title="End Time of the Interval",
        description="End time of the interval.",
    )
    step: PositiveFloat = Field(
        title="Step for the Interval",
        description="Time step for the interval",
    )

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_time_steps(cls, values):
        """
        Checks if the time steps are consistent.

        :param values: dictionary of time steps
        :type values: dict
        :return: dictionary of time steps
        :rtype: dict
        """

        if values["startTime"] > values["endTime"]:
            raise ValueError("Start time cannot be greater than the end time!")

        interval = values["endTime"] - values["startTime"]
        if (
            math.fmod(interval, values["step"]) > 1e-8
            and math.fmod(interval, values["step"]) - values["step"] < -1e-8
        ):
            raise ValueError("Time interval must be a multiple of the time step!")

        return values


class Pancake3DSolveTime(BaseModel):
    # 1) User inputs:
    adaptive: Pancake3DSolveAdaptiveTimeLoopSettings = Field(
        default=None,
        alias="adaptiveSteppingSettings",
        title="Adaptive Time Loop Settings",
        description=(
            "Adaptive time loop settings (only used if stepping type is adaptive)."
        ),
    )
    fixed: Union[
        List[Pancake3DSolveFixedLoopInterval], Pancake3DSolveFixedTimeLoopSettings
    ] = Field(
        default=None,
        alias="fixedSteppingSettings",
        title="Fixed Time Loop Settings",
        description="Fixed time loop settings (only used if stepping type is fixed).",
    )

    # Mandatory:
    start: float = Field(
        title="Start Time", description="Start time of the simulation."
    )
    end: float = Field(title="End Time", description="End time of the simulation.")

    timeSteppingType: Literal["fixed", "adaptive"] = Field(
        title="Time Stepping Type",
        description="Time stepping type.",
    )

    # Optionals:
    extrapolationOrder: Literal[0, 1, 2, 3] = Field(
        default=1,
        alias="extrapolationOrder",
        title="Extrapolation Order",
        description=(
            "Before solving for the next time steps, the previous solutions can be"
            " extrapolated for better convergence."
        ),
    )

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_mandotory_fields(cls, values):
        """
        Checks if the mandatory fields are specified.

        :param values: dictionary of time loop settings
        :type values: dict
        :return: dictionary of time loop settings
        """
        if values["timeSteppingType"] == "fixed":
            if values["fixed"] is None:
                raise ValueError(
                    "Fixed time stepping step must be specified if time loop type is"
                    " fixed!"
                )
        else:
            if values["adaptive"].initialStep is None:
                raise ValueError(
                    "Initial time step must be specified if time loop type is adaptive!"
                )
            if values["adaptive"].minimumStep is None:
                raise ValueError(
                    "Minimum time step must be specified if time loop type is adaptive!"
                )
            if values["adaptive"].maximumStep is None:
                raise ValueError(
                    "Maximum time step must be specified if time loop type is adaptive!"
                )
            if values["adaptive"].tolerances is None:
                raise ValueError(
                    "Tolerances must be specified if time loop type is adaptive!"
                )

        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_time(cls, values):
        """
        Checks if the time values are consistent and multiples of the time step.

        :param cls: class
        :type cls: class
        :param values: dictionary of time
        :type values: dict
        :return: dictionary of time
        :rtype: dict
        """
        if not (values["start"] < values["end"]):
            raise ValueError(
                "Time values are not consistent! Start time is greater than end time!"
            )

        times = [
            values["start"],
            values["end"],
        ]

        if values["timeSteppingType"] == "fixed":
            # Check if all the times are multiples of the time step:
            if hasattr(values["fixed"], "step"):
                timeStep = values["fixed"].step
                values["fixed"] = [
                    Pancake3DSolveFixedLoopInterval(
                        startTime=values["start"],
                        endTime=values["end"],
                        step=timeStep,
                    )
                ]
            else:
                for i in range(len(values["fixed"]) - 1):
                    if values["fixed"][i + 1].startTime != values["fixed"][i].endTime:
                        raise ValueError(
                            "Time intervals are not consistent! End time of the"
                            " interval is not equal to the start time of the next"
                            " interval!"
                        )

            if values["fixed"][0].startTime > values["end"]:
                raise ValueError(
                    "Time intervals are not consistent! Start time of the first"
                    " interval is greater than the end time of the simulation!"
                )

            for time in times:
                for interval in values["fixed"]:
                    if time >= interval.startTime and time < interval.endTime:
                        startTime = interval.startTime
                        timeStep = interval.step
                if (
                    math.fmod(time - startTime, timeStep) > 1e-8
                    and math.fmod(time - startTime, timeStep) - timeStep < -1e-8
                ):
                    raise ValueError("Time values are not multiples of the time step!")

        if values["timeSteppingType"] == "adaptive":
            values["adaptive"].breakPoints = list(set(values["adaptive"].breakPoints))
            values["adaptive"].breakPoints.sort()

            if values["adaptive"].initialStep > values["end"]:
                raise ValueError(
                    "Initial time step is greater than the end time of the simulation!"
                )

        return values


class Pancake3DSolveNonlinearSolverSettings(BaseModel):
    # 1) User inputs:

    # Mandatory:
    tolerances: List[Pancake3DSolveTolerance] = Field(
        default=None,
        title="Tolerances for Nonlinear Solver",
        description=(
            "The nonlinear solver will check the tolerance quantities to make sure it"
            " converged or not. If the quantities stay in the tolerance region after an"
            " iteration, it will conclude that the nonlinear solver converged."
        ),
    )

    # Optionals:
    maxIter: PositiveInt = Field(
        default=100,
        alias="maximumNumberOfIterations",
        title="Maximum Number of Iterations",
        description="Maximum number of iterations allowed for the nonlinear solver.",
    )
    relaxationFactor: float = Field(
        default=0.7,
        gt=0,
        alias="relaxationFactor",
        title="Relaxation Factor",
        description=(
            "Calculated step changes of the solution vector will be multiplied with"
            " this value for better convergence."
        ),
    )

    # 2) To be calculated:
    postOperationTolerances: List[Pancake3DSolveTolerance] = Field(
        default=None,
        description="post operation type tolerances (calculated by FiQuS)",
    )
    systemTolerances: List[Pancake3DSolveTolerance] = Field(
        default=None,
        description="system type tolerances (calculated by FiQuS)",
    )

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def parse_tolerances(cls, values):
        values["postOperationTolerances"] = []
        values["systemTolerances"] = []

        for tolerance in values["tolerances"]:
            if tolerance.quantity == "solutionVector":
                values["systemTolerances"].append(tolerance)
            else:
                values["postOperationTolerances"].append(tolerance)

        return values


class Pancake3DSolveInitialConditions(BaseModel):
    # 1) User inputs:

    # Mandatory:
    T: PositiveFloat = Field(
        alias="temperature",
        title="Initial Temperature",
        description="Initial temperature of the pancake coils.",
    )


class Pancake3DSolveLocalDefect(BaseModel):
    # 1) User inputs:

    # Mandatory:
    value: NonNegativeFloat = Field(
        default=None,
        alias="value",
        title="Value",
        description="Value of the local defect.",
    )
    transitionDuration: PositiveFloat = Field(
        default=None,
        title="Transition Duration",
        description=(
            "Transition duration of the local defect. If not given, the transition will"
            " be instantly."
        ),
    )
    whichPancakeCoil: PositiveInt = Field(
        default=None,
        title="Pancake Coil Number",
        description="The first pancake coil is 1, the second is 2, etc.",
    )
    startTurn: NonNegativeFloat = Field(
        default=None,
        alias="startTurn",
        title="Start Turn",
        description="Start turn of the local defect.",
    )
    endTurn: PositiveFloat = Field(
        default=None,
        alias="endTurn",
        title="End Turn",
        description="End turn of the local defect.",
    )
    startTime: NonNegativeFloat = Field(
        default=None,
        alias="startTime",
        title="Start Time",
        description="Start time of the local defect.",
    )

    # To be calculated:
    zTop: float = Field(
        default=None,
        description="z-coordinate of the top of the pancake coil (calculated by FiQuS)",
    )
    zBottom: float = Field(
        default=None,
        description=(
            "z-coordinate of the bottom of the pancake coil (calculated by FiQuS)"
        ),
    )

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_turns(cls, values):
        """
        Checks if the start turn is smaller than the end turn.

        :param values: dictionary of local defect
        :type values: dict
        :return: dictionary of local defect
        :rtype: dict
        """
        if values["startTurn"] is not None:
            if values["startTurn"] > values["endTurn"]:
                raise ValueError("The start turn can not be greater than the end turn!")

        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_entries(cls, values):
        # Check if all of them None first:
        AllNone = True
        for key, value in values.items():
            if value is not None:
                AllNone = False
                break
        if not AllNone:
            optionalEntries = ["transitionDuration", "zTop", "zBottom"]
            for key, value in values.items():
                if value is None and key not in optionalEntries:
                    raise ValueError(
                        f'"{key}" entry of the local defect must be specified!'
                    )

        return values


class Pancake3DSolveLocalDefects(BaseModel):
    # 1) User inputs:

    jCritical: Pancake3DSolveLocalDefect = Field(
        default=Pancake3DSolveLocalDefect(),
        alias="criticalCurrentDensity",
        title="Local Defect for Critical Current Density",
        description="Set critical current density locally.",
    )


class Pancake3DSolveSaveQuantity(BaseModel):
    # 1) User inputs:

    # Mandatory:
    quantity: Literal[
        "magneticField",
        "magnitudeOfMagneticField",
        "currentDensity",
        "magnitudeOfCurrentDensity",
        "resistiveHeating",
        "temperature",
        "voltageBetweenTerminals",
        "currentThroughCoil",
        "criticalCurrentDensity",
        "heatFlux",
        "resistivity",
        "thermalConductivity",
        "specificHeatCapacity",
        "jHTSOverjCritical",
        "criticalCurrent",
        "magneticEnergy",
    ] = Field(
        title="Quantity",
        description="Name of the quantity to be saved.",
    )

    # Optionals:
    timesToBeSaved: List[float] = Field(
        default=None,
        title="Times to be Saved",
        description=(
            "List of times that wanted to be saved. If not given, all the time steps"
            " will be saved."
        ),
    )

    # 2) To be calculated:
    getdpQuantityName: str = Field(
        default=None,
        description="name of the quantity name in GetDP (calculated by FiQuS)",
    )
    getdpPostOperationName: str = Field(
        default=None,
        description="name of the post operation in GetDP (calculated by FiQuS)",
    )

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def assign_getdp_names(cls, values):
        """ """
        quantityNames = {
            "magneticField": "RESULT_magneticField",
            "magnitudeOfMagneticField": "RESULT_magnitudeOfMagneticField",
            "currentDensity": "RESULT_currentDensity",
            "magnitudeOfCurrentDensity": "RESULT_magnitudeOfCurrentDensity",
            "resistiveHeating": "RESULT_resistiveHeating",
            "temperature": "RESULT_temperature",
            "currentThroughCoil": "RESULT_currentThroughCoil",
            "voltageBetweenTerminals": "RESULT_voltageBetweenTerminals",
            "criticalCurrentDensity": "RESULT_criticalCurrentDensity",
            "heatFlux": "RESULT_heatFlux",
            "resistivity": "RESULT_resistivity",
            "thermalConductivity": "RESULT_thermalConductivity",
            "specificHeatCapacity": "RESULT_specificHeatCapacity",
            "jHTSOverjCritical": "RESULT_jHTSOverjCritical",
            "criticalCurrent": "RESULT_criticalCurrent",
            "debug": "RESULT_debug",
            "magneticEnergy": "RESULT_magneticEnergy",
        }
        postOperationNames = {
            "magneticField": "POSTOP_magneticField",
            "magnitudeOfMagneticField": "POSTOP_magnitudeOfMagneticField",
            "currentDensity": "POSTOP_currentDensity",
            "magnitudeOfCurrentDensity": "POSTOP_magnitudeOfCurrentDensity",
            "resistiveHeating": "POSTOP_resistiveHeating",
            "temperature": "POSTOP_temperature",
            "currentThroughCoil": "POSTOP_currentThroughCoil",
            "voltageBetweenTerminals": "POSTOP_voltageBetweenTerminals",
            "criticalCurrentDensity": "POSTOP_criticalCurrentDensity",
            "heatFlux": "POSTOP_heatFlux",
            "resistivity": "POSTOP_resistivity",
            "thermalConductivity": "POSTOP_thermalConductivity",
            "specificHeatCapacity": "POSTOP_specificHeatCapacity",
            "jHTSOverjCritical": "POSTOP_jHTSOverjCritical",
            "criticalCurrent": "POSTOP_criticalCurrent",
            "debug": "POSTOP_debug",
            "magneticEnergy": "POSTOP_magneticEnergy",
        }

        values["getdpQuantityName"] = quantityNames[values["quantity"]]
        values["getdpPostOperationName"] = postOperationNames[values["quantity"]]

        return values


# ======================================================================================
# SOLVE CLASSES ENDS ===================================================================
# ======================================================================================

# ======================================================================================
# POSTPROCESS CLASSES STARTS ==============================================================
# ======================================================================================


class Pancake3DPostprocessTimeSeriesPlot(BaseModel):
    # 1) User inputs:

    position: Pancake3DPosition = Field(
        default=Pancake3DPosition(),
        title="Probing Position",
        description="Probing position of the quantity for time series plot.",
    )
    quantity: Literal[
        "magnitudeOfMagneticField",
        "temperature",
        "magnitudeOfCurrentDensity",
        "resistiveHeating",
        "axialComponentOfTheMagneticField",
        "totalResistiveHeating",
        "voltageBetweenTerminals",
        "currentThroughCoil",
        "magnitudeOfHeatFlux",
        "resistivity",
        "derivativeOfRhoWithRespectToJ",
        "magneticEnergy",
    ] = Field(
        default=None,
        title="Quantity",
        description="Name of the quantity to be plotted.",
    )

    # 2) To be calculated:
    fileName: str = Field(
        default=None,
        description="name of the file to be saved (calculated by FiQuS)",
    )
    quantityProperName: str = Field(
        default=None,
        description="proper name of the quantity (calculated by FiQuS)",
    )
    getdpQuantityName: str = Field(
        default=None,
        description="name of the quantity name in GetDP (calculated by FiQuS)",
    )
    units: str = Field(
        default=None,
        description="units of the quantity (calculated by FiQuS)",
    )

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def assign_names(cls, values):
        quantityNames = {
            "magnitudeOfMagneticField": "RESULT_magnitudeOfMagneticField",
            "temperature": "RESULT_temperature",
            "magnitudeOfCurrentDensity": "RESULT_magnitudeOfCurrentDensity",
            "resistiveHeating": "RESULT_resistiveHeating",
            "axialComponentOfTheMagneticField": (
                "RESULT_axialComponentOfTheMagneticField"
            ),
            "totalResistiveHeating": "RESULT_totalResistiveHeating",
            "voltageBetweenTerminals": "RESULT_voltageBetweenTerminals",
            "currentThroughCoil": "RESULT_currentThroughCoil",
            "magnitudeOfHeatFlux": "RESULT_magnitudeOfHeatFlux",
            "resistivity": "RESULT_resistivity",
            "derivativeOfRhoWithRespectToJ": "RESULT_derivativeOfRhoWithRespectToJ",
            "magneticEnergy": "RESULT_magneticEnergy",
        }
        units = {
            "magnitudeOfMagneticField": "T",
            "temperature": "K",
            "magnitudeOfCurrentDensity": "A/m^2",
            "resistiveHeating": "W/m^3",
            "axialComponentOfTheMagneticField": "T",
            "totalResistiveHeating": "W",
            "voltageBetweenTerminals": "V",
            "currentThroughCoil": "A",
            "magnitudeOfHeatFlux": "W/m^2",
            "resistivity": "Ohm*m",
            "derivativeOfRhoWithRespectToJ": "Ohm*m^3/A",
            "magneticEnergy": "J",
        }
        properNames = {
            "magnitudeOfMagneticField": "Magnitude of the Magnetic Field",
            "temperature": "Temperature",
            "magnitudeOfCurrentDensity": "Magnitude of the Current Density",
            "resistiveHeating": "Resistive Heating",
            "axialComponentOfTheMagneticField": "Axial Component of the Magnetic Field",
            "totalResistiveHeating": "Total Resistive Heating",
            "voltageBetweenTerminals": "Voltage Between Terminals",
            "currentThroughCoil": "Current Through Coil",
            "magnitudeOfHeatFlux": "Magnitude of the Heat Flux",
            "resistivity": "Resistivity",
            "derivativeOfRhoWithRespectToJ": "dRho-dJ",
            "magneticEnergy": "Magnetic Energy",
        }

        values["fileName"] = f"{values['quantity']}(TimeSeriesPlot)"
        values["getdpQuantityName"] = quantityNames[values["quantity"]]
        values["units"] = units[values["quantity"]]
        values["quantityProperName"] = properNames[values["quantity"]]

        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_position(cls, values):
        positionRequiredFor = [
            "magnitudeOfMagneticField",
            "temperature",
            "magnitudeOfCurrentDensity",
            "resistiveHeating",
            "axialComponentOfTheMagneticField",
            "magnitudeOfHeatFlux",
            "resistivity",
            "derivativeOfRhoWithRespectToJ",
        ]
        if (
            values["position"].x is None
            and values["position"].y is None
            and values["position"].z is None
            and values["position"].turnNumber is None
            and values["position"].whichPancakeCoil is None
        ):
            if values["quantity"] in positionRequiredFor:
                raise ValueError(
                    "Position must be specified for time series plot of"
                    f" {values['quantity']}!"
                )
        else:
            if values["quantity"] not in positionRequiredFor:
                logger.warning(
                    "Position must not be specified for time series plot of"
                    f" {values['quantity']}, because it's a global scalar quantity!"
                )

        return values


class Pancake3DPostprocessMagneticFieldOnPlane(BaseModel):
    colormap: str = Field(
        default="viridis",
        title="Colormap",
        description="Colormap for the plot.",
    )
    streamLines: bool = Field(
        default=True,
        title="Stream Lines",
        description=(
            "If True, streamlines will be plotted. Note that magnetic field vectors may"
            " have components perpendicular to the plane, and streamlines will be drawn"
            " depending on the vectors' projection onto the plane."
        ),
    )
    interpolationMethod: Literal["nearest", "linear", "cubic"] = Field(
        default="linear",
        title="Interpolation Method",
        description=(
            "Interpolation type for the plot.\nBecause of the FEM basis function"
            " selections of FiQuS, each mesh element has a constant magnetic field"
            " vector. Therefore, for smooth 2D plots, interpolation can be"
            " used.\nTypes:\nnearest: it will plot the nearest magnetic field value to"
            " the plotting point.\nlinear: it will do linear interpolation to the"
            " magnetic field values.\ncubic: it will do cubic interpolation to the"
            " magnetic field values."
        ),
    )
    timesToBePlotted: List[float] = Field(
        default=None,
        title="Times to be Plotted",
        description=(
            "List of times that wanted to be plotted. If not given, all the time steps"
            " will be plotted."
        ),
    )
    planeNormal: List[float] = Field(
        default=[1, 0, 0],
        title="Plane Normal",
        description="Normal vector of the plane. The default is YZ-plane (1, 0, 0).",
    )
    planeXAxisUnitVector: List[float] = Field(
        default=[0, 1, 0],
        title="Plane X Axis",
        description=(
            "If an arbitrary plane is wanted to be plotted, the arbitrary plane's X"
            " axis unit vector must be specified. The dot product of the plane's X axis"
            " and the plane's normal vector must be zero."
        ),
    )

    onSection: List[List[float]] = Field(
        default=None,
        description="Three corner points of the plane (calculated by FiQuS).",
    )

    @validator("colormap", allow_reuse=True)
    @classmethod
    def check_colormap(cls, value):
        """
        Check if the colormap exists.
        """
        if value not in matplotlib.pyplot.colormaps():
            raise ValueError(
                f"{value} is not a valid colormap! Please see"
                " https://matplotlib.org/stable/gallery/color/colormap_reference.html"
                " for available colormaps."
            )

        return value


# ======================================================================================
# POSTPROCESS CLASSES ENDS ================================================================
# ======================================================================================


class Pancake3DGeometry(BaseModel):
    # 1) User inputs:

    wi: Pancake3DGeometryWinding = Field(
        alias="winding",
        title="Winding Geometry",
        description="This dictionary contains the winding geometry information.",
    )

    ii: Pancake3DGeometryContactLayer = Field(
        alias="contactLayer",
        title="Contact Layer Geometry",
        description="This dictionary contains the contact layer geometry information.",
    )

    ti: Pancake3DGeometryTerminals = Field(
        alias="terminals",
        title="Terminals Geometry",
        description="This dictionary contains the terminals geometry information.",
    )

    ai: Pancake3DGeometryAir = Field(
        alias="air",
        title="Air Geometry",
        description="This dictionary contains the air geometry information.",
    )

    # Mandatory:

    N: PositiveInt = Field(
        alias="numberOfPancakes",
        title="Number of Pancakes",
        description="Number of pancake coils stacked on top of each other.",
    )

    gap: PositiveFloat = Field(
        alias="gapBetweenPancakes",
        title="Gap Between Pancakes",
        description="Gap distance between the pancake coils.",
    )

    # Optionals:
    dimTol: PositiveFloat = Field(
        default=1e-8,
        alias="dimensionTolerance",
        description="dimension tolerance (CAD related, not physical)",
    )
    pancakeBoundaryName: str = Field(
        default="PancakeBoundary",
        description=(
            "name of the pancake's curves that touches the air to be used in the mesh"
        ),
    )
    contactLayerBoundaryName: str = Field(
        default="contactLayerBoundary",
        description=(
            "name of the contact layers's curves that touches the air to be used in the"
            " mesh (only for TSA)"
        ),
    )

    @validator("N", allow_reuse=True)
    @classmethod
    def check_N(cls, value):
        """
        Checks if the number of pancakes is at least 1.

        :param cls: class
        :type cls: class
        :param value: number of pancakes
        :type value: int
        :return: number of pancakes
        :rtype: int
        """
        if value < 1:
            raise ValueError("Number of pancakes must be at least 1!")
        return value

    @validator("dimTol", allow_reuse=True)
    @classmethod
    def check_dimTol(cls, value):
        """
        Checks if the dimension tolerance is smaller than 1e-5.

        :param cls: class
        :type cls: class
        :param value: dimension tolerance
        :type value: float
        :return: dimension tolerance
        :rtype: float
        """
        if value > 1e-5:
            raise ValueError("Dimension tolerance must be smaller than 1e-5!")

        return value


class Pancake3DMesh(BaseModel):
    # 1) User inputs:
    wi: Pancake3DMeshWinding = Field(
        alias="winding",
        title="Winding Mesh",
        description="This dictionary contains the winding mesh information.",
    )
    ii: Pancake3DMeshContactLayer = Field(
        alias="contactLayer",
        title="Contact Layer Mesh",
        description="This dictionary contains the contact layer mesh information.",
    )
    ti: Pancake3DMeshAirAndTerminals = Field(
        default=Pancake3DMeshAirAndTerminals(),
        alias="terminals",
        title="Terminal Mesh",
        description="This dictionary contains the terminal mesh information.",
    )
    ai: Pancake3DMeshAirAndTerminals = Field(
        default=Pancake3DMeshAirAndTerminals(),
        alias="air",
        title="Air Mesh",
        description="This dictionary contains the air mesh information.",
    )

    # Mandatory:
    relSizeMin: PositiveFloat = Field(
        alias="minimumElementSize",
        title="Minimum Element Size",
        description=(
            "The minimum mesh element size in terms of the largest mesh size in the"
            " winding. This mesh size will be used in the regions close the the"
            " winding, and then the mesh size will increate to maximum mesh element"
            " size as it gets away from the winding."
        ),
    )
    relSizeMax: PositiveFloat = Field(
        alias="maximumElementSize",
        title="Maximum Element Size",
        description=(
            "The maximum mesh element size in terms of the largest mesh size in the"
            " winding. This mesh size will be used in the regions close the the"
            " winding, and then the mesh size will increate to maximum mesh element"
            " size as it gets away from the winding."
        ),
    )

    # 2) To be calculated:
    sizeMin: PositiveFloat = Field(
        default=None,
        description=(
            "minimum mesh element size in real dimensions (calculated by FiQuS)"
        ),
    )
    sizeMax: PositiveFloat = Field(
        default=None,
        description=(
            "maximum mesh element size in real dimensions (calculated by FiQuS)"
        ),
    )
    startGrowingDistance: PositiveFloat = Field(
        default=None,
        description=(
            "distance from the pancake coils to start growing the mesh elements"
            " (calculated by FiQuS)"
        ),
    )
    stopGrowingDistance: PositiveFloat = Field(
        default=None,
        description=(
            "distance from the pancake coils to stop growing the mesh elements"
            " (calculated by FiQuS)"
        ),
    )
    theWorstRectangularRatio: PositiveFloat = Field(
        default=None,
        description=(
            "the worst rectangular structured mesh element size ratio (calculated by"
            " FiQuS)"
        ),
    )
    theWorstTriangularRatio: PositiveFloat = Field(
        default=None,
        description=(
            "the worst triangular structured mesh element size ratio (calculated by"
            " FiQuS)"
        ),
    )

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_size(cls, values):
        """
        Checks if the minimum element size is smaller than the maximum element size.

        :param cls: class
        :type cls: class
        :param values: dictionary of mesh
        :type values: dict
        :return: dictionary of mesh
        :rtype: dict
        """
        if values["relSizeMin"] > values["relSizeMax"]:
            raise ValueError(
                "The minimum mesh element size must be smaller than the maximum mesh"
                " element size!"
            )

        return values


class Pancake3DSolve(BaseModel):
    # 1) User inputs:
    t: Pancake3DSolveTime = Field(
        alias="time",
        title="Time Settings",
        description="All the time related settings for transient analysis.",
    )

    nls: Pancake3DSolveNonlinearSolverSettings = Field(
        alias="nonlinearSolver",
        title="Nonlinear Solver Settings",
        description="All the nonlinear solver related settings.",
    )

    wi: Pancake3DSolveWindingMaterial = Field(
        alias="winding",
        title="Winding Properties",
        description="This dictionary contains the winding material properties.",
    )
    ii: Pancake3DSolveContactLayerMaterial = Field(
        alias="contactLayer",
        title="Contact Layer Properties",
        description="This dictionary contains the contact layer material properties.",
    )
    ti: Pancake3DSolveTerminalMaterialAndBoundaryCondition = Field(
        alias="terminals",
        title="Terminals Properties",
        description=(
            "This dictionary contains the terminals material properties and cooling"
            " condition."
        ),
    )
    ai: Pancake3DSolveAir = Field(
        alias="air",
        title="Air Properties",
        description="This dictionary contains the air material properties.",
    )

    ic: Pancake3DSolveInitialConditions = Field(
        alias="initialConditions",
        title="Initial Conditions",
        description="Initial conditions of the problem.",
    )

    save: List[Pancake3DSolveSaveQuantity] = Field(
        alias="quantitiesToBeSaved",
        default=None,
        title="Quantities to be Saved",
        description="List of quantities to be saved.",
    )

    # Mandatory:
    type: Literal[
        "electromagnetic", "thermal", "weaklyCoupled", "stronglyCoupled"
    ] = Field(
        title="Simulation Type",
        description=(
            "FiQuS/Pancake3D can solve only electromagnetics and thermal or"
            " electromagnetic and thermal coupled. In the weaklyCoupled setting,"
            " thermal and electromagnetics systems will be put into different"
            " matrices, whereas in the stronglyCoupled setting, they all will be"
            " combined into the same matrix. The solution should remain the same."
        ),
    )

    # Optionals:
    proTemplate: str = Field(
        default="Pancake3D_template.pro",
        description="file name of the .pro template file",
    )

    localDefects: Pancake3DSolveLocalDefects = Field(
        default=Pancake3DSolveLocalDefects(),
        alias="localDefects",
        title="Local Defects",
        description=(
            "Local defects (like making a small part of the winding normal conductor at"
            " some time) can be introduced."
        ),
    )

    initFromPrevious: str = Field(
        default="",
        title="Full path to res file to continue from",
        description=(
            "The simulation is continued from an existing .res file.  The .res file is"
            " from a previous computation on the same geometry and mesh. The .res file"
            " is taken from the folder Solution_<<initFromPrevious>>"
        ),
    )

    isothermalInAxialDirection: bool = Field(
        default=False,
        title="Equate DoF along axial direction",
        description=(
            "If True, the DoF along the axial direction will be equated. This means"
            " that the temperature will be the same along the axial direction reducing"
            " the number of DoF. This is only valid for the thermal analysis."
        ),
    )

    # 2) To be calculated:
    systemsOfEquationsType: Literal["linear", "nonlinear"] = Field(
        default=None, description="(calculated by FiQuS)"
    )

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def find_system_type(cls, values):
        values["systemsOfEquationsType"] = "linear"
        listOfGeometryParts = ["wi", "ii", "ti"]

        for geometryPart in listOfGeometryParts:
            if values["type"] == "electromagnetic":
                if (
                    not isinstance(values[geometryPart].resistivity, float)
                    and values[geometryPart].resistivity != "perfectlyInsulating"
                ):
                    values["systemsOfEquationsType"] = "nonlinear"

                    if values["ic"].T is None:
                        raise ValueError(
                            "Initial temperature must be specified if nonlinear"
                            " materials are used because of the temperature dependency"
                            " of the resistivity!"
                        )
            elif values["type"] == "thermal":
                if not isinstance(
                    values[geometryPart].thermalConductivity, float
                ) or not isinstance(values[geometryPart].specificHeatCapacity, float):
                    values["systemsOfEquationsType"] = "nonlinear"

                    if values["ic"].T is None:
                        raise ValueError(
                            "Initial temperature must be specified if nonlinear"
                            " materials are used because of the temperature dependency"
                            " of the thermal conductivity and specific heat capacity!"
                        )

            else:
                if (
                    (
                        not isinstance(values[geometryPart].resistivity, float)
                        and values[geometryPart].resistivity != "perfectlyInsulating"
                    )
                    or not isinstance(values[geometryPart].thermalConductivity, float)
                    or not isinstance(values[geometryPart].specificHeatCapacity, float)
                ):
                    values["systemsOfEquationsType"] = "nonlinear"

                    if values["ic"].T is None:
                        raise ValueError(
                            "Initial temperature must be specified if nonlinear"
                            " materials are used because of the temperature dependency"
                            " of the resistivity, thermal conductivity and specific"
                            " heat capacity!"
                        )
        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_tolerances(cls, values):
        electromagneticRequiredTolerances = [
            "totalResistiveHeating",
            "voltageBetweenTerminals",
            "resistiveHeating",
            "currentDensity",
            "magnitudeOfMagneticField",
            "axialComponentOfTheMagneticField",
            "magneticEnergy",
        ]
        thermalRequiredTolerances = ["temperature", "magnitudeOfHeatFlux"]

        allTolerances = []
        allTolerances.extend(values["nls"].tolerances)
        allTolerances.extend(values["t"].adaptive.tolerances)

        if values["type"] == "thermal":
            # Then totalResistiveHeating is not a valid tolerance:
            for tolerance in allTolerances:
                if tolerance.quantity in electromagneticRequiredTolerances:
                    raise ValueError(
                        f"{tolerance.quantity} is not a valid tolerance if the type"
                        " is thermal!"
                    )
        elif values["type"] == "electromagnetic":
            for tolerance in allTolerances:
                if tolerance.quantity in thermalRequiredTolerances:
                    raise ValueError(
                        f"{tolerance.quantity} is not a valid tolerance if the type"
                        " is electromagnetic!"
                    )

        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_times_to_be_saved(cls, values):
        """ """

        # Check if the times to be saved are between start and end times:
        allTimesToBeSaved = set()
        if values["save"]:
            for saveQuantity in values["save"]:
                if saveQuantity.timesToBeSaved:
                    for time in saveQuantity.timesToBeSaved:
                        if time < values["t"].start or time > values["t"].end:
                            raise ValueError(
                                f"Time {time:.5f} in the timesToBeSaved list is not"
                                " between start and end times!"
                            )

                        allTimesToBeSaved.add(time)

        if values["localDefects"]:
            if values["localDefects"].jCritical:
                if values["localDefects"].jCritical.startTime:
                    if (
                        values["localDefects"].jCritical.startTime > values["t"].start
                        and values["localDefects"].jCritical.startTime < values["t"].end
                    ):
                        allTimesToBeSaved.add(
                            values["localDefects"].jCritical.startTime
                        )

            allTimesToBeSaved = list(allTimesToBeSaved)

        if values["t"].timeSteppingType == "adaptive":
            # Add all times to be saved to the break points list:
            for timeToBeSaved in allTimesToBeSaved:
                values["t"].adaptive.breakPoints.append(timeToBeSaved)

            values["t"].adaptive.breakPoints = list(
                set(values["t"].adaptive.breakPoints)
            )
            values["t"].adaptive.breakPoints.sort()

            if len(values["t"].adaptive.breakPoints) == 1:
                values["t"].adaptive.breakPoints = []

        elif values["t"].timeSteppingType == "fixed":
            # Check if all times to be saved are multiples of the time step:
            for timeToBeSaved in allTimesToBeSaved:
                for interval in values["t"].fixed:
                    if (
                        timeToBeSaved >= interval.startTime
                        and timeToBeSaved <= interval.endTime
                    ):
                        startTime = interval.startTime
                        timeStep = interval.step
                if (
                    math.fmod(timeToBeSaved - startTime, timeStep) > 1e-8
                    and math.fmod(timeToBeSaved - startTime, timeStep) - timeStep
                    < -1e-8
                ):
                    raise ValueError(
                        f"A time value ({timeToBeSaved}) in the timesToBeSaved list is"
                        " not multiples of the time step!"
                    )

        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_local_defects(cls, values):
        """ """
        if not values["wi"].superConductor or values["wi"].resistivity:
            if values["localDefects"].jCritical.value is not None:
                raise ValueError(
                    "Critical current density local defect cannot be defined if"
                    " winding does not have superconductivity!"
                )

        if values["type"] in "thermal":
            if values["localDefects"].jCritical.value:
                raise ValueError(
                    "Critical current density local defect cannot be defined if the"
                    " simulation type is thermal!"
                )

        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_quantities_to_be_saved(cls, values):
        """ """
        if values["save"]:
            for saveQuantity in values["save"]:
                if saveQuantity.quantity == "criticalCurrentDensity":
                    if not values["wi"].superConductor or values["wi"].resistivity:
                        raise ValueError(
                            "Critical current density cannot be saved if winding does"
                            " not have superconductivity!"
                        )

            if values["type"] == "electromagnetic":
                for saveQuantity in values["save"]:
                    if saveQuantity.quantity in ["temperature", "heatFlux"]:
                        raise ValueError(
                            "Temperature cannot be saved if the type is electromagnetic"
                            " because it is not calculated!"
                        )
            elif values["type"] == "thermal":
                for saveQuantity in values["save"]:
                    if saveQuantity.quantity in [
                        "magneticField",
                        "magnitudeOfMagneticField",
                        "currentDensity",
                        "magnitudeOfCurrentDensity",
                        "resistiveHeating",
                        "criticalCurrentDensity",
                    ]:
                        raise ValueError(
                            "Magnetic field, current density and resistive heating"
                            " cannot be saved if the type is thermal because they are"
                            " not calculated!"
                        )

        return values


class Pancake3DPostprocess(BaseModel):
    """
    TO BE UPDATED
    """

    # 1) User inputs:
    timeSeriesPlots: List[Pancake3DPostprocessTimeSeriesPlot] = Field(
        default=None,
        title="Time Series Plots",
        description="Values can be plotted with respect to time.",
    )

    magneticFieldOnCutPlane: Pancake3DPostprocessMagneticFieldOnPlane = Field(
        default=None,
        title="Magnetic Field on a Cut Plane",
        description=(
            "Color map of the magnetic field on the YZ plane can be plotted with"
            " streamlines."
        ),
    )


class Pancake3D(BaseModel):
    """
    Level 1: Class for FiQuS Pancake3D
    """

    type: Literal["Pancake3D"] = "Pancake3D"
    geometry: Pancake3DGeometry = Field(
        default=None,
        title="Geometry",
        description="This dictionary contains the geometry information.",
    )
    mesh: Pancake3DMesh = Field(
        default=None,
        title="Mesh",
        description="This dictionary contains the mesh information.",
    )
    solve: Pancake3DSolve = Field(
        default=None,
        title="Solve",
        description="This dictionary contains the solve information.",
    )
    postproc: Pancake3DPostprocess = Field(
        default=None,
        title="Postprocess",
        description="This dictionary contains the postprocess information.",
    )
    input_file_path: str = Field(
        default=None,
        description="path of the input file (calculated by FiQuS)",
        exclude=True,
    )

    # skip_on_failure = True is used to make sure the submodels are validated.
    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def geometry_calculations_and_checks(cls, values):
        """
        This function calculates the geometry parameters and checks if the user inputs
        are valid.

        :param cls: class
        :type cls: class
        :param values: dictionary of PC3D
        :type values: dict
        :return: dictionary of PC3D
        :rtype: dict
        """
        # ==============================================================================
        # CALCULATIONS STARTS ==========================================================
        # ==============================================================================
        geo = values["geometry"]
        mesh = values["mesh"]

        # Calculate outer radius of the coil:
        geo.wi.r_o = geo.wi.r_i + geo.wi.t + geo.wi.N * (geo.wi.t + geo.ii.t)

        # Calculate the total tape length of the coil:

        # The same angle can be subtracted from both theta_1 and theta_2 to simplify the
        # calculations:
        theta2 = geo.wi.N * 2 * math.pi
        theta1 = 0

        # Since r = a * theta + b, r_1 = b since theta_1 = 0:
        b = geo.wi.r_i

        # Since r = a * theta + b, r_2 = a * theta2 + b:
        a = (geo.wi.r_o - b) / theta2

        def integrand(t):
            return math.sqrt(a**2 + (a * t + b) ** 2)

        geo.wi.totalTapeLength = abs(scipy.integrate.quad(integrand, theta1, theta2)[0])

        # Calculate the turn tolerance required due to the geometry input:
        # Turn tolerance is the smallest turn angle (in turns) that is allowed.
        turnTol = geo.wi.N % 1
        if math.isclose(turnTol, 0, abs_tol=geo.dimTol):
            turnTol = 0.5

        # Calculate the minimum turn tolerance possible due to the mesh input:
        if not isinstance(mesh.wi.ane, list):
            mesh.wi.ane = [mesh.wi.ane] * geo.N

        minimumTurnTol = 1 / min(mesh.wi.ane)

        if turnTol < minimumTurnTol:
            numberOfTurns = geo.wi.N

            raise ValueError(
                "The azimuthal number of elements per turn for one of the pancakes is"
                f" {min(mesh.wi.ane)}, and the number of turns is {numberOfTurns:.5f}."
                " The number of turns must always be divisible by the (1/(the"
                " azimuthal number of elements per turn)) to ensure conformality."
                " Please change the number of turns or the azimuthal number of"
                " elemenets per turn. The closest possible number of turns value is"
                f" {round(numberOfTurns * min(mesh.wi.ane))/min(mesh.wi.ane):.5f}"
            )
        else:
            # Minimum possible sections per turn is 16 (otherwise splines might collide
            # into each other). But it should be greater than the number of volumes per
            # turn and it should be divisible by both 1/turnTol and the number of
            # volumes per turn.
            sectionsPerTurn = 16
            while (
                (
                    math.fmod(sectionsPerTurn, (1 / turnTol)) > 1e-8
                    and math.fmod(sectionsPerTurn, (1 / turnTol)) - (1 / turnTol)
                    < -1e-8
                )
                or sectionsPerTurn % geo.wi.NofVolPerTurn != 0
                or sectionsPerTurn < geo.wi.NofVolPerTurn
            ):
                sectionsPerTurn += 1

            geo.wi.spt = sectionsPerTurn

            # Sections per turn will set the turn tolerance value as well.
            geo.wi.turnTol = 1 / sectionsPerTurn

        # Check if the NofVolPerTurn is compatible swith the azimuthal number of elements
        # per turn:
        if not isinstance(mesh.wi.ane, list):
            mesh.wi.ane = [mesh.wi.ane] * geo.N

        for i, ane in enumerate(mesh.wi.ane):
            if ane % geo.wi.NofVolPerTurn != 0:
                raise ValueError(
                    "The azimuthal number of elements per turn for the pancake coil"
                    f" number {i+1} is ({ane}), but it must be divisible by the number"
                    f" of volumes per turn ({geo.wi.NofVolPerTurn})! So it needs to be"
                    " rounded to"
                    f" {math.ceil(ane/geo.wi.NofVolPerTurn)*geo.wi.NofVolPerTurn:.5f} or"
                    f" {math.floor(ane/geo.wi.NofVolPerTurn)*geo.wi.NofVolPerTurn:.5f}."
                )

        # Calculate terminal radiuses:
        geo.ti.i.r = geo.wi.r_i - 2 * geo.ti.i.t
        if geo.ti.i.r < 0:
            raise ValueError(
                "Inner terminal's radius is smaller than 0! Please decrease the inner"
                " terminal's thickness or increase the winding's inner radius."
            )

        geo.ti.o.r = geo.wi.r_o + 2 * geo.ti.o.t

        # Calculate the total height of air:
        geo.ai.h = geo.N * (geo.wi.h + geo.gap) - geo.gap + geo.ai.margin * 2

        # ==============================================================================
        # CALCULATIONS ENDS ============================================================
        # ==============================================================================

        # =============================================================================
        # CHECKING TERMINALS STARTS ===================================================
        # =============================================================================

        if geo.ti.i.t < geo.wi.t / 2:
            raise ValueError(
                f"Inner terminal's thickness ({geo.ti.i.t:.5f}) is"
                " smaller than half of the winding's thickness"
                f" ({geo.wi.t/2:.5f}). Please increase the inner"
                " terminal's thickness."
            )
        if geo.ti.o.t < geo.wi.t / 2:
            raise ValueError(
                f"Outer terminal's thickness ({geo.ti.o.t:.5f}) is"
                " smaller than half of the winding's thickness"
                f" ({geo.wi.t/2:.5f}). Please increase the outer"
                " terminal's thickness."
            )

        if geo.ti.i.t != geo.ti.o.t:
            raise ValueError(
                f"Inner terminal's thickness ({geo.ti.i.t:.5f}) is"
                " not equal to the outer terminal's thickness"
                f" ({geo.ti.o.t:.5f}). Please make them equal. If"
                " you want to have different thicknesses, please comment out this"
                " error."
            )

        # =============================================================================
        # CHECKING TERMINALS ENDS =====================================================
        # =============================================================================

        # =============================================================================
        # CHECKING AIR STARTS =========================================================
        # =============================================================================

        if geo.ai.margin < geo.wi.h / 2:
            raise ValueError(
                f"Air margin ({geo.ai.margin:.5f}) is smaller than the"
                f" winding's half height ({geo.wi.h/2:.5f}). To avoid"
                " numerical errors, please increase the air margin."
            )

        if geo.ai.type == "cuboid":
            if geo.ti.o.r * 1.5 > geo.ai.a / 2:
                raise ValueError(
                    f"Side length of the air ({geo.ai.a:.5f}) must be at least 1.5"
                    " times larger than the outer terminal's diameter"
                    f" ({geo.ti.o.r*2:.5f}). Please increase the air side length."
                )

        elif geo.ai.type == "cylinder":
            if geo.ti.o.r * 1.5 > geo.ai.r:
                raise ValueError(
                    f"Radius of the air ({geo.ai.r:.5f}) must be at least 1.5 times"
                    f" larger than the outer terminal's radius ({geo.ti.o.r:.5f})."
                    " Please increase the air radius."
                )

        # =============================================================================
        # CHECKING AIR ENDS ===========================================================
        # =============================================================================

        values["mesh"] = mesh
        values["geometry"] = geo
        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def read_IcVSLength_CSV_file(cls, values):
        """
        Some fields are names of other files like CSVs. Users are asked to put those
        files in the same folder as the input file. This function appends the input
        file path to those file names and checks if the files exist.
        """
        geo = values["geometry"]
        solve = values["solve"]

        if solve.wi.superConductor is not None:
            if not isinstance(solve.wi.superConductor.IcAtTinit, float):
                IcVStapeLengthCSVFileName = solve.wi.superConductor.IcAtTinit
                if isinstance(IcVStapeLengthCSVFileName, str):
                    solve.wi.superConductor.IcAtTinit = os.path.join(
                        os.path.dirname(values["input_file_path"]),
                        IcVStapeLengthCSVFileName,
                    )
                    if not os.path.isfile(solve.wi.superConductor.IcAtTinit):
                        raise ValueError(
                            f"{solve.wi.superConductor.IcAtTinit} does not exist!"
                        )

                    with open(solve.wi.superConductor.IcAtTinit, newline="") as csvFile:
                        reader = csv.reader(csvFile, delimiter=",")

                        solve.wi.superConductor.lengthValues = []
                        solve.wi.superConductor.IcValues = []
                        for row in reader:
                            if len(row) != 2:
                                raise ValueError(
                                    f"{solve.wi.superConductor.IcAtTinit} needs to have"
                                    " 2 columns!"
                                )
                            try:
                                length = float(row[0])
                            except:
                                raise ValueError(
                                    f"{solve.wi.superConductor.IcAtTinit} has a"
                                    " non-numerical value!"
                                )

                            try:
                                Ic = float(row[1])
                            except:
                                raise ValueError(
                                    f"{solve.wi.superConductor.IcAtTinit} has a"
                                    " non-numerical value!"
                                )

                            if length >= 0:
                                solve.wi.superConductor.lengthValues.append(length)
                            else:
                                raise ValueError(
                                    f"{solve.wi.superConductor.IcAtTinit} cannot have"
                                    " negative length values!"
                                )

                            if Ic >= 0:
                                solve.wi.superConductor.IcValues.append(Ic)
                            else:
                                raise ValueError(
                                    f"{solve.wi.superConductor.IcAtTinit} cannot have"
                                    " negative critical current values!"
                                )

                        if len(solve.wi.superConductor.lengthValues) == 0:
                            raise ValueError(
                                f"{solve.wi.superConductor.IcAtTinit} is empty!"
                            )

                elif isinstance(IcVStapeLengthCSVFileName, Pancake3DSolveIcVsLength):
                    solve.wi.superConductor.lengthValues = (
                        solve.wi.superConductor.IcAtTinit.lengthValues
                    )
                    solve.wi.superConductor.IcValues = (
                        solve.wi.superConductor.IcAtTinit.criticalCurrentValues
                    )

                # check if the length values are exceeding the winding's length:
                if max(solve.wi.superConductor.lengthValues) > geo.wi.totalTapeLength:
                    raise ValueError(
                        "The length values in the criticalCurrentAtInitialTemperature"
                        " cannot be greater than the winding's total tape length"
                        f" ({geo.wi.totalTapeLength})!"
                    )

                if len(solve.wi.superConductor.lengthValues) != len(
                    solve.wi.superConductor.IcValues
                ):
                    raise ValueError(
                        "There needs to be the same number of length values and"
                        " critical current values for"
                        " criticalCurrentAtInitialTemperature!"
                    )

                # add Ic for start and end points of the tape:
                if solve.wi.superConductor.lengthValues[0] != 0:
                    solve.wi.superConductor.lengthValues.insert(0, 0)
                    solve.wi.superConductor.IcValues.insert(
                        0, solve.wi.superConductor.IcValues[0]
                    )

                if solve.wi.superConductor.lengthValues[-1] != geo.wi.totalTapeLength:
                    solve.wi.superConductor.lengthValues.append(geo.wi.totalTapeLength)
                    solve.wi.superConductor.IcValues.append(
                        solve.wi.superConductor.IcValues[-1]
                    )

                values["solve"] = solve

        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def mesh_calculations_and_checks(cls, values):
        """
        Checks if the length of the mesh lists are equal to the number of pancakes. If
        the length of the mesh lists are all one, then it means that the user wants to
        use the same mesh settings for all the pancakes. In this case, the length of
        the mesh lists are set to the number of pancakes. If all the settings' lengths
        are not one, and not equal to the number of pancakes, then the function raises
        an error.

        :param cls: class
        :type cls: class
        :param values: dictionary of PC3D
        :type values: dict
        :return: dictionary of PC3D
        :rtype: dict
        """
        geo = values["geometry"]
        mesh = values["mesh"]

        # ==============================================================================
        # MESH CHECKING STARTS =========================================================
        # ==============================================================================
        def check_mesh_input(meshInput, inputName):
            if not isinstance(meshInput, list):
                meshInput = [meshInput]

            length = len(meshInput)
            if length == 1:
                meshInput = meshInput * geo.N
            elif length != geo.N:
                raise ValueError(
                    "The list length of "
                    + inputName
                    + " must be either one (same mesh settings for all the pancakes) or"
                    " equal to the number of pancakes."
                )

            return meshInput

        mesh.wi.axne = check_mesh_input(mesh.wi.axne, inputName="axialNumberOfElements")
        mesh.wi.ane = check_mesh_input(
            mesh.wi.ane, inputName="azimuthalNumberOfElementsPerTurn"
        )
        mesh.wi.rne = check_mesh_input(
            mesh.wi.rne, inputName="radialNumberOfElementsPerTurn"
        )
        mesh.wi.axbc = check_mesh_input(
            mesh.wi.axbc, inputName="axialDistributionCoefficient"
        )
        if not geo.ii.tsa:
            if mesh.ii.rne is None:
                mesh.ii.rne = [1] * geo.N
            else:
                mesh.ii.rne = check_mesh_input(
                    mesh.ii.rne, inputName="radialNumberOfElementsPerTurn"
                )
        mesh.wi.elementType = check_mesh_input(
            mesh.wi.elementType, inputName="elementType"
        )

        for bumpCoefficient in mesh.wi.axbc:
            if bumpCoefficient > 1:
                raise ValueError(
                    "Axial bump coefficient must be smaller than or equal to 1!"
                )

        for ane in mesh.wi.ane:
            if ane < 7:
                raise ValueError(
                    "Azimuthal number of elements per turn must be greater than or"
                    " equal to 7!"
                )

        if True in mesh.wi.elementType == "hexahedron" and geo.N > 1:
            raise ValueError(
                "Hexahedron elements is not recommended for multiple pancakes due to"
                " the possible ill-shaped meshes at the gap between pancakes. If you"
                " still want to do it, please comment this error."
            )

        if not geo.ii.tsa and True in mesh.wi.elementType == "prism":
            raise ValueError(
                "Prism elements is not recommended for volume contact layer due to the"
                " possible ill-shaped meshes at the terminal's edges. If you still want"
                " to do it, please comment this error."
            )

        if not geo.ii.tsa and True in mesh.wi.elementType == "hexahedron":
            raise ValueError(
                "Hexahedron elements is not recommended for volume contact layer due to"
                " the possible ill-shaped meshes at the terminal's edges. If you still"
                " want to do it, please comment this error."
            )

        theWorstRectangularRatios = []
        theWorstTriangularRatios = []
        for i in range(geo.N):
            meshLengthPerElement = {}
            meshLengthPerElement["azimuthal elements"] = (
                2 * math.pi * geo.ti.o.r / mesh.wi.ane[i]
            )
            meshLengthPerElement["winding's radial elements"] = (
                geo.wi.t / mesh.wi.rne[i]
            )
            meshLengthPerElement["axial elements"] = geo.wi.h / mesh.wi.axne[i]
            if not geo.ii.tsa:
                meshLengthPerElement["contact layer's radial elements"] = (
                    geo.ii.t / mesh.ii.rne[i]
                )

            if mesh.wi.elementType[i] == "hexahedron":
                maxRectName = max(meshLengthPerElement, key=meshLengthPerElement.get)
                maxRectLengthPerElement = meshLengthPerElement[maxRectName]
                minRectName = min(meshLengthPerElement, key=meshLengthPerElement.get)
                minRectLengthPerElement = meshLengthPerElement[minRectName]

                maxTriLengthPerElement = 1
                minTriLengthPerElement = 1
                maxTriName = "dummy"
                minTriName = "dummy"

                theWorstRectangularRatio = (
                    maxRectLengthPerElement / minRectLengthPerElement
                )
                theWorstTriangularRatio = 1

            elif mesh.wi.elementType[i] == "tetrahedron":
                maxTriName = max(meshLengthPerElement, key=meshLengthPerElement.get)
                maxTriLengthPerElement = meshLengthPerElement[maxTriName]
                minTriName = min(meshLengthPerElement, key=meshLengthPerElement.get)
                minTriLengthPerElement = meshLengthPerElement[minTriName]

                maxRectLengthPerElement = 1
                minRectLengthPerElement = 1
                maxRectName = "dummy"
                minRectName = "dummy"

                theWorstRectangularRatio = 1
                theWorstTriangularRatio = (
                    maxTriLengthPerElement / minTriLengthPerElement
                )

            elif mesh.wi.elementType[i] == "prism":
                if geo.ii.tsa:
                    rectangularRatios = [
                        meshLengthPerElement["winding's radial elements"]
                        / meshLengthPerElement["axial elements"],
                        meshLengthPerElement["axial elements"]
                        / meshLengthPerElement["winding's radial elements"],
                        meshLengthPerElement["azimuthal elements"]
                        / meshLengthPerElement["axial elements"],
                        meshLengthPerElement["azimuthal elements"]
                        / meshLengthPerElement["axial elements"],
                    ]

                    triangularRatios = [
                        meshLengthPerElement["azimuthal elements"]
                        / meshLengthPerElement["winding's radial elements"],
                        meshLengthPerElement["winding's radial elements"]
                        / meshLengthPerElement["azimuthal elements"],
                    ]

                else:
                    rectangularRatios = [
                        meshLengthPerElement["winding's radial elements"]
                        / meshLengthPerElement["axial elements"],
                        meshLengthPerElement["axial elements"]
                        / meshLengthPerElement["winding's radial elements"],
                        meshLengthPerElement["azimuthal elements"]
                        / meshLengthPerElement["axial elements"],
                        meshLengthPerElement["azimuthal elements"]
                        / meshLengthPerElement["axial elements"],
                        meshLengthPerElement["contact layer's radial elements"]
                        / meshLengthPerElement["axial elements"],
                        meshLengthPerElement["axial elements"]
                        / meshLengthPerElement["contact layer's radial elements"],
                    ]

                    triangularRatios = [
                        meshLengthPerElement["azimuthal elements"]
                        / meshLengthPerElement["winding's radial elements"],
                        meshLengthPerElement["winding's radial elements"]
                        / meshLengthPerElement["azimuthal elements"],
                        meshLengthPerElement["azimuthal elements"]
                        / meshLengthPerElement["contact layer's radial elements"],
                        meshLengthPerElement["contact layer's radial elements"]
                        / meshLengthPerElement["azimuthal elements"],
                    ]

                theWorstRectangularRatio = max(rectangularRatios)
                indexRectangular = rectangularRatios.index(theWorstRectangularRatio)

                if indexRectangular == 0:
                    maxRectName = "winding's radial elements"
                    minRectName = "axial elements"
                elif indexRectangular == 1:
                    maxRectName = "axial elements"
                    minRectName = "winding's radial elements"
                elif indexRectangular == 2:
                    maxRectName = "azimuthal elements"
                    minRectName = "axial elements"
                elif indexRectangular == 3:
                    maxRectName = "azimuthal elements"
                    minRectName = "axial elements"
                elif indexRectangular == 4:
                    maxRectName = "contact layer's radial elements"
                    minRectName = "axial elements"
                elif indexRectangular == 5:
                    maxRectName = "axial elements"
                    minRectName = "contact layer's radial elements"

                theWorstTriangularRatio = max(triangularRatios)
                indexTriangular = triangularRatios.index(theWorstTriangularRatio)

                if indexTriangular == 0:
                    maxTriName = "azimuthal elements"
                    minTriName = "winding's radial elements"
                elif indexTriangular == 1:
                    maxTriName = "winding's radial elements"
                    minTriName = "azimuthal elements"
                elif indexTriangular == 2:
                    maxTriName = "azimuthal elements"
                    minTriName = "contact layer's radial elements"
                elif indexTriangular == 3:
                    maxTriName = "contact layer's radial elements"
                    minTriName = "azimuthal elements"

            numOfElements = {
                "azimuthal elements": mesh.wi.ane[i],
                "axial elements": mesh.wi.axne[i],
                "winding's radial elements": mesh.wi.rne[i],
            }
            if not geo.ii.tsa:
                numOfElements["contact layer's radial elements"] = mesh.ii.rne[i]

            lengths = {
                "azimuthal elements": 2 * math.pi * geo.ti.o.r,
                "axial elements": geo.wi.h,
                "winding's radial elements": geo.wi.t,
            }
            if not geo.ii.tsa:
                lengths["contact layer's radial elements"] = geo.ii.t

            allowedTriangularRatio = 120
            allowedRectangularRatio = 115

            allowedTriangularRatio = 999999
            allowedRectangularRatio = 999999

            theWorstRectangularRatios.append(theWorstRectangularRatio)
            theWorstTriangularRatios.append(theWorstTriangularRatio)
            for theWorstRatio, maxName, minName, allowedRatio in zip(
                [theWorstTriangularRatio, theWorstRectangularRatio],
                [maxTriName, maxRectName],
                [minTriName, minRectName],
                [allowedTriangularRatio, allowedRectangularRatio],
            ):
                if theWorstRatio > allowedRatio:
                    if numOfElements[minName] == 1:
                        # If the number of elements is 1, then the user cannot decrease the
                        # number of elements. So the only option is to increase the number
                        # of elements.
                        newMaxLengthPerElement = (
                            meshLengthPerElement[minName] * allowedRatio
                        )
                        newNumberOfElements = math.ceil(
                            lengths[maxName] / newMaxLengthPerElement
                        )
                        raise ValueError(
                            "The structred mesh inputs for pancake coil number"
                            f" {i+1} might cause ill-shaped meshes. Please increase the"
                            f" {maxName} per turn up to {newNumberOfElements}."
                        )
                    else:
                        newMaxLengthPerElement = (
                            meshLengthPerElement[minName] * allowedRatio
                        )
                        newNumberOfElementsToIncrease = math.ceil(
                            lengths[maxName] / newMaxLengthPerElement
                        )

                        newMinLengthPerElement = (
                            meshLengthPerElement[maxName] / allowedRatio
                        )
                        newNumberOfElementsToDecrease = math.floor(
                            lengths[minName] / newMinLengthPerElement
                        )
                        raise ValueError(
                            "The structred mesh inputs might cause ill-shaped meshes."
                            f" Please either increase the {maxName} per turn up"
                            f" to {newNumberOfElementsToIncrease} or decrease the"
                            f" {minName} per turn down to"
                            f" {newNumberOfElementsToDecrease}."
                        )

        mesh.theWorstRectangularRatio = max(theWorstRectangularRatios)
        mesh.theWorstTriangularRatio = max(theWorstTriangularRatios)

        # Structured air and terminals checks:
        if mesh.ai.structured == True:
            # Air type cannot be cuboid!
            if geo.ai.type == "cuboid":
                raise ValueError(
                    "Structured air cannot be used if the air type is cuboid!"
                )

            # Element type cannot be hexahedron!
            if mesh.wi.elementType[0] == "hexahedron":
                raise ValueError(
                    "Structured air cannot be used if the element type is hexahedron!"
                    " Only tetrahedron and prism are allowed."
                )

        if mesh.ai.structured == True or mesh.ti.structured == True:
            # Every winding and contact layer mesh settings must be the same:
            if len(set(mesh.wi.axne)) != 1:
                raise ValueError(
                    "The axial number of elements per turn must be the same for all the"
                    " windings if structured air or structured terminals meshes are"
                    " used!"
                )
            if len(set(mesh.wi.ane)) != 1:
                raise ValueError(
                    "The azimuthal number of elements per turn must be the same for all"
                    " the windings if structured air or structured terminals meshes are"
                    " used!"
                )
            if len(set(mesh.wi.rne)) != 1:
                raise ValueError(
                    "The radial number of elements per turn must be the same for all"
                    " the windings if structured air or structured terminals meshes are"
                    " used!"
                )
            if not geo.ii.tsa:
                if len(set(mesh.ii.rne)) != 1:
                    raise ValueError(
                        "The radial number of elements per turn must be the same for"
                        " all the contact layers if structured air or structured"
                        " terminals meshes are used!"
                    )

            # Start angle must be 0:
            if math.isclose(geo.wi.theta_i, 0, abs_tol=geo.dimTol) == False:
                raise ValueError(
                    "The start angle of the winding must be 0 if structured air or"
                    " structured terminals meshes are used!"
                )

            # The number of volumes per turn must be 4:
            if geo.wi.NofVolPerTurn != 4:
                logger.warning(
                    "The number of volumes per turn will be set to 4 since"
                    " structured air or structured terminals meshes are used."
                )

            geo.wi.NofVolPerTurn = 4

            # The number of azimuthal elements per turn must be divisible by 4:
            if mesh.wi.ane[0] % 4 != 0:
                raise ValueError(
                    "The number of azimuthal elements per turn must be divisible by 4"
                    " if structured air or structured terminals meshes are used!"
                )

        # ==============================================================================
        # MESH CHECKING ENDS ===========================================================
        # ==============================================================================

        # ==============================================================================
        # MESH CALCULATIONS STARTS =====================================================
        # ==============================================================================
        mesh.sizeMin = max(meshLengthPerElement.values()) * mesh.relSizeMin
        mesh.sizeMax = max(meshLengthPerElement.values()) * mesh.relSizeMax

        mesh.startGrowingDistance = (geo.ti.o.r - geo.ti.i.r) / 2
        if geo.ai.type == "cylinder":
            mesh.stopGrowingDistance = geo.ai.r - geo.ti.o.r
        elif geo.ai.type == "cuboid":
            mesh.stopGrowingDistance = geo.ai.a / 2 - geo.ti.o.r

        def getSizeAtTopAndBottom(sizeMax, airMargin):
            if airMargin > mesh.stopGrowingDistance:
                sizeAtTopAndBottom = mesh.sizeMax
            elif airMargin < mesh.startGrowingDistance:
                sizeAtTopAndBottom = mesh.sizeMin
            else:
                sizeAtTopAndBottom = mesh.sizeMin + (sizeMax - mesh.sizeMin) * (
                    (airMargin - mesh.startGrowingDistance)
                    / (mesh.stopGrowingDistance - mesh.startGrowingDistance)
                )

            return sizeAtTopAndBottom

        def getSizeMax(sizeAtTopAndBottom, airMargin):
            if airMargin > mesh.stopGrowingDistance:
                sizeMax = sizeAtTopAndBottom
            elif airMargin < mesh.startGrowingDistance:
                # any sizeMax value will work here
                sizeMax = -1
            else:
                sizeMax = (sizeAtTopAndBottom - mesh.sizeMin) * (
                    (mesh.stopGrowingDistance - mesh.startGrowingDistance)
                    / (airMargin - mesh.startGrowingDistance)
                ) + mesh.sizeMin

            return sizeMax

        def getAirMargin(sizeAtTopAndBottom, sizeMax):
            airMargin = (sizeAtTopAndBottom - mesh.sizeMin) * (
                (mesh.stopGrowingDistance - mesh.startGrowingDistance)
                / (sizeMax - mesh.sizeMin)
            ) + mesh.startGrowingDistance

            return airMargin

        sizeAtTopAndBottom = getSizeAtTopAndBottom(mesh.sizeMax, geo.ai.margin)

        # tolerance = 10.7
        tolerance = 999999
        if sizeAtTopAndBottom / min(geo.ti.i.t, geo.ti.o.t) > tolerance:
            desiredSizeAtTopAndBottom = min(geo.ti.i.t, geo.ti.o.t) * tolerance
            desiredTerminalRadius = sizeAtTopAndBottom / tolerance
            desiredAirMargin = getAirMargin(desiredSizeAtTopAndBottom, mesh.sizeMax)
            desiredRelSizeMax = math.floor(
                getSizeMax(desiredSizeAtTopAndBottom, geo.ai.margin)
                / max(meshLengthPerElement.values())
            )
            raise ValueError(
                "Terminals are too thin for the given maximum mesh element size."
                f" Please either decrease the air margin to {desiredAirMargin:.5f},"
                f" decrease the maximum mesh element size to {desiredRelSizeMax}, or"
                f" increase the terminal radius to {desiredTerminalRadius:.5f}."
            )

        # ==============================================================================
        # MESH CALCULATIONS ENDS =======================================================
        # ==============================================================================

        values["mesh"] = mesh
        values["geometry"] = geo
        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_contact_layer_materials(cls, values):
        if values["geometry"].ii.tsa:
            if values["solve"].ii.resistivity is None:
                if not (
                    values["solve"].ii.material.getdpTSAMassResistivityFunction
                    and values["solve"].ii.material.getdpTSAStiffnessResistivityFunction
                    and values["solve"].ii.material.getdpTSARHSFunction
                    and values["solve"].ii.material.getdpTSATripleFunction
                ):
                    raise ValueError(
                        "Thin-shell resistivity properties for"
                        f" {values['solve'].ii.material.name} are not"
                        " defined! Please define custom constant resistivity value or"
                        " use a different material."
                    )
            if values["solve"].ii.thermalConductivity is None:
                if not (
                    values["solve"].ii.material.getdpTSAMassThermalConductivityFunction
                    and values[
                        "solve"
                    ].ii.material.getdpTSAStiffnessThermalConductivityFunction
                ):
                    raise ValueError(
                        "Thin-shell thermal conductivity properties for"
                        f" {values['solve'].ii.material.name} are not"
                        " defined! Please define custom constant thermal conductivity"
                        " value or use a different material."
                    )
            if values["solve"].ii.specificHeatCapacity is None:
                if not values["solve"].ii.material.getdpTSAMassHeatCapacityFunction:
                    raise ValueError(
                        "Thin-shell specific heat capacity properties for"
                        f" {values['solve'].ii.material.name} are not"
                        " defined! Please define custom constant specific heat capacity"
                        " value or use a different material."
                    )

        if values["solve"].ii.resistivity is not None:
            if values["solve"].ii.resistivity == "perfectlyInsulating":
                if values["geo"].N > 1:
                    raise ValueError(
                        "perfectlyInsulating cannot be used if there are multiple"
                        " pancakes!"
                    )

        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def check_and_calculate_postprocessing_quantities(cls, values):
        """ """
        solve = values["solve"]
        postproc = values["postproc"]

        if postproc is None:
            return values

        if postproc.timeSeriesPlots is not None:
            electromagneticRequiredQuantities = [
                "magnitudeOfMagneticField",
                "magnitudeOfCurrentDensity",
                "resistiveHeating",
                "axialComponentOfTheMagneticField",
                "totalResistiveHeating",
                "voltageBetweenTerminals",
                "currentThroughCoil",
                "resistivity",
                "derivativeOfRhoWithRespectToJ",
                "magneticEnergy",
            ]
            thermalRequiredQuantities = [
                "temperature",
                "magnitudeOfHeatFlux",
            ]
            for timeSeriesPlot in postproc.timeSeriesPlots:
                if (
                    timeSeriesPlot.quantity in thermalRequiredQuantities
                    and solve.type == "electromagnetic"
                ):
                    raise ValueError(
                        f'"{timeSeriesPlot.quantity}" cannot be plotted with'
                        " timeSeriesPlots if the type is electromagnetic because"
                        " it is not calculated!"
                    )

                if (
                    timeSeriesPlot.quantity in electromagneticRequiredQuantities
                    and solve.type == "thermal"
                ):
                    raise ValueError(
                        f'"{timeSeriesPlot.quantity}" cannot be plotted with'
                        " timeSeriesPlots if the type is thermal because it is not"
                        " calculated!"
                    )
                if (
                    timeSeriesPlot.quantity == "derivativeOfRhoWithRespectToJ"
                    and solve.wi.resistivity is not None
                ):
                    raise ValueError(
                        "derivativeOfRhoWithRespectToJ cannot be plotted with"
                        " timeSeriesPlots if the winding resistivity is linear!"
                    )

        if postproc.magneticFieldOnCutPlane is not None:
            if solve.type == "thermal":
                raise ValueError(
                    "magneticFieldOnCutPlane cannot be plotted if the type is thermal!"
                )

        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def calculate_positions(cls, values):
        """"""
        geo: Pancake3DGeometry = values["geometry"]
        mesh: Pancake3DMesh = values["mesh"]
        solve: Pancake3DSolve = values["solve"]
        postproc: Pancake3DPostprocess = values["postproc"]

        def calculate_position(position):
            coordinatesAreGiven = False
            if (
                position.x is not None
                and position.y is not None
                and position.z is not None
            ):
                coordinatesAreGiven = True

            turnNumberIsGiven = False
            if position.turnNumber is not None:
                turnNumberIsGiven = True
                if position.turnNumber < 0:
                    raise ValueError("Turn number for the position cannot be negative!")

                if position.turnNumber > geo.wi.N:
                    raise ValueError(
                        "Turn number for the position must be smaller than"
                        " the number of turns of the winding!"
                    )

                if geo.N == 1:
                    position.whichPancakeCoil = 1
                else:
                    if position.whichPancakeCoil is None:
                        raise ValueError(
                            "whichPancakeCoil entry must be specified if the position"
                            " is specified with turnNumber!"
                        )
                    if position.whichPancakeCoil > geo.N:
                        raise ValueError(
                            "whichPancakeCoil entry must be smaller than or equal to"
                            " the number of pancakes!"
                        )

            if turnNumberIsGiven:
                if position.x or position.y or position.z:
                    raise ValueError(
                        "Either turn number or x, y, and z coordinates can be"
                        " specified!"
                    )
                if geo.N == 1:
                    position.whichPancakeCoil = 1
                elif geo.N > 1:
                    if position.whichPancakeCoil is None:
                        raise ValueError(
                            "whichPancakeCoil entry must be specified if the"
                            " position is specified with turnNumber!"
                        )
                if position.turnNumber > geo.wi.N:
                    raise ValueError(
                        "Turn number for the position must be smaller than"
                        " the number of turns of the winding!"
                    )
                # Calculate x, y, and z coordinates from turn number:
                if geo.ii.tsa:
                    windingThickness = geo.wi.t + geo.ii.t * (geo.wi.N - 1) / geo.wi.N
                    gapThickness = 0
                else:
                    windingThickness = geo.wi.t
                    gapThickness = geo.ii.t

                innerRadius = geo.wi.r_i
                initialTheta = geo.wi.theta_i
                ane = mesh.wi.ane[0]
                numberOfPancakes = geo.N
                gapBetweenPancakes = geo.gap
                windingHeight = geo.wi.h

                turnNumber = position.turnNumber
                whichPancake = position.whichPancakeCoil

                elementStartTurnNumber = math.floor(turnNumber / (1 / ane)) * (1 / ane)
                elementEndTurnNumber = elementStartTurnNumber + 1 / ane

                class point:
                    def __init__(self, x, y, z):
                        self.x = x
                        self.y = y
                        self.z = z

                    def __add__(self, other):
                        return point(
                            self.x + other.x, self.y + other.y, self.z + other.z
                        )

                    def __sub__(self, other):
                        return point(
                            self.x - other.x, self.y - other.y, self.z - other.z
                        )

                    def __mul__(self, scalar):
                        return point(self.x * scalar, self.y * scalar, self.z * scalar)

                    def __truediv__(self, scalar):
                        return point(self.x / scalar, self.y / scalar, self.z / scalar)

                    def rotate(self, degrees):
                        return point(
                            self.x * math.cos(degrees) - self.y * math.sin(degrees),
                            self.x * math.sin(degrees) + self.y * math.cos(degrees),
                            self.z,
                        )

                    def normalize(self):
                        return self / math.sqrt(self.x**2 + self.y**2 + self.z**2)

                if whichPancake % 2 == 1:
                    # If the spiral is counter-clockwise, the initial theta angle decreases,
                    # and r increases as the theta angle decreases.
                    multiplier = 1
                elif whichPancake % 2 == 0:
                    # If the spiral is clockwise, the initial theta angle increases, and r
                    # increases as the theta angle increases.
                    multiplier = -1

                # Mesh element's starting point:
                elementStartTheta = 2 * math.pi * elementStartTurnNumber * multiplier
                elementStartRadius = (
                    innerRadius
                    + elementStartTheta
                    / (2 * math.pi)
                    * (gapThickness + windingThickness)
                    * multiplier
                )
                elementStartPointX = elementStartRadius * math.cos(
                    initialTheta + elementStartTheta
                )
                elementStartPointY = elementStartRadius * math.sin(
                    initialTheta + elementStartTheta
                )
                elementStartPointZ = (
                    -(
                        numberOfPancakes * windingHeight
                        + (numberOfPancakes - 1) * gapBetweenPancakes
                    )
                    / 2
                    + windingHeight / 2
                    + (whichPancake - 1) * (windingHeight + gapBetweenPancakes)
                )
                elementStartPoint = point(
                    elementStartPointX, elementStartPointY, elementStartPointZ
                )

                # Mesh element's ending point:
                elementEndTheta = 2 * math.pi * elementEndTurnNumber * multiplier
                elementEndRadius = (
                    innerRadius
                    + elementEndTheta
                    / (2 * math.pi)
                    * (gapThickness + windingThickness)
                    * multiplier
                )
                elementEndPointX = elementEndRadius * math.cos(
                    initialTheta + elementEndTheta
                )
                elementEndPointY = elementEndRadius * math.sin(
                    initialTheta + elementEndTheta
                )
                elementEndPointZ = elementStartPointZ
                elementEndPoint = point(
                    elementEndPointX, elementEndPointY, elementEndPointZ
                )

                turnNumberFraction = (turnNumber - elementStartTurnNumber) / (
                    elementEndTurnNumber - elementStartTurnNumber
                )
                location = (
                    elementStartPoint
                    + (elementEndPoint - elementStartPoint) * turnNumberFraction
                ) + (elementEndPoint - elementStartPoint).rotate(
                    -math.pi / 2
                ).normalize() * windingThickness / 2 * multiplier

                position.x = location.x
                position.y = location.y
                position.z = location.z

            return position

        # Calculate positons for time series plots:
        if postproc is not None:
            if postproc.timeSeriesPlots is not None:
                for timeSeriesPlot in postproc.timeSeriesPlots:
                    timeSeriesPlot.position = calculate_position(
                        timeSeriesPlot.position
                    )

        if solve is not None:
            # Calculate positions for tolerances:
            for tolerance in solve.t.adaptive.tolerances:
                if tolerance.position is not None:
                    tolerance.position = calculate_position(tolerance.position)

            for tolerance in solve.nls.tolerances:
                if tolerance.position is not None:
                    tolerance.position = calculate_position(tolerance.position)

        # Calculate z-position for local defect:
        if solve.localDefects is not None:
            if (
                solve.localDefects.jCritical is not None
                and solve.localDefects.jCritical.startTurn is not None
            ):
                localDefect: Pancake3DSolveLocalDefect = solve.localDefects.jCritical
                if geo.N == 1:
                    localDefect.whichPancakeCoil = 1
                elif geo.N > 1:
                    if localDefect.whichPancakeCoil is None:
                        raise ValueError(
                            "whichPancakeCoil entry must be specified if the"
                            " position is specified with turnNumber!"
                        )
                if localDefect.endTurn > geo.wi.N or localDefect.startTurn > geo.wi.N:
                    raise ValueError(
                        "Turn number for the position must be smaller than"
                        " the number of turns of the winding! (jCritical local defect)"
                    )

                bottomZ = -(geo.N * geo.wi.h + (geo.N - 1) * geo.gap) / 2 + (
                    localDefect.whichPancakeCoil - 1
                ) * (geo.wi.h + geo.gap)
                topZ = bottomZ + geo.wi.h

                localDefect.zTop = topZ
                localDefect.zBottom = bottomZ

        return values

    @root_validator(pre=False, allow_reuse=True, skip_on_failure=True)
    @classmethod
    def calculate_onSection(cls, values):
        """ """
        geo: Pancake3DGeometry = values["geometry"]
        solve: Pancake3DSolve = values["solve"]
        postproc: Pancake3DPostprocess = values["postproc"]

        import numpy as np

        if postproc is not None:
            if postproc.magneticFieldOnCutPlane is not None:

                class unitVector:
                    def __init__(self, u, v, w) -> None:
                        length = math.sqrt(u**2 + v**2 + w**2)
                        self.u = u / length
                        self.v = v / length
                        self.w = w / length

                    def rotate(self, theta, withRespectTo):
                        # Rotate with respect to the withRespectTo vector by theta degrees:
                        # https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
                        a = withRespectTo.u
                        b = withRespectTo.v
                        c = withRespectTo.w

                        rotationMatrix = np.array(
                            [
                                [
                                    math.cos(theta) + a**2 * (1 - math.cos(theta)),
                                    a * b * (1 - math.cos(theta)) - c * math.sin(theta),
                                    a * c * (1 - math.cos(theta)) + b * math.sin(theta),
                                ],
                                [
                                    b * a * (1 - math.cos(theta)) + c * math.sin(theta),
                                    math.cos(theta) + b**2 * (1 - math.cos(theta)),
                                    b * c * (1 - math.cos(theta)) - a * math.sin(theta),
                                ],
                                [
                                    c * a * (1 - math.cos(theta)) - b * math.sin(theta),
                                    c * b * (1 - math.cos(theta)) + a * math.sin(theta),
                                    math.cos(theta) + c**2 * (1 - math.cos(theta)),
                                ],
                            ]
                        )
                        vector = np.array([[self.u], [self.v], [self.w]])
                        rotatedVector = rotationMatrix @ vector
                        return unitVector(
                            rotatedVector[0][0],
                            rotatedVector[1][0],
                            rotatedVector[2][0],
                        )

                    def __pow__(self, otherUnitVector):
                        # Cross product:
                        u = self.v * otherUnitVector.w - self.w * otherUnitVector.v
                        v = self.w * otherUnitVector.u - self.u * otherUnitVector.w
                        w = self.u * otherUnitVector.v - self.v * otherUnitVector.u
                        return unitVector(u, v, w)

                    def __mul__(self, otherUnitVector) -> float:
                        # Dot product:
                        return (
                            self.u * otherUnitVector.u
                            + self.v * otherUnitVector.v
                            + self.w * otherUnitVector.w
                        )

                planeNormal = postproc.magneticFieldOnCutPlane.planeNormal
                if len(planeNormal) != 3:
                    raise ValueError(
                        "planeNormal for magneticFieldOnCutPlane must be a list of"
                        " three numbers!"
                    )

                planeNormal = unitVector(planeNormal[0], planeNormal[1], planeNormal[2])

                # planeXAxis = postproc.magneticFieldOnCutPlane.planeXAxis
                # if len(planeXAxis) != 3:
                #     raise ValueError(
                #         "planeXAxis for magneticFieldOnCutPlane must be a list of"
                #         " three numbers!"
                #     )

                # planeXAxis = unitVector(planeXAxis[0], planeXAxis[1], planeXAxis[2])

                # if (
                #     math.isclose(planeNormal * planeXAxis, 0, abs_tol=geo.dimTol)
                #     == False
                # ):
                #     raise ValueError(
                #         "planeNormal and planeXAxis must be perpendicular to each"
                #         " other! If planeNormal is chosen arbitrarily, planeXAxis must"
                #         " be specified."
                #     )

                # A plane that passes through the origin with the normal vector planeNormal
                # can be defined as:
                # a*x + b*y + c*z = 0
                a = planeNormal.u
                b = planeNormal.v
                c = planeNormal.w

                # Pick three points on the plane to define a rectangle. The points will
                # be the corners of the rectangle.

                # To do that, change coordinate system:

                # Find a vector that is perpendicular to planeNormal:
                randomVector = unitVector(c, a, b)
                perpendicularVector1 = planeNormal**randomVector

                # Rotate perperndicular vector with respect to the plane's normal vector
                # by 90 degrees to find the second perpendicular vector:
                perpendicularVector2 = perpendicularVector1.rotate(
                    math.pi / 2, planeNormal
                )

                # Build the transformation matrix to change from the plane's coordinate
                # system to the global coordinate system:
                transformationMatrix = np.array(
                    [
                        [
                            perpendicularVector1.u,
                            perpendicularVector1.v,
                            perpendicularVector1.w,
                        ],
                        [
                            perpendicularVector2.u,
                            perpendicularVector2.v,
                            perpendicularVector2.w,
                        ],
                        [planeNormal.u, planeNormal.v, planeNormal.w],
                    ]
                )
                transformationMatrix = np.linalg.inv(transformationMatrix)

                # Select three points to define the rectangle. Pick large points because
                # only the intersection of the rectangle and the mesh will be used.
                if geo.ai.type == "cuboid":
                    airMaxWidth = 2 * math.sqrt(
                        (geo.ai.a / 2) ** 2 + (geo.ai.a / 2) ** 2
                    )
                if geo.ai.type == "cylinder":
                    airMaxWidth = geo.ai.r

                point1InPlaneCoordinates = np.array(
                    [5 * max(airMaxWidth, geo.ai.h), 5 * max(airMaxWidth, geo.ai.h), 0]
                )
                point1 = transformationMatrix @ point1InPlaneCoordinates

                point2InPlaneCoordinates = np.array(
                    [-5 * max(airMaxWidth, geo.ai.h), 5 * max(airMaxWidth, geo.ai.h), 0]
                )
                point2 = transformationMatrix @ point2InPlaneCoordinates

                point3InPlaneCoordinates = np.array(
                    [
                        -5 * max(airMaxWidth, geo.ai.h),
                        -5 * max(airMaxWidth, geo.ai.h),
                        0,
                    ]
                )
                point3 = transformationMatrix @ point3InPlaneCoordinates

                # Round the point coordinates to the nearest multiple of the dimTol:
                point1[0] = round(point1[0] / geo.dimTol) * geo.dimTol
                point1[1] = round(point1[1] / geo.dimTol) * geo.dimTol
                point1[2] = round(point1[2] / geo.dimTol) * geo.dimTol
                point2[0] = round(point2[0] / geo.dimTol) * geo.dimTol
                point2[1] = round(point2[1] / geo.dimTol) * geo.dimTol
                point2[2] = round(point2[2] / geo.dimTol) * geo.dimTol
                point3[0] = round(point3[0] / geo.dimTol) * geo.dimTol
                point3[1] = round(point3[1] / geo.dimTol) * geo.dimTol
                point3[2] = round(point3[2] / geo.dimTol) * geo.dimTol

                postproc.magneticFieldOnCutPlane.onSection = [
                    [float(point1[0]), float(point1[1]), float(point1[2])],
                    [float(point2[0]), float(point2[1]), float(point2[2])],
                    [float(point3[0]), float(point3[1]), float(point3[2])],
                ]

                # Add break points:
                if postproc.magneticFieldOnCutPlane.timesToBePlotted is not None:
                    solve.t.adaptive.breakPoints.extend(
                        postproc.magneticFieldOnCutPlane.timesToBePlotted
                    )
                    solve.t.adaptive.breakPoints = list(
                        set(solve.t.adaptive.breakPoints)
                    )
                    solve.t.adaptive.breakPoints.sort()

        values["postproc"] = postproc

        return values
