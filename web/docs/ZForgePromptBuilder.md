# Z-Forge Prompt Builder

The main node for building structured prompts from GUI inputs with optional LLM expansion.

## Overview

Z-Forge Prompt Builder compiles your visual inputs into structured YAML variables that an LLM can expand into flowing image prompts. It supports up to 3 people, scene settings, and composition controls.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Z-Forge Prompt Builder                       │
├─────────────────────────────────────────────────────────────────┤
│  [Widget Mode]          [YAML Mode]                             │
│       │                      │                                  │
│       ▼                      ▼                                  │
│  ┌─────────┐           ┌──────────┐                             │
│  │ Person 1│           │yaml_input│                             │
│  │ Scene   │           └────┬─────┘                             │
│  │ Compose │                │                                   │
│  └────┬────┘                │                                   │
│       │                     │                                   │
│       └──────────┬──────────┘                                   │
│                  ▼                                              │
│         ┌───────────────┐                                       │
│         │  YAML Output  │──────────────────┐                    │
│         └───────────────┘                  │                    │
│                                            ▼                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ [External Mode]              [Internal Mode]             │   │
│  │      │                             │                     │   │
│  │      ▼                             ▼                     │   │
│  │ variables ────► Other LLM    LM Studio call              │   │
│  │ llm_instructions  Node       (via LLM Config)            │   │
│  │                                    │                     │   │
│  │                                    ▼                     │   │
│  │                              image_prompt                │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

Optional connections:
  [Z-Forge Person] ──► person_2 / person_3
  [Z-Forge LM Studio] ──► llm_config
```

## Input Modes

### Widget Mode (Default)
Use the GUI fields to define your scene. Each field maps to a structured variable that the LLM understands.

### YAML Mode
Bypass the GUI and paste raw YAML directly into the `yaml_input` field. Useful for:
- Importing previously generated prompts
- Fine-tuning specific variables
- Working with external tools

## LLM Modes

### External (Output Only)
Outputs the compiled `variables` and `llm_instructions` for use with other LLM nodes in your workflow (e.g., Florence, LLaVA, or external API nodes).

**Connect:**
- `variables` → Your LLM node's prompt/input
- `llm_instructions` → Your LLM node's system prompt

### Internal (LM Studio)
Calls LM Studio directly for prompt expansion. Requires:
1. LM Studio running with server enabled (default: `127.0.0.1:1234`)
2. A model loaded in LM Studio
3. Optional: Connect a **Z-Forge LM Studio** node for custom settings

## Genre Setting

The **genre** dropdown switches between realistic ethnicities and fantasy races in the ethnicity dropdown.

| Genre | Ethnicity Options |
|-------|-------------------|
| `realistic` | Real-world ethnicities (Japanese, German, Nigerian, etc.) |
| `fantasy` | Fantasy races (elf, dwarf, tiefling, dragonborn, etc.) |

**Best Practice:** Match the genre setting with your LM Studio template selection for a cohesive experience. If using the fantasy template in LM Studio, set genre to "fantasy" here.

When you switch genres:
- The ethnicity dropdown automatically updates to show relevant options
- If your current selection is invalid for the new genre, it resets to "NA"
- Randomization uses genre-appropriate options

## Master Settings

| Setting | Options | Description |
|---------|---------|-------------|
| `people` | 1, 2, 3 | Number of people in the scene. Connect Person nodes for 2+ |
| `aspect` | portrait, landscape, square | Aspect ratio hint passed to the LLM |

## Reset and Randomization

### Reset All
Clears all Person 1 and Scene fields back to empty/default values. Toggle auto-disables after execution.

### Randomize All People
Master toggle that randomizes:
- Person 1 (in this node)
- Person 2 and Person 3 (in connected Person nodes)

### Randomize Person 1
Randomizes only Person 1 fields in this node. Does not affect connected Person nodes.

### Randomize Scene
Generates random values for: location, time, weather, atmosphere, lighting, framing, and camera angle.

## Person 1 Fields

### Identity
| Field | Description |
|-------|-------------|
| `age` | Age number (25) or description (early 30s) |
| `gender` | Select: female, male, non-binary, or custom |
| `ethnicity` | Ethnicity (realistic) or Race (fantasy) - dropdown filters by genre |

### Physical Attributes
| Field | Description |
|-------|-------------|
| `body_type` | Select from presets or choose "custom" |
| `body_type_custom` | Custom body description (when body_type is "custom") |
| `hair` | Color, length, and style |
| `face` | Facial structure and features |
| `skin_texture` | Skin surface quality |
| `skin_details` | Freckles, moles, tattoos, scars |
| `extras` | Additional details (glasses, beard, etc.) |

### Expression & Pose
| Field | Description |
|-------|-------------|
| `expression` | Emotional expression |
| `gaze` | Where they're looking |
| `hands` | Hand position and activity |
| `pose` | Body position and stance |

### Clothing
| Field | Description |
|-------|-------------|
| `outfit` | Main clothing description (multiline) |
| `accessories` | Jewelry, watches, etc. |
| `footwear` | Shoes if visible |

## Scene Fields

| Field | Description |
|-------|-------------|
| `location` | Where the scene takes place |
| `time` | Time of day (morning, noon, evening, etc.) |
| `weather` | Weather conditions |
| `atmosphere` | Overall mood and feeling |
| `props` | Objects in the scene |
| `background` | Background description |
| `era` | Time period (1920s, futuristic, etc.) |
| `action` | What's happening in the scene |
| `story` | Narrative context |
| `lighting` | Lighting description |

## Composition Fields

| Field | Description |
|-------|-------------|
| `framing` | Shot type (close-up, medium, full body, etc.) |
| `camera_angle` | Camera perspective (eye level, low angle, etc.) |
| `interaction` | How multiple people interact (multiline, 2+ people only) |

## Outputs

| Output | Description |
|--------|-------------|
| `variables` | YAML-formatted prompt variables |
| `llm_instructions` | System prompt for the LLM |
| `image_prompt` | Expanded prompt (Internal mode only, empty in External mode) |
| `status` | Debug information and generation status |

## Optional Inputs

### yaml_input
Raw YAML text input, active only in **YAML Mode**. Paste complete YAML variable blocks here to bypass widget entry entirely.

### system_prompt_override
Replace the default LLM expansion instructions with your own system prompt. Takes priority over:
- The template selected in Z-Forge LM Studio
- The built-in v3 system prompt

Use this for specialized prompt expansion styles or to experiment with different instruction sets.

## Multi-Person Workflows

For scenes with 2 or 3 people:

1. Set **people** to "2" or "3"
2. Add **Z-Forge Person** nodes for Person 2/3
3. Connect their `person` output to `person_2` / `person_3` inputs
4. Use the **interaction** field to describe how they relate

The main node handles Person 1. Connected Person nodes provide data for additional people.

## Tips

- **Quick variations**: Toggle Randomize, queue, toggle off - widgets update with new values you can tweak
- **Template override**: Use `system_prompt_override` to replace the default expansion instructions
- **Config node**: Connect **Z-Forge LM Studio** for model selection and generation parameters
- **Check status**: The `status` output shows randomized values, connected nodes, and LLM activity
