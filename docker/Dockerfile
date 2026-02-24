# LSST image version — override at build time with:
#   docker compose build --build-arg LSST_VERSION=al9-w_2025_29
ARG LSST_VERSION=al9-v29_2_1
FROM ghcr.io/lsst/scipipe:${LSST_VERSION}

# Set to a plain non-login bash shell here
SHELL ["/bin/bash", "-c"]

# All installation steps run as root
USER root

# System packages 
# nodejs lives in the AppStream module stream and must be enabled first;
# Claude Code is a Nodejs application if Claude code is not installed then this is not needed.
RUN dnf module enable -y nodejs:20 \
    && dnf install -y nodejs \
    && dnf clean all

# Claude Code CLI 
RUN npm install -g @anthropic-ai/claude-code

# Non-root user 
RUN useradd --create-home --shell /bin/bash jupyter

# Requirements
# Install all requirements into the LSST stack's own Python environment so
# that every notebook has direct access to lsst.* packages.
COPY docker/requirements.txt /tmp/requirements.txt
RUN /bin/bash -c " \
    source /opt/lsst/software/stack/loadLSST.bash \
    && setup lsst_distrib \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && python -m ipykernel install \
         --sys-prefix \
         --name lsst \
         --display-name 'LSST Science Pipelines (Python 3)'"

# Jupyter configuration 
ENV JUPYTER_CONFIG_PATH=/usr/local/etc/jupyter

RUN mkdir -p /usr/local/etc/jupyter
COPY docker/jupyterlab-overrides.json /usr/local/etc/jupyter/overrides.json
COPY docker/jupyter_server_config.py  /usr/local/etc/jupyter/jupyter_server_config.py
RUN chmod 644 /usr/local/etc/jupyter/overrides.json \
              /usr/local/etc/jupyter/jupyter_server_config.py

# Deploy overrides.json into the JupyterLab application-settings directory.
# sys.prefix resolves to the LSST stack's Python prefix at build time.
RUN /bin/bash -c " \
    source /opt/lsst/software/stack/loadLSST.bash \
    && setup lsst_distrib \
    && SETTINGS_DIR=\$(python3 -c \"import sys; print(f'{sys.prefix}/share/jupyter/lab/settings')\") \
    && mkdir -p \"\$SETTINGS_DIR\" \
    && cp /usr/local/etc/jupyter/overrides.json \"\$SETTINGS_DIR/overrides.json\" \
    && chmod 644 \"\$SETTINGS_DIR/overrides.json\""

# ── User-level JupyterLab settings ───────────────────────────────────────────
# User settings take priority over overrides.json 
# -- suppress restart-confirmation dialogs, news popups, session restore, etc.
RUN mkdir -p \
    /home/jupyter/.local/share/jupyter/lab/user-settings/@jupyterlab/apputils-extension \
    /home/jupyter/.local/share/jupyter/lab/user-settings/@jupyterlab/notebook-extension
COPY docker/user-settings/@jupyterlab/apputils-extension/notification.jupyterlab-settings \
     /home/jupyter/.local/share/jupyter/lab/user-settings/@jupyterlab/apputils-extension/notification.jupyterlab-settings
COPY docker/user-settings/@jupyterlab/apputils-extension/sessionDialogs.jupyterlab-settings \
     /home/jupyter/.local/share/jupyter/lab/user-settings/@jupyterlab/apputils-extension/sessionDialogs.jupyterlab-settings
RUN chown -R jupyter:jupyter /home/jupyter/.local

# Workspace 
RUN mkdir -p /home/jupyter/workspace/notebooks \
    && chown -R jupyter:jupyter /home/jupyter/workspace

WORKDIR /home/jupyter/workspace

# Copy project files
COPY --chown=jupyter:jupyter . .

# Entrypoint
# Use explicit bash invocation to avoid execute-bit permission issues that can
# occur on some host filesystems / Docker Desktop versions (exit code 126).
COPY docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod 755 /usr/local/bin/docker-entrypoint.sh

EXPOSE 8888

USER jupyter

ENTRYPOINT ["/bin/bash", "/usr/local/bin/docker-entrypoint.sh"]
CMD ["jupyter", "lab", \
     "--ip=0.0.0.0", \
     "--port=8888", \
     "--no-browser", \
     "--notebook-dir=/home/jupyter/workspace", \
     "--ServerApp.token=''", \
     "--ServerApp.password=''"]
