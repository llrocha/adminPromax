#!/usr/bin/sh

if [ -n "$1" ]
then
	CONFIG=$1
fi

if [ -f "$CONFIG" ];then
	. ${CONFIG}
fi

if [ ! -d /buildbot/gitpoller-work ]
then
	mkdir -p /buildbot/gitpoller-workdir
	cd /buildbot/gitpoller-workdir
	git clone https://${GIT_USER}:${GIT_PASS}@github.com/hbsistec/2A.git
else
	cd /buildbot/gitpoller-workdir
	git pull https://${GIT_USER}:${GIT_PASS}@github.com/hbsistec/2A.git
fi

cd fontes

make -j 16 all

exit $?
