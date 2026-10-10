"""
This script automates the generation of mesh geometries and parses .frd output 
files for displacement-controlled and force-controlled cube simulations.

Author: Muhammad Mohsin Khan
Date: October 09, 2026
License: MIT
Repository: https://github.com/m0m0khan/calculix-fea-examples
"""

import os
import subprocess
import sys

# ==========================================================
# CONFIGURATION
# ==========================================================
WORKDIR = os.getcwd()

CGX = "cgx.exe"
CCX = "ccx.exe"

# Geometry / Mesh base name
DRAWING = "cube"
FBD = os.path.join(WORKDIR, f"{DRAWING}.fbd")

# Master template filenames (Keep your original hardcoded files as templates)
POSTVM_TEMPLATE = os.path.join(WORKDIR, "post_mises.fbd")
POSTD2_TEMPLATE = os.path.join(WORKDIR, "post_d2.fbd")

# List all the jobs you want to solve and visualize
JOBS = ["cube_displacement_controlled", "cube_force_controlled"]


# ==========================================================
# 1. RUN CGX TO CREATE THE MESH (Shared by all jobs)
# ==========================================================
def run_preprocessing():
    print("\n[1/3] Running CGX batch preprocessing...")

    cgx_result = subprocess.run(
        [str(CGX), "-b", str(FBD)],
        cwd=WORKDIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        check=False,
    )

    log_cgxfile_path = os.path.join(WORKDIR, f"{DRAWING}_cgx.log")
    with open(log_cgxfile_path, "w", encoding="utf-8", errors="replace") as f:
        f.write(cgx_result.stdout)
    print(cgx_result.stdout)

    if cgx_result.returncode != 0:
        sys.exit(f"CGX returned an error. Check {DRAWING}_cgx.log.")


# ==========================================================
# HELPER: GENERATE DYNAMIC FBD FILE
# ==========================================================
def create_dynamic_fbd(template_path, job_name, suffix):
    """
    Reads a master .fbd template, replaces the hardcoded base job name
    with the current active job_name, and writes out a temporary .fbd file.
    """
    if not os.path.exists(template_path):
        print(f"[WARNING] Template file missing: {template_path}")
        return None

    # Define the temporary file path (e.g., post_mises_cube_force_controlled.fbd)
    base_template_name = os.path.splitext(os.path.basename(template_path))[0]
    temp_fbd_path = os.path.join(WORKDIR, f"{base_template_name}_{job_name}.fbd")

    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Swap out the hardcoded name with our current active job name
    updated_content = content.replace("cube_displacement_controlled", job_name)

    with open(temp_fbd_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    return temp_fbd_path


# ==========================================================
# 2. RUN CCX SOLVER AND LAUNCH CGX POST-PROCESSING FOR A JOB
# ==========================================================
def run_solver_and_post(job_name):
    print(f"\n--- Processing Job: {job_name} ---")
    print("[2/3] Running CalculiX CrunchiX...")

    ccx_result = subprocess.run(
        [str(CCX), "-i", job_name],
        cwd=WORKDIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        check=False,
    )

    log = ccx_result.stdout
    log_file_path = os.path.join(WORKDIR, f"{job_name}_solver.log")
    with open(log_file_path, "w", encoding="utf-8", errors="replace") as f:
        f.write(log)
    print(log)

    if ccx_result.returncode != 0:
        print(f"[ERROR] CCX returned an error for {job_name}. Check {job_name}_solver.log.")
        return 

    print(f"[OK] Analysis completed for {job_name}.")
    print(f"[OK] Results: {os.path.join(WORKDIR, f'{job_name}.frd')}")

    # Generate the custom .fbd scripts on the fly for this specific job
    temp_vm_fbd = create_dynamic_fbd(POSTVM_TEMPLATE, job_name, "mises")
    temp_d2_fbd = create_dynamic_fbd(POSTD2_TEMPLATE, job_name, "d2")

    print(f"[3/3] Opening results for {job_name} in CGX...")
    if temp_d2_fbd:
        subprocess.Popen([str(CGX), "-b", temp_d2_fbd], cwd=WORKDIR)
    if temp_vm_fbd:
        subprocess.Popen([str(CGX), "-b", temp_vm_fbd], cwd=WORKDIR)


# ==========================================================
# MAIN EXECUTION
# ==========================================================
if __name__ == "__main__":
    # Generate the mesh once
    run_preprocessing()

    # Loop through and solve each job sequentially
    for job in JOBS:
        run_solver_and_post(job)

    print("\nAll jobs triggered.")
