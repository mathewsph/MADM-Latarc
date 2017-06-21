#!/bin/bash

net_file=response.txt
actual_value=0
while true
do
 if [ -e $net_file ]; then
  new_value=`cat $net_file`
  if [ $new_value != " " ]; then
   if [ $new_value != $actual_value ]; then
    iw dev sta1-wlan0 disconnect
#    iw dev sta1-wlan1 connect $new_value-ssid
    actual_value=$new_value
   fi
  else
    sleep 1 
  fi
 fi
done
#echo $x
