FROM ros:kinetic-ros-core

RUN apt-get update \ 
  && apt-get install -y --no-install-recommends python3 python3-virtualenv \ 
  $(awk -F: '/^[^#]/ { print $1 }' apt.txt | uniq) \
  && rm -rf /var/lib/apt/lists/*

RUN python3 -m virtualenv --python=/usr/bin/python3 /opt/venv

# Install dependencies:
COPY requirements.txt .
RUN . /opt/venv/bin/activate && . /opt/ros/kinetic/setup.sh && pip install -r requirements.txt



# Run the application:
COPY app.py .
CMD . /opt/ros/kinetic/setup.sh && . /opt/venv/bin/activate && exec python app.py