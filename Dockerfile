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
#CUSTOM
RUN apt-get update \
  && apt-get install -y --no-install-recommends python3 \
  python3-pip python3-setuptools python3-dev \
    $(awk -F: '/^[^#]/ { print $1 }' dependencies-apt.txt | uniq) \
  && rm -rf /var/lib/apt/lists/*

# install python dependencies
COPY ./dependencies-py.txt "${REPO_PATH}/"
# CUSTOM
RUN pip3 install -r dependencies-py.txt

# copy the source code
COPY . "${REPO_PATH}/"

# build packages
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
  catkin build \
    --workspace ${CATKIN_WS_DIR}/

# define launch script
ENV LAUNCHFILE "${REPO_PATH}/launch.sh"

# define command
CMD ["bash", "-c", "${LAUNCHFILE}"]

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

VOLUME [ "/data" ]
EXPOSE 5000

# maintainer
LABEL maintainer="Luzian Bieri (luzibier@ethz.ch)"