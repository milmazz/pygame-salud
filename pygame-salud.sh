#!/bin/sh

path=$(readlink $0)

if [ $path ]; then
	gamedir=$(dirname $path)
else
	gamedir=$(dirname $0)
fi

cd $gamedir/src

python salud.py $* 
