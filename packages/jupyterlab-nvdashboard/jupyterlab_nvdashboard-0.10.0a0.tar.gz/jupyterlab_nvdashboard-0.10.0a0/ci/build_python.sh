#!/bin/bash
# Copyright (c) 2023, NVIDIA CORPORATION.

set -euo pipefail

source rapids-env-update

rapids-print-env

rapids-logger "Begin py build"

# TODO: Remove `--no-test` flag once importing on a CPU
# node works correctly
rapids-conda-retry mambabuild --no-test conda/recipes/jupyterlab-nvdashboard

rapids-upload-conda-to-s3 python