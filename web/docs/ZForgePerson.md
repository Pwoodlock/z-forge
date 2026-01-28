# Z-Forge Person

Defines an additional person (Person 2 or Person 3) to connect to the main Prompt Builder node.

## Overview

When your scene includes multiple people, use Z-Forge Person nodes to define Person 2 and Person 3. Each Person node provides the same attribute fields as Person 1 in the main node.

## Connection

1. Add a **Z-Forge Person** node to your workflow
2. Connect its `person` output to:
   - `person_2` input on the main Prompt Builder, OR
   - `person_3` input on the main Prompt Builder
3. Set **people** to "2" or "3" on the main Prompt Builder

The main node will include this person's data in the generated YAML variables.

## Genre Setting

The **genre** dropdown switches between realistic ethnicities and fantasy races in the ethnicity dropdown.

| Genre | Ethnicity Options |
|-------|-------------------|
| `realistic` | Real-world ethnicities (Japanese, German, Nigerian, etc.) |
| `fantasy` | Fantasy races (elf, dwarf, tiefling, dragonborn, etc.) |

**Best Practice:** Match the genre setting with your main Prompt Builder's genre setting for consistency.

## Reset and Randomize

### Reset
Clears all fields back to empty/default values. The toggle auto-disables after execution.

### Randomize
Generates random values for all 17 person attributes. When enabled:
- Widget values are ignored
- New random values are generated each execution
- Widget fields update to show the randomized values

**Note:** The main node's **Randomize All People** toggle will override this node's randomize setting, generating new random values for all connected people.

## Person Attributes

### Identity
| Field | Description |
|-------|-------------|
| `age` | Age number (25) or description (early 30s, mid-50s) |
| `gender` | Select: female, male, non-binary, or custom |
| `ethnicity` | Ethnicity (realistic) or Race (fantasy) - dropdown filters by genre |

### Physical Attributes
| Field | Description |
|-------|-------------|
| `body_type` | Select from presets or choose "custom" |
| `body_type_custom` | Your custom body description (when body_type is "custom") |
| `hair` | Color, length, and style |
| `face` | Facial structure and features |
| `skin_texture` | Skin surface quality (smooth, weathered, matte, etc.) |
| `skin_details` | Freckles, moles, tattoos, scars, stretch marks |
| `extras` | Additional details: glasses, beard, piercings |

### Expression & Pose
| Field | Description |
|-------|-------------|
| `expression` | Emotional expression and mood |
| `gaze` | Where they're looking (direct at camera, off-camera left, etc.) |
| `hands` | Hand position and activity |
| `pose` | Body position and stance |

### Clothing
| Field | Description |
|-------|-------------|
| `outfit` | Complete clothing description (multiline) |
| `accessories` | Jewelry, watches, etc. |
| `footwear` | Shoes if visible |

## Output

| Output | Type | Description |
|--------|------|-------------|
| `person` | ZFORGE_PERSON | JSON-encoded person data for the main node |

The output is a custom type that only connects to the main Prompt Builder's `person_2` and `person_3` inputs.

## Status Passthrough

The Person node includes status information in its output that the main Prompt Builder displays:

- **[RESET]** - Fields were cleared
- **[RANDOMIZED]** - Shows key randomized values (age, gender, ethnicity, body, expression)
- **[MANUAL] X/17 fields set** - Shows how many fields you've filled

This status appears in the main node's `status` output prefixed with `[Person 2]` or `[Person 3]`.

## Tips

- **Quick character generation**: Toggle Randomize, queue the workflow, then toggle off to keep the generated values for tweaking
- **Consistent characters**: Fill in key attributes manually and leave others empty for the LLM to interpret
- **Master randomize**: Use the main node's **Randomize All People** to regenerate all characters at once
