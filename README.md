## Deploy
```bash
docker build . -t bm_backend
docker run -dit -p 5000:5000 -e MYSQL_USER=user -e MYSQL_PW=pw -e MYSQL_URL=url -e MYSQL_DB=db bm_backend
```

## Run locally
```bash
docker run -dit -p 5000:5000 -e LOCAL=true -v /data:/~/data bm_backend
```

to see the API Documentation go to `localhost:5000`

## Send data from CLI
E.g
```bash
curl -X POST "http://127.0.0.1:5000/hw_benchmark/files/v1__test__new__autobot14__1589916105" -F "meta={\"bot_type\":\"DB18p4\",\"battery_type\":\"Old Alu\",\"release\":\"master19\"}" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "sd_card_json=@sd_speed.json" -F "latencies_bag=@meas_01/master19_autobot14_01.bag"  -F "meta_json=@meta.json"
```


## Develop in container
Start Developer Container, attach to said container. (Port 5000 needs to be forwarded)
in the attached terminal:
```bash
source /opt/ros/kinetic/setup.bash
source /opt/venv/bin/activate

python app.py
```
Have fun developing.

Linting:

```bash
pip install -r requirements-dev.txt
pylint --load-plugins pylint_flask apis/ files/ logic/ schemas/ sql/ app.py
autopep8 --in-place --aggressiv --aggressiv --recursive apis/ files/ logic/ schemas/ sql/ app.py
```

