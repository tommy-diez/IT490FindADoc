#!/usr/bin/bash

#declaring array of addresses:ports and standarize variables
declare -a arr=("172.26.96.163 8081" "172.26.224.180 5432" "172.26.192.203 5672" "172.26.169.103 5672" "172.26.71.194 5000")
pass="Findadoc!"

#loop through the array and send it to the variable ipPort
for ipPort in "${arr[@]}"
do
	#use netcat to see if the the ip@port is open and working then send it to a file
	nc -w 1 -v $ipPort > ncResults.txt 2>&1
	#use sed to parse the file to see if nc succeeded
	line=$(sed -n 's/.*\(succeeded\).*/\1/p' ncResults.txt)

	#if the line in the file doesn't equal succeeded ssh into that system and run the start.sh
	if [[ "$line" != "succeeded" ]]; then
		ip=${ipPort% *}
		echo "Failed to NC $line  $ipPort"
		echo "$pass" | ssh -tt findadoc@$ip "cd /home/findadoc/IT490; sudo bash start.sh"
	else
		echo "NC worked $line  $ipPort"
	fi
done
