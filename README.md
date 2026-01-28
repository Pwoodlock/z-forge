# Z-Forge

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> ⚠️ **BETA** - Early release. Features may change. Feedback welcome.

Structured Prompt Compiler for ComfyUI - Build consistent image generation prompts using the v3 variable system.

## Requirements

**Z-Forge requires an LLM to expand prompts.** Choose one:

| Option | Description |
|--------|-------------|
| **LM Studio (Local)** | Free, runs on your machine. Download from [lmstudio.ai](https://lmstudio.ai) and load a model. |
| **External LLM Node** | Connect Z-Forge outputs to any ComfyUI LLM node (OpenAI, Ollama, etc.) |

Without an LLM, Z-Forge outputs structured YAML variables only - not finished image prompts.

## Compatibility

**Designed for:** Z Image Turbo

Z-Forge is developed and tested specifically with Z Image Turbo. Compatibility with other prompt-based models (Flux, SDXL, etc.) is not guaranteed and may vary. No support is provided for other image generators.

## Installation

### Manual Installation
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/Pwoodlock/z-forge
```
Restart ComfyUI after cloning.

### Optional: LM Studio Integration
```bash
pip install lmstudio
```

## Nodes

| Node | Description |
|------|-------------|
| **Z-Forge Prompt Builder** | Main node with Person 1, Scene, Composition settings |
| **Z-Forge Person** | Additional person node (connect to main node for Person 2/3) |
| **Z-Forge LM Studio** | LM Studio connection and generation settings |

## System Prompt Templates

Z-Forge includes system prompt templates optimized for Z Image Turbo:

| Template | Description |
|----------|-------------|
| `v3_system_prompt` | Realistic/cinematic photography style |
| `v3_fantasy_system_prompt` | Fantasy illustration style with race presets |

Select templates in the **Z-Forge LM Studio** node. Add custom templates by placing `.md` files in the `system_prompts/` folder.

## Features

- **Widget Mode**: GUI inputs for all prompt variables
- **YAML Mode**: Raw YAML passthrough for advanced users
- **Randomization**: Generate random person/scene data with toggles
- **External Mode**: Output YAML + instructions for use with other LLM nodes
- **Internal Mode**: Built-in LM Studio integration

## Usage

### Basic Workflow
1. Add "Z-Forge Prompt Builder" to your workflow
2. Configure Person 1 and Scene fields
3. Connect outputs to your image generation pipeline

### Multi-Person Scenes
1. Add "Z-Forge Person" node(s)
2. Connect to `person_2` / `person_3` inputs
3. Set `people` count and add `interaction`

### LM Studio Integration
1. Add "Z-Forge LM Studio" node
2. Connect to Prompt Builder's `llm_config` input
3. Set Prompt Builder's `llm_mode` to "Internal (LM Studio)"
4. Ensure LM Studio is running with a model loaded

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check .
```

## Disclaimer

This software is provided "as is" without warranty of any kind. See the [LICENSE](LICENSE) file for full terms. The author is not liable for any damages or issues arising from the use of this software.

## License

[MIT License](LICENSE) - Copyright (c) 2026 Patrick Woodlock

You are free to use, modify, and distribute this software, provided the copyright notice and license are included in all copies.
