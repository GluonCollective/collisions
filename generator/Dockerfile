FROM python:3.8-slim-buster

ARG PYTHIA_VERSION=8303
ARG NCORES=4

RUN apt-get update && \
    apt-get install -y --no-install-recommends\
    build-essential \
    clang \
    cmake \
    g++ \
    gcc \
    gdb \
    libboost-program-options-dev \
    libyaml-cpp-dev \
    rsync \
    tar \
    wget --fix-missing &&\
    apt-get clean


# Build Pythia
ENV PYTHIA_IMAGE http://home.thep.lu.se/~torbjorn/pythia8/pythia${PYTHIA_VERSION}.tgz
ENV PYTHIA_DIRNAME pythia${PYTHIA_VERSION}
WORKDIR /software
RUN wget -q -O pythia8.tgz $PYTHIA_IMAGE && \
    tar -xzf pythia8.tgz && \
    rm pythia8.tgz &&\
    mv $PYTHIA_DIRNAME pythia8

RUN cd pythia8 && \
    ./configure --enable-optdebug && \
    make -j${NCORES} && \
    rm -rf /software/pythia8/tmp

# Install components for Flask REST API
COPY rest_api/requeriments.txt requiriments.txt
RUN pip install -r requiriments.txt

WORKDIR /
# Build collisions
COPY pythia_interface pythia_interface

WORKDIR /pythia_interface

RUN mkdir build && \
    cd build && \
    cmake ../ . -DPYTHIA8=/software/pythia8 && \
    make -j${NCORES}

COPY pythia_interface/pythia_config /pythia_config

WORKDIR /
COPY rest_api rest_api

ENTRYPOINT ["python", "/rest_api/app.py"]