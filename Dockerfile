ARG BASE_CONTAINER=ucsdets/datahub-base-notebook:2021.2-stable

FROM $BASE_CONTAINER

LABEL maintainer="UC San Diego ITS/ETS <ets-consult@ucsd.edu>"

USER root

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y default-jre && \
    apt-get install -y default-jdk

ADD cplex_studio1210.linux-x86-64.bin /tmp
ADD response.properties /tmp

RUN chmod u+x /tmp/cplex_studio1210.linux-x86-64.bin
RUN /tmp/cplex_studio1210.linux-x86-64.bin -f /tmp/response.properties

USER jovyan

#RUN pip install --no-cache-dir networkx scipy && \
#    pip install --no-cache-dir geopandas && \
#    pip install --no-cache-dir babypandas && \
#    python /home/tyabuta/opt/ibm/ILOG/CPLEX_Studio1210/python/setup.py install

# Override command to disable running jupyter notebook at launch
# CMD ["/bin/bash"]
