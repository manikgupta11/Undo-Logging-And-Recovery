#!/bin/bash

argc="$#" 

if [ $argc -eq 1 ]
then
    python2 2019202007_2.py "$1"
else
    python2 2019202007_1.py "$1" "$2"
fi