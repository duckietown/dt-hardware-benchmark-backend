# wsgi server (used in docker container)
# [bjoern](https://github.com/jonashaag/bjoern) required.

from app import app
import bjoern

if __name__ == '__main__':
  print('Starting bjoern on port 5000...', flush=True)
  bjoern.run(app, '0.0.0.0', 5000)