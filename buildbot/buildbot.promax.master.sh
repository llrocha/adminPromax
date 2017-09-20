#!/usr/bin/sh

export LD_LIBRARY_PATH=/mfocus64/lib:/lib64:/lib:/opt/rh/rh-python35/root/usr/lib64
export PYTHONPATH=/buildbot/buildbot

PYTHON_EXE=/usr/bin/python3
MASTER_DIR=/buildbot/bb-master
VIRTUAL_DIR=${MASTER_DIR}/venv-master

function Usage
{
	echo "Uso: $0"
	echo "		-h Exibe ajuda"
	echo "		-s Iniciar BuildBot Master"
	echo "		-c Criar BuildBot Master e Iniciar"
	exit 0
}

function VirtualEnv
{
	if [ -d ${VIRTUAL_DIR} ]
	then
		rm -f ${VIRTUAL_DIR}
	fi
	#virtualenv --no-site-packages sandbox-master
        ${PYTHON_EXE} -m venv ${VIRTUAL_DIR}
	source ${VIRTUAL_DIR}/bin/activate
	pip install --upgrade pip
	pip install 'buildbot[bundle]'
}

function CreateMasterBuildBot
{
	if [ -d ${MASTER_DIR} ]
	then
		echo Master já existe!
		exit 1
	fi
	VirtualEnv
	mkdir -p ${MASTER_DIR}
	cd ${MASTER_DIR}
	buildbot create-master master
	cp ${PYTHONPATH}/master.cfg master/
}

function InitMasterBuildBot
{
	cd ${MASTER_DIR}
	VirtualEnv
	buildbot start master
}

if [ "$1" == "-c" ]
then
	CreateMasterBuildBot
	InitMasterBuildBot
elif [ "$1" == "-s" ]
then
	InitMasterBuildBot
else
	Usage
fi	
