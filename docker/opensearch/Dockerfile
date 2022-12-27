FROM opensearchproject/opensearch:1.0.1
ADD ./docker/opensearch/opensearch.yml /usr/share/opensearch/config/
USER root
RUN chown opensearch:opensearch config/opensearch.yml
USER opensearch
