#!/bin/sh
if test $# -ne 1;
then
	echo "Usage: start.sh init.csv";
	exit;
fi
if test -f $1
then
	FULL_PATH=`realpath $1`;
	echo "\$1 = " $1;
	echo "FullPATH = $FULL_PATH";
fi
docker run --rm --name crewJournal-docker \
-p 9000:9000 \
-v $FULL_PATH:/crew.csv \
-v $(pwd)/log:/log \
-v $(pwd)/data:/data \
-v $(pwd)/build:/build \
-v $(pwd)/src:/src \
crewjournal-jar:latest \
-ip `hostname -I | sed -e 's/ /\n/' | grep 192`
