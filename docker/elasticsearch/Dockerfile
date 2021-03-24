FROM docker.elastic.co/elasticsearch/elasticsearch:7.5.2
ADD ./docker/elasticsearch/elasticsearch.yml /usr/share/elasticsearch/config/
USER root
RUN chown elasticsearch:elasticsearch config/elasticsearch.yml
USER elasticsearch
