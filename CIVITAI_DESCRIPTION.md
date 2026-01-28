# Z-Forge - Structured Prompt Builder for ComfyUI

**GitHub:** https://github.com/Pwoodlock/z-forge

> ⚠️ **BETA RELEASE** - This is an early release. Features may change and bugs may exist. Feedback and bug reports welcome on GitHub.

> ⚡ **REQUIRES AN LLM** - Z-Forge needs a language model to expand prompts. Use [LM Studio](https://lmstudio.ai) (free, local) or connect to any external LLM node.

Stop writing prompts from scratch every time. Z-Forge gives you a structured system for building consistent, detailed image prompts with just a few clicks.

---

## What is Z-Forge?

Z-Forge is a ComfyUI custom node pack that transforms how you create prompts. Instead of typing long descriptions manually, you fill in structured fields (age, ethnicity, hair, outfit, location, lighting, etc.) and Z-Forge compiles them into cinematic image prompts.

**Two modes:**
- **Realistic** - Real-world ethnicities, modern/period clothing, natural locations
- **Fantasy** - Elves, dwarves, tieflings, medieval armor, mystical forests, and 220+ cinematic fantasy locations

---

**[UPLOAD YOUR SCREENSHOTS HERE USING CIVITAI'S IMAGE UPLOAD BUTTON]**

---

## Features

### Structured Character Building
Define every aspect of your character through organized fields:
- **Identity**: Age, gender, ethnicity/race
- **Physical**: Body type, hair, face, skin texture, skin details
- **Expression & Pose**: Emotion, gaze direction, hand position, body pose
- **Clothing**: Outfit, accessories, footwear

### Multi-Person Scenes
Build scenes with up to 3 characters. Each person gets their own complete set of attributes, plus interaction descriptions for how they relate to each other.

### Genre-Aware System
Switch between **Realistic** and **Fantasy** modes:
- Dropdown options change automatically based on genre
- Randomizer generates appropriate content for each mode
- Server-side validation prevents mismatched selections

### Powerful Randomization
- **Randomize Person**: Generate complete random characters with one toggle
- **Randomize Scene**: Random locations, weather, lighting, atmosphere
- **Randomize All**: Regenerate entire scenes instantly
- Widget values update to show what was generated

### Scene & Composition
- Location, time of day, weather, atmosphere
- Props, background, era, action, story context
- Framing (close-up to wide shot)
- Camera angle (eye level to bird's eye)

### LM Studio Integration (Optional)
Connect to a local LLM via LM Studio to automatically expand your structured variables into flowing prose. No API costs, runs entirely on your machine.

---

## Installation

### Manual Installation
```
cd ComfyUI/custom_nodes
git clone https://github.com/Pwoodlock/z-forge
```
Restart ComfyUI after cloning.

### Optional: LM Studio Integration
```
pip install lmstudio
```
Then install [LM Studio](https://lmstudio.ai/) and load a model.

---

## Included Nodes

| Node | Purpose |
|------|---------|
| **Z-Forge Prompt Builder** | Main node - Person 1, Scene, Composition, all controls |
| **Z-Forge Person** | Additional person data (connect for Person 2 or 3) |
| **Z-Forge LM Studio** | LLM connection settings and generation parameters |

---

## Quick Start

### Basic Single-Person Prompt
1. Add **Z-Forge Prompt Builder** to your workflow
2. Set genre (realistic/fantasy)
3. Fill in Person 1 fields (or toggle **Randomize Person 1**)
4. Fill in Scene fields (or toggle **Randomize Scene**)
5. Connect outputs to your image generation pipeline

### Multi-Person Scene
1. Add **Z-Forge Person** node(s)
2. Connect to `person_2` or `person_3` inputs on main node
3. Set **people** count to 2 or 3
4. Add **interaction** description

### With LM Studio (Local LLM)
1. Start LM Studio and load a model
2. Add **Z-Forge LM Studio** node
3. Connect to Prompt Builder's `llm_config` input
4. Set **llm_mode** to "Internal (LM Studio)"
5. The `image_prompt` output will contain expanded prose

---

## Fantasy Mode Highlights

220+ cinematic fantasy locations across categories:
- Ancient forests, mountains, ruins
- Elven cities, dwarven halls, Viking settlements
- Gothic cathedrals, Slavic villages, desert temples
- Jungle ruins, mystical seas, enchanted groves
- Celtic hillforts, Nordic turf farms, Mediterranean ruins
- Fortifications, harsh environments, industrial sites

Fantasy-appropriate randomization:
- Races: Elves, dwarves, halflings, orcs, tieflings, dragonborn, and more
- Outfits: Peasant garb, noble finery, battle armor, wizard robes
- Accessories: Amulets, circlets, belt pouches
- Footwear: Leather boots, elven shoes, armored greaves

---

## Requirements

- ComfyUI
- Python 3.10+
- **An LLM (required)** - One of the following:
  - **LM Studio** (recommended) - Free, local, no API costs. Download from [lmstudio.ai](https://lmstudio.ai), install `pip install lmstudio`, load a model.
  - **External LLM node** - Connect Z-Forge's `variables` and `llm_instructions` outputs to any ComfyUI LLM node (OpenAI, Ollama, Claude, etc.)

Without an LLM, Z-Forge outputs YAML variables only - not finished prompts.

---

## Links

- **GitHub**: https://github.com/Pwoodlock/z-forge
- **License**: MIT (free to use and modify)

---

*Built for creators who want consistency without sacrificing creativity.*
