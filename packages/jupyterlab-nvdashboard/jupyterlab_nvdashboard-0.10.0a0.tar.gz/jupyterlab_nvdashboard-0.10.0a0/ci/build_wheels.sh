#!/bin/bash
# Copyright (c) 2023, NVIDIA CORPORATION.

set -euo pipefail

package_name="jupyterlab-nvdashboard"

source rapids-configure-sccache
source rapids-date-string


rapids-logger "Install dependencies for py build"
# Install NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

nvm install 18 && nvm use 18

rapids-logger "Begin py build"

# TODO: Remove `--no-test` flag once importing on a CPU
# node works correctly
python -m pip install build
python -m build -s

RAPIDS_PY_WHEEL_NAME="${package_name}" rapids-upload-wheels-to-s3 dist