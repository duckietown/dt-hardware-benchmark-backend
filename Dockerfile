FROM ros:kinetic-ros-core

COPY apt.txt .
RUN apt update \ 
  && apt install -y --no-install-recommends python3 python3-virtualenv\ 
  $(awk -F: '/^[^#]/ { print $1 }' apt.txt | uniq)

RUN python3 -m virtualenv --python=/usr/bin/python3 /opt/venv

# Install dependencies:
COPY requirements.txt .
RUN . /opt/venv/bin/activate && pip install -r requirements.txt

EXPOSE 5000
# Run the application:
ADD . /backend
CMD . /opt/ros/kinetic/setup.sh && . /opt/venv/bin/activate && exec python /backend/app.py