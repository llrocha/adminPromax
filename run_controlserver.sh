#!/bin/bash

. /opt/rh/rh-python36/enable

if [ ! -d venv/bin/ ]
then
  pip3 install virtualenv --upgrade
  virtualenv venv
fi

. venv/bin/activate

pip3 install -r requirements.txt

cd controlServer

#./start.sh
export PYTHONPATH=/root/adminPromax

echo "Running Control Server:"
python controlserver.py
