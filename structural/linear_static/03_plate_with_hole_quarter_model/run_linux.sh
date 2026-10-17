#!/bin/bash

cd "$(dirname "$0")" || exit 1

# Build geometry and mesh
cgx -b plate_with_hole_quarter.fbd

# Solve using ccx
ccx -i plate_with_hole_quarter

# Visualize displacement in x direction
cgx -b post_d1.fbd

# Visualize von Mises stress
cgx -b post_mises.fbd