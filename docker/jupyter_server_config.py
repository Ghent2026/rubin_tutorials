# jupyter_server_config.py
#
# Patches the jupyter-ai Anthropic provider to include Claude 4.x models
# that may not yet be in jupyter-ai's built-in model list.
# This file is read automatically by Jupyter at server startup.

def _patch_anthropic_models():
    claude4_models = [
        "claude-opus-4-6",
        "claude-sonnet-4-6",
        "claude-haiku-4-6",
        "claude-opus-4-5-20251101",
        "claude-sonnet-4-5-20250929",
        "claude-haiku-4-5-20251001",
    ]
    try:
        from jupyter_ai_magics import providers
        provider = getattr(providers, "AnthropicProvider", None)
        if provider is not None:
            existing = list(provider.models)
            combined = list(dict.fromkeys(claude4_models + existing))
            provider.models = combined
    except Exception:
        pass  # silently skip if jupyter-ai is not installed or API changes

_patch_anthropic_models()
