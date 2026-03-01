# EDUCADO_2026
Lectures on Rubin and LSST for the EDUCADO 2026 school


## Setting up the JupyterLab instance

1. Install and start Docker. If updates are available, install them.

2. Start the JupyterLab server:
```bash
docker compose up --build
```
> `--build` rebuilds the image from the Dockerfile each time, so any changes to `Dockerfile` or `requirements.txt` are picked up. Omit it on subsequent runs if nothing has changed.

3. Open [http://localhost:8888](http://localhost:8888) in a browser (or Cmd+click in Cursor) to access JupyterLab.

---

## Using the AI extension in JupyterLab

The JupyterLab AI extension (`jupyter-ai`) is pre-installed in the Docker image. It provides a chat panel and AI-powered cell completions, backed by an LLM of your choosing. This guide uses Anthropic's Claude.

### Get an Anthropic API key

1. Go to [https://console.anthropic.com](https://console.anthropic.com) and sign in.
2. In the left sidebar, click **API Keys**.
3. Click **Create Key**, give it a name, and copy the key (it starts with `sk-ant-`).
   > You can only see the key once — save it somewhere safe.

### Set the key before starting Docker

Export the key into your shell environment before running `docker compose`:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
docker compose up --build
```

To avoid doing this every session, add the export line to your shell profile:

```bash
echo 'export ANTHROPIC_API_KEY=sk-ant-...' >> ~/.zshrc   # or ~/.bash_profile
```

The `docker-compose.yml` is already configured to forward this variable into the container automatically.

### Open the AI chat panel in JupyterLab

1. Open JupyterLab at [http://localhost:8888](http://localhost:8888).
2. Click the **two-circle chat icon** (◎) in the left sidebar.
3. On first use, click the **settings cog** and select:
   - **Language model:** `Anthropic` → choose a model from the dropdown.
   - If the model you want (e.g. `claude-opus-4-6`) is not listed, type the model ID directly — jupyter-ai accepts custom model strings.
   - Paste your API key if prompted (it reads `ANTHROPIC_API_KEY` from the environment automatically in most cases).
4. Type a question in the chat box and press Enter.

### Use the `%%ai` magic in a notebook cell

You can call Claude directly from a notebook cell:

```python
%%ai anthropic:claude-opus-4-6
Explain what étendue means for a survey telescope in two sentences.
```

The result is rendered as formatted output below the cell — useful for explanations, code generation, and debugging inline with your work.
