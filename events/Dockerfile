FROM debian:buster-slim AS download

ARG PYTHIA_IMAGE=http://home.thep.lu.se/~torbjorn/pythia8/pythia8244.tgz
ARG PYTHIA_DIRNAME=pythia8244

RUN apt-get update && \
    apt-get install -y wget

WORKDIR /download
RUN wget -q -O pythia8.tgz $PYTHIA_IMAGE && \
    tar -xzf pythia8.tgz && \
    rm pythia8.tgz &&\
    mv $PYTHIA_DIRNAME pythia8

FROM python:3.8-slim-buster
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    clang \
    cmake \
    g++ \
    gcc \
    gdb \
    libboost-program-options-dev \
    rsync \
    tar && \
    apt-get clean

COPY --from=download /download/pythia8 /software/pythia8
RUN cd /software/pythia8 && \
    ./configure --enable-optdebug && \
    make -j2 && \
    rm -rf /software/pythia8/tmp

COPY collisions collisions


RUN cd collisions && \
    mkdir build && \
    cd build && \
    cmake /collisions . -DPYTHIA8=/software/pythia8 && \
    make -j2

# Flask REST API
COPY event_api/requeriments.txt requiriments.txt
RUN pip install -r requiriments.txt

#ENTRYPOINT ["python", "/event_api/event_api.py"]