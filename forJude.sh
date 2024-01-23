#!/bin/bash

set -e

FORMAT="%Y-%m-%dT%H:%M:%S"
URL="http://127.0.0.1:8983/solr/timestamps/update"

json() {
	while :
	do
		start_time=$(date --date '-5 min' +$FORMAT)
		end_time=$(date +$FORMAT)
		doc_id=$(date +%s)
		up_time=$(uptime | awk '{print $3}' | sed -r 's/,//g')
		disk_space=$(df -hT -t ext4)
		disk_percentage=$(df / | grep / | awk '{ print $5}' | sed 's/%//g')

		# ,\"end_time\":\"$end_time\"

		document='{'\"id\":$doc_id,\"uptime\":\"$up_time\",\"disk_percentage\":$disk_percentage,\"added_on\":\"$end_time\"'}'
		echo $document		
		curl -s $URL -X POST -d '{"add":{"doc":'$document',"commitWithin":1000}}' | python3 -m json.tool
		echo
		sleep 3
	done
}

# docker pull solr:9.2.1

# for core
# docker run -p 0.0.0.0:8983:8983 --name exsolr --restart always -d solr:9.2.1 solr start -c -f -Dsolr.modules=sql
# docker exec -i exsolr solr create_collection -c timestamps
# docker exec -i exsolr solr create_collection -c books

# Run this before uploading to solr
curl http://localhost:8983/solr/timestamps/schema -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"uptime",
     "type":"string",
     "stored":true
  },
  "add-field":{
    "name":"disk_percentage",
    "type":"plong",
    "stored":true
  },
  "add-field":{
    "name":"added_on",
    "type":"pdate",
    "multiValued": false,
    "stored":true
  },
}'

# curl "http://localhost:8983/solr/timestamps/select?q=*:*&wt=json&indent=on"

# mkdir dumpdata
# wget -O dumpdata/books.csv https://raw.githubusercontent.com/apache/solr/main/solr/example/exampledocs/books.csv
# docker run --rm -v "$PWD/dumpdata:/dumpdata" --network=host solr:9.2.1 post -c books /dumpdata/books.csv

# docker run --rm solr:9.2.1 cat /etc/default/solr.in.sh
# docker run --name exsolr -d -v $PWD/custom.sh:/docker-entrypoint-initdb.d/custom.sh solr:9.2.1

# https://mavenlibs.com/jar/file/org.apache.solr/solr-sql
# https://solr.apache.org/guide/solr/latest/deployment-guide/solr-in-docker.html

# -d <confdir>            Configuration directory to copy when creating the new collection, built-in options are:

#     _default: Minimal configuration, which supports enabling/disabling field-guessing support
#     sample_techproducts_configs: Example configuration with many optional features enabled to
#        demonstrate the full power of Solr

#     If not specified, default is: _default

#     Alternatively, you can pass the path to your own configuration directory instead of using
#     one of the built-in configurations, such as: bin/solr create_collection -c mycoll -d /tmp/myconfig

#     By default the script will upload the specified confdir directory into Zookeeper using the same
#     name as the collection (-c) option. Alternatively, if you want to reuse an existing directory
#     or create a confdir in Zookeeper that can be shared by multiple collections, use the -n option

json
