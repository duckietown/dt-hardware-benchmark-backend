# parameters
ARG REPO_NAME="dt-hardware-benchmark-backend"

# ==================================================>
# ==> Do not change this code
ARG ARCH=arm32v7
ARG MAJOR=daffy
ARG BASE_TAG=${MAJOR}-${ARCH}
ARG BASE_IMAGE=dt-ros-commons

# define base image
FROM duckietown/${BASE_IMAGE}:${BASE_TAG}

# define repository path
ARG REPO_NAME
ARG REPO_PATH="${CATKIN_WS_DIR}/src/${REPO_NAME}"
WORKDIR "${REPO_PATH}"

# create repo directory
RUN mkdir -p "${REPO_PATH}"

# install apt dependencies
COPY ./dependencies-apt.txt "${REPO_PATH}/"
# CUSTOM
RUN apt-get update \
  && apt-get install -y --no-install-recommends python3 python3-virtualenv \
    $(awk -F: '/^[^#]/ { print $1 }' dependencies-apt.txt | uniq) \
  && rm -rf /var/lib/apt/lists/*

# CUSTOM
RUN python3 -m virtualenv --python=/usr/bin/python3 /opt/venv
# install python dependencies
COPY ./dependencies-py.txt "${REPO_PATH}/"
# CUSTOM
RUN . /opt/venv/bin/activate && pip install -r dependencies-py.txt

# copy the source code
COPY . "${REPO_PATH}/"

# build packages
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
  catkin build \
    --workspace ${CATKIN_WS_DIR}/

# define launch script
#CUSTOM
ENV APPFILE "${REPO_PATH}/app.py"

# define command
# CUSTOM
CMD . /opt/ros/kinetic/setup.sh && . /opt/venv/bin/activate && ls /data && exec python "${APPFILE}" 

#CUSTOM
VOLUME [ "/data" ]

# store module name
LABEL org.duckietown.label.module.type "${REPO_NAME}"
ENV DT_MODULE_TYPE "${REPO_NAME}"

# store module metadata
ARG ARCH
ARG MAJOR
ARG BASE_TAG
ARG BASE_IMAGE
LABEL org.duckietown.label.architecture "${ARCH}"
LABEL org.duckietown.label.code.location "${REPO_PATH}"
LABEL org.duckietown.label.code.version.major "${MAJOR}"
LABEL org.duckietown.label.base.image "${BASE_IMAGE}:${BASE_TAG}"
# <== Do not change this code
# <==================================================

# CUSTOM
EXPOSE 5000

# maintainer
LABEL maintainer="Luzian Bieri (luzibier@ethz.ch)"