#!/usr/bin/sh

if [ ! -d /buildbot/gitpoller-work ]
then
	mkdir -p /buildbot/gitpoller-workdir
	cd /buildbot/gitpoller-workdir
	git clone https://hbbuildbot:HbSiS1029384756@github.com/hbsistec/2A.git
else
	cd /buildbot/gitpoller-workdir
	git pull https://hbbuildbot:HbSiS1029384756@github.com/hbsistec/2A.git
fi

cd fontes

make -j 16 all

exit $?
