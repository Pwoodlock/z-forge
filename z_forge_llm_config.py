"""
Z-Forge LLM Config Node
Separate node for LM Studio connection and generation settings.

This node outputs a ZFORGE_LLM_CONFIG that can be connected to the
main Z-Forge Prompt Builder node for Internal mode LLM generation.
"""
import json
import os

from .model_fetcher import (
    CUSTOM_MODEL_OPTION,
    get_model_choices,
    refresh_model_cache,
    test_connection,
)

# System prompts directory
_SYSTEM_PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "system_prompts")

# Cache for system prompt templates
_cached_templates: list[str] = []


def get_system_prompt_templates() -> list[str]:
    """
    Scan system_prompts directory for .md files.

    Returns:
        List of template names (without .md extension)
    """
    global _cached_templates

    if not os.path.isdir(_SYSTEM_PROMPTS_DIR):
        return ["v3_system_prompt"]

    templates = []
    try:
        for filename in os.listdir(_SYSTEM_PROMPTS_DIR):
            if filename.endswith(".md"):
                # Remove .md extension for display
                name = filename[:-3]
                templates.append(name)
    except OSError:
        pass

    if not templates:
        templates = ["v3_system_prompt"]

    _cached_templates = sorted(templates)
    return _cached_templates


def load_system_prompt(template_name: str) -> str:
    """
    Load a system prompt template by name.

    Args:
        template_name: Template name (without .md extension)

    Returns:
        Template content or error message
    """
    filepath = os.path.join(_SYSTEM_PROMPTS_DIR, f"{template_name}.md")

    try:
        with open(filepath, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"[ERROR] Template not found: {template_name}.md"
    except OSError as e:
        return f"[ERROR] Failed to load template: {e}"


class ZForgeLLMConfig:
    """
    LLM Configuration node for Z-Forge.

    Provides LM Studio connection settings, generation parameters,
    and system prompt template selection.
    """

    CATEGORY = "Z-Forge"
    RETURN_TYPES = ("ZFORGE_LLM_CONFIG",)
    RETURN_NAMES = ("llm_config",)
    FUNCTION = "build_config"

    @classmethod
    def INPUT_TYPES(cls):
        model_choices = get_model_choices()
        template_choices = get_system_prompt_templates()

        return {
            "required": {
                # ═══════════════════════════════════════════════════════════════
                #                     SYSTEM PROMPT TEMPLATE
                # ═══════════════════════════════════════════════════════════════
                "system_prompt_template": (
                    template_choices,
                    {
                        "default": template_choices[0] if template_choices else "v3_system_prompt",
                        "tooltip": "Select a system prompt template from system_prompts/ folder",
                    },
                ),
                # ═══════════════════════════════════════════════════════════════
                #                        LM STUDIO CONNECTION
                # ═══════════════════════════════════════════════════════════════
                "lm_server_host": (
                    "STRING",
                    {
                        "default": "127.0.0.1",
                        "tooltip": "LM Studio server host address",
                    },
                ),
                "lm_server_port": (
                    "INT",
                    {
                        "default": 1234,
                        "min": 1,
                        "max": 65535,
                        "tooltip": "LM Studio server port",
                    },
                ),
                "test_connection": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Test connection to LM Studio server",
                    },
                ),
                "refresh_models": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Refresh the model list from server",
                    },
                ),
                # ═══════════════════════════════════════════════════════════════
                #                          MODEL SELECTION
                # ═══════════════════════════════════════════════════════════════
                "model_selection": (
                    model_choices,
                    {
                        "tooltip": "Select a model or choose Custom to enter manually",
                    },
                ),
                "custom_model_name": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": "Custom model name (used if Custom Model selected)",
                    },
                ),
                # ═══════════════════════════════════════════════════════════════
                #                      GENERATION PARAMETERS
                # ═══════════════════════════════════════════════════════════════
                "temperature": (
                    "FLOAT",
                    {
                        "default": 0.45,
                        "min": 0.0,
                        "max": 2.0,
                        "step": 0.05,
                        "tooltip": "Generation temperature (0=deterministic, higher=creative)",
                    },
                ),
                "max_tokens": (
                    "INT",
                    {
                        "default": 512,
                        "min": 64,
                        "max": 4096,
                        "step": 64,
                        "tooltip": "Maximum tokens to generate",
                    },
                ),
                "top_p": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.05,
                        "tooltip": "Nucleus sampling threshold",
                    },
                ),
                "top_k": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 500,
                        "tooltip": "Top-K sampling (0=disabled)",
                    },
                ),
                "repeat_penalty": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 0.0,
                        "max": 2.0,
                        "step": 0.05,
                        "tooltip": "Repetition penalty (1.0=none)",
                    },
                ),
                "unload_llm": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "Unload model after generation to free VRAM",
                    },
                ),
                # ═══════════════════════════════════════════════════════════════
                #                          SEED CONTROL
                # ═══════════════════════════════════════════════════════════════
                "seed": (
                    "INT",
                    {
                        "default": -1,
                        "min": -1,
                        "max": 2147483647,
                        "tooltip": "Random seed (-1 = random each time). Note: LLM seeds are less reliable than image seeds.",
                    },
                ),
            }
        }

    @classmethod
    def IS_CHANGED(cls, refresh_models, test_connection, **kwargs):
        """Force re-execution when refresh or test is requested."""
        if refresh_models or test_connection:
            import time

            return str(time.time())
        return ""

    def build_config(
        self,
        system_prompt_template: str,
        lm_server_host: str,
        lm_server_port: int,
        test_connection: bool,
        refresh_models: bool,
        model_selection: str,
        custom_model_name: str,
        temperature: float,
        max_tokens: int,
        top_p: float,
        top_k: int,
        repeat_penalty: float,
        unload_llm: bool,
        seed: int,
    ) -> tuple[str]:
        """
        Build the LLM configuration.

        Returns:
            Tuple containing JSON-encoded config string
        """
        status_lines = []
        server_url = f"http://{lm_server_host}:{lm_server_port}"

        # Load the selected system prompt template
        system_prompt = load_system_prompt(system_prompt_template)
        status_lines.append(f"Template: {system_prompt_template}")

        # Handle test connection request
        if test_connection:
            success, msg = test_connection_func(lm_server_host, lm_server_port)
            status_lines.append(f"Connection: {msg}")

        # Handle refresh models request
        if refresh_models:
            success, msg = refresh_model_cache(server_url)
            status_lines.append(f"Models: {msg}")

        # Determine which model to use
        if model_selection == CUSTOM_MODEL_OPTION:
            model = custom_model_name if custom_model_name.strip() else ""
        else:
            model = model_selection

        # Build config dictionary
        config = {
            "host": lm_server_host,
            "port": lm_server_port,
            "server_url": server_url,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "top_k": top_k,
            "repeat_penalty": repeat_penalty,
            "unload": unload_llm,
            "seed": seed,
            "system_prompt": system_prompt,
            "system_prompt_template": system_prompt_template,
            "status": "\n".join(status_lines) if status_lines else "Ready",
        }

        return (json.dumps(config),)


# Alias to avoid name collision with parameter
test_connection_func = test_connection


# Node registration
NODE_CLASS_MAPPINGS = {
    "ZForgeLLMConfig": ZForgeLLMConfig,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZForgeLLMConfig": "Z-Forge LM Studio",
}
