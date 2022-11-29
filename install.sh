#!/bin/bash
if [ -x "$(command -v pip3)" ]; then
  pip3 uninstall -y fx-py-sdk
else
  # echo "Error: pip is not installed, replaced with command pip..."
  pip uninstall -y fx-py-sdk
fi

rm -rf ./build
rm -rf ./dist
rm -rf ./*.egg-info
python setup.py install

