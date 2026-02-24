# EDUCADO_2026

This directory provides a Docker container to run a JuypterLab instance with the LSST Science Pipelines installed to run the educado tutorials 

## Setting up the jupyterlab instance using Dcocker

1. Install and start Docker. If updates are avalable, install them.

2. Start the Jupyterlab server
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

5. Using the AI extension in JupyterLab

The JupyterLab AI extension (`jupyter-ai`) is pre-installed in the Docker image. It gives you a chat panel and AI-powered cell completions inside JupyterLab, backed by an LLM of your choosing.
For this example, we will use Anthropic's Claude

### 5.1 Get an Anthropic API key

1. Go to [https://console.anthropic.com](https://console.anthropic.com) and sign in.
2. In the left sidebar, click **API Keys**.
3. Click **Create Key**, give it a name, and copy the key (it starts with `sk-ant-`).
   > You can only see the key once — save it somewhere safe.

### 5.2 Set the key before starting Docker

In your terminal, export the key into your shell environment before running `docker compose`:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
docker compose up --build 2>&1
 ```

To avoid doing this every session, add the export line to your shell profile:

```bash
echo 'export ANTHROPIC_API_KEY=sk-ant-...' >> ~/.zshrc   # or ~/.bash_profile
```

The `docker-compose.yml` is already configured to forward this variable into the container automatically.

### 5.3 Open the AI chat panel in JupyterLab

1. Open JupyterLab at [http://localhost:8888](http://localhost:8888).
2. Look for the **two-circle chat icon** (◎) in the left sidebar — click it to open the Jupyter AI panel.
3. On first use, click the **settings cog** at the top of the panel and select:
   - **Language model:** `Anthropic` → choose a model from the dropdown.
   - If the model you want (e.g. `claude-opus-4-6`) does not appear in the list, type the model ID directly into the model field — jupyter-ai accepts custom model strings even when they are not yet in its built-in list.
   - Paste your API key if prompted (it reads from the `ANTHROPIC_API_KEY` environment variable automatically in most cases).
4. Type a question in the chat box and press Enter.

### 5.4 Use the `%%ai` magic in a notebook cell

You can also call Claude directly from a notebook cell using the `%%ai` cell magic:

```python
%%ai anthropic:claude-opus-4-6
Explain what étendue means for a survey telescope in two sentences.
```

The result is rendered as formatted output below the cell — useful for explanations, code generation, and debugging inline with your work.
