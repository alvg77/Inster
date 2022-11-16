# Twistagram

# To run tha app in docker:
 - Open a terminal (WSL2 if you use windows)
 - Navigate to the project folder
 - To build a docker image run ``docker build -t flask_app-docker:python3.8 -f Dockerfile .``
 - To create a container from that image run ``docker run -p 5000:5000 --name flask_app flask_app-docker:python3.8``
 - To start the container run ``docker start flask_app``
 - Open a browser and go to ``localhost:5000``
