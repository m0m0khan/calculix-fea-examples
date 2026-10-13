# Cantilever Beam

## Purpose
Demonstration of linear static analysis of a cantilever beam fully fixed at one end.

A cantilever beam loaded by point forces at its free end is analyzed. The problem is taken from the CalculiX 2.23 manual. The geometry, loading and boundary conditions are shown in the figure below.

<img src="inputs/problem.png" width="600" title="Problem description">

The beam size is 1000 x 1000 x 8000 mm<sup>3</sup>, which is loaded with a point force of 9x10<sup>6</sup> N and is completely fixed in all directions on the left end.

## Platform
Software: Tested with cgx 2.23/ccx 2.23
OS: Windows 11 and Ubuntu 26.04 on WSL2 (Windows 11)

## Contents

File                                                         | Contents    
:-------------                                               | :-------------
[cantilever_linearstatic.fbd](cantilever_linearstatic.fbd)   | Pre-processing script for CGX for generating cube and its mesh     
[cantilever_linearstatic.inp](cantilever_linearstatic.inp)   | CCX input of the simulation
[post_disp.fbd](post_disp.fbd)                               | Post-processing script for CGX (contour plot of displacement magnitude)
[post_mises.fbd](post_mises.fbd)                             | Post-processing script for CGX (contour plot of von Mises stress)
[post_Szz.fbd](post_Szz.fbd)                                 | Post-processing script for CGX (contour plot of stress in axial direction)
[run.py](run.py)                                             | Run all commands to solve and view the simulation's results

## Preprocessing
Elements of second order quadrilateral with reduced integration (C3D20R) are used for the analysis.

Boundary conditions:
* Left end fixed in all directions: ux = uy = uz = 0 mm

Loading:
* Point force applied on the right end with 9x10<sup>6</sup> N

### Generating mesh and node sets

```
> cgx -b cantilever_linearstatic.fbd
```

## Solving
```
> ccx -i cantilever_linearstatic
```

## Postprocessing
```
> cgx -b post_disp.fbd
```

This creates a contour plot of the displacement magnitude with a deformation factor of 10.

<img src="results/plot_disp_linearStatic.png" width="300" title="Displacement magnitude">

This figure shows the deformation of the bea, under the load. As expected, the beam bends due to the lateral force at its right end.

```
> cgx -b post_mises.fbd
```

This creates a contour plot of the von Mises stress.

<img src="results/plot_mises_linearStatic.png" width="300" title="Von Mises Stress">


```
> cgx -b post_Szz.fbd
```

This creates a contour plot of the stress in axial direction.

<img src="results/plot_Szz_linearStatic.png" width="300" title="Stress in axial direction">

This figure shows the normal stress in axial direction, which is distributed almost linearly across the height of the beam due to the bending moment.

## Run complete project
To run the complete project, run:
```
> py run.py
```