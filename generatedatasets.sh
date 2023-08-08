#!/bin/bash
sudo apt-get install -y python3.10 python3-pip
pip3 install virtualenv
virtualenv ./venv
source ./venv/bin/activate
pip3 install -r requirements.txt
python3 retorch/core.py


deactivate
