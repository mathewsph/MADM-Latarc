#!/bin/bash


while true
do
    cat packet.txt|cut -d " " -f9,15,37,16|tail -1 > host_data.txt &
    sleep 1
done

#while ; do
#   cat packet.txt|cut -d " " -f9,14 > host_data.txt &
#done > host_data.txt;
