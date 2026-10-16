@echo off
cd /d "%~dp0"

# Build geometry and mesh
cgx -b cube_linearstatic.fbd

# Solve using ccx
ccx -i cube_linearstatic

# Visualize displacement in y direction
cgx -b post_d2.fbd

# Visualize von mises stress
cgx -b post_mises.fbd

pause