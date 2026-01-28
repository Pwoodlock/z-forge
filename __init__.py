"""
Z-Forge - Structured Prompt Compiler for ComfyUI
Build structured prompts using the v3 variable system with LLM integration.

Nodes:
- Z-Forge Prompt Builder: Main node with Person 1, Scene, Composition settings
- Z-Forge Person: Separate node for Person 2/3 data (connect to main node)
- Z-Forge LLM Config: LM Studio connection and generation settings

Features:
- Widget Mode: GUI inputs for all variables
- YAML Mode: Raw YAML passthrough
- Randomize toggles: Generate random person/scene data
- Master Randomize: Randomizes all people at once
- External Mode: Output for use with other LLM nodes
- Internal Mode: Full LM Studio integration with separate config node
"""

from .z_image_prompt import NODE_CLASS_MAPPINGS as MAIN_MAPPINGS
from .z_image_prompt import NODE_DISPLAY_NAME_MAPPINGS as MAIN_DISPLAY_MAPPINGS
from .subject_node import NODE_CLASS_MAPPINGS as PERSON_MAPPINGS
from .subject_node import NODE_DISPLAY_NAME_MAPPINGS as PERSON_DISPLAY_MAPPINGS
from .z_forge_llm_config import NODE_CLASS_MAPPINGS as LLM_MAPPINGS
from .z_forge_llm_config import NODE_DISPLAY_NAME_MAPPINGS as LLM_DISPLAY_MAPPINGS

# Combine mappings
NODE_CLASS_MAPPINGS = {**MAIN_MAPPINGS, **PERSON_MAPPINGS, **LLM_MAPPINGS}
NODE_DISPLAY_NAME_MAPPINGS = {
    **MAIN_DISPLAY_MAPPINGS,
    **PERSON_DISPLAY_MAPPINGS,
    **LLM_DISPLAY_MAPPINGS,
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

# Web directory for custom JavaScript
WEB_DIRECTORY = "./web"

# Version info
__version__ = "0.0.3"

# Initialize model cache at startup (silent failure if LM Studio not running)
try:
    from .model_fetcher import initialize_model_cache
    initialize_model_cache()
except Exception:
    pass  # Don't fail startup if model fetching fails
