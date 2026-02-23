#!/bin/bash
# Entrypoint for the JupyterLab container.
set -e

# Exec the server
exec "$@"
