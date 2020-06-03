##Deploy##
```bash
docker build . -t bm_backend
docker run -dit -p 5000:5000 bm_backend
```


##Develop in container##
Start Developer Container, attach to said container. (Port 5000 needs to be forwarded)
in the attached terminal:
```bash
source /opt/ros/kinetic/setup.bash
source /opt/venv/bin/activate

python app.py
```
Have fun developing.
