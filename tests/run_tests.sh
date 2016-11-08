#!/usr/bin/env bash
# get parent directory of the directory where script is stored
MAINDIR="$(dirname "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )")"
# export python directory where to search for modules
export PYTHONPATH=${MAINDIR}
# run tests
cd ${MAINDIR} && ./tests/integration_test.py