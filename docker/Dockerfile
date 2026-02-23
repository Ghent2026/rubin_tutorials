# Base image
FROM python:3.11-slim

# System dependencies 
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        curl \
        nodejs \
        npm \
    && rm -rf /var/lib/apt/lists/*

# Install Claude Code CLI globally
RUN npm install -g @anthropic-ai/claude-code

# Create non root user
RUN useradd --create-home --shell /bin/bash jupyter

# Install Python dependencies as system-wide root 
COPY docker/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && python -m ipykernel install --sys-prefix --name python3 --display-name "Python 3"

# Store overrides + server config in the system-wide Jupyter config dir.
RUN mkdir -p /usr/local/etc/jupyter
COPY docker/jupyterlab-overrides.json /usr/local/etc/jupyter/overrides.json
COPY docker/jupyter_server_config.py  /usr/local/etc/jupyter/jupyter_server_config.py
RUN chmod 644 /usr/local/etc/jupyter/overrides.json \
           /usr/local/etc/jupyter/jupyter_server_config.py

# Deploy overrides.json at build time to the JupyterLab application settings
# directory. Using sys.prefix avoids hardcoding /usr/local and works regardless
# of the Python installation prefix.
RUN SETTINGS_DIR=$(python3 -c "import sys; print(f'{sys.prefix}/share/jupyter/lab/settings')") \
    && mkdir -p "$SETTINGS_DIR" \
    && cp /usr/local/etc/jupyter/overrides.json "$SETTINGS_DIR/overrides.json" \
    && chmod 644 "$SETTINGS_DIR/overrides.json"

# Write JupyterLab user settings directly into the jupyter user's home.
# User settings take priority over overrides.json and are the most reliable way
# to suppress dialogs (restart confirmation, news popup, session restore).
RUN mkdir -p \
    /home/jupyter/.local/share/jupyter/lab/user-settings/@jupyterlab/apputils-extension \
    /home/jupyter/.local/share/jupyter/lab/user-settings/@jupyterlab/notebook-extension
COPY docker/user-settings/@jupyterlab/apputils-extension/notification.jupyterlab-settings \
     /home/jupyter/.local/share/jupyter/lab/user-settings/@jupyterlab/apputils-extension/notification.jupyterlab-settings
COPY docker/user-settings/@jupyterlab/apputils-extension/sessionDialogs.jupyterlab-settings \
     /home/jupyter/.local/share/jupyter/lab/user-settings/@jupyterlab/apputils-extension/sessionDialogs.jupyterlab-settings
RUN chown -R jupyter:jupyter /home/jupyter/.local

# Create workspace and give ownership to jupyter user
RUN mkdir -p /home/jupyter/workspace/notebooks \
    && chown -R jupyter:jupyter /home/jupyter/workspace

WORKDIR /home/jupyter/workspace


# Copy project files 
COPY --chown=jupyter:jupyter . .

# Entrypoint
COPY docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8888

# Drop to a non-root user  
USER jupyter

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["jupyter", "lab", \
     "--ip=0.0.0.0", \
     "--port=8888", \
     "--no-browser", \
     "--notebook-dir=/home/jupyter/workspace", \
     "--ServerApp.token=''", \
     "--ServerApp.password=''"]
