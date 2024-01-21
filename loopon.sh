#!/bin/bash

set -e

FORMAT="%Y-%m-%dT%H:%M:%S"

json() {
	while :
	do
		start_time=$(date --date '-5 min' +$FORMAT)
		end_time=$(date +$FORMAT)

		echo '{"start_time":'\"$start_time\"',"end_time":'\"$end_time\"'}' | python3 -m json.tool
		echo
		sleep 1
	done
}

json
