#!/bin/bash
echo "Creating virtual environment..."
python -m venv network_detector_env

echo "Activating virtual environment..."
source network_detector_env/bin/activate

echo "Installing required packages..."
pip install -r requirements.txt

echo "Setup complete! Activate the environment using:"
echo "source network_detector_env/bin/activate"
