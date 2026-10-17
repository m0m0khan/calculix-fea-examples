@echo off
cd /d "%~dp0"

# Build geometry and mesh
cgx -b plate_with_hole_quarter.fbd

# Solve using ccx
ccx -i plate_with_hole_quarter

# Visualize displacement in x direction
cgx -b post_d1.fbd

# Visualize von mises stress
cgx -b post_mises.fbd

pause