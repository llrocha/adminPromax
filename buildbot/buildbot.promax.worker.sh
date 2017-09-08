#!/usr/bin/sh


WORKER_DIR=/buildbot/bb-worker
VIRTUAL_DIR=${WORKER_DIR}/sandbox-worker

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
	virtualenv --no-site-packages sandbox-worker
	source sandbox-worker/bin/activate
	pip install 'buildbot-worker'
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
