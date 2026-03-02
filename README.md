# EDUCADO_2026

This directory provides a Docker container to run a JuypterLab instance with the LSST Science Pipelines installed to run the educado tutorials 

## Quickstart  

1. Install and start Docker. If updates are avalable, install them.

2. Clone this repository
   > git clone git@github.com:leannep/EDUCADO_2026.git
   > cd EDUCADO_2026

4. Build and start the container
   > docker compose up --build

   To change the version of the sicnece pipelines 
   > docker compose build --build-arg LSST_VERSION=al9-w_2025_29
   > docker compose up 
   > d (to free terminal)

5. Open http://localhost:8888 (http://127.0.0.1:8888/lab)  to see the JupyteLab server
If you are using Cursor, use cmd+click and it will open a tab in Cursor. Otherwise you can go to a browser. 
Go to  JupyterLab and explore the files. You should see JupyterLab with a LSST Science Pipelines kernel availble

Open any of th tutorials and run them

6. The version of the science pipelines can also be changed in the docker-compose.yml file 
     build:
      args:
        LSST_VERSION: al9-v29_2_1
   
7. Stop the service 
   > docker compose down
