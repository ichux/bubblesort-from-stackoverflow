#!/bin/bash

set -e

FORMAT="%Y-%m-%dT%H:%M:%S"
URL="http://192.168.87.25:8983/solr/test/update"

json() {
	while :
	do
		start_time=$(date --date '-5 min' +$FORMAT)
		end_time=$(date +$FORMAT)
		doc_id=$(date +%s)

		document='{'\"id\":\"$doc_id\",\"start_time\":\"$start_time\",\"end_time\":\"$end_time\"'}'
		
		curl $URL -X POST -d '{"add":{"doc":'$document',"commitWithin":1000}}'
		
		echo
		sleep 1
	done
}

json
