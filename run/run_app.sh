#!/usr/bin/bash

export PYTHONPATH='/usr/bin/'
export PVM='/home/nabil/Documents/other'
export MAINAPP='/opt/rest/'
export PICONFIG='/etc/pihole'
export PYTHONPYCACHEPREFIX='/opt/rest/.cache'
rm -rf $PYTHONPYCACHEPREFIX/*
exec /usr/bin/python $* $1