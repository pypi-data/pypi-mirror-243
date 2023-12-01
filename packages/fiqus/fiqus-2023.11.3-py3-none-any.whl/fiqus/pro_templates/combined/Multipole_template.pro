// BH curve for iron yoke
Include "<<BHcurves>>";

Group {
  // Physical regions:
  <<rm.air.vol.name>> = Region[ <<rm.air.vol.number>> ];  // Air
  <<rm.air_far_field.vol.names[0]>> = Region[ <<rm.air_far_field.vol.numbers[0]>> ];  // AirInf
{% for name, number in zip(rm.powered.vol.names, rm.powered.vol.numbers) %}
  <<name>> = Region[ <<number>> ];
{% endfor %}

{% for name, number in zip(rm.induced.vol.names, rm.induced.vol.numbers) %}
  <<name>> = Region[ <<number>> ];
{% endfor %}

{% for name, number in zip(rm.iron.vol.names, rm.iron.vol.numbers) %}
  <<name>> = Region[ <<number>> ];
{% endfor %}

  // Surface_ht0 = Region[ 1100 ];
  // Surface_bn0 = Region[ 1101 ];
  <<rm.air_far_field.surf.name>> = Region[ <<rm.air_far_field.surf.number>> ];

  <<nc.omega>><<nc.powered>> = Region[ {<<rm.powered.vol.names|join(', ')>>} ];
  <<nc.omega>><<nc.iron>> = Region[ {<<rm.iron.vol.names|join(', ')>>} ];
  <<nc.omega>><<nc.induced>> = Region[ {<<rm.induced.vol.names|join(', ')>>} ];
  <<nc.omega>><<nc.air_far_field>> = Region[ <<rm.air_far_field.vol.names[0]>> ];
  <<nc.omega>><<nc.conducting>> = Region[ {<<nc.omega>><<nc.powered>>, <<nc.omega>><<nc.iron>>, <<nc.omega>><<nc.induced>>} ];
  <<nc.omega>> = Region[ {<<rm.air.vol.name>>, <<rm.air_far_field.vol.names[0]>>, <<nc.omega>><<nc.powered>>, <<nc.omega>><<nc.iron>>, <<nc.omega>><<nc.induced>>} ];
  <<nc.boundary>><<nc.omega>> = Region[ <<rm.air_far_field.surf.name>> ];
  //Sur_Neu_Mag = Region[ {} ]; // empty
  //Dom_Hcurl_a_Mag_2D = Region[ {<<nc.omega>>, Sur_Neu_Mag} ];
}

Function {
  mu0 = 4.e-7 * Pi;
  
  /* New ONELAB variables can then be defined using DefineNumber, e.g.: */
  //murCore = DefineNumber[100, Name "Model parameters/Mur core",
			 //Help "Magnetic relative permeability of Core"];

  nu [ Region[{<<rm.air.vol.name>>, <<nc.omega>><<nc.powered>>, <<rm.air_far_field.vol.names[0]>>, <<nc.omega>><<nc.induced>>}] ]  = 1. / mu0;

{% for name in rm.iron.vol.names %}
  nu [ <<name>> ]  = nu<<name>>[$1];
  dnuIronYoke [ <<name>> ]  = dnu<<name>>[$1];
{% endfor %}
  /*nu [ BHiron2 ]  = nuBHiron2[$1]; //1. / (murCore * mu0);
  dnuIronYoke [ BHiron2 ]  = dnuBHiron2[$1];*/

  //Current = DefineNumber[7180, Name "Model parameters/Current",
	//		 Help "Current injected in coil [A]"];

  // NbTurns = 1 ; // number of turns in the coil
{% for name, current in zip(rm.powered.vol.names, rm.powered.vol.currents) %}
  js_fct[ <<name>> ] = <<current>>/SurfaceArea[];
{% endfor %}
  //js_fct[ PowPos ] = Current/SurfaceArea[];
  //js_fct[ PowNeg ] = -Current/SurfaceArea[];
  /* The minus sign is to have the current in -e_z direction,
     so that the magnetic induction field is in +e_y direction */
}

Constraint {
  { Name Dirichlet_a_Mag;
    Case {
      { Region <<nc.boundary>><<nc.omega>> ; Value 0.; }
    }
  }
  { Name SourceCurrentDensityZ;
    Case {
      { Region <<nc.omega>><<nc.powered>> ; Value js_fct[]; }
    }
  }
}

FunctionSpace {
  { Name Hcurl_a_Mag_2D; Type Form1P; // Magnetic vector potential a
    BasisFunction {
      { Name se; NameOfCoef ae; Function BF_PerpendicularEdge;
        Support <<nc.omega>> ; Entity NodesOf[ All ]; }
    }
    Constraint {
      { NameOfCoef ae; EntityType NodesOf;
        NameOfConstraint Dirichlet_a_Mag; }
    }
  }

  { Name Hregion_j_Mag_2D; Type Vector; // Electric current density js
    BasisFunction {
      { Name sr; NameOfCoef jsr; Function BF_RegionZ;
        Support <<nc.omega>><<nc.powered>>; Entity <<nc.omega>><<nc.powered>>; }
    }
    Constraint {
      { NameOfCoef jsr; EntityType Region;
        NameOfConstraint SourceCurrentDensityZ; }
    }
  }

}

Jacobian {
  { Name Jac ;
    Case { { Region <<nc.omega>><<nc.air_far_field>> ;
             Jacobian VolSphShell {<<rm.air_far_field.vol.radius_in>>, <<rm.air_far_field.vol.radius_out>>} ; }
           { Region All ; Jacobian Vol ; }
    }
  }
}

Integration {
  { Name Int ;
    Case { { Type Gauss ;
	Case {
	  { GeoElement Point       ; NumberOfPoints  1 ; }
	  { GeoElement Line        ; NumberOfPoints  3 ; }
	  { GeoElement Triangle{% if dm.mesh.ElementOrder == 2 %}2{% endif %}    ; NumberOfPoints  {% if dm.mesh.ElementOrder == 2 %}3{% else %}4{% endif %} ; }
	  { GeoElement Quadrangle  ; NumberOfPoints  4 ; }
	}
      } }
  }
}

Formulation {
  { Name Magnetostatics_a_2D; Type FemEquation;
    Quantity {
      { Name a ; Type Local; NameOfSpace Hcurl_a_Mag_2D; }
      { Name js; Type Local; NameOfSpace Hregion_j_Mag_2D; }
    }
    Equation {
      // all terms on the left-hand side (hence the "-" sign in front of
      // Dof{js}):
      //Integral { [ nu[] * Dof{d a} , {d a} ];
        //In <<nc.omega>>; Jacobian Jac; Integration Int; }
      Integral { [ nu[{d a}] * Dof{d a} , {d a} ];
        In <<nc.omega>>; Jacobian Jac; Integration Int; }

      {% if dm.geometry.with_iron_yoke %}
          Integral { JacNL[ dnuIronYoke[{d a}] * Dof{d a} , {d a} ];
            In <<nc.omega>><<nc.iron>>; Jacobian Jac; Integration Int; }
      {% endif %}

      Integral { [ -Dof{js} , {a} ];
        In <<nc.omega>><<nc.powered>>; Jacobian Jac; Integration Int; }
    }
  }
}

relTol         = 1e-5;
absTol         = 1e-5;
relaxFactor    = 0.9;
NmaxIterations = 100;

Resolution {
  { Name MagSta_a;
    System {
      { Name Sys_Mag; NameOfFormulation Magnetostatics_a_2D; }  // NameOfMesh "mesh.msh";
    }
    Operation {
      InitSolution[Sys_Mag];
      IterativeLoopN[NmaxIterations, relaxFactor,
        System        { { Sys_Mag, relTol, absTol, Solution LinfNorm } }
        // PostOperation { { V_Top,   ReltolP, AbstolP,          MeanL1Norm } }
      ] {
          GenerateJac[Sys_Mag]; SolveJac[Sys_Mag];
        }
      // Generate[Sys_Mag]; Solve[Sys_Mag]; SaveSolution[Sys_Mag];
    }
  }
}

PostProcessing {
  { Name MagSta_a_2D; NameOfFormulation Magnetostatics_a_2D;
    Quantity {
      { Name a;
        Value {
          Term { [ {a} ]; In <<nc.omega>>; Jacobian Jac; }
        }
      }
      { Name az;
        Value {
          Term { [ CompZ[{a}] ]; In <<nc.omega>>; Jacobian Jac; }
        }
      }
      { Name b;
        Value {
          Term { [ {d a} ]; In <<nc.omega>>; Jacobian Jac; }
        }
      }
      { Name h;
        Value {
          Term { [ nu[{d a}] * {d a} ]; In <<nc.omega>>; Jacobian Jac; }
        }
      }
      { Name js;
        Value {
          Term { [ {js} ]; In <<nc.omega>>; Jacobian Jac; }
        }
      }
      /*{ Name field_current;
          Value { Integral{[ Abs[CompZ[{js}]] ];
    				In <<nc.omega>><<nc.powered>>; Jacobian Jac; Integration Int; }
           }
      }*/

    }
  }
}

/*e = 1.e-5;
h = 0.02;
p2 = {0.25-e,h,0}; // horizontal cut through model, just above x-axis.*/

p1 = {0,0,0};
p2 = {<<rm.air_far_field.vol.radius_out>>,0,0};
PostOperation {
  { Name Map_a; NameOfPostProcessing MagSta_a_2D;
    Operation {
      /* Echo[ Str["l=PostProcessing.NbViews-1;",
		"View[l].IntervalsType = 1;",
		"View[l].NbIso = 40;"],
	    File "tmp.geo", LastTimeStepOnly] ; */
    {% for var_name, vol_name, file_ext in zip(dm.postproc.variables, dm.postproc.volumes, dm.postproc.file_exts) %}
	  Print[ <<var_name>>, OnElementsOf <<vol_name>>, File "<<var_name>>_<<vol_name>>.<<file_ext>>"] ;
	{% endfor %}
	  Print [ b, OnLine {{List[p1]}{List[p2]}} {1000}, Format SimpleTable, File "Center_line.csv"];
      //Print[ field_current[block_1_1_pos], OnGlobal, Format Table, File "field_current.txt" ];
      //Print[ b, OnLine{{List[p1]}{List[p2]}} {50}, File "by.pos" ];
    }
  }
}

/*DefineConstant[
  R_ = {"Analysis", Name "GetDP/1ResolutionChoices", Visible 0},
  C_ = {"-solve -v2", Name "GetDP/9ComputeCommand", Visible 0},
  P_ = {"", Name "GetDP/2PostOperationChoices", Visible 0}
];*/