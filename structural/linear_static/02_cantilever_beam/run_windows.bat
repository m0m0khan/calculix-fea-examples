@echo off
cd /d "%~dp0"

# Build geometry and mesh
cgx -b cantilever_linearstatic.fbd

# Solve using ccx
ccx -i cantilever_linearstatic

# Visualize displacement in y direction
cgx -b post_d2.fbd

# Visualize von mises stress
cgx -b post_mises.fbd

# Visualize stress in axial direction
cgx -b post_Szz.fbd

pause