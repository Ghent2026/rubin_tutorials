# EDUCADO_2026
Lectures on Rubin and LSST for the EDUCADO 2026 school 


## Setting up the jupyterlab instance 

1. Install and start Docker. If updates are avalable, install them.

2. Statt the Jupyterlab server
> docker compist up --build

Explanation: 
docker compose up --build is actually two instructions combined into one command:

docker compose up tells Docker to start all the services defined in your docker-compose.yml file. In your case, that's one service — the JupyterLab server. "Up" means "bring it up and keep it running."

--build tells Docker to (re)build the image from your Dockerfile before starting. Without this flag, Docker reuses a previously built image if one exists — which means any changes you've made to the Dockerfile or requirements.txt would be ignored. Adding --build ensures you're always starting fresh from your current code.

What actually happens, step by step:

Docker reads docker-compose.yml to understand what to build and run
It reads the Dockerfile and builds a new image — this includes pulling the Python 3.11 base image, installing JupyterLab, and installing your requirements.txt packages

Once the image is built, Docker starts a container from it
The notebooks/ folder on your laptop is linked ("mounted") into the container, so files you create there are saved to your actual machine

JupyterLab starts inside the container and listens on port 8888
You open http://localhost:8888 in a browser to use it

A useful analogy: Think of the image as a recipe and the container as the meal you cook from it. --build means "re-cook from the recipe" rather than reheating leftovers.

3. Open http://localhost:8888  to see the JupyteLab server
If you are using Cursor, use cmd+click and it will open a tab in Cursor. Otherwise you can go to a browser. 
Go to the JupyterLab and explore the files

4. Requirements.txt
requirements.txt — added ipykernel, the package that provides the Python kernel JupyterLab talks to
Dockerfile — added a python -m ipykernel install step that explicitly registers the kernel so JupyterLab can find it

5. Using the AI extension in jupyterlab

