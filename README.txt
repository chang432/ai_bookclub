backend:
- nginx docker container exposes /data and /webapp for the website
- on startup nginx docker container calls update.py and does a transfer only to move
desired files into /data location.