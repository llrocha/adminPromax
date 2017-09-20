#!/usr/bin/sh

export LD_LIBRARY_PATH=/mfocus64/lib:/lib64:/lib:/opt/rh/rh-python35/root/usr/lib64
export PYTHONPATH=/buildbot/buildbot

PYTHON_EXE=/usr/bin/python3
WORKER_DIR=/buildbot/bb-worker
VIRTUAL_DIR=${WORKER_DIR}/venv-worker

function Usage
{
	echo "Uso: $0"
	echo "		-h Exibe ajuda"
	echo "		-s Iniciar BuildBot Worker"
	echo "		-c Criar BuildBot Worker e Iniciar"
	exit 0
}

function VirtualEnv
{
	#virtualenv --no-site-packages sandbox-worker
        ${PYTHON_EXE} -m venv ${VIRTUAL_DIR}
	source ${VIRTUAL_DIR}/bin/activate
        pip install --upgrade pip
	pip install buildbot-worker
        pip install setuptools-trial
}

function CreateWorkerBuildBot
{
	mkdir -p ${WORKER_DIR}
	cd ${WORKER_DIR}
	VirtualEnv
	buildbot-worker create-worker worker localhost promax-worker Hb515
}

function InitWorkerBuildBot
{
	cd ${WORKER_DIR}
	VirtualEnv
	buildbot-worker start worker
}

if [ "$1" == "-c" ]
then
	CreateWorkerBuildBot
	InitWorkerBuildBot
elif [ "$1" == "-s" ]
then
	InitWorkerBuildBot
else
	Usage
fi	
