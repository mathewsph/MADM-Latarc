#!/bin/bash

stdbuf -oL tcpdump -i mon1 dst host 10.0.0.2 -e -n -tt > packet.txt &

while read -r line; do
	echo True
done < packet.txt;

