# Twistagram

# To run tha app in docker:
 - Open a terminal (WSL2 if you use windows)
 - Navigate to the project folder
 - Run ``docker build -t flask_app-docker:python3.8 -f Dockerfile .``
 - Run ``docker run -p 5000:5000 flask_app-docker:python3.8 ``
 - Open a browser and go to ``localhost:5000``
