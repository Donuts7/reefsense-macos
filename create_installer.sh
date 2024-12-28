#!/bin/bash

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
pip install pyinstaller

# Build executable
python build_exe.py

# Create distribution folder
mkdir -p dist/reefsense/models

# Copy model files
cp models/*.pt dist/reefsense/models/

# Create zip file
cd dist
zip -r reefsense_linux.zip reefsense
cd ..

echo "Installation package created successfully!"
echo "The package is available at: dist/reefsense_linux.zip"