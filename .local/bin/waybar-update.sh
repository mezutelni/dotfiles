#!/usr/bin/env bash

sudo pacman -Syu 

for num in {10..1}; 
do
	printf "terminal will close in $num s\n"
	sleep 1
done
