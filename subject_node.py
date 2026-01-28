"""
Z-Forge Person Node
Separate node for Person 2 and Person 3 data.
"""
import json
import logging

from .presets import (
    BODY_TYPES_ALL,
    ETHNICITIES_ALL,
    ETHNICITIES_FANTASY,
    ETHNICITIES_REALISTIC,
    GENDERS,
    GENRES,
    EXPRESSION_HINTS,
    POSE_HINTS,
)
from .randomizer import randomize_subject

logger = logging.getLogger("ZForge")


def validate_ethnicity_for_genre(ethnicity: str, genre: str) -> tuple[str, str | None]:
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


class ZForgePerson:
    """
    Person definition node for Z-Forge Prompt Builder.
    Connect to the main node's person_2 or person_3 inputs.
    """

    CATEGORY = "Z-Forge"
    RETURN_TYPES = ("ZFORGE_PERSON",)
    RETURN_NAMES = ("person",)
    OUTPUT_NODE = True  # Required for UI return data (widget updates)
    FUNCTION = "build_person"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "genre": (GENRES, {
                    "default": "realistic",
                    "tooltip": "Switches ethnicity options. Match with main Prompt Builder genre setting."
                }),
                "reset": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Clear all fields to defaults (toggle on then off)"
                }),
                "randomize": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Randomize all fields (ignores widget values when enabled)"
                }),
                "age": ("STRING", {
                    "default": "",
                    "tooltip": "Age: number (25) or range (early 30s, mid-50s)"
                }),
                "gender": (GENDERS, {
                    "default": "female",
                    "tooltip": "Person gender"
                }),
                "ethnicity": (ETHNICITIES_ALL, {
                    "default": "NA",
                    "tooltip": "Ethnicity (realistic) or Race (fantasy). Dropdown filters by genre."
                }),
                "body_type": (BODY_TYPES_ALL, {
                    "default": "NA",
                    "tooltip": "Body type preset. Select 'custom' to use custom field."
                }),
                "body_type_custom": ("STRING", {
                    "default": "",
                    "tooltip": "Enter custom body type here (only used when body_type dropdown is set to 'custom')"
                }),
                "hair": ("STRING", {
                    "default": "",
                    "tooltip": "Hair color, length, style"
                }),
                "face": ("STRING", {
                    "default": "",
                    "tooltip": "Facial structure and features"
                }),
                "expression": ("STRING", {
                    "default": "",
                    "tooltip": EXPRESSION_HINTS
                }),
                "gaze": ("STRING", {
                    "default": "",
                    "tooltip": "Where they're looking: direct at camera, off-camera left, etc."
                }),
                "hands": ("STRING", {
                    "default": "",
                    "tooltip": "What the hands are doing"
                }),
                "skin_texture": ("STRING", {
                    "default": "",
                    "tooltip": "Skin surface quality: matte, weathered, smooth, etc."
                }),
                "skin_details": ("STRING", {
                    "default": "",
                    "tooltip": "Freckles, moles, tattoos, scars, stretch marks, etc."
                }),
                "extras": ("STRING", {
                    "default": "",
                    "tooltip": "Additional details: glasses, beard, piercings, etc."
                }),
                "outfit": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Complete clothing description"
                }),
                "accessories": ("STRING", {
                    "default": "",
                    "tooltip": "Jewelry, watches, etc."
                }),
                "footwear": ("STRING", {
                    "default": "",
                    "tooltip": "Shoes if visible"
                }),
                "pose": ("STRING", {
                    "default": "",
                    "tooltip": POSE_HINTS
                }),
            },
        }

    @classmethod
    def IS_CHANGED(cls, genre, reset, randomize, **kwargs):
        """Force re-execution when reset or randomize is True."""
        if reset or randomize:
            import time
            return str(time.time())
        return ""

    def build_person(
        self,
        genre: str,
        reset: bool,
        randomize: bool,
        age: str,
        gender: str,
        ethnicity: str,
        body_type: str,
        body_type_custom: str,
        hair: str,
        face: str,
        expression: str,
        gaze: str,
        hands: str,
        skin_texture: str,
        skin_details: str,
        extras: str,
        outfit: str,
        accessories: str,
        footwear: str,
        pose: str,
    ) -> dict:
        """
        Build person data.

        Returns:
            Dict with UI data and result tuple containing JSON-encoded person data
        """
        # Track values for widget updates
        widget_updates = {}
        status_lines = []

        # Handle reset - clear all fields to defaults
        if reset:
            widget_updates = {
                "reset": False,  # Auto-toggle off
                "randomize": False,
                "age": "",
                "gender": "female",
                "ethnicity": "NA",
                "body_type": "NA",
                "body_type_custom": "",
                "hair": "",
                "face": "",
                "expression": "",
                "gaze": "",
                "hands": "",
                "skin_texture": "",
                "skin_details": "",
                "extras": "",
                "outfit": "",
                "accessories": "",
                "footwear": "",
                "pose": "",
            }
            data = {k: v for k, v in widget_updates.items() if k not in ("reset", "randomize")}
            status_lines.append("[RESET] All fields cleared")
        elif randomize:
            # Use randomized values
            data = randomize_subject(genre=genre)
            # Copy data to widget_updates for widget update
            widget_updates = data.copy()
            status_lines.append("[RANDOMIZED]")
            status_lines.append(f"  Age: {data.get('age', 'NA')}")
            status_lines.append(f"  Gender: {data.get('gender', 'NA')}")
            status_lines.append(f"  Ethnicity: {data.get('ethnicity', 'NA')}")
            status_lines.append(f"  Body: {data.get('body_type', 'NA')}")
            status_lines.append(f"  Expression: {data.get('expression', 'NA')}")
        else:
            # Validate ethnicity against genre before using widget values
            validated_ethnicity, eth_warning = validate_ethnicity_for_genre(ethnicity, genre)
            if eth_warning:
                status_lines.append(eth_warning)
                widget_updates["ethnicity"] = validated_ethnicity

            # Use widget values
            data = {
                "age": age,
                "gender": gender,
                "ethnicity": validated_ethnicity,
                "body_type": body_type,
                "body_type_custom": body_type_custom,
                "hair": hair,
                "face": face,
                "expression": expression,
                "gaze": gaze,
                "hands": hands,
                "skin_texture": skin_texture,
                "skin_details": skin_details,
                "extras": extras,
                "outfit": outfit,
                "accessories": accessories,
                "footwear": footwear,
                "pose": pose,
            }
            # Count filled fields for status
            filled = sum(1 for v in data.values() if v and str(v).strip() and str(v) != "NA")
            status_lines.append(f"[MANUAL] {filled}/17 fields set")

        # Include status in data for main node to extract
        data["_status"] = "\n".join(status_lines)

        # Return with UI data for widget updates
        return {
            "ui": {"randomized_values": [widget_updates]},
            "result": (json.dumps(data),),
        }


# Node registration
NODE_CLASS_MAPPINGS = {
    "ZForgePerson": ZForgePerson
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZForgePerson": "Z-Forge Person"
}
