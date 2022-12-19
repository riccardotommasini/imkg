#! /bin/sh

export CALL_PER_SECOND=10


for ((i=25;i<=160;i=i+5)); 
do
 	for ((j=$i;j<=$i+5;j++)); 
 	do
 		export FILENAME=$j
 		echo "nohup ./spotlight.py > output.${FILENAME}.log &"
		nohup ./spotlight.py > output.${FILENAME}.log &
	done
	echo "---"
	SLEEP 1800
done


