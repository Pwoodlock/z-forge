"""
Z-Forge - YAML Construction
Converts widget values to formatted YAML string.
"""
from typing import Dict, Any, Optional


def is_empty(value: Any) -> bool:
    """Check if a value should be treated as empty/NA."""
    if value is None:
        return True
    if isinstance(value, str):
        v = value.strip().lower()
        return v in ("", "na", "n/a", "none", "skip", "custom")
    if isinstance(value, (int, float)):
        return value == 0
    return False


def format_value(value: Any) -> str:
    """Format a value for YAML output."""
    if isinstance(value, str):
        # If contains special chars or newlines, use quotes
        if any(c in value for c in [":", "#", "'", '"', "\n", "{"]):
            # Escape quotes and use double quotes
            escaped = value.replace('"', '\\"')
            return f'"{escaped}"'
        return value
    return str(value)


def build_subject_yaml(
    prefix: str,
    age: Any,
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
) -> str:
    """Build YAML for a single subject."""
    lines = []

    # Determine actual body type value
    actual_body_type = body_type_custom if body_type == "custom" else body_type

    # Map of field names to values
    fields = [
        ("age", age),
        ("gender", gender),
        ("ethnicity", ethnicity),
        ("body_type", actual_body_type),
        ("hair", hair),
        ("face", face),
        ("expression", expression),
        ("gaze", gaze),
        ("hands", hands),
        ("skin_texture", skin_texture),
        ("skin_details", skin_details),
        ("extras", extras),
        ("outfit", outfit),
        ("accessories", accessories),
        ("footwear", footwear),
        ("pose", pose),
    ]

    for field_name, value in fields:
        if is_empty(value):
            lines.append(f"{prefix}{field_name}: NA")
        else:
            lines.append(f"{prefix}{field_name}: {format_value(value)}")

    return "\n".join(lines)


def build_yaml_from_widgets(
    # Master settings
    subjects: int,
    aspect: str,
    # Subject 1
    s1_age: Any,
    s1_gender: str,
    s1_ethnicity: str,
    s1_body_type: str,
    s1_body_type_custom: str,
    s1_hair: str,
    s1_face: str,
    s1_expression: str,
    s1_gaze: str,
    s1_hands: str,
    s1_skin_texture: str,
    s1_skin_details: str,
    s1_extras: str,
    s1_outfit: str,
    s1_accessories: str,
    s1_footwear: str,
    s1_pose: str,
    # Subject 2 (optional)
    s2_age: Any = None,
    s2_gender: str = "NA",
    s2_ethnicity: str = "",
    s2_body_type: str = "NA",
    s2_body_type_custom: str = "",
    s2_hair: str = "",
    s2_face: str = "",
    s2_expression: str = "",
    s2_gaze: str = "",
    s2_hands: str = "",
    s2_skin_texture: str = "",
    s2_skin_details: str = "",
    s2_extras: str = "",
    s2_outfit: str = "",
    s2_accessories: str = "",
    s2_footwear: str = "",
    s2_pose: str = "",
    # Subject 3 (optional)
    s3_age: Any = None,
    s3_gender: str = "NA",
    s3_ethnicity: str = "",
    s3_body_type: str = "NA",
    s3_body_type_custom: str = "",
    s3_hair: str = "",
    s3_face: str = "",
    s3_expression: str = "",
    s3_gaze: str = "",
    s3_hands: str = "",
    s3_skin_texture: str = "",
    s3_skin_details: str = "",
    s3_extras: str = "",
    s3_outfit: str = "",
    s3_accessories: str = "",
    s3_footwear: str = "",
    s3_pose: str = "",
    # Interaction
    interaction: str = "",
    # Scene
    location: str = "",
    time: str = "NA",
    weather: str = "NA",
    atmosphere: str = "",
    props: str = "",
    background: str = "",
    era: str = "",
    action: str = "",
    story: str = "",
    lighting: str = "",
    # Composition
    framing: str = "NA",
    camera_angle: str = "NA",
) -> str:
    """Build complete YAML from all widget values."""

    yaml_parts = []

    # Master settings
    yaml_parts.append("# === MASTER SETTINGS ===")
    yaml_parts.append(f"subjects: {subjects}")
    yaml_parts.append(f"aspect: {aspect}")
    yaml_parts.append("")

    # Subject 1
    yaml_parts.append("# === SUBJECT 1 ===")
    yaml_parts.append(build_subject_yaml(
        "",
        s1_age, s1_gender, s1_ethnicity, s1_body_type, s1_body_type_custom,
        s1_hair, s1_face, s1_expression, s1_gaze, s1_hands,
        s1_skin_texture, s1_skin_details, s1_extras,
        s1_outfit, s1_accessories, s1_footwear, s1_pose
    ))
    yaml_parts.append("")

    # Subject 2 (if multiple subjects)
    yaml_parts.append("# === SUBJECT 2 ===")
    if subjects >= 2:
        yaml_parts.append(build_subject_yaml(
            "s2_",
            s2_age, s2_gender, s2_ethnicity, s2_body_type, s2_body_type_custom,
            s2_hair, s2_face, s2_expression, s2_gaze, s2_hands,
            s2_skin_texture, s2_skin_details, s2_extras,
            s2_outfit, s2_accessories, s2_footwear, s2_pose
        ))
    else:
        # All NA for unused subjects
        yaml_parts.append("s2_age: NA")
        yaml_parts.append("s2_gender: NA")
        yaml_parts.append("s2_ethnicity: NA")
        yaml_parts.append("s2_body_type: NA")
        yaml_parts.append("s2_hair: NA")
        yaml_parts.append("s2_face: NA")
        yaml_parts.append("s2_expression: NA")
        yaml_parts.append("s2_gaze: NA")
        yaml_parts.append("s2_hands: NA")
        yaml_parts.append("s2_skin_texture: NA")
        yaml_parts.append("s2_skin_details: NA")
        yaml_parts.append("s2_extras: NA")
        yaml_parts.append("s2_outfit: NA")
        yaml_parts.append("s2_accessories: NA")
        yaml_parts.append("s2_footwear: NA")
        yaml_parts.append("s2_pose: NA")
    yaml_parts.append("")

    # Subject 3 (if 3 subjects)
    yaml_parts.append("# === SUBJECT 3 ===")
    if subjects >= 3:
        yaml_parts.append(build_subject_yaml(
            "s3_",
            s3_age, s3_gender, s3_ethnicity, s3_body_type, s3_body_type_custom,
            s3_hair, s3_face, s3_expression, s3_gaze, s3_hands,
            s3_skin_texture, s3_skin_details, s3_extras,
            s3_outfit, s3_accessories, s3_footwear, s3_pose
        ))
    else:
        yaml_parts.append("s3_age: NA")
        yaml_parts.append("s3_gender: NA")
        yaml_parts.append("s3_ethnicity: NA")
        yaml_parts.append("s3_body_type: NA")
        yaml_parts.append("s3_hair: NA")
        yaml_parts.append("s3_face: NA")
        yaml_parts.append("s3_expression: NA")
        yaml_parts.append("s3_gaze: NA")
        yaml_parts.append("s3_hands: NA")
        yaml_parts.append("s3_skin_texture: NA")
        yaml_parts.append("s3_skin_details: NA")
        yaml_parts.append("s3_extras: NA")
        yaml_parts.append("s3_outfit: NA")
        yaml_parts.append("s3_accessories: NA")
        yaml_parts.append("s3_footwear: NA")
        yaml_parts.append("s3_pose: NA")
    yaml_parts.append("")

    # Interaction (only for multi-subject)
    yaml_parts.append("# === INTERACTION ===")
    if subjects >= 2 and not is_empty(interaction):
        yaml_parts.append(f"interaction: {format_value(interaction)}")
    else:
        yaml_parts.append("interaction: NA")
    yaml_parts.append("")

    # Scene
    yaml_parts.append("# === SCENE ===")
    scene_fields = [
        ("location", location),
        ("time", time),
        ("weather", weather),
        ("atmosphere", atmosphere),
        ("props", props),
        ("background", background),
        ("era", era),
        ("action", action),
        ("story", story),
        ("lighting", lighting),
    ]
    for field_name, value in scene_fields:
        if is_empty(value):
            yaml_parts.append(f"{field_name}: NA")
        else:
            yaml_parts.append(f"{field_name}: {format_value(value)}")
    yaml_parts.append("")

    # Composition
    yaml_parts.append("# === COMPOSITION ===")
    if is_empty(framing):
        yaml_parts.append("framing: NA")
    else:
        yaml_parts.append(f"framing: {format_value(framing)}")
    if is_empty(camera_angle):
        yaml_parts.append("camera_angle: NA")
    else:
        yaml_parts.append(f"camera_angle: {format_value(camera_angle)}")

    return "\n".join(yaml_parts)
