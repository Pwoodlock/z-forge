"""
Z-Forge Prompt Builder - Main Node
ComfyUI custom node for building structured prompts.

v0.0.3: LLM settings moved to separate ZForgeLLMConfig node.
"""
import json
import logging
import os
from typing import Any, Optional

from .presets import (
    ASPECTS,
    BODY_TYPES_ALL,
    CAMERA_ANGLES,
    ETHNICITIES_ALL,
    ETHNICITIES_FANTASY,
    ETHNICITIES_REALISTIC,
    EXPRESSION_HINTS,
    FRAMINGS,
    GENDERS,
    GENRES,
    POSE_HINTS,
    TIMES,
    WEATHERS,
)
from .randomizer import randomize_scene as generate_random_scene
from .randomizer import randomize_subject
from .yaml_builder import build_yaml_from_widgets

logger = logging.getLogger("ZForge")

# System prompts directory
_SYSTEM_PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "system_prompts")

# Load default system prompt at module load
_SYSTEM_PROMPT_PATH = os.path.join(_SYSTEM_PROMPTS_DIR, "v3_system_prompt.md")

try:
    with open(_SYSTEM_PROMPT_PATH, encoding="utf-8") as f:
        DEFAULT_SYSTEM_PROMPT = f.read()
except Exception as e:
    logger.error(f"Failed to load system prompt: {e}")
    DEFAULT_SYSTEM_PROMPT = (
        "You are a cinematic image prompt engineer. "
        "Expand the YAML variables into flowing prose."
    )

# Default LLM config values (used when no LLM Config node connected)
DEFAULT_LLM_CONFIG = {
    "host": "127.0.0.1",
    "port": 1234,
    "server_url": "http://127.0.0.1:1234",
    "model": "",  # Empty = use currently loaded model
    "temperature": 0.45,
    "max_tokens": 512,
    "top_p": 1.0,
    "top_k": 0,
    "repeat_penalty": 1.0,
    "unload": True,
    "seed": -1,  # -1 = random
}

# Mode options
INPUT_MODES = ["Widget Mode", "YAML Mode"]
LLM_MODES = ["External (Output Only)", "Internal (LM Studio)"]
PERSON_COUNTS = ["1", "2", "3"]


def validate_ethnicity_for_genre(ethnicity: str, genre: str) -> tuple[str, Optional[str]]:
    """
    Validate that ethnicity matches the selected genre.

    Args:
        ethnicity: The selected ethnicity/race value
        genre: "realistic" or "fantasy"

    Returns:
        Tuple of (validated_ethnicity, warning_message or None)
    """
    if not ethnicity or ethnicity == "NA" or ethnicity == "custom":
        return ethnicity, None

    if genre == "realistic":
        if ethnicity not in ETHNICITIES_REALISTIC:
            return "NA", f"[WARNING] '{ethnicity}' is a fantasy race, not valid in realistic mode. Reset to NA."
    elif genre == "fantasy":
        if ethnicity not in ETHNICITIES_FANTASY:
            return "NA", f"[WARNING] '{ethnicity}' is a real-world ethnicity, not valid in fantasy mode. Reset to NA."

    return ethnicity, None


def parse_person_input(person_json: Optional[str]) -> dict[str, Any]:
    """Parse person JSON from connected Person node."""
    if not person_json:
        return {}
    try:
        return json.loads(person_json)
    except (json.JSONDecodeError, TypeError):
        return {}


def parse_llm_config(config_json: Optional[str]) -> dict[str, Any]:
    """Parse LLM config JSON from connected LLM Config node."""
    if not config_json:
        return DEFAULT_LLM_CONFIG.copy()
    try:
        config = json.loads(config_json)
        # Merge with defaults for any missing keys
        result = DEFAULT_LLM_CONFIG.copy()
        result.update(config)
        return result
    except (json.JSONDecodeError, TypeError):
        return DEFAULT_LLM_CONFIG.copy()


def format_randomized_person(data: dict[str, Any], label: str) -> list:
    """Format randomized person data for status output."""
    lines = [f"[RANDOMIZED {label}]"]
    lines.append(f"  Age: {data.get('age', 'NA')}")
    lines.append(f"  Gender: {data.get('gender', 'NA')}")
    lines.append(f"  Ethnicity: {data.get('ethnicity', 'NA')}")
    lines.append(f"  Body: {data.get('body_type', 'NA')}")
    lines.append(f"  Hair: {data.get('hair', 'NA')}")
    lines.append(f"  Expression: {data.get('expression', 'NA')}")
    lines.append(f"  Gaze: {data.get('gaze', 'NA')}")
    lines.append(f"  Pose: {data.get('pose', 'NA')}")
    lines.append(f"  Outfit: {data.get('outfit', 'NA')}")
    return lines


class ZForgePromptBuilder:
    """
    Build Z-Forge prompts from structured variables.

    Supports GUI widget input, raw YAML input, and connected Person nodes.
    LLM settings are now in a separate ZForgeLLMConfig node.
    """

    CATEGORY = "Z-Forge"
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("variables", "llm_instructions", "image_prompt", "status")
    OUTPUT_NODE = True
    FUNCTION = "build_prompt"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # ═══════════════════════════════════════════════════════════════
                #                       MODE SELECTION
                # ═══════════════════════════════════════════════════════════════
                "input_mode": (
                    INPUT_MODES,
                    {
                        "default": "Widget Mode",
                        "tooltip": "Widget Mode: use GUI inputs. YAML Mode: paste raw YAML.",
                    },
                ),
                "llm_mode": (
                    LLM_MODES,
                    {
                        "default": "External (Output Only)",
                        "tooltip": (
                            "External: output for another LLM node. "
                            "Internal: call LM Studio directly."
                        ),
                    },
                ),
                "genre": (
                    GENRES,
                    {
                        "default": "realistic",
                        "tooltip": "Switches ethnicity options. Match with LM Studio template for best results.",
                    },
                ),
                # ═══════════════════════════════════════════════════════════════
                #                       MASTER SETTINGS
                # ═══════════════════════════════════════════════════════════════
                "people": (
                    PERSON_COUNTS,
                    {
                        "default": "1",
                        "tooltip": "Number of people (connect Person nodes for 2 or 3)",
                    },
                ),
                "aspect": (
                    ASPECTS,
                    {"default": "portrait", "tooltip": "Aspect ratio hint"},
                ),
                # ═══════════════════════════════════════════════════════════════
                #                      RESET & RANDOMIZE
                # ═══════════════════════════════════════════════════════════════
                "reset_all": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Clear all Person 1 and Scene fields to defaults",
                    },
                ),
                "randomize_all_people": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Master randomize: all people including connected nodes",
                    },
                ),
                "randomize_person_1": (
                    "BOOLEAN",
                    {"default": False, "tooltip": "Randomize Person 1 fields only"},
                ),
                "randomize_scene": (
                    "BOOLEAN",
                    {"default": False, "tooltip": "Randomize scene fields"},
                ),
                # ═══════════════════════════════════════════════════════════════
                #                          PERSON 1
                # ═══════════════════════════════════════════════════════════════
                "person_1_age": (
                    "STRING",
                    {"default": "", "tooltip": "Age: number (25) or description (early 30s)"},
                ),
                "person_1_gender": (
                    GENDERS,
                    {"default": "female", "tooltip": "Person 1 gender"},
                ),
                "person_1_ethnicity": (
                    ETHNICITIES_ALL,
                    {
                        "default": "NA",
                        "tooltip": "Ethnicity (realistic) or Race (fantasy). Dropdown filters by genre.",
                    },
                ),
                "person_1_body_type": (
                    BODY_TYPES_ALL,
                    {"default": "NA", "tooltip": "Body type preset"},
                ),
                "person_1_body_type_custom": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": "Enter custom body type here (only used when body_type dropdown is set to 'custom')",
                    },
                ),
                "person_1_hair": (
                    "STRING",
                    {"default": "", "tooltip": "Hair color, length, style"},
                ),
                "person_1_face": (
                    "STRING",
                    {"default": "", "tooltip": "Facial structure and features"},
                ),
                "person_1_expression": (
                    "STRING",
                    {"default": "", "tooltip": EXPRESSION_HINTS},
                ),
                "person_1_gaze": (
                    "STRING",
                    {"default": "", "tooltip": "Where they're looking"},
                ),
                "person_1_hands": (
                    "STRING",
                    {"default": "", "tooltip": "What the hands are doing"},
                ),
                "person_1_skin_texture": (
                    "STRING",
                    {"default": "", "tooltip": "Skin surface quality"},
                ),
                "person_1_skin_details": (
                    "STRING",
                    {"default": "", "tooltip": "Freckles, moles, tattoos, scars, etc."},
                ),
                "person_1_extras": (
                    "STRING",
                    {"default": "", "tooltip": "Additional details: glasses, beard, etc."},
                ),
                "person_1_outfit": (
                    "STRING",
                    {"default": "", "multiline": True, "tooltip": "Clothing description"},
                ),
                "person_1_accessories": (
                    "STRING",
                    {"default": "", "tooltip": "Jewelry, watches, etc."},
                ),
                "person_1_footwear": (
                    "STRING",
                    {"default": "", "tooltip": "Shoes if visible"},
                ),
                "person_1_pose": (
                    "STRING",
                    {"default": "", "tooltip": POSE_HINTS},
                ),
                # ═══════════════════════════════════════════════════════════════
                #                            SCENE
                # ═══════════════════════════════════════════════════════════════
                "location": (
                    "STRING",
                    {"default": "", "tooltip": "Scene location description"},
                ),
                "time": (TIMES, {"default": "NA", "tooltip": "Time of day"}),
                "weather": (WEATHERS, {"default": "NA", "tooltip": "Weather conditions"}),
                "atmosphere": (
                    "STRING",
                    {"default": "", "tooltip": "Overall mood and atmosphere"},
                ),
                "props": ("STRING", {"default": "", "tooltip": "Objects in the scene"}),
                "background": (
                    "STRING",
                    {"default": "", "tooltip": "Background description"},
                ),
                "era": ("STRING", {"default": "", "tooltip": "Time period or era"}),
                "action": (
                    "STRING",
                    {"default": "", "tooltip": "What's happening in the scene"},
                ),
                "story": ("STRING", {"default": "", "tooltip": "Narrative context"}),
                "lighting": (
                    "STRING",
                    {"default": "", "tooltip": "Lighting description"},
                ),
                # ═══════════════════════════════════════════════════════════════
                #                         COMPOSITION
                # ═══════════════════════════════════════════════════════════════
                "framing": (FRAMINGS, {"default": "NA", "tooltip": "Shot framing"}),
                "camera_angle": (
                    CAMERA_ANGLES,
                    {"default": "NA", "tooltip": "Camera angle"},
                ),
            },
            "optional": {
                # ═══════════════════════════════════════════════════════════════
                #                       CONNECTED NODES
                # ═══════════════════════════════════════════════════════════════
                "person_2": (
                    "ZFORGE_PERSON",
                    {"tooltip": "Connect a Z-Forge Person node for Person 2"},
                ),
                "person_3": (
                    "ZFORGE_PERSON",
                    {"tooltip": "Connect a Z-Forge Person node for Person 3"},
                ),
                "llm_config": (
                    "ZFORGE_LLM_CONFIG",
                    {
                        "tooltip": (
                            "Connect a Z-Forge LLM Config node for LM Studio settings. "
                            "If not connected, defaults are used for Internal mode."
                        )
                    },
                ),
                # ═══════════════════════════════════════════════════════════════
                #                          INTERACTION
                # ═══════════════════════════════════════════════════════════════
                "interaction": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "How people interact (only used when 2+ people)",
                    },
                ),
                # ═══════════════════════════════════════════════════════════════
                #                        YAML MODE INPUT
                # ═══════════════════════════════════════════════════════════════
                "yaml_input": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Raw YAML input (only active in YAML Mode)",
                    },
                ),
                # ═══════════════════════════════════════════════════════════════
                #                     SYSTEM PROMPT OVERRIDE
                # ═══════════════════════════════════════════════════════════════
                "system_prompt_override": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Replace default prompt expansion instructions",
                    },
                ),
            },
        }

    @classmethod
    def IS_CHANGED(cls, reset_all, randomize_all_people, randomize_person_1, randomize_scene, **kwargs):
        """Force re-execution when reset or randomize is True."""
        if reset_all or randomize_all_people or randomize_person_1 or randomize_scene:
            import time

            return str(time.time())
        return ""

    def _call_lm_studio(
        self,
        system_prompt: str,
        yaml_input: str,
        config: dict[str, Any],
    ) -> tuple[str, str]:
        """
        Call LM Studio for prompt expansion.

        Args:
            system_prompt: System prompt for the LLM
            yaml_input: YAML variables to expand
            config: LLM configuration dictionary

        Returns:
            Tuple of (expanded_prompt, status_info)
        """
        status_lines = []

        try:
            import lmstudio as lms
        except ImportError:
            return "", "[ERROR] lmstudio SDK not installed. Install with: pip install lmstudio"

        try:
            server_address = f"{config['host']}:{config['port']}"
            status_lines.append(f"[LLM] Connecting to {server_address}")

            model_id = config.get("model", "").strip() or None

            with lms.Client(server_address) as client:
                # Get model
                if model_id:
                    model = client.llm.model(model_id)
                    status_lines.append(f"[LLM] Using model: {model_id}")
                else:
                    model = client.llm.model()
                    status_lines.append("[LLM] Using currently loaded model")

                # Build chat
                chat = lms.Chat(system_prompt)
                chat.add_user_message(yaml_input)

                # Generation config
                gen_config = {
                    "temperature": config["temperature"],
                    "maxTokens": config["max_tokens"],
                    "contextOverflowPolicy": "truncateMiddle",
                }

                if config["top_p"] < 1.0:
                    gen_config["topPSampling"] = config["top_p"]
                if config["top_k"] > 0:
                    gen_config["topKSampling"] = config["top_k"]
                if config["repeat_penalty"] != 1.0:
                    gen_config["repeatPenalty"] = config["repeat_penalty"]

                # Add seed if specified (not -1)
                seed = config.get("seed", -1)
                if seed >= 0:
                    gen_config["seed"] = seed
                    status_lines.append(f"[LLM] Using seed: {seed}")

                status_lines.append(
                    f"[LLM] Generating: temp={config['temperature']}, "
                    f"max_tokens={config['max_tokens']}"
                )

                # Generate
                response = model.respond(chat, config=gen_config)
                result = str(response).strip()

                status_lines.append(f"[LLM] Generated {len(result)} characters")

                # Unload if requested
                if config.get("unload", True):
                    try:
                        model.unload()
                        status_lines.append("[LLM] Model unloaded")
                    except Exception as e:
                        status_lines.append(f"[WARNING] Unload failed: {e}")

                return result, "\n".join(status_lines)

        except Exception as e:
            status_lines.append(f"[ERROR] {type(e).__name__}: {e}")

            error_str = str(e).lower()
            if "connection" in error_str or "refused" in error_str:
                status_lines.append("[HINT] Ensure LM Studio is running with server enabled")
            elif "model" in error_str:
                status_lines.append("[HINT] Load a model in LM Studio first")

            return "", "\n".join(status_lines)

    def build_prompt(
        self,
        # Mode Selection
        input_mode: str,
        llm_mode: str,
        genre: str,
        # Master Settings
        people: str,
        aspect: str,
        # Reset & Randomize
        reset_all: bool,
        randomize_all_people: bool,
        randomize_person_1: bool,
        randomize_scene: bool,
        # Person 1
        person_1_age: str,
        person_1_gender: str,
        person_1_ethnicity: str,
        person_1_body_type: str,
        person_1_body_type_custom: str,
        person_1_hair: str,
        person_1_face: str,
        person_1_expression: str,
        person_1_gaze: str,
        person_1_hands: str,
        person_1_skin_texture: str,
        person_1_skin_details: str,
        person_1_extras: str,
        person_1_outfit: str,
        person_1_accessories: str,
        person_1_footwear: str,
        person_1_pose: str,
        # Scene
        location: str,
        time: str,
        weather: str,
        atmosphere: str,
        props: str,
        background: str,
        era: str,
        action: str,
        story: str,
        lighting: str,
        # Composition
        framing: str,
        camera_angle: str,
        # Optional
        person_2: Optional[str] = None,
        person_3: Optional[str] = None,
        llm_config: Optional[str] = None,
        interaction: str = "",
        yaml_input: str = "",
        system_prompt_override: str = "",
    ):
        """Build the prompt."""
        status_lines = []
        randomized_values = {}  # Track values for UI update

        # Handle reset - clear all Person 1 and Scene fields
        if reset_all:
            randomized_values = {
                "reset_all": False,  # Auto-toggle off
                "randomize_all_people": False,
                "randomize_person_1": False,
                "randomize_scene": False,
                # Person 1 defaults
                "person_1_age": "",
                "person_1_gender": "female",
                "person_1_ethnicity": "NA",
                "person_1_body_type": "NA",
                "person_1_body_type_custom": "",
                "person_1_hair": "",
                "person_1_face": "",
                "person_1_expression": "",
                "person_1_gaze": "",
                "person_1_hands": "",
                "person_1_skin_texture": "",
                "person_1_skin_details": "",
                "person_1_extras": "",
                "person_1_outfit": "",
                "person_1_accessories": "",
                "person_1_footwear": "",
                "person_1_pose": "",
                # Scene defaults
                "location": "",
                "time": "NA",
                "weather": "NA",
                "atmosphere": "",
                "props": "",
                "background": "",
                "era": "",
                "action": "",
                "story": "",
                "lighting": "",
                "framing": "NA",
                "camera_angle": "NA",
                "interaction": "",
            }
            status_lines.append("[RESET] All Person 1 and Scene fields cleared")
            # Return early with reset values
            return {
                "ui": {"randomized_values": [randomized_values]},
                "result": ("", "", "", "\n".join(status_lines)),
            }

        # Parse LLM config (uses defaults if not connected)
        config = parse_llm_config(llm_config)

        if llm_config:
            # Show config status if connected
            if config.get("status"):
                status_lines.append(f"[LLM Config] {config['status']}")
        else:
            status_lines.append("[LLM Config] Using defaults (no config node connected)")

        status_lines.append(f"[Genre] {genre}")

        # Validate Person 1 ethnicity against genre
        person_1_ethnicity, eth_warning = validate_ethnicity_for_genre(person_1_ethnicity, genre)
        if eth_warning:
            status_lines.append(eth_warning)

        # Determine system prompt (priority: override > config > default)
        if system_prompt_override.strip():
            system_prompt = system_prompt_override.strip()
            status_lines.append("[Prompt] Using override")
        elif config.get("system_prompt"):
            system_prompt = config["system_prompt"]
            template_name = config.get("system_prompt_template", "from config")
            status_lines.append(f"[Prompt] Using template: {template_name}")
        else:
            system_prompt = DEFAULT_SYSTEM_PROMPT
            status_lines.append("[Prompt] Using default v3")

        num_people = int(people)

        # Handle YAML mode
        if input_mode == "YAML Mode":
            yaml_output = yaml_input.strip()
            status_lines.append("[MODE] YAML Mode - passthrough")
        else:
            # Widget Mode
            status_lines.append("[MODE] Widget Mode - building YAML")

            # Determine if we should randomize Person 1
            should_randomize_p1 = randomize_all_people or randomize_person_1

            # Apply Person 1 randomization if enabled
            if should_randomize_p1:
                p1_data = randomize_subject(genre=genre)
                person_1_age = p1_data["age"]
                person_1_gender = p1_data["gender"]
                person_1_ethnicity = p1_data["ethnicity"]
                person_1_body_type = p1_data["body_type"]
                person_1_body_type_custom = p1_data["body_type_custom"]
                person_1_hair = p1_data["hair"]
                person_1_face = p1_data["face"]
                person_1_expression = p1_data["expression"]
                person_1_gaze = p1_data["gaze"]
                person_1_hands = p1_data["hands"]
                person_1_skin_texture = p1_data["skin_texture"]
                person_1_skin_details = p1_data["skin_details"]
                person_1_extras = p1_data["extras"]
                person_1_outfit = p1_data["outfit"]
                person_1_accessories = p1_data["accessories"]
                person_1_footwear = p1_data["footwear"]
                person_1_pose = p1_data["pose"]
                status_lines.extend(format_randomized_person(p1_data, "Person 1"))

                # Track for UI update
                randomized_values.update({
                    "person_1_age": person_1_age,
                    "person_1_gender": person_1_gender,
                    "person_1_ethnicity": person_1_ethnicity,
                    "person_1_body_type": person_1_body_type,
                    "person_1_hair": person_1_hair,
                    "person_1_face": person_1_face,
                    "person_1_expression": person_1_expression,
                    "person_1_gaze": person_1_gaze,
                    "person_1_hands": person_1_hands,
                    "person_1_skin_texture": person_1_skin_texture,
                    "person_1_skin_details": person_1_skin_details,
                    "person_1_extras": person_1_extras,
                    "person_1_outfit": person_1_outfit,
                    "person_1_accessories": person_1_accessories,
                    "person_1_footwear": person_1_footwear,
                    "person_1_pose": person_1_pose,
                })

            # Apply scene randomization if enabled
            if randomize_scene:
                scene_data = generate_random_scene(genre=genre)
                location = scene_data["location"]
                time = scene_data["time"]
                weather = scene_data["weather"]
                atmosphere = scene_data["atmosphere"]
                lighting = scene_data["lighting"]
                framing = scene_data["framing"]
                camera_angle = scene_data["camera_angle"]
                era = scene_data["era"]
                status_lines.append("[RANDOMIZED Scene]")
                status_lines.append(f"  Location: {location}")
                status_lines.append(f"  Time: {time}")
                status_lines.append(f"  Weather: {weather}")
                status_lines.append(f"  Atmosphere: {atmosphere}")
                status_lines.append(f"  Lighting: {lighting}")

                # Track for UI update
                randomized_values.update({
                    "location": location,
                    "time": time,
                    "weather": weather,
                    "atmosphere": atmosphere,
                    "lighting": lighting,
                    "framing": framing,
                    "camera_angle": camera_angle,
                    "era": era,
                })

            # Parse connected people
            p2_data = parse_person_input(person_2) if num_people >= 2 else {}
            p3_data = parse_person_input(person_3) if num_people >= 3 else {}

            # Validate connected Person ethnicities against main node's genre
            if p2_data and p2_data.get("ethnicity"):
                p2_eth, p2_eth_warning = validate_ethnicity_for_genre(p2_data["ethnicity"], genre)
                if p2_eth_warning:
                    status_lines.append(f"[Person 2] {p2_eth_warning}")
                p2_data["ethnicity"] = p2_eth

            if p3_data and p3_data.get("ethnicity"):
                p3_eth, p3_eth_warning = validate_ethnicity_for_genre(p3_data["ethnicity"], genre)
                if p3_eth_warning:
                    status_lines.append(f"[Person 3] {p3_eth_warning}")
                p3_data["ethnicity"] = p3_eth

            # Extract and remove status from person data (don't include in YAML)
            p2_node_status = p2_data.pop("_status", None) if p2_data else None
            p3_node_status = p3_data.pop("_status", None) if p3_data else None

            # Master randomize cascades to connected Person nodes
            if randomize_all_people:
                if num_people >= 2:
                    p2_data = randomize_subject(genre=genre)
                    status_lines.extend(format_randomized_person(p2_data, "Person 2"))
                if num_people >= 3:
                    p3_data = randomize_subject(genre=genre)
                    status_lines.extend(format_randomized_person(p3_data, "Person 3"))
            else:
                # Log connected nodes with their status from Person node
                if p2_data and p2_node_status:
                    for line in p2_node_status.split("\n"):
                        status_lines.append(f"[Person 2] {line}")
                elif p2_data:
                    status_lines.append("[Person 2] connected")
                if p3_data and p3_node_status:
                    for line in p3_node_status.split("\n"):
                        status_lines.append(f"[Person 3] {line}")
                elif p3_data:
                    status_lines.append("[Person 3] connected")

            # Build YAML
            yaml_output = build_yaml_from_widgets(
                subjects=num_people,
                aspect=aspect,
                # Person 1
                s1_age=person_1_age,
                s1_gender=person_1_gender,
                s1_ethnicity=person_1_ethnicity,
                s1_body_type=person_1_body_type,
                s1_body_type_custom=person_1_body_type_custom,
                s1_hair=person_1_hair,
                s1_face=person_1_face,
                s1_expression=person_1_expression,
                s1_gaze=person_1_gaze,
                s1_hands=person_1_hands,
                s1_skin_texture=person_1_skin_texture,
                s1_skin_details=person_1_skin_details,
                s1_extras=person_1_extras,
                s1_outfit=person_1_outfit,
                s1_accessories=person_1_accessories,
                s1_footwear=person_1_footwear,
                s1_pose=person_1_pose,
                # Person 2
                s2_age=p2_data.get("age", ""),
                s2_gender=p2_data.get("gender", "NA"),
                s2_ethnicity=p2_data.get("ethnicity", ""),
                s2_body_type=p2_data.get("body_type", "NA"),
                s2_body_type_custom=p2_data.get("body_type_custom", ""),
                s2_hair=p2_data.get("hair", ""),
                s2_face=p2_data.get("face", ""),
                s2_expression=p2_data.get("expression", ""),
                s2_gaze=p2_data.get("gaze", ""),
                s2_hands=p2_data.get("hands", ""),
                s2_skin_texture=p2_data.get("skin_texture", ""),
                s2_skin_details=p2_data.get("skin_details", ""),
                s2_extras=p2_data.get("extras", ""),
                s2_outfit=p2_data.get("outfit", ""),
                s2_accessories=p2_data.get("accessories", ""),
                s2_footwear=p2_data.get("footwear", ""),
                s2_pose=p2_data.get("pose", ""),
                # Person 3
                s3_age=p3_data.get("age", ""),
                s3_gender=p3_data.get("gender", "NA"),
                s3_ethnicity=p3_data.get("ethnicity", ""),
                s3_body_type=p3_data.get("body_type", "NA"),
                s3_body_type_custom=p3_data.get("body_type_custom", ""),
                s3_hair=p3_data.get("hair", ""),
                s3_face=p3_data.get("face", ""),
                s3_expression=p3_data.get("expression", ""),
                s3_gaze=p3_data.get("gaze", ""),
                s3_hands=p3_data.get("hands", ""),
                s3_skin_texture=p3_data.get("skin_texture", ""),
                s3_skin_details=p3_data.get("skin_details", ""),
                s3_extras=p3_data.get("extras", ""),
                s3_outfit=p3_data.get("outfit", ""),
                s3_accessories=p3_data.get("accessories", ""),
                s3_footwear=p3_data.get("footwear", ""),
                s3_pose=p3_data.get("pose", ""),
                # Interaction
                interaction=interaction,
                # Scene
                location=location,
                time=time,
                weather=weather,
                atmosphere=atmosphere,
                props=props,
                background=background,
                era=era,
                action=action,
                story=story,
                lighting=lighting,
                # Composition
                framing=framing,
                camera_angle=camera_angle,
            )

        # Handle LLM mode
        expanded_prompt = ""

        if llm_mode == "Internal (LM Studio)":
            status_lines.append("[LLM] Internal mode - generating prompt")
            expanded_prompt, lm_info = self._call_lm_studio(
                system_prompt=system_prompt,
                yaml_input=yaml_output,
                config=config,
            )
            status_lines.append(lm_info)
        else:
            status_lines.append(
                "[MODE] External mode - connect 'variables' + 'llm_instructions' to your LLM node"
            )

        status = "\n".join(status_lines)

        # Return with UI data for widget updates
        return {
            "ui": {"randomized_values": [randomized_values]},
            "result": (yaml_output, system_prompt, expanded_prompt, status),
        }


# Node registration
NODE_CLASS_MAPPINGS = {"ZForgePromptBuilder": ZForgePromptBuilder}

NODE_DISPLAY_NAME_MAPPINGS = {"ZForgePromptBuilder": "Z-Forge Prompt Builder"}
