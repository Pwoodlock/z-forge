# Z-Forge LM Studio

Configure LM Studio connection settings and generation parameters for Internal mode prompt expansion.

## Overview

Z-Forge LLM Config provides centralized control over:
- System prompt template selection
- LM Studio server connection
- Model selection
- Generation parameters (temperature, tokens, sampling)

Connect this node to the main Prompt Builder to customize how prompts are expanded in Internal mode.

## System Prompt Template

The `system_prompt_template` dropdown lists all `.md` files found in the `system_prompts/` folder within Z-Forge.

**Default:** `v3_system_prompt` - Optimized instructions for expanding YAML variables into cinematic image prompts.

**Custom templates:** Add your own `.md` files to `system_prompts/` and they'll appear in the dropdown after restarting ComfyUI.

## LM Studio Connection

### Server Settings
| Setting | Default | Description |
|---------|---------|-------------|
| `lm_server_host` | 127.0.0.1 | LM Studio server address |
| `lm_server_port` | 1234 | LM Studio server port |

These match LM Studio's default local server settings. Change them if you're running LM Studio on a different machine or port.

### Test Connection
Toggle `test_connection` to verify Z-Forge can reach your LM Studio server. The status will show:
- **Success** - Server is reachable and responding
- **Failed** - Connection refused or server not running

### Refresh Models
Toggle `refresh_models` to fetch the current list of loaded models from LM Studio. This updates the `model_selection` dropdown.

## Model Selection

### Using the Dropdown
The `model_selection` dropdown shows:
1. **>> Custom Model <<** - Use the `custom_model_name` field (or currently loaded model if empty)
2. **Cached models** - Models fetched from LM Studio (after toggling `refresh_models`)

### Custom Model Name
When `model_selection` is set to ">> Custom Model <<":
- **Leave empty** → Uses whatever model is currently loaded in LM Studio
- **Enter a model ID** → Requests that specific model by name

This is useful for:
- Using the currently loaded model without knowing its name
- Specifying a model before it appears in the dropdown
- Requesting models not yet cached

## Generation Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `temperature` | 0.45 | 0.0 - 2.0 | Creativity level. Lower = more focused, higher = more varied |
| `max_tokens` | 512 | 64 - 4096 | Maximum output length |
| `top_p` | 1.0 | 0.0 - 1.0 | Nucleus sampling threshold (1.0 = disabled) |
| `top_k` | 0 | 0 - 500 | Top-K sampling (0 = disabled) |
| `repeat_penalty` | 1.0 | 0.0 - 2.0 | Repetition penalty (1.0 = none) |
| `unload_llm` | True | - | Unload model after generation to free VRAM |
| `seed` | -1 | -1 to 2147483647 | Random seed for reproducibility (-1 = random each time) |

### Recommended Settings

**For consistent prompts:**
- temperature: 0.3 - 0.5
- top_p: 1.0
- top_k: 0

**For creative variation:**
- temperature: 0.7 - 1.0
- top_p: 0.9
- repeat_penalty: 1.1

### Unload LLM
When enabled (default), the model is unloaded from LM Studio after each generation. This frees VRAM for image generation but means the model reloads on the next prompt expansion.

Disable if you're doing multiple prompt generations in sequence and have sufficient VRAM.

### Seed
The `seed` parameter helps with reproducibility:
- **-1** (default): Random seed each time, different outputs
- **Any positive number**: Attempts to reproduce similar outputs

**Important:** LLM seeds are less reliable than image generation seeds. Even with the same seed, you may get slightly different results due to:
- GPU floating-point non-determinism
- Model quantization variations
- Different batch sizes

Use it as a "helps sometimes" feature rather than a guarantee. If you find a prompt you like, save the actual text output rather than relying on the seed.

## Output

| Output | Type | Description |
|--------|------|-------------|
| `llm_config` | ZFORGE_LLM_CONFIG | JSON-encoded configuration for the main node |

Connect this to the main Prompt Builder's `llm_config` input.

## Usage Workflow

1. **Set up LM Studio**
   - Start LM Studio and enable the local server
   - Load your preferred model

2. **Configure this node**
   - Toggle `test_connection` to verify connectivity
   - Toggle `refresh_models` to populate the model dropdown
   - Select your model or use "(Use currently loaded)"
   - Adjust generation parameters if needed

3. **Connect to main node**
   - Connect `llm_config` output to Prompt Builder's `llm_config` input
   - Set Prompt Builder's `llm_mode` to "Internal (LM Studio)"

4. **Generate**
   - Queue the workflow
   - Check the Prompt Builder's `status` output for generation details

## Tips

- **No config node?** The main Prompt Builder uses sensible defaults if no config node is connected
- **Template not appearing?** Restart ComfyUI after adding new `.md` files to `system_prompts/`
- **Model list empty?** Make sure LM Studio is running and toggle `refresh_models`
- **Out of VRAM?** Keep `unload_llm` enabled to free memory for image generation
