#!/usr/bin/env bash
sudo fuser -n tcp -k 9200
sudo fuser -n tcp -k 8000
sudo fuser -n tcp -k 5601
