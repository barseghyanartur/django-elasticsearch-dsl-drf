#!/usr/bin/env bash
version="6.3.2"
port="9200"
if [[ $1 == "--version" ]]
then
    version="$2"
    shift
    shift
    args="$@"
else
    version="6.3.2"
    args="$@"
fi

echo "Starting elasticsearch version $version."
echo "If you wish to start a different version, provide --version {version} argument."
echo "    Example: --version 6.4.0"

if [[ $args ]]
then
    docker pull docker.elastic.co/elasticsearch/elasticsearch:"$version"
    docker run -p "$port:$port" -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:"$version"
else
    docker pull docker.elastic.co/elasticsearch/elasticsearch:"$version"
    docker run -p "$port:$port" -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:"$version"
fi
