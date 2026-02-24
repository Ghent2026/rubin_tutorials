#!/bin/bash
set -e

echo "Activating LSST Science Pipelines environment..."

# Source the LSST stack initialisation script.  This sets up EUPS and puts
# the stack's Python (and jupyter) on PATH.
source /opt/lsst/software/stack/loadLSST.bash

# Activate the top-level LSST distribution so that all lsst.* packages are
# importable in notebooks without any manual setup step.
setup lsst_distrib

echo "LSST Science Pipelines environment ready."
echo "Launching JupyterLab..."

exec "$@"
