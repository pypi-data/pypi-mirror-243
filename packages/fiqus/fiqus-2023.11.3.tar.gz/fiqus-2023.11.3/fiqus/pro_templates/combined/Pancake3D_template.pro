{% import "materials.pro" as materials %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro FUNCTIONSPACE_TSAFunctionSpaces(type) %}
// TSA function spaces starts ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
For i In {1:INPUT_NumOfTSAElements - 1}
{% if type == "electromagnetic" %}
    {
        Name SPACE_hPhiThinShell~{i};
        Type Form1;
        BasisFunction{
            {
                Name se;
                NameOfCoef he~{i};
                Function BF_Edge;
                Support DOM_insulationSurface;
                Entity EdgesOf[ All ];
            }
        }
    }
{% elif type == "thermal" %}
    {
        Name SPACE_temperatureThinShell~{i};
        Type Form0;
        BasisFunction{
            {
                Name se;
                NameOfCoef te~{i};
                Function BF_Node;
                Support DOM_insulationSurface;
                Entity NodesOf[ All ];
            }
        }
        Constraint{
            {
                NameOfCoef te~{i};
                EntityType NodesOf;
                NameOfConstraint CONSTRAINT_initialTemperature;
            }
        }
    }
{% endif %}
EndFor
// TSA function spaces ends ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro FUNCTIONSPACE_TSABasisFunctions(type) %}
// TSA basis functions starts ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

// TSA contributions following special indexing to restrict them to one side of the thin
// layer split in plus and minus side.
{% for i in range(1, NofSets+1) %}
{
    Name BASISFUN_snMinus_<<i>>;
    NameOfCoef BASISFUN_snMinus_coeff_<<i>>;
    {% if type == "electromagnetic" %}
    Function BF_Edge;
    {% elif type == "thermal" %}
    Function BF_Node;
    {% endif %}
    Support Region[
                {
                    DOM_insulationSurface_<<i>>,
                    DOM_insulationSurface_<<i+1>>,
                    DOM_windingMinus_<<i>>,
                    DOM_windingMinus_<<i+1>>
                }
            ];
    {% if type == "electromagnetic" %}
    Entity EdgesOf[
                DOM_insulationSurface_<<i>>,
                Not {DOM_insulationBoundaryCurvesAir, DOM_insulationBoundaryCurvesTerminal, DOM_insulationSurface_<<i-1>>}
                ];
    {% elif type == "thermal" %}
    Entity NodesOf[
                DOM_insulationSurface_<<i>>,
                Not { DOM_insulationSurface_<<i-1>>, DOM_insulationBoundaryCurvesTerminal }
                ];
    {% endif %}
}

{
    Name BASISFUN_snPlus_<<i>>;
    NameOfCoef BASISFUN_snPlus_coeff_<<i>>;
    {% if type == "electromagnetic" %}
    Function BF_Edge;
    {% elif type == "thermal" %}
    Function BF_Node;
    {% endif %}
    Support Region[
                {
                    DOM_insulationSurface_<<i>>,
                    DOM_insulationSurface_<<i+1>>,
                    DOM_windingPlus_<<i>>,
                    DOM_windingPlus_<<i+1>>
                }
            ];
    {% if type == "electromagnetic" %}
    Entity EdgesOf[
                DOM_insulationSurface_<<i>>,
                Not {DOM_insulationBoundaryCurvesAir, DOM_insulationBoundaryCurvesTerminal, DOM_insulationSurface_<<i-1>>}
                ];
    {% elif type == "thermal" %}
    Entity NodesOf[
                DOM_insulationSurface_<<i>>,
                Not { DOM_insulationSurface_<<i-1>>, DOM_insulationBoundaryCurvesTerminal }
                ];
    {% endif %}
}
{% endfor %}

// TSA basis functions ends ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro FUNCTIONSPACE_TSASubSpaces(aditionalBasisFunctions=[]) %}
// TSA subspaces starts ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

// identification of the positive and negative side of the contact layer:
{
    Name SUBSPACE_insulationSurface_down;
    NameOfBasisFunction{
{% for i in range(1, NofSets+1) %}
    {% if loop.last and len(aditionalBasisFunctions)==0 %}
        BASISFUN_snMinus_<<i>>
    {% else %}
        BASISFUN_snMinus_<<i>>,
    {% endif %}
{% endfor %}
{% for bf in aditionalBasisFunctions %}
        {% if loop.last %}
        <<bf>>
        {% else %}
        <<bf>>,
        {% endif %}
{% endfor %}
    };
}
{
    Name SUBSPACE_insulationSurface_up;
    NameOfBasisFunction{
{% for i in range(1, NofSets+1) %}
    {% if loop.last and len(aditionalBasisFunctions)==0 %}
        BASISFUN_snPlus_<<i>>
    {% else %}
        BASISFUN_snPlus_<<i>>,
    {% endif %}
{% endfor %}
{% for bf in aditionalBasisFunctions %}
        {% if loop.last %}
        <<bf>>
        {% else %}
        <<bf>>,
        {% endif %}
{% endfor %}
    };
}

// TSA subspaces ends ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro FORMULATION_VolumetricQuantities(type) %}
// Volumetric quantities starts ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
{% if type == "electromagnetic" %}
{
    Name LOCALQUANT_h;
    Type Local;
    NameOfSpace SPACE_hPhi;
}
{
    // Different test function is needed for non-symmetric tensors, otherwise, getdp
    // assumes the tensors are symmetric and the result is wrong.
    Name LOCALQUANT_h_Derivative;
    Type Local;
    NameOfSpace SPACE_hPhi;
}
{
    Name GLOBALQUANT_I;
    Type Global;
    NameOfSpace SPACE_hPhi[GLOBALQUANT_I];
}
{
    Name GLOBALQUANT_V;
    Type Global;
    NameOfSpace SPACE_hPhi[GLOBALQUANT_V];
}
{% elif type == "thermal" %}
{
    Name LOCALQUANT_T;
    Type Local;
    NameOfSpace SPACE_temperature;
}
{% else %}
<<0/0>>
// ERROR: wrong type for FORMULATION_VolumetricQuantities!
{% endif %}
// Volumetric quantities ends ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro FORMULATION_TSAQuantities(type) %}
// TSA quantities starts +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
{% if type == "electromagnetic" %}
{
    Name LOCALQUANT_hThinShell~{0};
    Type Local;
    NameOfSpace SPACE_hPhi[SUBSPACE_insulationSurface_down];
}

For i In {1:INPUT_NumOfTSAElements-1}
    {
        Name LOCALQUANT_hThinShell~{i};
        Type Local;
        NameOfSpace SPACE_hPhiThinShell~{i};
    }
EndFor

{
    Name LOCALQUANT_hThinShell~{INPUT_NumOfTSAElements};
    Type Local;
    NameOfSpace SPACE_hPhi[SUBSPACE_insulationSurface_up];
}
{% elif type == "thermal" %}
{
    Name LOCALQUANT_TThinShell~{0};
    Type Local;
    NameOfSpace SPACE_temperature[SUBSPACE_insulationSurface_up];
}

For i In{1 : INPUT_NumOfTSAElements - 1}
    {
        Name LOCALQUANT_TThinShell~{i};
        Type Local;
        NameOfSpace SPACE_temperatureThinShell~{i};
    }
EndFor

{
    Name LOCALQUANT_TThinShell~{INPUT_NumOfTSAElements};
    Type Local;
    NameOfSpace SPACE_temperature[SUBSPACE_insulationSurface_down];
}
{% else %}
<<0/0>>
// ERROR: wrong type for FORMULATION_TSAQuantities!
{% endif %}
// TSA quantities ends +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro FORMULATION_VolumetricIntegrals(type) %}
{% if type == "electromagnetic" %}
Integral{
    // note that it is only defined in DOM_allConducting, not all domain
    [ rho[<<rhoArguments>>] * Dof{d LOCALQUANT_h}, {d LOCALQUANT_h} ];
    In DOM_allConducting;
    Jacobian JAC_vol;
    Integration Int;
}

Integral{
    DtDof[mu[] * Dof{LOCALQUANT_h}, {LOCALQUANT_h}];
    In DOM_total;
    Jacobian JAC_vol;
    Integration Int;
}
    {% if dm.magnet.solve.wi.superConductor and not dm.magnet.solve.wi.resistivity and type == "electromagnetic" %}
Integral
{
    JacNL[d_of_rho_wrt_j_TIMES_j[<<rhoArguments>>] * Dof{d LOCALQUANT_h} , {d LOCALQUANT_h_Derivative} ];
    In DOM_allWindings; 
    Jacobian JAC_vol;
    Integration Int; 
}
    {% endif %}
// the global term allows to link current and voltage in the cuts
GlobalTerm{
    [ Dof{GLOBALQUANT_V}, {GLOBALQUANT_I} ];
    In DOM_airCuts;
}
{% elif type == "thermal" %}
Integral {
    [ kappa[<<kappaArguments>>] * Dof{d LOCALQUANT_T}, {d LOCALQUANT_T} ];
    In DOM_allConducting;
    Jacobian JAC_vol;
    Integration Int;
}
Integral {
    DtDof[ Cv[<<CvArguments>>] * Dof{LOCALQUANT_T}, {LOCALQUANT_T} ];
    In DOM_allConducting;
    Jacobian JAC_vol;
    Integration Int;
}
{% if dm.magnet.solve.ti.cooling == "cryocooler" %}
Integral {
    // Division by area to compute Watts per meter squared
    // SurfaceArea function does not allow DOM_*** as argument, so we need to use
    // the actual ids
    [  CFUN_PvsT_cryocooler_SHI_SRDE_418D4[{LOCALQUANT_T}]/SurfaceArea[]{<< rm.powered.surf_in.numbers | join(', ') >>, << rm.powered.surf_out.numbers | join(', ') >> }, {LOCALQUANT_T} ];
    In Region[{DOM_bottomTerminalSurface, DOM_topTerminalSurface}];
    Jacobian JAC_sur;
    Integration Int;
}
{% endif %}

{% elif type == "resistiveHeating" %}
Integral {
    [ -(rho[<<rhoArguments>>] * {d LOCALQUANT_h}) * {d LOCALQUANT_h}, {LOCALQUANT_T} ];
    In DOM_allConducting;
    Jacobian JAC_vol;
    Integration Int;
}
{% endif %}
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro FORMULATION_TSAIntegrals(type) %}
{% if type == "electromagnetic" %}
    {% set quantityName = "LOCALQUANT_hThinShell" %}
    {% set functionKey = "electromagnetic" %}
{% elif  type == "thermal" %}
    {% set quantityName = "LOCALQUANT_TThinShell" %}
    {% set functionKey = "thermal" %}
{% elif type == "resistiveHeating" %}
{% else %}
    <<0/0>>
    // ERROR: wrong type for FORMULATION_TSAIntegrals!
{% endif %}

{% if dm.magnet.solve.type in ["weaklyCoupled", "stronglyCoupled", "thermal"] %}
    {% set temperatureArgument1 = "{LOCALQUANT_TThinShell~{i}}" %}
    {% set temperatureArgument2 = "{LOCALQUANT_TThinShell~{i+1}}" %}
{% elif dm.magnet.solve.type == "electromagnetic" %}
    {% set temperatureArgument1 = "INPUT_initialTemperature" %}
    {% set temperatureArgument2 = "INPUT_initialTemperature" %}
{% endif %}

{% if type == "electromagnetic" or type == "thermal" %}
For i In {0:INPUT_NumOfTSAElements-1}
    {% for a in range(1,3) %}
        {% for b in range(1,3) %}
    Integral {
        [
            <<functionKey>>MassFunctionNoDta<<a>>b<<b>>[
                <<temperatureArgument1>>,
                <<temperatureArgument2>>
            ] * Dof{d <<quantityName>>~{i + <<a>> - 1}},
            {d <<quantityName>>~{i + <<b>> - 1}}
        ];
        In DOM_insulationSurface;
        Integration Int;
        Jacobian JAC_sur;
    }

    Integral {
        [
            <<functionKey>>StiffnessFunctiona<<a>>b<<b>>[
                <<temperatureArgument1>>,
                <<temperatureArgument2>>
            ] * Dof{<<quantityName>>~{i + <<a>> - 1}},
            {<<quantityName>>~{i + <<b>> - 1}}
        ];
        In DOM_insulationSurface;
        Integration Int;
        Jacobian JAC_sur;
    }

    Integral {
        DtDof[
            <<functionKey>>MassFunctionDta<<a>>b<<b>>[
                <<temperatureArgument1>>,
                <<temperatureArgument2>>
            ] * Dof{<<quantityName>>~{i + <<a>> - 1}},
            {<<quantityName>>~{i + <<b>> - 1}}
        ];
        In DOM_insulationSurface;
        Integration Int;
        Jacobian JAC_sur;
    }
        {% endfor %}
    {% endfor %}
EndFor
{% elif type == "resistiveHeating" %}
For i In {0:INPUT_NumOfTSAElements-1}
    {% for k in range(1,3) %} // row of the 1D FE matrix
    Integral {
        [
            - electromagneticRHSFunctionk<<k>>[
                <<temperatureArgument1>>,
                <<temperatureArgument2>>
            ] * SquNorm[
                ({LOCALQUANT_hThinShell~{i + 1}} - {LOCALQUANT_hThinShell~{i}})/th_ins_k
            ],
            {LOCALQUANT_TThinShell~{i + <<k>> - 1}}
        ];
        In DOM_insulationSurface;
        Integration Int;
        Jacobian JAC_sur;
    } 

        {% for a in range(1,3) %}
            {% for b in range(1,3) %}
    Integral {
        [
            -electromagneticTripleFunctionk<<k>>a<<a>>b<<b>>[
                <<temperatureArgument1>>,
                <<temperatureArgument2>>
            ] * {d LOCALQUANT_hThinShell~{i + <<a>> - 1}} * {d LOCALQUANT_hThinShell~{i + <<b>> - 1}},
            {LOCALQUANT_TThinShell~{i + <<k>> - 1}}
        ];
        In DOM_insulationSurface;
        Integration Int;
        Jacobian JAC_sur;
    }
            {% endfor %}
        {% endfor %}
    {% endfor %}
EndFor
{% else %}
<<0/0>>
// ERROR: Wrong type for FORMULATION_TSAIntegrals!
{% endif %}
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro RESOLUTION_tolerances(systemNames, systemTolerances, postOperationTolerances, type) %}
{% for tolerance in systemTolerances %}
    {% if loop.first %}
System{
    {% endif %}
    {% for systemName in systemNames %}
    {
        <<systemName>>,
        <<tolerance["relative"]>>,
        <<tolerance["absolute"]>>,
        {% if type == "nonlinearSolver" %}
        Solution <<tolerance["normType"]>>
        {% elif type == "timeLoop" %}
        <<tolerance["normType"]>>
        {% else %}
        <<0/0>>
        // ERROR: wrong type for RESOLUTION_tolerances!
        {% endif %}
    }
    {% endfor %}
    {% if loop.last %}
}
    {% endif %}
{% endfor %}
{% for tolerance in postOperationTolerances %}
    {% if loop.first %}
PostOperation{
    {% endif %}
    {
        POSTOP_CONV_<<tolerance["quantity"]>>,
        <<tolerance["relative"]>>,
        <<tolerance["absolute"]>>,
        <<tolerance["normType"]>>
    }
    {% if loop.last %}
}
    {% endif %}
{% endfor %}
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro RESOLUTION_systemsOfEquationsSolver(systemNames, type, solveAfterThisTimes=[0, 0]) %}
{#
solveAfterThisTimes and systemNames are lists of equal lengths, and each entry
corresponds to the other. This is used because sometimes, in coupled problems, the
thermal system is started being solved right before exciting things (like local defects)
begin in order to speed up the program.
#}
{% if type == "nonlinear" %}
// Nonlinear solver starts +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
IterativeLoopN[
    INPUT_NLSMaxNumOfIter,
    INPUT_NLSRelaxFactor,
    <<RESOLUTION_tolerances(
        systemNames,
        dm.magnet.solve.nls.systemTolerances,
        dm.magnet.solve.nls.postOperationTolerances,
        type="nonlinearSolver")|indent(4)>>
]{
    {% for systemName, solveAfterThisTime in zip(systemNames, solveAfterThisTimes) %}
        {% if solveAfterThisTime == 0 %}
    GenerateJac <<systemName>>;
    // Print[<<systemName>>];
    SolveJac <<systemName>>;

    GetNormSolution[<<systemName>>, $normOfTheSolutionVector];
    Print[{$normOfTheSolutionVector}, Format "Critical: Solution vector norm: %.3g"];

    PostOperation[POSTOP_CONV_temperature];
    Print[{ $test }, Format "Critical: Temperature: %.3g"];

        {% else %}
    Test[$Time >= <<solveAfterThisTime>>]{
        GenerateJac <<systemName>>;
        SolveJac <<systemName>>;
        PostOperation[POSTOP_CONV_temperature];
        Print[{$test}];
    }
        {% endif %}
    {% endfor %}

    PostOperation[POSTOP_Ic];
    Print[{ #1 }, Format "Critical: Lowest Ic: %.3g"];

    PostOperation[POSTOP_I];
    Print[{ $I }, Format "Critical: I: %.3g"];

    Test[$I > #1]{
        Print[{10}, Format "Critical: Quench started! %.1g"];
    }
}
// Nonlinear solver ends +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
{% elif type == "linear" %}
// Linear solver starts ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    {% for systemName in systemNames %}
Generate <<systemName>>;
Evaluate[$initializationDone = 1];
Solve <<systemName>>;
    {% endfor %}
// Linear solver ends ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
{% else %}
<<0/0>>
// ERROR: wrong for RESOLUTION_systemsOfEquationsSolver!
{% endif %}
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro RESOLUTION_saveSpecificTimes(postOperationName, timesToBeSaved) %}
// Saving quantities at specific times starts ++++++++++++++++++++++++++++++++++++++++++
{% for time in timesToBeSaved %}
    {% set timeMax = time+1e-6 %}
    {% set timeMin = time-1e-6 %}
Test[$Time < <<timeMax>> && $Time > <<timeMin>>]{
    PostOperation[<<postOperationName>>];
}
{% endfor %}
// Saving quantities at specific times ends ++++++++++++++++++++++++++++++++++++++++++++
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro RESOLUTION_InitializeSolutions(systemNames) %}
{% for systemName in systemNames %}
InitSolution[<<systemName>>];
SaveSolution[<<systemName>>];
{% endfor %}
SetExtrapolationOrder[INPUT_extrapolationOrder];
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro RESOLUTION_SaveSolutions(systemNames, solveAfterThisTimes) %}
{% if dm.magnet.solve.save %}
    {% for quantity in dm.magnet.solve.save %}
        {% if quantity.timesToBeSaved %}
<<RESOLUTION_saveSpecificTimes(
    postOperationName = quantity.getdpPostOperationName,
    timesToBeSaved=quantity.timesToBeSaved)>>
        {% endif %}
    {% endfor %}
{% endif %}
{% for systemName, solveAfterThisTime in zip(systemNames, solveAfterThisTimes) %}
    {% if solveAfterThisTime == 0 %}
SaveSolution[<<systemName>>];
    {% else %}
        {% if 'solutionVector' in dm.magnet.solve.t.adaptive.tolerances|map(attribute="quantity") %}
SaveSolution[<<systemName>>];
        {% else %}
Test[$Time < <<solveAfterThisTime>>]{
    CopySolution[<<systemName>>, 'DummySolution'];
    CreateSolution[<<systemName>>];
    CopySolution['DummySolution', <<systemName>>];
    SaveSolution[<<systemName>>];
}
        {% endif %}
    {% endif %}
{% endfor %}
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro RESOLUTION_PostOperations() %}
{% if dm.magnet.solve.save is not none %}
    {% for quantity in dm.magnet.solve.save %}
        {% if not quantity.timesToBeSaved %}
PostOperation[<<quantity.getdpPostOperationName>>];
        {% endif %}
    {% endfor %}
{% endif %}
{% if dm.magnet.postproc.timeSeriesPlots is not none %}
    {% for timeSeriesPlot in dm.magnet.postproc.timeSeriesPlots %}
PostOperation[POSTOP_timeSeriesPlot_<<timeSeriesPlot.quantity>>];
    {% endfor %}
{% endif %}
{% if dm.magnet.postproc.magneticFieldOnCutPlane is not none %}
PostOperation[POSTOP_magneticFieldOnCutPlaneVector];
PostOperation[POSTOP_magneticFieldOnCutPlaneMagnitude];
{% endif %}
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro RESOLUTION_SolveTransientProblemFixedStepping(systemNames, solveAfterThisTimes=[0,0]) %}
<<RESOLUTION_InitializeSolutions(systemNames)>>
{% set intervals = dm.magnet.solve.t.fixed %}
{% for interval in intervals %}
TimeLoopTheta[<<interval.startTime>>, <<interval.endTime>>, <<interval.step>>, 1]{
    <<RESOLUTION_systemsOfEquationsSolver(
        systemNames = systemNames,
        type=dm.magnet.solve.systemsOfEquationsType,
        solveAfterThisTimes = solveAfterThisTimes)|indent(4)>>
    {% if dm.magnet.solve.systemsOfEquationsType == "linear" %}
    GetNormSolution[<<systemNames[0]>>, $normOfTheSolutionVector];
    Print[{$normOfTheSolutionVector}];
    {% endif %}
    <<RESOLUTION_SaveSolutions(systemNames, solveAfterThisTimes)|indent(4)>>
}
{% endfor %}
<<RESOLUTION_PostOperations()>>
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro RESOLUTION_SolveTransientProblemAdaptiveStepping(systemNames, solveAfterThisTimes=[0,0]) %}
<<RESOLUTION_InitializeSolutions(systemNames)>>

TimeLoopAdaptive[
    INPUT_tStart,
    INPUT_tEnd,
    INPUT_tAdaptiveInitStep,
    INPUT_tAdaptiveMinStep,
    INPUT_tAdaptiveMaxStep,
    "<<dm.magnet.solve.t.adaptive.integrationMethod>>",
    List[INPUT_tAdaptiveBreakPoints],
    <<RESOLUTION_tolerances(
        systemNames,
        dm.magnet.solve.t.adaptive.systemTolerances,
        dm.magnet.solve.t.adaptive.postOperationTolerances,
        type="timeLoop")|indent(4)>>
]{
    <<RESOLUTION_systemsOfEquationsSolver(
        systemNames = systemNames,
        type=dm.magnet.solve.systemsOfEquationsType,
        solveAfterThisTimes = solveAfterThisTimes)|indent(4)>>
    {% if dm.magnet.solve.systemsOfEquationsType == "linear" %}
    GetNormSolution[<<systemNames[0]>>, $normOfTheSolutionVector];
    Print[{$normOfTheSolutionVector}];
    {% endif %}
}{
    <<RESOLUTION_SaveSolutions(systemNames, solveAfterThisTimes)|indent(4)>>
}

<<RESOLUTION_PostOperations()>>
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro RESOLUTION_SolveTransientProblem(systemNames, solveAfterThisTimes=[0,0]) %}
{% if dm.magnet.solve.t.timeSteppingType == "adaptive" %}
<<RESOLUTION_SolveTransientProblemAdaptiveStepping(systemNames, solveAfterThisTimes)>>
{% elif dm.magnet.solve.t.timeSteppingType == "fixed" %}
<<RESOLUTION_SolveTransientProblemFixedStepping(systemNames, solveAfterThisTimes)>>
{% endif %}
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{% macro POSTOPERATION_printResults(
    quantity,
    onElementsOf="None",
    onPoint="None",
    onRegion="None",
    onGlobal="None",
    onSection="None",
    depth="None",
    format="Default",
    name="None",
    fileName="None") %}
Print[
    <<quantity>>,
{% if onElementsOf != "None" %}
    OnElementsOf <<onElementsOf>>,
{% elif onPoint != "None" %}
    OnPoint {<<onPoint[0]>>, <<onPoint[1]>>, <<onPoint[2]>>},
{% elif onRegion != "None" %}
    OnRegion <<onRegion>>,
{% elif onGlobal != "None" %}
    OnGlobal,
{% elif onSection != "None" %}
    OnSection{
        {<<onSection[0][0]>>, <<onSection[0][1]>>, <<onSection[0][2]>>}
        {<<onSection[1][0]>>, <<onSection[1][1]>>, <<onSection[1][2]>>}
        {<<onSection[2][0]>>, <<onSection[2][1]>>, <<onSection[2][2]>>}
    },
{% else %}
    {# <<0/0>> #}
    // ERROR: No print region specified!
{% endif %}
{% if depth != "None" %}
    Depth <<depth>>,
{% endif %}
{% if fileName != "None" %}
    {% if format != "Default" %}
    File "<<fileName>>-<<format>>Format.txt",
    {% else %}
    File "<<fileName>>-<<format>>Format.pos",
    {% endif %}
{% else %}
    {% if format != "Default" %}
    File "<<quantity>>-<<format>>Format.txt",
    {% else %}
    File "<<quantity>>-<<format>>Format.pos",
    {% endif %}
{% endif %}
{% if format != "Default" %}
    Format <<format>>,
{% endif %}
{% if dm.magnet.solve.save is not none %}
    {% for quantityDict in dm.magnet.solve.save %}
        {% if quantityDict.getdpQuantityName == quantity %}
            {% if quantityDict.timesToBeSaved %}
    AppendToExistingFile 1,
    LastTimeStepOnly 1,
            {% endif %}
        {% endif %}
    {% endfor %}
{% endif %}
{% if name != "None" %}
    Name "<<name>>"
{% elif fileName != "None" %}
    Name "<<fileName>>"
{% else %}
    Name "<<quantity>>"
{% endif %}
];
{% endmacro %}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
{# ================================================================================== #}
//======================================================================================
// Physical regions: ===================================================================
//======================================================================================
Group{
{% if dm.magnet.geometry.ii.tsa %}
    {% set NofSets = len(rm.insulator.surf.numbers) %}
    {% set HalfNofSets = (len(rm.insulator.surf.numbers)/2)|int %}

    DOM_insulationSurface_0 = Region[{ <<rm.insulator.surf.numbers[-1]>> }];

    {% for i in range(1, NofSets+1+1) %}
    DOM_windingMinus_<<i>> = Region[{ <<rm.powered.vol.numbers[(i-1)%NofSets]>> }];

    DOM_windingPlus_<<i>> = Region[{ <<rm.powered.vol.numbers[(i-1+HalfNofSets)%NofSets]>> }];

    DOM_insulationSurface_<<i>> = Region[{ <<rm.insulator.surf.numbers[(i-1)%NofSets]>> }];
    {% endfor %}

    // Add terminals to winding region logic:
    // <<rm.powered.vol_in.number>>: inner terminal
    // <<rm.powered.vol_out.number>>: outer terminal
    /*{% for i in range(1, HalfNofSets+1) %}
    DOM_windingMinus_<<i>> += Region[{ <<rm.powered.vol_in.number>> }];
    {% endfor %}

    {% for i in range(HalfNofSets+1, NofSets+1) %}
    DOM_windingMinus_<<i>> += Region[{ <<rm.powered.vol_out.number>> }];
    {% endfor %}*/

    DOM_insulationSurface = Region[{ <<rm.insulator.surf.numbers|join(', ')>> }];

    DOM_insulationBoundaryCurvesAir = Region[{ <<rm.insulator.curve.numbers[0]>> }];
    DOM_insulationBoundaryCurvesTerminal = Region[{ <<rm.insulator.curve.numbers[1]>> }];
{% else %}
    DOM_insulations = Region[{ <<rm.insulator.vol.numbers|join(', ')>> }];
{% endif %}


    // create windings region:
    DOM_allWindings = Region[{ <<rm.powered.vol.numbers|join(', ')>> }];

    // create terminals region:
    DOM_terminals = Region[{ <<rm.powered.vol_in.number>>, <<rm.powered.vol_out.number>> }];

    // create powered region:
    DOM_powered = Region[{ DOM_allWindings, DOM_terminals }];

    // support of edge-based magnetic field strength, i.e., all conducting doms:
{% if dm.magnet.geometry.ii.tsa or dm.magnet.solve.ii.resistivity == "perfectlyInsulating" %}
    DOM_allConducting = Region[{ DOM_powered }];
{% else %}
    DOM_allConducting = Region[{ DOM_powered, DOM_insulations }];
{% endif %}
    DOM_air = Region[{ <<rm.air.vol.number>> }];
{% if dm.magnet.solve.ii.resistivity == "perfectlyInsulating" %}
    DOM_airPoints = Region[{ <<rm.air.point.numbers[1]>> }];
{% else %}
    DOM_airPoints = Region[{ <<rm.air.point.numbers|join(', ')>> }];
{% endif %}

{% if dm.magnet.solve.ii.resistivity == "perfectlyInsulating" and
    not dm.magnet.geometry.ii.tsa %}
    DOM_air += Region[{ <<rm.insulator.vol.numbers|join(', ')>> }];
{% endif %}

{% if dm.magnet.geometry.ai.shellTransformation %}
    {% if dm.magnet.geometry.ai.type == "cylinder" %}
    // add shell volume for shell transformation:
    DOM_air += Region[{ <<rm.air_far_field.vol.numbers|join(", ")>> }];
    DOM_airInf = Region[{ <<rm.air_far_field.vol.numbers|join(", ")>> }];
    {% elif dm.magnet.geometry.ai.type == "cuboid" %}
    // add shell volume for shell transformation:
    DOM_air += Region[{ <<rm.air_far_field.vol.numbers|join(", ")>> }];
    DOM_airInfX = Region[{ <<rm.air_far_field.vol.numbers[0]>> }];
    DOM_airInfY = Region[{ <<rm.air_far_field.vol.numbers[1]>> }];
    {% endif %}
{% endif %}


    // boundary surface between the all conducting and non-conducting domains:
{% if dm.magnet.geometry.ii.tsa or dm.magnet.solve.ii.resistivity != "perfectlyInsulating" %}
    DOM_pancakeBoundary = Region[{ <<rm.powered.surf.numbers[0]>> }];
{% else %}
    DOM_pancakeBoundary = Region[{ <<rm.powered.surf.numbers[1]>> }];
{% endif %}

    // support of magnetic scalar potential, i.e., all non-conducting doms:
    DOM_Phi = Region[{ DOM_air }];

    // cut inbetween current leads, used to impose current or voltage:
{% if dm.magnet.solve.ii.resistivity == "perfectlyInsulating" %}
    DOM_terminalCut = Region[{ <<rm.air.cochain.numbers[1]>> }];
    DOM_airHoleCut = Region[{ <<rm.air.cochain.numbers[2:]|join(', ')>> }];
    DOM_airCuts = Region[{ DOM_terminalCut, DOM_airHoleCut }];
{% else %}
    DOM_terminalCut = Region[{ <<rm.air.cochain.numbers[0]>> }];
    DOM_airCuts = Region[{ DOM_terminalCut }];
{% endif %}

    // total computational domain (Omega):
    DOM_total = Region[{ DOM_allConducting, DOM_Phi }];

    // top and bottom surfaces of the terminals for constant temperature BC:
    DOM_bottomTerminalSurface = Region[{ << rm.powered.surf_in.numbers | join(', ') >> }];

    DOM_topTerminalSurface = Region[{ << rm.powered.surf_out.numbers | join(', ') >> }];
}

//======================================================================================
// Physical properties: ================================================================
//======================================================================================
Function{
    // Power supply / current source:
    listOfTimeValues = {<<dm.power_supply.t_control_LUT|join(", ")>>};
    listOfCurrentValues = {<<dm.power_supply.I_control_LUT|join(", ")>>};
    current[] = InterpolationLinear[$1]{ListAlt[listOfTimeValues, listOfCurrentValues]};

    // Pancake3D geometry related functions:

    // We use SetVariable and GetVariable to ensure some variables are only evaluated once
    // and saved in the memory. Input of the functions below is the position vector XYZ[].
{% if dm.magnet.geometry.ii.tsa %}
    {% set windingThickness = dm.magnet.geometry.wi.t + dm.magnet.geometry.ii.t * (dm.magnet.geometry.wi.N - 1) / dm.magnet.geometry.wi.N %}
    {# A scaling factor needs to be used for TSA because winding is slightly thicker in #}
    {# TSA compared to volume insulation. #}
    {% set scalingFactor = dm.magnet.geometry.wi.t / windingThickness %}
    {% set gapThickness = 0 %}
{% else %}
    {% set windingThickness = dm.magnet.geometry.wi.t %}
    {% set scalingFactor = 1 %}
    {% set gapThickness = dm.magnet.geometry.ii.t %}
{% endif %}

    normalVectorOfWinding[] = GetVariable[ElementNum[], QuadraturePointIndex[]]{$coilNormalVector} ? 
        GetVariable[ElementNum[], QuadraturePointIndex[]]{$coilNormalVector}
        :
        SetVariable[
            Pancake3DGetNormal[XYZ[]]{
                <<dm.magnet.geometry.wi.r_i>>,
                <<windingThickness>>,
                <<gapThickness>>,
                <<dm.magnet.geometry.wi.theta_i>>,
                <<dm.magnet.mesh.wi.ane[0]>>,
                <<dm.magnet.geometry.N>>,
                <<dm.magnet.geometry.wi.h>>,
                <<dm.magnet.geometry.gap>>
            },
            ElementNum[],
            QuadraturePointIndex[]
        ]{$coilNormalVector};

    arcLengthOfWinding[] = GetVariable[ElementNum[], QuadraturePointIndex[]]{$arcLengthOfWinding} ?
        GetVariable[ElementNum[], QuadraturePointIndex[]]{$arcLengthOfWinding}
        :
        SetVariable[
            Pancake3DGetContinuousArcLength[XYZ[]]{
                <<dm.magnet.geometry.wi.r_i>>,
                <<windingThickness>>,
                <<gapThickness>>,
                <<dm.magnet.geometry.wi.theta_i>>,
                <<dm.magnet.mesh.wi.ane[0]>>,
                <<dm.magnet.geometry.N>>,
                <<dm.magnet.geometry.wi.h>>,
                <<dm.magnet.geometry.gap>>
            },
            ElementNum[],
            QuadraturePointIndex[]
        ]{$arcLengthOfWinding};

    turnNumberOfWinding[] = GetVariable[ElementNum[], QuadraturePointIndex[]]{$turnNumberOfWinding} ?
        GetVariable[ElementNum[], QuadraturePointIndex[]]{$turnNumberOfWinding}
        :
        SetVariable[
            Pancake3DGetContinuousTurnNumber[XYZ[]]{
                <<dm.magnet.geometry.wi.r_i>>,
                <<windingThickness>>,
                <<gapThickness>>,
                <<dm.magnet.geometry.wi.theta_i>>,
                <<dm.magnet.mesh.wi.ane[0]>>,
                <<dm.magnet.geometry.N>>,
                <<dm.magnet.geometry.wi.h>>,
                <<dm.magnet.geometry.gap>>
            },
            ElementNum[],
            QuadraturePointIndex[]
        ]{$turnNumberOfWinding};
    
    // Transformation tensor from winding coordinate system to XYZ coordinate system:
    // see: https://www.continuummechanics.org/coordxforms.html
    // X, Y, Z are the global coordinate system, x, y, z are the winding coordinate system.
    // x: normal to the winding, positive direction is from the inner radius to the outer radius
    // y: parallel to the windng, positive direction is in counterclockwise direction (i.e., right-hand rule applies for the winding coordinate system, assuming z and Z are the same)
    // z: the same with Z

    // n1: Unit vector of X in the winding coordinate system
    // n2: Unit vector of Y in the winding coordinate system
    // n3: Unit vector of Z in the winding coordinate system
    n1[] = Vector[CompX[normalVectorOfWinding[]], -CompY[normalVectorOfWinding[]], 0];
    n2[] = Vector[CompY[normalVectorOfWinding[]], CompX[normalVectorOfWinding[]], 0];
    n3[] = Vector[0, 0, 1];
    TransformationTensor[] = TensorV[
        n1[],
        n2[],
        n3[]
    ];

    // to be templated below
    oneDGaussianOrder = 2;
    // to be templated above

    // Initial conditions:
    INPUT_initialTemperature = <<dm.magnet.solve.ic.T>>; // initial temperature, [K]

    // Time stepping parameters:
    INPUT_tStart = <<dm.magnet.solve.t.start>>; // start time, [s]
    INPUT_tEnd = <<dm.magnet.solve.t.end>>; // end time, [s]
    INPUT_extrapolationOrder = <<dm.magnet.solve.t.extrapolationOrder>>; // order of extrapolation for the time stepping scheme
{% if dm.magnet.solve.t.timeSteppingType == "adaptive" %}
    // Adaptive time stepping parameters:
    INPUT_tAdaptiveMinStep = <<dm.magnet.solve.t.adaptive.minimumStep>>; // minimum time step, [s]
    INPUT_tAdaptiveMaxStep = <<dm.magnet.solve.t.adaptive.maximumStep>>; // maximum time step, [s]
    INPUT_tAdaptiveInitStep = <<dm.magnet.solve.t.adaptive.initialStep>>; // initial time step, [s]
    INPUT_tAdaptiveBreakPoints ={ << list(set(dm.magnet.solve.t.adaptive.breakPoints+dm.power_supply.t_control_LUT))|sort|join(', ') >> }; // force solution at these time points, [s]
{% endif %}

{% if dm.magnet.solve.systemsOfEquationsType == "nonlinear" %}
    // Nonlinear solver parameters:
    INPUT_NLSMaxNumOfIter = <<dm.magnet.solve.nls.maxIter>>; // maximum number of iterations for the nonlinear solver
    INPUT_NLSRelaxFactor = <<dm.magnet.solve.nls.relaxationFactor>>; // relaxation factor for the nonlinear solver
{% endif %}

    //==================================================================================
    // Material parameters: ============================================================
    //==================================================================================
{% if dm.magnet.solve.type in ["electromagnetic", "weaklyCoupled", "stronglyCoupled"] %}
    // Air permeability starts =========================================================
    // Linear:
    INPUT_airMagneticPermeability = <<dm.magnet.solve.ai.permeability>>;
    mu[] = INPUT_airMagneticPermeability;
    // Air permeability ends ===========================================================
{% endif %}

{%
if (
        (
            not (
                dm.magnet.solve.wi.resistivity and
                dm.magnet.solve.wi.thermalConductivity and
                dm.magnet.solve.wi.specificHeatCapacity
            ) and dm.magnet.solve.type in ["weaklyCoupled", "stronglyCoupled"]
        )
        or (not(dm.magnet.solve.wi.resistivity) and dm.magnet.solve.type in ["electromagnetic"])
        or (not(
            dm.magnet.solve.wi.thermalConductivity and
            dm.magnet.solve.wi.specificHeatCapacity
        ) and dm.magnet.solve.type in ["thermal"])
    )
%}
    // Winding material combination parameters start ===================================
    {% for material in dm.magnet.solve.wi.normalConductors %}
    INPUT_relativeThickness<<material.name>> = <<material.relativeThickness>>;
    {% endfor %}

    INPUT_relativeThicknessOfSuperConductor = <<dm.magnet.solve.wi.relativeThicknessOfSuperConductor>>;
    INPUT_relativeThicknessOfNormalConductor = <<dm.magnet.solve.wi.relativeThicknessOfNormalConductor>>;
    INPUT_relativeWidthOfPlating = <<dm.magnet.solve.wi.plating.relativeWidth>>;
    // Factor 1.0/<<scalingFactor>> is used equate the scaling applied to Jcritical in the parallel direction 
    INPUT_jCriticalScalingNormalToWinding = 1.0/<<scalingFactor>> * <<dm.magnet.solve.wi.superConductor.jCriticalScalingNormalToWinding>>;
    // Winding material combination parameters end =====================================
{% endif %}

{% if dm.magnet.geometry.ii.tsa %}
    // TSA parameters start ============================================================
    INPUT_insulationThickness = <<dm.magnet.geometry.ii.t>>; // thickness of the insulation, [m]
    INPUT_NumOfTSAElements = <<dm.magnet.solve.ii.numberOfThinShellElements>>;
    th_ins_k = INPUT_insulationThickness / (INPUT_NumOfTSAElements == 0 ? 1 : INPUT_NumOfTSAElements);
    // TSA parameters end ==============================================================
{% endif %}

{% if dm.magnet.solve.type in ["electromagnetic", "weaklyCoupled", "stronglyCoupled"] %}
    // Winding resistivity starts ======================================================
    {% if dm.magnet.solve.wi.resistivity %}
    // Linear:
    INPUT_coilResistivity = <<dm.magnet.solve.wi.resistivity>>; // resistivity of the coil, [Ohm*m]
    rho[DOM_allWindings] = INPUT_coilResistivity;
    {% else %}
    // Nonlinear:

    // Generally, tapes consist of more than one material. They are modeled as one
    // material (including the superconductor), and their effective homogenized
    // resistivity, thermal conductivity, and specific heat capacity are calculated
    // below.

    // Resistivity calculation starts.
        {% for material in dm.magnet.solve.wi.normalConductors %}
    rho<<material.name>>[] = <<materials[material.resistivityMacroName](RRR=material.rrr, rrrRefT=material.rrrRefT)>>;

        {% endfor %}

    rhoNormalConductorParallelToWinding[] =
            EffectiveResistivity[
                {% for material in dm.magnet.solve.wi.normalConductors %}
                    {% if loop.last %}
                rho<<material.name>>[$1, $2]
                    {% else %}
                rho<<material.name>>[$1, $2],
                    {% endif %}
                {% endfor %}
            ]{
                {% for material in dm.magnet.solve.wi.normalConductors %}
                    {% if loop.last %}
                INPUT_relativeThickness<<material.name>>
                    {% else %}
                INPUT_relativeThickness<<material.name>>,
                    {% endif %}
                {% endfor %}
            };

    rhoNormalConductorNormalToWinding[] =
            RuleOfMixtures[
                {% for material in dm.magnet.solve.wi.normalConductors %}
                    {% if loop.last %}
                rho<<material.name>>[$1, $2]
                    {% else %}
                rho<<material.name>>[$1, $2],
                    {% endif %}
                {% endfor %}
            ]{
                {% for material in dm.magnet.solve.wi.normalConductors %}
                    {% if loop.last %}
                INPUT_relativeThickness<<material.name>>
                    {% else %}
                INPUT_relativeThickness<<material.name>>,
                    {% endif %}
                {% endfor %}
            };
    
    // In normal direction, we consider the plating of the tape, typcially copper as a 
    // parallel connection between the series connection of all layers and the plating.
    rhoPlatingNormalToWinding[] = rho<<dm.magnet.solve.wi.plating.name>>[$1, $2];

        {% if dm.magnet.solve.wi.superConductor %}
    // There is a superconductor in the winding.

    // To make it easier for the linear solver, a lower bound for the resistivity in the
    // superconductor is defined:
    winding_minimumPossibleRho = <<dm.magnet.solve.wi.minimumPossibleResistivity>>;
    // An upper bound for the resistivity in the normal direction is defined too:
    winding_maximumPossibleRho = <<dm.magnet.solve.wi.maximumPossibleResistivity>>;

    // The critical current density is calculated based on the angle between the tape
    // and the magnetic field. Pancake3DGetNormal is a function that returns the normal
    // vector of the tape at a given point. Then, the angle between the tape and the
    // magnetic field is calculated.
    angle[] = Norm[$1] > 0 ?
        Acos[normalVectorOfWinding[] * $1 / Norm[$1]] * 180/Pi
        :
        normalVectorOfWinding[] * Vector[0,0,0];

    {% if dm.magnet.solve.wi.superConductor.lengthValues is not none %}
    listOfLengthValues = {<<dm.magnet.solve.wi.superConductor.lengthValues|join(", ")>>};
    listOfIcValues = {<<dm.magnet.solve.wi.superConductor.IcValues|join(", ")>>};
    IcAtTinit[] = InterpolationLinear[$1]{ListAlt[listOfLengthValues, listOfIcValues]};
    {% else %}
    IcAtTinit[] = <<dm.magnet.solve.wi.superConductor.IcAtTinit>>;
    {% endif %}
    JcriticalMultiplier[] =
            IcAtTinit[$1]/(<<dm.magnet.solve.wi.superConductor.getdpCriticalCurrentDensityFunction>>[
                INPUT_initialTemperature,
                0,
                0
            ] * INPUT_relativeThicknessOfSuperConductor * 1/<<scalingFactor>> * <<dm.magnet.geometry.wi.t>> * <<dm.magnet.geometry.wi.h>>);
    
    JcriticalWithoutLocalDefects[] = 
            JcriticalMultiplier[$4] * <<dm.magnet.solve.wi.superConductor.getdpCriticalCurrentDensityFunction>>[$1, Norm[$2], angle[$2]];

            {% if dm.magnet.solve.localDefects.jCritical.startTime is not none %}
                {% if dm.magnet.solve.localDefects.jCritical.transitionDuration or dm.magnet.solve.localDefects.jCritical.transitionDuration == 0 %}    
    Jcritical[] = (
            turnNumberOfWinding[] >= <<dm.magnet.solve.localDefects.jCritical.startTurn>> &&
            turnNumberOfWinding[] <= <<dm.magnet.solve.localDefects.jCritical.endTurn>> &&
            ($Time >= <<dm.magnet.solve.localDefects.jCritical.startTime>>) &&
            <<dm.magnet.solve.localDefects.jCritical.zTop>> >= Z[] &&
            <<dm.magnet.solve.localDefects.jCritical.zBottom>> <= Z[]
        ) ?
            (
                $Time < <<dm.magnet.solve.localDefects.jCritical.startTime>> + <<dm.magnet.solve.localDefects.jCritical.transitionDuration>>
            ) ?     
                (JcriticalWithoutLocalDefects[$1, $2, $3, $4] - <<dm.magnet.solve.localDefects.jCritical.value>>)/(-<<dm.magnet.solve.localDefects.jCritical.transitionDuration>>) * ($Time - <<dm.magnet.solve.localDefects.jCritical.startTime>> - <<dm.magnet.solve.localDefects.jCritical.transitionDuration>>) + <<dm.magnet.solve.localDefects.jCritical.value>>
                :
                <<dm.magnet.solve.localDefects.jCritical.value>>
            :
            JcriticalWithoutLocalDefects[$1, $2, $3, $4];
                {% else %}
    Jcritical[] = (
        turnNumberOfWinding[] >= <<dm.magnet.solve.localDefects.jCritical.startTurn>> &&
        turnNumberOfWinding[] <= <<dm.magnet.solve.localDefects.jCritical.endTurn>> &&
        $Time >= <<dm.magnet.solve.localDefects.jCritical.startTime>> &&
        <<dm.magnet.solve.localDefects.jCritical.zTop>> >= Z[] &&
        <<dm.magnet.solve.localDefects.jCritical.zBottom>> <= Z[]
        ) ?
            <<dm.magnet.solve.localDefects.jCritical.value>>
            :
            JcriticalWithoutLocalDefects[$1, $2, $3, $4];
                {% endif %}
            {% else %}
    Jcritical[] =  JcriticalWithoutLocalDefects[$1, $2, $3, $4];
            {% endif %}

    // Lamba (current sharing index) is a number between 0 and 1. 1 means all the
    // current flows through the superconductor. 0 means all the current flows through
    // the normal conductor.

    // the electric field at which the current density reaches the critical current density, [V/m]:
    Ecriterion = <<dm.magnet.solve.wi.superConductor.electricFieldCriterion>>;
    n = <<dm.magnet.solve.wi.superConductor.nValue>>; // n-value for the power law

    lambda[] =
            AnisotropicCurrentSharing[
                $3,
                Jcritical[$1, $2, $3, $4],
                rhoNormalConductorParallelToWinding[$1, $2]
            ]{
                Ecriterion,
                n,
                INPUT_relativeThicknessOfSuperConductor * <<dm.magnet.geometry.wi.t>>,
                INPUT_relativeThicknessOfNormalConductor * <<dm.magnet.geometry.wi.t>>,
                1.0, // scaling applied to J, not applicable
                20, // number of current sharing maximum iterations
                1E-5  // absolute tolerance current sharing
            };

    d_of_lambda_wrt_j[] = 
            AnisotropicCurrentSharingDerivative[
                $3,
                Jcritical[$1, $2, $3, $4],
                rhoNormalConductorParallelToWinding[$1, $2],
                lambda[$1, $2, $3, $4]
            ]{
                Ecriterion,
                n,
                INPUT_relativeThicknessOfSuperConductor * <<dm.magnet.geometry.wi.t>>,
                INPUT_relativeThicknessOfNormalConductor * <<dm.magnet.geometry.wi.t>>,
                1.0 // scaling applied to J, not applicable
            };

    jHTS[] = 
            Vector[
                    CompX[$3], 
                    lambda[$1, $2, $3, $4]#1/INPUT_relativeThicknessOfSuperConductor * CompY[$3], // get variable can be used
                    #1/INPUT_relativeThicknessOfSuperConductor * CompZ[$3] // get variable can be used
            ];
    
    // Get variable can be used below
    d_of_jHTS_wrt_j[] =
            Tensor[
                1,
                0,
                0,
                CompX[d_of_lambda_wrt_j[$1, $2, $3, $4]#1]#2/INPUT_relativeThicknessOfSuperConductor * CompY[$3]#5,
                CompY[#1]#3/INPUT_relativeThicknessOfSuperConductor * #5 + lambda[$1, $2, $3, $4]#7/INPUT_relativeThicknessOfSuperConductor,
                CompZ[#1]#4/INPUT_relativeThicknessOfSuperConductor * #5,
                #2/INPUT_relativeThicknessOfSuperConductor * CompZ[$3]#6,
                #3/INPUT_relativeThicknessOfSuperConductor * #6,
                #4/INPUT_relativeThicknessOfSuperConductor * #6 + #7/INPUT_relativeThicknessOfSuperConductor
            ];

    rhoSuperConductorParallelToWinding[] =
            Max[
                rho_PowerLaw[
                    Norm[jHTS[$1, $2, $3, $4]],
                    Jcritical[$1, $2, $3, $4]
                ]{
                    Ecriterion,
                    n
                },
                winding_minimumPossibleRho
            ];


    rhoSuperConductorParallelToWindingDerivative[] = 
            d_of_jHTS_wrt_j[$1, $2, $3, $4]*drhodj_PowerLaw[
                    jHTS[$1, $2, $3, $4],
                    Jcritical[$1, $2, $3, $4]
            ]{
                Ecriterion,
                n
            };

    rhoSuperConductorNormalToWinding[] =
            Min[
                rho_PowerLaw[
                    Norm[jHTS[$1, $2, $3, $4]],
                    INPUT_jCriticalScalingNormalToWinding * Jcritical[$1, $2, $3, $4]
                ]{
                    Ecriterion,
                    n
                },
                winding_maximumPossibleRho
            ];
    
    rhoSuperConductorNormalToWindingDerivative[] =
            d_of_jHTS_wrt_j[$1, $2, $3, $4]*drhodj_PowerLaw[
                jHTS[$1, $2, $3, $4],
                INPUT_jCriticalScalingNormalToWinding * Jcritical[$1, $2, $3, $4]
            ]{
                Ecriterion,
                n
            };
    
    // The effective resistivity for currents parallel to the winding (parallel connection
    // of materials):
    rhoParallelToWinding[DOM_allWindings] =
            EffectiveResistivity[
                rhoNormalConductorParallelToWinding[$1, $2],
                rhoSuperConductorParallelToWinding[$1, $2, $3, $4]
            ]{
                INPUT_relativeThicknessOfNormalConductor,
                INPUT_relativeThicknessOfSuperConductor
            };
    // get variable can be used
    rhoParallelToWindingDerivative[DOM_allWindings] =
            EffectiveResistivityDerivative[
                rhoParallelToWinding[$1, $2, $3, $4],
                rhoSuperConductorParallelToWinding[$1, $2, $3, $4],
                rhoSuperConductorParallelToWindingDerivative[$1, $2, $3, $4]
            ]{
                INPUT_relativeThicknessOfNormalConductor
            };

    // The effective resistivity for currents perpendicular to the winding (series
    // connection of materials):
    rhoNormalToWindingWithoutPlating[DOM_allWindings] = 
            RuleOfMixtures[
                rhoNormalConductorNormalToWinding[$1, $2],
                rhoSuperConductorNormalToWinding[$1, $2, $3, $4]
            ]{
                    INPUT_relativeThicknessOfNormalConductor,
                    INPUT_relativeThicknessOfSuperConductor
            };

    rhoNormalToWinding[DOM_allWindings] =
            EffectiveResistivity[
                rhoNormalToWindingWithoutPlating[$1, $2, $3, $4], 
                rhoPlatingNormalToWinding[$1, $2]
            ]{
                1.0 - INPUT_relativeWidthOfPlating, 
                INPUT_relativeWidthOfPlating
            };
        
    rhoNormalToWindingDerivative[DOM_allWindings] =
            EffectiveResistivityDerivative[
                rhoNormalToWinding[$1, $2, $3, $4],
                rhoNormalToWindingWithoutPlating[$1, $2, $3, $4],
                INPUT_relativeThicknessOfSuperConductor * rhoSuperConductorNormalToWindingDerivative[$1, $2, $3, $4]
            ]{
                INPUT_relativeThicknessOfNormalConductor
            };

    rhoTensorInWindingCoordinates[] =
            TensorDiag[
                <<scalingFactor>> * rhoNormalToWinding[$1, $2, $3, $4],
                1.0/<<scalingFactor>> * rhoParallelToWinding[$1, $2, $3, $4]#1,
                1.0/<<scalingFactor>> * #1
            ];

    // Homogenized resistivity tensor of the winding in XYZ coordinate system:
    // rho($1 = T, $2 = b, $3 = jinWindingCoordinates)
    rho[DOM_allWindings] = 
            TransformationTensor[] * rhoTensorInWindingCoordinates[$1, $2, $3, $4] * Transpose[TransformationTensor[]];

    // Moreover, for nonlinear simulations, we need the derivative of rho with respect
    // to the current density for Newton-Raphson method.

    // ================================================================================
    // FINITE DIFFERENCE DERIVATIVES BELOW ============================================
    // ================================================================================
    // step_j = 1E-1;

    // lambdaForFD[] = AnisotropicCurrentSharing[
    //     $3,
    //     Jcritical[$1, $2, $3, $4],
    //     rhoNormalConductorParallelToWinding[$1, $2]
    // ]{
    //     Ecriterion,
    //     n,
    //     INPUT_relativeThicknessOfSuperConductor * <<dm.magnet.geometry.wi.t>>,
    //     INPUT_relativeThicknessOfNormalConductor * <<dm.magnet.geometry.wi.t>>,
    //     1.0, // scaling applied to J, not applicable
    //     20, // number of current sharing maximum iterations
    //     1E-5  // absolute tolerance current sharing
    // };
    
    // d_of_lambda_wrt_jFD[] = Vector[
    //     (lambdaForFD[$1, $2, $3 + Vector[step_j, 0, 0], $4] - lambdaForFD[$1, $2, $3 - Vector[step_j, 0, 0], $4])/2/step_j,
    //     (lambdaForFD[$1, $2, $3 + Vector[0, step_j, 0], $4] - lambdaForFD[$1, $2, $3 - Vector[0, step_j, 0], $4])/2/step_j,
    //     (lambdaForFD[$1, $2, $3 + Vector[0, 0, step_j], $4] - lambdaForFD[$1, $2, $3 - Vector[0, 0, step_j], $4])/2/step_j
    // ];

    // jHTSForFD[] = Vector[
    //         CompX[$3], 
    //         lambdaForFD[$1, $2, $3, $4]/INPUT_relativeThicknessOfSuperConductor * CompY[$3],
    //         lambdaForFD[$1, $2, $3, $4]/INPUT_relativeThicknessOfSuperConductor * CompZ[$3]
    //     ];
    
    // d_of_jHTS_wrt_jFD[] = TensorV[
    //     (jHTSForFD[$1, $2, $3 + Vector[step_j, 0, 0], $4] - jHTSForFD[$1, $2, $3 - Vector[step_j, 0, 0], $4])/2/step_j,
    //     (jHTSForFD[$1, $2, $3 + Vector[0, step_j, 0], $4] - jHTSForFD[$1, $2, $3 - Vector[0, step_j, 0], $4])/2/step_j,
    //     (jHTSForFD[$1, $2, $3 + Vector[0, 0, step_j], $4] - jHTSForFD[$1, $2, $3 - Vector[0, 0, step_j], $4])/2/step_j
    // ];
    
    // rhoSuperConductorNormalToWindingForFD[] = rho_PowerLaw[
    //         Norm[jHTSForFD[$1, $2, $3, $4]],
    //         INPUT_jCriticalScalingNormalToWinding * Jcritical[$1, $2, $3, $4]
    //     ]{
    //         Ecriterion,
    //         n
    //     };

    // rhoSuperConductorParallelToWindingForFD[] = rho_PowerLaw[
    //         Norm[jHTSForFD[$1, $2, $3, $4]],
    //         Jcritical[$1, $2, $3, $4]
    //     ]{
    //         Ecriterion,
    //         n
    //     };

    // rhoNormalToWindingForFD[DOM_allWindings] = EffectiveResistivity[
    //     RuleOfMixtures[
    //         rhoNormalConductorNormalToWinding[$1, $2],
    //         rhoSuperConductorNormalToWindingForFD[$1, $2, $3, $4]]{
    //             INPUT_relativeThicknessOfNormalConductor,
    //             INPUT_relativeThicknessOfSuperConductor
    //         }, 
    //         rhoPlatingNormalToWinding[$1, $2]
    //     ]{
    //         1.0 - INPUT_relativeWidthOfPlating, 
    //         INPUT_relativeWidthOfPlating
    //     };

    // rhoParallelToWindingForFD[DOM_allWindings] = EffectiveResistivity[
    //         rhoNormalConductorParallelToWinding[$1, $2],
    //         rhoSuperConductorParallelToWindingForFD[$1, $2, $3, $4]
    //     ]{
    //         INPUT_relativeThicknessOfNormalConductor,
    //         INPUT_relativeThicknessOfSuperConductor
    //     };

    // rhoNormalToWindingDerivativeFD[] = SetVariable[
    //         Vector[
    //             <<scalingFactor>> * (rhoNormalToWindingForFD[$1, $2, $3 + Vector[step_j, 0, 0], $4] - rhoNormalToWindingForFD[$1, $2, $3 - Vector[step_j, 0, 0], $4])/(2 * step_j), 
    //             <<scalingFactor>> * (rhoNormalToWindingForFD[$1, $2, $3 + Vector[0, step_j, 0], $4] - rhoNormalToWindingForFD[$1, $2, $3 - Vector[0, step_j, 0], $4])/(2 * step_j),
    //             <<scalingFactor>> * (rhoNormalToWindingForFD[$1, $2, $3 + Vector[0, 0, step_j], $4] - rhoNormalToWindingForFD[$1, $2, $3 - Vector[0, 0, step_j], $4])/(2 * step_j)
    //         ],
    //         ElementNum[],
    //         QuadraturePointIndex[],
    //         $Time,
    //         $NLIteration
    //     ]{
    //         $rhoNormalToWindingDerivativeFD
    //     };

    // rhoParallelToWindingDerivativeFD[] = SetVariable[
    //         Vector[
    //             1/<<scalingFactor>> * (rhoParallelToWindingForFD[$1, $2, $3 + Vector[step_j, 0, 0], $4] - rhoParallelToWindingForFD[$1, $2, $3 - Vector[step_j, 0, 0], $4])/(2 * step_j), 
    //             1/<<scalingFactor>> * (rhoParallelToWindingForFD[$1, $2, $3 + Vector[0, step_j, 0], $4] - rhoParallelToWindingForFD[$1, $2, $3 - Vector[0, step_j, 0], $4])/(2 * step_j),
    //             1/<<scalingFactor>> * (rhoParallelToWindingForFD[$1, $2, $3 + Vector[0, 0, step_j], $4] - rhoParallelToWindingForFD[$1, $2, $3 - Vector[0, 0, step_j], $4])/(2 * step_j)
    //         ],
    //         ElementNum[],
    //         QuadraturePointIndex[],
    //         $Time,
    //         $NLIteration
    //     ]{
    //         $rhoParallelToWindingDerivativeFD
    //     };

    // d_of_rho_wrt_jWindingCoords_windingCoordinates_TIMES_jWindingCoordsFD[] = Tensor[
    //     // ------------- first row ----------------
    //     CompX[rhoNormalToWindingDerivativeFD[$1, $2, $3, $4]] * CompX[$3], 
    //     CompY[GetVariable[ElementNum[], QuadraturePointIndex[], $Time, $NLIteration]{$rhoNormalToWindingDerivativeFD}] * CompX[$3], 
    //     CompZ[GetVariable[ElementNum[], QuadraturePointIndex[], $Time, $NLIteration]{$rhoNormalToWindingDerivativeFD}] * CompX[$3], 
    //     // ------------- second row ----------------
    //     CompX[rhoParallelToWindingDerivativeFD[$1, $2, $3, $4]] * CompY[$3], 
    //     CompY[GetVariable[ElementNum[], QuadraturePointIndex[], $Time, $NLIteration]{$rhoParallelToWindingDerivativeFD}] * CompY[$3],
    //     CompZ[GetVariable[ElementNum[], QuadraturePointIndex[], $Time, $NLIteration]{$rhoParallelToWindingDerivativeFD}] * CompY[$3], 
    //     // ------------- third row ----------------
    //     CompX[GetVariable[ElementNum[], QuadraturePointIndex[], $Time, $NLIteration]{$rhoParallelToWindingDerivativeFD}] * CompZ[$3], 
    //     CompY[GetVariable[ElementNum[], QuadraturePointIndex[], $Time, $NLIteration]{$rhoParallelToWindingDerivativeFD}] * CompZ[$3],
    //     CompZ[GetVariable[ElementNum[], QuadraturePointIndex[], $Time, $NLIteration]{$rhoParallelToWindingDerivativeFD}] * CompZ[$3]
    // ];
    // ================================================================================
    // FINITE DIFFERENCE DERIVATIVES ABOVE ============================================
    // ================================================================================

    // Please note that the expression below is not only the derivative, it's entries
    // are multiplied by the current density.

    d_of_rho_wrt_jWindingCoords_windingCoordinates_TIMES_jWindingCoords[] = Pancake3DDerivativeTensorWRTjINWindingCoordsTimesJ[
        rhoNormalToWindingDerivative[$1, $2, $3, $4],
        rhoParallelToWindingDerivative[$1, $2, $3, $4],
        rhoSuperConductorParallelToWinding[$1, $2, $3, $4],
        rhoSuperConductorNormalToWinding[$1, $2, $3, $4],
        $3
    ]{
        winding_minimumPossibleRho,
        winding_maximumPossibleRho
    };
    d_of_rho_wrt_j_TIMES_j[DOM_allWindings] = TransformationTensor[] * d_of_rho_wrt_jWindingCoords_windingCoordinates_TIMES_jWindingCoords[$1, $2, $3, $4] * Transpose[TransformationTensor[]];

        {% else %}
    // There is no superconductor in the winding.

    rhoTensorInWindingCoordinates[] = TensorDiag[
        rhoNormalConductorNormalToWinding[$1, $2],
        rhoNormalConductorParallelToWinding[$1, $2],
        rhoNormalConductorParallelToWinding[$1, $2]
    ];

    // Homogenized resistivity tensor of the winding in XYZ coordinate system:
    // rho($1 = T, $2 = b, $3 = jinWindingCoordinates)
    rho[DOM_allWindings] = TransformationTensor[] * rhoTensorInWindingCoordinates[$1, $2, $3] * Transpose[TransformationTensor[]];

        {% endif %}
    {% endif %}
    // Winding resistivity ends ========================================================

    // Terminals resistivity starts ====================================================
    {% if dm.magnet.solve.ti.resistivity %}
    // Linear:
    INPUT_terminalResistivity = <<dm.magnet.solve.ti.resistivity>>; // resistivity of the terminals, [Ohm*m]
    rho[DOM_terminals] = INPUT_terminalResistivity;
    {% else %}
    // Nonlinear:
    rho[DOM_terminals] = <<materials[dm.magnet.solve.ti.material.resistivityMacroName](RRR=dm.magnet.solve.ti.material.rrr, rrrRefT=dm.magnet.solve.ti.material.rrrRefT)>>;
    
    {% endif %}
    // Terminals resistivity ends ======================================================

    // Insulation resistivity starts ===================================================
    {% if dm.magnet.solve.ii.resistivity and dm.magnet.solve.ii.resistivity != "perfectlyInsulating" %}
    // Linear:
    INPUT_insulationResistivity = <<dm.magnet.solve.ii.resistivity>>; // resistivity of the insulation, [Ohm*m]

        {% if dm.magnet.geometry.ii.tsa %}
    // Thin-shell insulation:
            {% for a in range(1,3) %}
                {% for b in range(1,3) %}
    electromagneticMassFunctionNoDta<<a>>b<<b>>[] = TSA_constantMaterial_constantThickness_mass[]{
            th_ins_k, INPUT_insulationResistivity, <<a>>, <<b>>
        };
    
    electromagneticStiffnessFunctiona<<a>>b<<b>>[] = TSA_constantMaterial_constantThickness_stiffness[]{
            th_ins_k, INPUT_insulationResistivity, <<a>>, <<b>>
        };

    electromagneticMassFunctionDta<<a>>b<<b>>[] = TSA_constantMaterial_constantThickness_mass[]{
            th_ins_k, INPUT_airMagneticPermeability, <<a>>, <<b>>
        };

                {% endfor %}
        {% endfor %}
        
            {% for k in range(1,3) %}
    electromagneticRHSFunctionk<<k>>[] = TSA_constantMaterial_constantThickness_rhs[]{
            th_ins_k, INPUT_insulationResistivity
        };

                {% for a in range(1,3) %}
                    {% for b in range(1,3) %}
    electromagneticTripleFunctionk<<k>>a<<a>>b<<b>>[] = TSA_constantMaterial_constantThickness_triple[]{
            th_ins_k, INPUT_insulationResistivity, <<k>>, <<a>>, <<b>>
        };

                    {% endfor %}
                {% endfor %}
            {% endfor %}

        {% else %}
    // Volume insulation:
    rho[DOM_insulations] = INPUT_insulationResistivity;
        {% endif %}
    {% elif not dm.magnet.solve.ii.resistivity %}
    // Nonlinear:
        {% if dm.magnet.geometry.ii.tsa %}
    // Thin-shell insulation:
            {% for a in range(1,3) %}   
                {% for b in range(1,3) %}
    electromagneticMassFunctionNoDta<<a>>b<<b>>[] = <<dm.magnet.solve.ii.material.getdpTSAMassResistivityFunction>>[$1, $2]{
            <<a>>, <<b>>, oneDGaussianOrder, th_ins_k
        };
    
    electromagneticStiffnessFunctiona<<a>>b<<b>>[] = <<dm.magnet.solve.ii.material.getdpTSAStiffnessResistivityFunction>>[$1, $2]{
            <<a>>, <<b>>, oneDGaussianOrder, th_ins_k
        };

    electromagneticMassFunctionDta<<a>>b<<b>>[] = TSA_constantMaterial_constantThickness_mass[]{
            th_ins_k, INPUT_airMagneticPermeability, <<a>>, <<b>>
        };

                {% endfor %}
            {% endfor %}
    
            {% for k in range(1,3) %}
    electromagneticRHSFunctionk<<k>>[] = <<dm.magnet.solve.ii.material.getdpTSARHSFunction>>[$1, $2]{
            <<k>>, oneDGaussianOrder, th_ins_k
        };

                {% for a in range(1,3) %}
                    {% for b in range(1,3) %}
    electromagneticTripleFunctionk<<k>>a<<a>>b<<b>>[] = <<dm.magnet.solve.ii.material.getdpTSATripleFunction>>[$1, $2]{
            <<k>>, <<a>>, <<b>>, oneDGaussianOrder, th_ins_k
        };

                    {% endfor %}
                {% endfor %}
            {% endfor %}
        {% else %}
    // Volume insulation:
    rho[DOM_insulations] = <<materials[dm.magnet.solve.ii.material.resistivityMacroName](RRR=dm.magnet.solve.ii.material.rrr, rrrRefT=dm.magnet.solve.ii.material.rrrRefT)>>;

        {% endif %}
    {% endif %}
    // Insulation resistivity ends =====================================================
{% endif %}

{% if dm.magnet.solve.type in ["thermal", "weaklyCoupled", "stronglyCoupled"] %}
    // Winding thermal conductivity starts =============================================
    {% if dm.magnet.solve.wi.thermalConductivity %}
    // Linear:
    INPUT_windingThermalConductivity = <<dm.magnet.solve.wi.thermalConductivity>>; // thermal conductivity of the winding, [W/*(m*K)]
    kappa[DOM_allWindings] = INPUT_windingThermalConductivity;
    {% else %}
    // Nonlinear:
        {% for material in dm.magnet.solve.wi.normalConductors %}
    kappa<<material.name>>[] = <<materials[material.thermalConductivityMacroName](RRR=material.rrr, rrrRefT=material.rrrRefT)>>;
        {% endfor %}

    // The effective thermal conductivity parallel to the winding (parallel connection
    // of materials):
    kappaParallelToWinding[DOM_allWindings] = RuleOfMixtures[
        {% for material in dm.magnet.solve.wi.normalConductors %}
            {% if loop.last %}
        kappa<<material.name>>[$1, $2]
            {% else %}
        kappa<<material.name>>[$1, $2],
            {% endif %}
        {% endfor %}
    ]{
        {% for material in dm.magnet.solve.wi.normalConductors %}
            {% if loop.last %}
        INPUT_relativeThickness<<material.name>>
            {% else %}
        INPUT_relativeThickness<<material.name>>,
            {% endif %}
        {% endfor %}
    };

    // The effective resistivity for currents perpendicular to the winding (series
    // connection of materials):
    kappaNormalToWinding[DOM_allWindings] = RuleOfMixtures[
        EffectiveResistivity[
            {% for material in dm.magnet.solve.wi.normalConductors %}
                {% if loop.last %}
            kappa<<material.name>>[$1, $2]
                {% else %}
            kappa<<material.name>>[$1, $2],
                {% endif %}
            {% endfor %}
        ]{
            {% for material in dm.magnet.solve.wi.normalConductors %}
                {% if loop.last %}
            INPUT_relativeThickness<<material.name>>
                {% else %}
            INPUT_relativeThickness<<material.name>>,
                {% endif %}
            {% endfor %}
        }, 
        kappa<<dm.magnet.solve.wi.plating.name>>[$1, $2]
    ]{
        1.0 - INPUT_relativeWidthOfPlating, 
        INPUT_relativeWidthOfPlating
    };

    kappaTensorInWindingCoordinates[] = TensorDiag[
        1.0/<<scalingFactor>> * kappaNormalToWinding[$1, $2],
        <<scalingFactor>> * kappaParallelToWinding[$1, $2],
        <<scalingFactor>> * kappaParallelToWinding[$1, $2]
    ];

    // Homogenized thermal conductivity tensor of the winding in XYZ coordinate system:
    // rho($1 = T, $2 = b, $3 = jMagnitude)
    kappa[DOM_allWindings] = TransformationTensor[] * kappaTensorInWindingCoordinates[$1, $2] * Transpose[TransformationTensor[]];

    {% endif %}
    // Winding thermal conductivity ends ===============================================

    // Terminals thermal conductivity starts ===========================================
    {% if dm.magnet.solve.ti.thermalConductivity %}
    // Linear:
    INPUT_terminalThermalConductivity = <<dm.magnet.solve.ti.thermalConductivity>>; // thermal conductivity of the terminal, [W/*(m*K)]
    kappa[DOM_terminals] = INPUT_terminalThermalConductivity;
    kappa[DOM_topTerminalSurface] = INPUT_terminalThermalConductivity;
    kappa[DOM_bottomTerminalSurface] = INPUT_terminalThermalConductivity;
    {% else %}
    // Nonlinear:
    kappa[DOM_terminals] = <<materials[dm.magnet.solve.ti.material.thermalConductivityMacroName](RRR=dm.magnet.solve.ti.material.rrr, rrrRefT=dm.magnet.solve.ti.material.rrrRefT)>>;
    kappa[DOM_topTerminalSurface] = <<materials[dm.magnet.solve.ti.material.thermalConductivityMacroName](RRR=dm.magnet.solve.ti.material.rrr, rrrRefT=dm.magnet.solve.ti.material.rrrRefT)>>;
    kappa[DOM_bottomTerminalSurface] = <<materials[dm.magnet.solve.ti.material.thermalConductivityMacroName](RRR=dm.magnet.solve.ti.material.rrr, rrrRefT=dm.magnet.solve.ti.material.rrrRefT)>>;
    {% endif %}
    // Terminals thermal conductivity ends =============================================

    // Insulation thermal conductivity starts ==========================================
    {% if dm.magnet.solve.ii.thermalConductivity %}
    // Linear:
    INPUT_insulationThermalConductivity = <<dm.magnet.solve.ii.thermalConductivity>>; // thermal conductivity of the insulation, [W/*(m*K)]

        {% if dm.magnet.geometry.ii.tsa %}
    // Thin-shell insulation:
            {% for a in range(1,3) %}
                {% for b in range(1,3) %}
    thermalMassFunctionNoDta<<a>>b<<b>>[] = TSA_constantMaterial_constantThickness_mass[]{
            th_ins_k, INPUT_insulationThermalConductivity, <<a>>, <<b>>
        };

    thermalStiffnessFunctiona<<a>>b<<b>>[] = TSA_constantMaterial_constantThickness_stiffness[]{
            th_ins_k, INPUT_insulationThermalConductivity, <<a>>, <<b>>
        };

                {% endfor %}
            {% endfor %}
        {% else %}
    // Volume insulation:
    kappa[DOM_insulations] = INPUT_insulationThermalConductivity;
        {% endif %}
    {% else %}
    // Nonlinear:
        {% if dm.magnet.geometry.ii.tsa %}
    // Thin-shell insulation:
            {% for a in range(1,3) %}
                {% for b in range(1,3) %}
    thermalMassFunctionNoDta<<a>>b<<b>>[] = <<dm.magnet.solve.ii.material.getdpTSAMassThermalConductivityFunction>>[$1, $2]{
            <<a>>, <<b>>, oneDGaussianOrder, th_ins_k
        };

    thermalStiffnessFunctiona<<a>>b<<b>>[] = <<dm.magnet.solve.ii.material.getdpTSAStiffnessThermalConductivityFunction>>[$1, $2]{
            <<a>>, <<b>>, oneDGaussianOrder, th_ins_k
        };
                {% endfor %}
            {% endfor %}
        {% else %}
    // Volume insulation:
    kappa[DOM_insulations] = <<materials[dm.magnet.solve.ii.material.thermalConductivityMacroName](RRR=dm.magnet.solve.ii.material.rrr, rrrRefT=dm.magnet.solve.ii.material.rrrRefT)>>;
        {% endif %}
    {% endif %}
    // Insulation thermal conductivity ends ============================================

    // Winding specific heat capacity starts ===========================================
    {% if dm.magnet.solve.wi.specificHeatCapacity %}
    // Linear:
    INPUT_coilSpecificHeatCapacity = <<dm.magnet.solve.wi.specificHeatCapacity>>; // specific heat capacity of the coil, [J/(kg*K)]
    Cv[DOM_allWindings] = INPUT_coilSpecificHeatCapacity;
    {% else %}
    // Nonlinear:
        {% for material in dm.magnet.solve.wi.normalConductors %}
    Cv<<material.name>>[] =  <<materials[material.heatCapacityMacroName]()>>;
        {% endfor %}

    Cv[DOM_allWindings] = <<scalingFactor>> * RuleOfMixtures[
        {% for material in dm.magnet.solve.wi.normalConductors %}
            {% if loop.last %}
        Cv<<material.name>>[$1]
            {% else %}
        Cv<<material.name>>[$1],
            {% endif %}
        {% endfor %}
    ]{
        {% for material in dm.magnet.solve.wi.normalConductors %}
            {% if loop.last %}
        INPUT_relativeThickness<<material.name>>
            {% else %}
        INPUT_relativeThickness<<material.name>>,
            {% endif %}
        {% endfor %}
    };
    {% endif %}
    // Winding specific heat capacity ends =============================================

    // Terminals specific heat capacity starts =========================================
    {% if dm.magnet.solve.ti.specificHeatCapacity %}
    // Linear:
    INPUT_terminalSpecificHeatCapacity = <<dm.magnet.solve.ti.specificHeatCapacity>>; // specific heat capacity of the terminal, [J/(kg*K)]
    Cv[DOM_terminals] = INPUT_terminalSpecificHeatCapacity;
    {% else %}
    // Nonlinear:
    Cv[DOM_terminals] =  <<materials[dm.magnet.solve.ti.material.heatCapacityMacroName]()>>;
    {% endif %}
    // Terminals specific heat capacity ends ===========================================
    
    // Insulation specific heat capacity starts ========================================
    {% if dm.magnet.solve.ii.specificHeatCapacity %}
    // Linear:
    INPUT_insulationSpecificHeatCapacity = <<dm.magnet.solve.ii.specificHeatCapacity>>; // specific heat capacity of the terminal, [J/(kg*K)]

        {% if dm.magnet.geometry.ii.tsa %}
    // Thin-shell insulation:
            {% for a in range(1,3) %}
                {% for b in range(1,3) %}
    thermalMassFunctionDta<<a>>b<<b>>[] = TSA_constantMaterial_constantThickness_mass[]{
            th_ins_k, INPUT_insulationSpecificHeatCapacity, <<a>>, <<b>>
        };

                {% endfor %}
            {% endfor %}
        {% else %}
    // Volume insulation:
    Cv[DOM_insulations] = INPUT_insulationSpecificHeatCapacity;
        {% endif %}
    {% else %}
    // Nonlinear:
        {% if dm.magnet.geometry.ii.tsa %}
    // Thin-shell insulation:
            {% for a in range(1,3) %}
                {% for b in range(1,3) %}
    thermalMassFunctionDta<<a>>b<<b>>[] = <<dm.magnet.solve.ii.material.getdpTSAMassHeatCapacityFunction>>[$1, $2]{
            <<a>>, <<b>>, oneDGaussianOrder, th_ins_k
        };

                {% endfor %}
            {% endfor %}
        {% else %}
    // Volume insulation:
    Cv[DOM_insulations] = <<materials[dm.magnet.solve.ii.material.heatCapacityMacroName]()>>;
        {% endif %}
    {% endif %}
    // Insulation specific heat capacity ends ==========================================
{% endif %}
{% if dm.magnet.geometry.ai.shellTransformation %}

    // Shell transformation parameters:
    {% if dm.magnet.geometry.ai.type == "cylinder" %}
    INPUT_shellInnerRadius = <<dm.magnet.geometry.ai.r>>; // inner radius of the shell, [m]
    INPUT_shellOuterRadius = <<dm.magnet.geometry.ai.shellOuterRadius>>; // outer radius of the shell, [m]
    {% elif dm.magnet.geometry.ai.type == "cuboid" %}
        {% set shellInnerDistance = dm.magnet.geometry.ai.a/2 %}
        {% set shellOuterDistance = dm.magnet.geometry.ai.shellSideLength/2 %}
    INPUT_shellInnerDistance = <<shellInnerDistance>>; // inner radius of the shell, [m]
    INPUT_shellOuterDistance = <<shellOuterDistance>>; // outer radius of the shell, [m]
    <<0/0>>
    // ERROR: Shell transformation is not implemented for cuboid type of air yet!
    {% endif %}
{% endif %}
{% if dm.magnet.solve.systemsOfEquationsType == "nonlinear" %}
    {% if dm.magnet.solve.type in ["weaklyCoupled", "stronglyCoupled"] %}
        {% set rhoArguments = "{LOCALQUANT_T}, mu[] * {LOCALQUANT_h}, Transpose[TransformationTensor[]] * {d LOCALQUANT_h}, arcLengthOfWinding[]" %}
        {% set kappaArguments = "{LOCALQUANT_T}, Norm[mu[] * {LOCALQUANT_h}]" %}
        {% set CvArguments = "{LOCALQUANT_T}, Norm[mu[] * {LOCALQUANT_h}]" %}
        {% set JcriticalArguments = rhoArguments %}
    {% elif dm.magnet.solve.type == "electromagnetic" %}
        {% set rhoArguments = "INPUT_initialTemperature, mu[] * {LOCALQUANT_h}, Transpose[TransformationTensor[]] * {d LOCALQUANT_h}, arcLengthOfWinding[]" %}
        {% set kappaArguments = "INPUT_initialTemperature, Norm[mu[] * {LOCALQUANT_h}]" %}
        {% set CvArguments = "INPUT_initialTemperature, Norm[mu[] * {LOCALQUANT_h}]" %}
        {% set JcriticalArguments = rhoArguments %}
    {% elif dm.magnet.solve.type == "thermal" %}
        {% set rhoArguments = "{LOCALQUANT_T}, 0, 0, 0" %}
        {% set kappaArguments = "{LOCALQUANT_T}, 0, 0" %}
        {% set CvArguments = "{LOCALQUANT_T}, 0, 0" %}
        {% set JcriticalArguments = rhoArguments %}
    {% endif %}
{% elif dm.magnet.solve.systemsOfEquationsType == "linear" %}
    {% set rhoArguments = "" %}
    {% set kappaArguments = "" %}
    {% set CvArguments = "" %}
{% endif %}
}

//======================================================================================
// Jacobian and integration: ===========================================================
//======================================================================================
Jacobian{
    {
        Name JAC_vol; // volume Jacobian
        Case
        {
{% if dm.magnet.geometry.ai.shellTransformation %}
    {% if dm.magnet.geometry.ai.type == "cylinder" %}
            {
                Region DOM_airInf;
                Jacobian VolCylShell {INPUT_shellInnerRadius, INPUT_shellOuterRadius};
            }
    {% elif dm.magnet.geometry.ai.type == "cuboid" %}
            {
                Region DOM_airInfX;
                Jacobian VolRectShell {INPUT_shellInnerDistance, INPUT_shellOuterDistance, 1};
            }
            {
                Region DOM_airInfY;
                Jacobian VolRectShell {INPUT_shellInnerDistance, INPUT_shellOuterDistance, 2};
            }
    {% endif %}
{% endif %}
            {
                Region All;
                Jacobian Vol;
            }
        }
    }

    // surface Jacobian for TSA:
    {
        Name JAC_sur; // surface Jacobian
        Case
        {
            {
                Region All;
                Jacobian Sur;
            }
        }
    }
}

Integration{
    {
        Name Int; // Gauss integraion scheme
        Case{
            {
                Type Gauss;
                Case{
                    {
                        GeoElement Triangle;
                        NumberOfPoints 4;
                    }
                    {
                        GeoElement Quadrangle;
                        NumberOfPoints 4;
                    }
                    {
                        GeoElement Tetrahedron;
                        NumberOfPoints 4;
                    }
                    {
                        GeoElement Hexahedron;
                        NumberOfPoints 6;
                    }
                    {
                        GeoElement Prism;
                        NumberOfPoints 9;
                    }
                    {
                        GeoElement Pyramid;
                        NumberOfPoints 8;
                    }
                }
            }
        }
    }
}

//======================================================================================
// Constraints: ========================================================================
//======================================================================================
Constraint{
    {
        // Impose current:
        Name CONSTRAINT_current;
        Case{
            {
                Region DOM_terminalCut;
                Type Assign;
                Value 1;

                {% set t = dm.power_supply.t_control_LUT%}
                {% set I = dm.power_supply.I_control_LUT%}

                TimeFunction current[$Time];
            }
        }
    }
    {% if dm.magnet.solve.ii.resistivity == "perfectlyInsulating" %}
    {
        // Impose current:
        Name CONSTRAINT_voltage;
        Case{
            {
                Region DOM_airHoleCut;
                Type Assign;
                Value 0;
            }
        }
    }
    {% endif %}
    
    {
        Name CONSTRAINT_zeroPhiAtOuterPoint;
        Case{
            {
                Region DOM_airPoints;
                Type Assign;
                Value 0;
            }
        }
    }
    {
        Name CONSTRAINT_initialTemperature;
        Case {
        {% if dm.magnet.solve.ti.cooling == "fixedTemperature" %}
            {
                Region DOM_bottomTerminalSurface;
                Type Assign;
                Value <<dm.magnet.solve.ic.T>>;
            }
            {
                Region DOM_topTerminalSurface;
                Type Assign;
                Value <<dm.magnet.solve.ic.T>>;
            }
        {% endif %}
        {% if dm.magnet.solve.isothermalInAxialDirection %}
            {% if dm.magnet.geometry.ii.tsa %}
            {
                Region Region[{DOM_allWindings, DOM_insulationSurface}];
                Type Link;
                RegionRef Region[{DOM_allWindings, DOM_insulationSurface}];
                Coefficient 1;
                Function Vector[X[], Y[], <<dm.magnet.geometry.wi.h/2>>];
            }
            {% else %}
            {
                Region Region[{DOM_allWindings, DOM_insulations}];
                Type Link;
                RegionRef Region[{DOM_allWindings, DOM_insulations}];
                Coefficient 1;
                Function Vector[X[], Y[], <<dm.magnet.geometry.wi.h/2>>];
            }
            {% endif %}
        {% endif %}
            {
                {% if dm.magnet.geometry.ii.tsa %}
                Region Region[
                            {
                                DOM_powered, 
                                DOM_insulationSurface
                            }
                        ];
                {% else %}
                Region Region[{DOM_powered, DOM_insulations}];
                {% endif %}
                Type Init;
                Value <<dm.magnet.solve.ic.T>>;
            }
        }
    }
}

//======================================================================================
// Function spaces: ====================================================================
//======================================================================================
FunctionSpace{
    {
        Name SPACE_hPhi;
        Type Form1;
        BasisFunction{
            // gradient of nodal basis functions in DOM_Phi and on DOM_pancakeBoundary
            {
                Name BASISFUN_gradspin;
                NameOfCoef phin;
                Function BF_GradNode;
{% if dm.magnet.geometry.ii.tsa %}
{% if dm.magnet.solve.ii.resistivity == "perfectlyInsulating" %}
                Support Region[{DOM_total, DOM_insulationSurface}];
                Entity NodesOf[{DOM_Phi, DOM_insulationSurface}];
{% else %}
                Support DOM_total;
                Entity NodesOf[{DOM_Phi}, Not {DOM_insulationBoundaryCurvesAir, DOM_insulationBoundaryCurvesTerminal}];
{% endif %}
{% else %}
                Support DOM_total;
                Entity NodesOf[DOM_Phi];
{% endif %}
            }
            // edge basis functions in DOM_allConducting, and not on DOM_pancakeBoundary or DOM_insulationSurface
            {
                Name BASISFUN_psie;
                NameOfCoef he;
                Function BF_Edge;
                Support DOM_allConducting;
{% if dm.magnet.geometry.ii.tsa %}
                Entity EdgesOf[All, Not {DOM_pancakeBoundary, DOM_insulationSurface}];
{% else %}
                Entity EdgesOf[All, Not DOM_pancakeBoundary];
{% endif %}
            }
            // edge-based cohomology basis functions on both cuts
            {
                Name BASISFUN_sc;
                NameOfCoef Ii;
                Function BF_GroupOfEdges;
{% if dm.magnet.geometry.ii.tsa %}
                Support Region[{DOM_total, DOM_insulationSurface}];
{% else %}
                Support DOM_total;
{% endif %}
                Entity GroupsOfEdgesOf[DOM_airCuts];
            }
{% if dm.magnet.geometry.ii.tsa and dm.magnet.solve.ii.resistivity != "perfectlyInsulating" %}
            <<FUNCTIONSPACE_TSABasisFunctions(type="electromagnetic")|indent(12)>>
            // TSA contribution on boundary of the thin layer
            {
                Name BASISFUN_gradpsinBnd;
                NameOfCoef phin_bnd;
                Function BF_GradNode;
                Support Region[
                            {
                                DOM_allConducting,
                                DOM_Phi,
                                DOM_insulationSurface
                            }
                        ];
                Entity NodesOf[DOM_insulationBoundaryCurvesAir];
            }
            {
                Name BASISFUN_psieBnd;
                NameOfCoef phie_bnd;
                Function BF_Edge;
                Support Region[
                            {
                                DOM_allConducting,
                                DOM_insulationSurface
                            }
                        ];
                Entity EdgesOf[DOM_insulationBoundaryCurvesTerminal];
            }
        }
        SubSpace{
            <<FUNCTIONSPACE_TSASubSpaces(["BASISFUN_sc", "BASISFUN_gradpsinBnd", "BASISFUN_psieBnd"])|indent(12)>>
        }
{% else %}
        }
{% endif %}
        // global quantities in order to impose/extract currents or voltages
        GlobalQuantity{
            {
                Name GLOBALQUANT_I;
                Type AliasOf;
                NameOfCoef Ii;
            }
            {
                Name GLOBALQUANT_V;
                Type AssociatedWith;
                NameOfCoef Ii;
            }
        }

        // imposing source current or voltage using global quantities
        Constraint
        {
            {
                NameOfCoef GLOBALQUANT_I;
                EntityType GroupsOfEdgesOf;
                NameOfConstraint CONSTRAINT_current;
            }
            {% if dm.magnet.solve.ii.resistivity == "perfectlyInsulating" %}
            {
                NameOfCoef GLOBALQUANT_V;
                EntityType GroupsOfEdgesOf;
                NameOfConstraint CONSTRAINT_voltage;
            }
            {% endif %}
            {
                NameOfCoef phin;
                EntityType NodesOf;
                NameOfConstraint CONSTRAINT_zeroPhiAtOuterPoint;
            }
            {% if dm.magnet.geometry.ii.tsa and dm.magnet.solve.ii.resistivity != "perfectlyInsulating" %}
            {
                NameOfCoef phin_bnd;
                EntityType NodesOf;
                NameOfConstraint CONSTRAINT_zeroPhiAtOuterPoint;
            }
            {% endif %}
        }
    }
    {
        Name SPACE_temperature;
        Type Form0;
        BasisFunction{
            {
                Name BASISFUN_sn;
                NameOfCoef Tn;
                Function BF_Node;
            {% if dm.magnet.solve.ti.cooling == "cryocooler" %}
                Support Region[{DOM_allConducting, DOM_bottomTerminalSurface, DOM_topTerminalSurface}];
            {% else %}
                Support DOM_allConducting;
            {% endif %}
{% if dm.magnet.geometry.ii.tsa %}
                Entity NodesOf[DOM_allConducting, Not DOM_insulationSurface];
{% else %}
                Entity NodesOf[DOM_allConducting];
{% endif %}
            }
{% if dm.magnet.geometry.ii.tsa %}
            <<FUNCTIONSPACE_TSABasisFunctions(type="thermal")|indent(12)>>

            {
                Name BASISFUN_snBndTerminal;
                NameOfCoef Tn_Bnd;
                Function BF_Node;
                Support Region[{DOM_allConducting, DOM_insulationSurface}];
                Entity NodesOf[DOM_insulationBoundaryCurvesTerminal];
            }
{% endif %}
        }
{% if dm.magnet.geometry.ii.tsa %}
        SubSpace {
            <<FUNCTIONSPACE_TSASubSpaces(["BASISFUN_snBndTerminal"])|indent(12)>>
        }
{% endif %}
        Constraint{
            {
                NameOfCoef Tn;
                EntityType NodesOf;
                NameOfConstraint CONSTRAINT_initialTemperature;
            }
{% if dm.magnet.geometry.ii.tsa %}
    {% for i in range(1, NofSets+1) %}
            {
                NameOfCoef BASISFUN_snMinus_coeff_<<i>>;
                EntityType NodesOf;
                NameOfConstraint CONSTRAINT_initialTemperature;
            }
            {
                NameOfCoef BASISFUN_snPlus_coeff_<<i>>;
                EntityType NodesOf;
                NameOfConstraint CONSTRAINT_initialTemperature;
            }
    {% endfor %}
    {
        NameOfCoef Tn_Bnd;
        EntityType NodesOf;
        NameOfConstraint CONSTRAINT_initialTemperature;
    }
{% endif %}
        }
    }
{% if dm.magnet.geometry.ii.tsa %}
    <<FUNCTIONSPACE_TSAFunctionSpaces("electromagnetic")|indent(4)>>
    <<FUNCTIONSPACE_TSAFunctionSpaces("thermal")|indent(4)>>
{% endif %}
}

//======================================================================================
// Formulations: =======================================================================
//======================================================================================
Formulation{
{% if dm.magnet.solve.type == "stronglyCoupled" %}
    {
        Name FORMULATION_<<dm.magnet.solve.type>>;
        Type FemEquation;
        Quantity{
            <<FORMULATION_VolumetricQuantities("electromagnetic")|indent(12)>>
            <<FORMULATION_VolumetricQuantities("thermal")|indent(12)>>
    {% if dm.magnet.geometry.ii.tsa %}
            {% if dm.magnet.solve.ii.resistivity != "perfectlyInsulating" %}
            <<FORMULATION_TSAQuantities("electromagnetic")|indent(12)>>
            {% endif %}
            <<FORMULATION_TSAQuantities("thermal")|indent(12)>>
    {% endif %}
        }

        Equation{
            <<FORMULATION_VolumetricIntegrals("electromagnetic")|indent(12)>>
            <<FORMULATION_VolumetricIntegrals("thermal")|indent(12)>> 
            <<FORMULATION_VolumetricIntegrals("resistiveHeating")|indent(12)>>
    {% if dm.magnet.geometry.ii.tsa %}
        {% if dm.magnet.solve.ii.resistivity != "perfectlyInsulating" %}
            <<FORMULATION_TSAIntegrals("electromagnetic")|indent(12)>>
            <<FORMULATION_TSAIntegrals("resistiveHeating")|indent(12)>>
        {% endif %}
            <<FORMULATION_TSAIntegrals("thermal")|indent(12)>>
    {% endif %}
        }
    }
{% elif dm.magnet.solve.type == "weaklyCoupled" %}
    {
        Name FORMULATION_electromagnetic;
        Type FemEquation;
        Quantity{
            <<FORMULATION_VolumetricQuantities("thermal")|indent(12)>>
            <<FORMULATION_VolumetricQuantities("electromagnetic")|indent(12)>>
    {% if dm.magnet.geometry.ii.tsa %}
            <<FORMULATION_TSAQuantities("thermal")|indent(12)>>
        {% if dm.magnet.solve.ii.resistivity != "perfectlyInsulating" %}
            <<FORMULATION_TSAQuantities("electromagnetic")|indent(12)>>
        {% endif %}
    {% endif %}
        }

        Equation{
            <<FORMULATION_VolumetricIntegrals("electromagnetic")|indent(12)>>
    {% if dm.magnet.geometry.ii.tsa %}
        {% if dm.magnet.solve.ii.resistivity != "perfectlyInsulating" %}
            <<FORMULATION_TSAIntegrals("electromagnetic")|indent(12)>>
        {% endif %} 
    {% endif %}
        }
    }

    {
        Name FORMULATION_thermal;
        Type FemEquation;
        Quantity {
            <<FORMULATION_VolumetricQuantities("thermal")|indent(12)>>
            <<FORMULATION_VolumetricQuantities("electromagnetic")|indent(12)>>
    {% if dm.magnet.geometry.ii.tsa %}
            <<FORMULATION_TSAQuantities("thermal")|indent(12)>>
        {% if dm.magnet.solve.ii.resistivity != "perfectlyInsulating" %}
            <<FORMULATION_TSAQuantities("electromagnetic")|indent(12)>>
        {% endif %}
    {% endif %}
        }
        
        Equation{
            <<FORMULATION_VolumetricIntegrals("thermal")|indent(12)>>
            <<FORMULATION_VolumetricIntegrals("resistiveHeating")|indent(12)>>
    {% if dm.magnet.geometry.ii.tsa %}
            <<FORMULATION_TSAIntegrals("thermal")|indent(12)>>
        {% if dm.magnet.solve.ii.resistivity != "perfectlyInsulating" %}
            <<FORMULATION_TSAIntegrals("resistiveHeating")|indent(12)>>
        {% endif %}
    {% endif %}
        }
    }

{% elif dm.magnet.solve.type == "electromagnetic" %}
    {
        Name FORMULATION_<<dm.magnet.solve.type>>;
        Type FemEquation;
        Quantity{
            <<FORMULATION_VolumetricQuantities("electromagnetic")|indent(12)>>
    {% if dm.magnet.geometry.ii.tsa %}
        {% if dm.magnet.solve.ii.resistivity != "perfectlyInsulating" %}
            <<FORMULATION_TSAQuantities("electromagnetic")|indent(12)>>
        {% endif %}
    {% endif %}
        }

        Equation{
            <<FORMULATION_VolumetricIntegrals("electromagnetic")|indent(12)>>
    {% if dm.magnet.geometry.ii.tsa %}
        {% if dm.magnet.solve.ii.resistivity != "perfectlyInsulating" %}
            <<FORMULATION_TSAIntegrals("electromagnetic")|indent(12)>>
        {% endif %}
    {% endif %}
        }
    }
{% elif dm.magnet.solve.type == "thermal" %}
    {
        Name FORMULATION_<<dm.magnet.solve.type>>;
        Type FemEquation;
        Quantity {
            <<FORMULATION_VolumetricQuantities("thermal")|indent(12)>>
    {% if dm.magnet.geometry.ii.tsa %}
            <<FORMULATION_TSAQuantities("thermal")|indent(12)>>
    {% endif %}
        }
        
        Equation{
            <<FORMULATION_VolumetricIntegrals("thermal")|indent(12)>>
    {% if dm.magnet.geometry.ii.tsa %}
            <<FORMULATION_TSAIntegrals("thermal")|indent(12)>>
    {% endif %}
        }
    }
{% endif %}
}

//======================================================================================
// Resolution: =========================================================================
//======================================================================================
Resolution{
    {
        Name RESOLUTION_<<dm.magnet.solve.type>>;
        System{
{% if dm.magnet.solve.type == "weaklyCoupled" %}
            {
                Name SYSTEM_thermal;
                NameOfFormulation FORMULATION_thermal;
            }
            {
                Name SYSTEM_electromagnetic;
                NameOfFormulation FORMULATION_electromagnetic;
            }
{% else%}
            {
                Name SYSTEM_<<dm.magnet.solve.type>>;
                NameOfFormulation FORMULATION_<<dm.magnet.solve.type>>;
            }
{% endif %}
        }

        Operation{
            Evaluate[$initializationDone = 0];
{% if dm.magnet.solve.type == "weaklyCoupled" %}
    {% set systemNames = ["SYSTEM_electromagnetic", "SYSTEM_thermal"] %}
    {% set solveAfterThisTimes = [0, 0]%}
{% else %}
    {% set systemNames = ["SYSTEM_"+dm.magnet.solve.type] %}
    {% set solveAfterThisTimes = [0]%}
{% endif %}
            <<RESOLUTION_SolveTransientProblem(
                systemNames = systemNames,
                solveAfterThisTimes = solveAfterThisTimes)|indent(12)>>
        }
    }
}

//======================================================================================
// Post-processing: ====================================================================
//======================================================================================
PostProcessing{
    {
        Name POSTPRO_<<dm.magnet.solve.type>>;
{% if dm.magnet.solve.type == "weaklyCoupled" %}
        NameOfFormulation FORMULATION_electromagnetic;
        NameOfSystem SYSTEM_electromagnetic;
{% else %}
        NameOfFormulation FORMULATION_<<dm.magnet.solve.type>>;
        NameOfSystem SYSTEM_<<dm.magnet.solve.type>>;
{% endif %}
        Quantity{
{% if dm.magnet.solve.type == "electromagnetic" or dm.magnet.solve.type in ["weaklyCoupled", "stronglyCoupled"] %}
            {
                Name RESULT_magneticField; // magnetic flux density (magnetic field)
                Value{
                    Local{
                        [mu[] * {LOCALQUANT_h}];
                        In Region[{ DOM_total }];
                        Jacobian JAC_vol;
                    }
                }
            }

            {
                Name RESULT_magnitudeOfMagneticField; // magnetic flux density magnitude
                Value{
                    Local{
                        [Norm[mu[] * {LOCALQUANT_h}]];
                        In Region[{ DOM_total }];
                        Jacobian JAC_vol;
                    }
                }
            }

            {
                Name RESULT_currentDensity; // current density
                Value{
                    Local{
                        [{d LOCALQUANT_h}];
                        In Region[{ DOM_allConducting }];
                        Jacobian JAC_vol;
                    }
                }
            }

            {
                Name RESULT_magnitudeOfCurrentDensity; // current density magnitude
                Value{
                    Local{
                        [Norm[{d LOCALQUANT_h}]];
                        In Region[{ DOM_allConducting }];
                        Jacobian JAC_vol;
                    }
                }
            }

            {
                Name RESULT_resistivity; // current density magnitude
                Value{
                    Local{
                        [rho[<<rhoArguments>>]];
                        In Region[{ DOM_allConducting }];
                        Jacobian JAC_vol;
                    }
                }
            }

    {% if dm.magnet.solve.wi.resistivity is none %}
            {
                Name RESULT_derivativeOfRhoWithRespectToJ; // current density magnitude
                Value{
                    Local{
                        // [d_of_lambda_wrt_jFD[<<rhoArguments>>]];
                        // [d_of_lambda_wrt_j[<<rhoArguments>>]];

                        // [rhoParallelToWindingDerivativeFD[<<rhoArguments>>]];
                        // [rhoParallelToWindingDerivative[<<rhoArguments>>]];

                        // [rhoNormalToWindingDerivativeFD[<<rhoArguments>>]];
                        [rhoNormalToWindingDerivative[<<rhoArguments>>]];

                        // [d_of_jHTS_wrt_jFD[<<rhoArguments>>]];
                        // [d_of_jHTS_wrt_j[<<rhoArguments>>]];

                        In Region[{ DOM_allConducting }];
                        Jacobian JAC_vol;
                    }
                }
            }

    {% endif %}
    {% if dm.magnet.solve.wi.superConductor and not dm.magnet.solve.wi.resistivity and type != "thermal" %}
            {
                Name RESULT_criticalCurrentDensity; // critical current density of the winding
                Value{
                    Local{
                        [Jcritical[<<JcriticalArguments>>]];
                        In Region[{ DOM_allWindings }];
                        Jacobian JAC_vol;
                    }
                }
            }

            {
                Name RESULT_jHTSOverjCritical;
                Value{
                    Local{
                        [(TransformationTensor[]*jHTS[<<JcriticalArguments>>])/Jcritical[<<JcriticalArguments>>]];
                        In Region[{ DOM_allWindings }];
                        Jacobian JAC_vol;
                    }
                }
            }

            {
                Name RESULT_criticalCurrent;
                Value{
                    Local{
                        [Jcritical[<<JcriticalArguments>>] * INPUT_relativeThicknessOfSuperConductor * 1/<<scalingFactor>> * <<dm.magnet.geometry.wi.t>> * <<dm.magnet.geometry.wi.h>>];
                        In Region[{ DOM_allWindings }];
                        Jacobian JAC_vol;
                    }
                }
            }
    {% endif %}

            {
                Name RESULT_magneticEnergy;
                Value{
                    Integral{
                        Type Global;
                        [1/2 * mu[] * {LOCALQUANT_h} * {LOCALQUANT_h}];
                        In DOM_total;
                        Jacobian JAC_vol;
                        Integration Int;
                    }
                }
            }

            {
                Name RESULT_resistiveHeating; // resistive heating
                Value{
                    Local{
                        [(rho[<<rhoArguments>>] * {d LOCALQUANT_h}) * {d LOCALQUANT_h}];
                        In Region[{ DOM_allConducting }];
                        Jacobian JAC_vol;
                    }
                }
            }

            {
                Name RESULT_voltageBetweenTerminals; // voltages in cuts
                Value{
                    Local{
                        [ - {GLOBALQUANT_V} ];
                        In DOM_terminalCut;
                    }
                }
            }

            {
                Name RESULT_currentThroughCoil; // currents in cuts
                Value{
                    Local{
                        [ {GLOBALQUANT_I} ];
                        In DOM_terminalCut;
                    }
                }
            }

            {
                Name RESULT_axialComponentOfTheMagneticField; // axial magnetic flux density
                Value{
                    Local{
                        [ CompZ[mu[] * {LOCALQUANT_h}] ];
                        In DOM_total;
                        Jacobian JAC_vol;
                    }
                }
            }

            {
                Name RESULT_totalResistiveHeating; // total resistive heating for convergence
                Value{
                    Integral{
                        Type Global;
                        [(rho[<<rhoArguments>>] * {d LOCALQUANT_h}) * {d LOCALQUANT_h}];
                        In DOM_allConducting;
                        Jacobian JAC_vol;
                        Integration Int;
                    }
                }
            }
{% endif %}
{% if dm.magnet.solve.type in ["weaklyCoupled", "stronglyCoupled", "thermal"]  %}
            {
                Name RESULT_temperature;
                Value {
                    Local{
                        [{LOCALQUANT_T}];
                        In DOM_allConducting;
                        Jacobian JAC_vol;
                    }
                }
            }

            {
                Name RESULT_heatFlux;
                Value {
                    Local{
                        [-kappa[<<kappaArguments>>] * {d LOCALQUANT_T}];
                        In DOM_allConducting;
                        Jacobian JAC_vol;
                    }
                }
            }

            {
                Name RESULT_magnitudeOfHeatFlux;
                Value {
                    Local{
                        [Norm[-kappa[<<kappaArguments>>] * {d LOCALQUANT_T}]];
                        In DOM_allConducting;
                        Jacobian JAC_vol;
                    }
                }
            }

            {
                Name RESULT_thermalConductivity; // current density magnitude
                Value{
                    Local{
                        [kappa[<<kappaArguments>>]];
                        In Region[{ DOM_allConducting }];
                        Jacobian JAC_vol;
                    }
                }
            }

            {
                Name RESULT_specificHeatCapacity; // current density magnitude
                Value{
                    Local{
                        [Cv[<<CvArguments>>]];
                        In Region[{ DOM_allConducting }];
                        Jacobian JAC_vol;
                    }
                }
            }
{% endif %}
            {
                Name RESULT_debug;
                Value{
                    Local{
                        [ TransformationTensor[] ];
                        In Region[{ DOM_allWindings }];
                        Jacobian JAC_vol;
                    }
                }
            }
        }
    }
}

//======================================================================================
// Post-operation: =====================================================================
//======================================================================================
PostOperation{
    {
        Name POSTOP_dummy;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation {
        }
    }
    {
        Name POSTOP_debug;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            // 3D magnetic field vector field:
            <<POSTOPERATION_printResults(
                quantity="RESULT_debug",
                onElementsOf="DOM_allWindings",
                name="Debug Variable",
                fileName="debug"
            )|indent(12)>>
        }
    }
{% if dm.magnet.solve.type in ["electromagnetic", "weaklyCoupled", "stronglyCoupled"] %}
    {
        Name POSTOP_magneticField;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            // 3D magnetic field vector field:
            <<POSTOPERATION_printResults(
                quantity="RESULT_magneticField",
                onElementsOf="DOM_total",
                name="Magnetic Field [T]",
                fileName="MagneticField"
            )|indent(12)>>
        }
    }
    {
        Name POSTOP_magnitudeOfMagneticField;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            // 3D magnetic field magnitude scalar field:
            <<POSTOPERATION_printResults(
                quantity="RESULT_magnitudeOfMagneticField",
                onElementsOf="DOM_total",
                name="The Magnitude of the Magnetic Field [T]",
                fileName="MagneticFieldMagnitude"
            )|indent(12)>>
        }
    }
    {
        Name POSTOP_currentDensity;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            // 3D current density vector field:
            <<POSTOPERATION_printResults(
                quantity="RESULT_currentDensity",
                onElementsOf="DOM_allConducting",
                name="Current Density [A/m^2]",
                fileName="CurrentDensity"
            )|indent(12)>>
        }
    }
    {
        Name POSTOP_magnitudeOfCurrentDensity;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            // 3D current density vector field:
            <<POSTOPERATION_printResults(
                quantity="RESULT_magnitudeOfCurrentDensity",
                onElementsOf="DOM_allConducting",
                name="The Magnitude of the Current Density [A/m^2]",
                fileName="CurrentDensityMagnitude"
            )|indent(12)>>
        }
    }
    {
        Name POSTOP_resistiveHeating;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            // Resistive heating:
            <<POSTOPERATION_printResults(
                quantity="RESULT_resistiveHeating",
                onElementsOf="DOM_allConducting",
                name="Resistive Heating [W/m^3]",
                fileName="ResistiveHeating"
            )|indent(12)>>
        }
    }
    {
        Name POSTOP_resistivity;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            // Resistive heating:
            <<POSTOPERATION_printResults(
                quantity="RESULT_resistivity",
                onElementsOf="DOM_allConducting",
                name="Resistivity [Ohm*m]",
                fileName="Resistivity"
            )|indent(12)>>
        }
    }
    {% if dm.magnet.solve.wi.superConductor and not dm.magnet.solve.wi.resistivity %}
    {
        Name POSTOP_criticalCurrentDensity;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            // Current at the cut:
            <<POSTOPERATION_printResults(
                quantity="RESULT_criticalCurrentDensity",
                onElementsOf="DOM_allWindings",
                name="Critical Current Density [A/m^2]",
                fileName="CriticalCurrentDensity"
            )|indent(12)>>
        }
    }
    {
        Name POSTOP_jHTSOverjCritical;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            // Current at the cut:
            <<POSTOPERATION_printResults(
                quantity="RESULT_jHTSOverjCritical",
                onElementsOf="DOM_allWindings",
                name="(HTS Current Density)/(Critical Current Density)",
                fileName="HTSCurrentDensityOverCriticalCurrentDensity"
            )|indent(12)>>
        }
    }
    {
        Name POSTOP_criticalCurrent;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            // Current at the cut:
            <<POSTOPERATION_printResults(
                quantity="RESULT_criticalCurrent",
                onElementsOf="DOM_allWindings",
                name="Critical Current [A]",
                fileName="CriticalCurrent"
            )|indent(12)>>
        }
    }
    {
        Name POSTOP_Ic;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        LastTimeStepOnly 1;
        Operation {
            Print[
                RESULT_criticalCurrent,
                OnElementsOf DOM_allWindings,
                StoreMinInRegister 1
            ];
        }
    }
    {
        Name POSTOP_I;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        LastTimeStepOnly 1;
        Operation {
            Print[
                RESULT_currentThroughCoil,
                OnRegion DOM_terminalCut,
                StoreInVariable $I
            ];
        }
    }
    {% endif %}
    {
        Name POSTOP_voltageBetweenTerminals;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            // Voltage at the cut:
            <<POSTOPERATION_printResults(
                quantity="RESULT_voltageBetweenTerminals",
                onRegion="DOM_terminalCut",
                format="TimeTable",
                name="Voltage [V]",
                fileName="VoltageBetweenTerminals"
            )|indent(12)>>
        }
    }
    {
        Name POSTOP_currentThroughCoil;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            // Current at the cut:
            <<POSTOPERATION_printResults(
                quantity="RESULT_currentThroughCoil",
                onRegion="DOM_terminalCut",
                format="TimeTable",
                name="Current [A]",
                fileName="CurrentThroughCoil"
            )|indent(12)>>
        }
    }
{% endif %}
{% if dm.magnet.solve.type in ["thermal", "weaklyCoupled", "stronglyCoupled"] %}
    {
        Name POSTOP_temperature;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation {
            // 3D temperature scalar field:
            <<POSTOPERATION_printResults(
                quantity="RESULT_temperature",
                onElementsOf="DOM_allConducting",
                name="Temperature [K]",
                fileName="Temperature"
            )|indent(12)>>
        }
    }
    {
        Name POSTOP_heatFlux;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation {
            // 3D temperature scalar field:
            <<POSTOPERATION_printResults(
                quantity="RESULT_heatFlux",
                onElementsOf="DOM_allConducting",
                name="Heat Flux [W/m^2]",
                fileName="HeatFlux"
            )|indent(12)>>
        }
    }
    {
        Name POSTOP_thermalConductivity;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            // Resistive heating:
            <<POSTOPERATION_printResults(
                quantity="RESULT_thermalConductivity",
                onElementsOf="DOM_allConducting",
                name="Thermal Conductivity [W/(m*K)]",
                fileName="thermalConductivity"
            )|indent(12)>>
        }
    }
    {
        Name POSTOP_specificHeatCapacity;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            // Resistive heating:
            <<POSTOPERATION_printResults(
                quantity="RESULT_specificHeatCapacity",
                onElementsOf="DOM_allConducting",
                name="Specific Heat Capacity [J/(kg*K)]",
                fileName="specificHeatCapacity"
            )|indent(12)>>
        }
    }
{% endif %}
{% if dm.magnet.postproc.timeSeriesPlots is not none %}
    {% for timeSeriesPlot in dm.magnet.postproc.timeSeriesPlots %}
    {
        Name POSTOP_timeSeriesPlot_<<timeSeriesPlot.quantity>>;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
    {% if timeSeriesPlot.quantity in ["currentThroughCoil", "voltageBetweenTerminals"] %}
            <<POSTOPERATION_printResults(
                quantity=timeSeriesPlot.getdpQuantityName,
                onRegion="DOM_terminalCut",
                format="TimeTable",
                fileName=timeSeriesPlot.fileName
            )|indent(12)>>
                {% elif timeSeriesPlot.position.x is none %}
            <<POSTOPERATION_printResults(
                quantity=timeSeriesPlot.getdpQuantityName,
                onGlobal=True,
                format="TimeTable",
                fileName=timeSeriesPlot.fileName
            )|indent(12)>>
    {% else %}
            <<POSTOPERATION_printResults(
                quantity=timeSeriesPlot.getdpQuantityName,
                onPoint=[timeSeriesPlot.position.x, timeSeriesPlot.position.y, timeSeriesPlot.position.z],
                format="TimeTable",
                fileName=timeSeriesPlot.fileName
            )|indent(12)>>
    {% endif %}
        }
    }
    {% endfor %}
{% endif %}
{% if dm.magnet.postproc is not none %}
{% if dm.magnet.postproc.magneticFieldOnCutPlane is not none %}
    {
        Name POSTOP_magneticFieldOnCutPlaneVector;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            <<POSTOPERATION_printResults(
                quantity="RESULT_magneticField",
                onSection=dm.magnet.postproc.magneticFieldOnCutPlane.onSection,
                fileName="magneticFieldOnCutPlaneVector",
                depth=1
            )|indent(12)>>
        }
    }
    {
        Name POSTOP_magneticFieldOnCutPlaneMagnitude;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        Operation{
            <<POSTOPERATION_printResults(
                quantity="RESULT_magnitudeOfMagneticField",
                onSection=dm.magnet.postproc.magneticFieldOnCutPlane.onSection,
                fileName="magneticFieldOnCutPlaneMagnitude",
                depth=1
            )|indent(12)>>
        }
    }
{% endif %}
{% endif %}
    // convergence criteria as postoperations:
{% for tolerance in (dm.magnet.solve.nls.postOperationTolerances + dm.magnet.solve.t.adaptive.postOperationTolerances)|unique(attribute="quantity") %}
    {% if tolerance.quantity == "totalResistiveHeating" %}
    {
        Name POSTOP_CONV_totalResistiveHeating;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        LastTimeStepOnly 1;
        Operation {
            Print[RESULT_totalResistiveHeating, OnElementsOf DOM_allConducting];
        }
    }
    {% elif tolerance.quantity in ["voltageBetweenTerminals", "currentThroughCoil"] %}
    {
        Name POSTOP_CONV_<<tolerance.quantity>>;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        LastTimeStepOnly 1;
        Operation {
            Print[RESULT_<<tolerance.quantity>>, OnRegion DOM_terminalCut];
        }
    }
    {% else %}
    {
        Name POSTOP_CONV_<<tolerance.quantity>>;
        NameOfPostProcessing POSTPRO_<<dm.magnet.solve.type>>;
        LastTimeStepOnly 1;
        Operation {
            Print[
                RESULT_<<tolerance.quantity>>,
                OnPoint {<<tolerance.position.x>>, <<tolerance.position.y>>, <<tolerance.position.z>>},
                StoreInVariable $test
            ];
        }
    }
    {% endif %}
{% endfor %}
}
