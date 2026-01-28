"""
Z-Forge - Presets and Dropdown Options
Easy to edit - add/remove options as needed.
"""

# Body type presets (female) - must match v3 system prompt keywords
BODY_TYPES_FEMALE = [
    "NA",
    "supersize",
    "SSBBW",
    "SBBW",
    "BBW",
    "curvy",
    "hourglass",
    "thick",
    "chubby",
    "pear",
    "apple",
    "athletic",
    "muscular",
    "fit",
    "slim",
    "skinny",
    "petite",
    "tiny",
    "heart-shape",
    "average",
    "custom",
]

# Body type presets (male)
BODY_TYPES_MALE = [
    "NA",
    "superchub",
    "chub",
    "bear",
    "dad-bod",
    "stocky",
    "muscular",
    "athletic",
    "lean",
    "slim",
    "average",
    "custom",
]

# Combined body types for universal dropdown
BODY_TYPES_ALL = [
    "NA",
    # Large sizes
    "supersize",
    "SSBBW",
    "SBBW",
    "BBW",
    "superchub",
    "chub",
    "bear",
    # Medium sizes
    "curvy",
    "hourglass",
    "thick",
    "chubby",
    "pear",
    "apple",
    "dad-bod",
    "stocky",
    # Slim/athletic
    "athletic",
    "muscular",
    "fit",
    "lean",
    "slim",
    "skinny",
    "petite",
    "tiny",
    "heart-shape",
    "average",
    "custom",
]

# Gender options
GENDERS = [
    "NA",
    "female",
    "male",
    "non-binary",
    "custom",
]

# Time of day options
TIMES = [
    "NA",
    "dawn",
    "early morning",
    "morning",
    "late morning",
    "midday",
    "afternoon",
    "late afternoon",
    "evening",
    "dusk",
    "night",
    "late night",
    "custom",
]

# Framing options
FRAMINGS = [
    "NA",
    "extreme close-up",
    "close-up",
    "medium close-up",
    "medium shot",
    "3/4 shot",
    "full body",
    "environmental",
    "wide shot",
    "custom",
]

# Camera angle options
CAMERA_ANGLES = [
    "NA",
    "eye level",
    "slightly low angle",
    "low angle",
    "worm's eye",
    "slightly high angle",
    "high angle",
    "bird's eye",
    "Dutch angle",
    "over-the-shoulder",
    "custom",
]

# Aspect ratio hints
ASPECTS = [
    "portrait",
    "landscape",
    "square",
    "cinematic-wide",
]

# Weather options
WEATHERS = [
    "NA",
    "clear",
    "sunny",
    "overcast",
    "cloudy",
    "rainy",
    "stormy",
    "foggy",
    "misty",
    "snowy",
    "windy",
    "humid",
    "custom",
]

# Common expression suggestions (for tooltip, not dropdown)
EXPRESSION_HINTS = """Common expressions: confident, contemplative, joyful, serene, defiant,
vulnerable, amused, intense, melancholic, fierce, tender, mysterious, weary, playful, stoic"""

# Common ethnicity suggestions (for tooltip)
ETHNICITY_HINTS = """Examples: Japanese, Korean, Chinese, Vietnamese, Thai, Filipino,
Indian, Pakistani, Arab, Persian, Turkish, Nigerian, Ethiopian, Kenyan, South African,
British, Irish, German, French, Italian, Spanish, Greek, Swedish, Russian, Polish,
African American, Mexican, Brazilian, Puerto Rican, Colombian, Polynesian, Samoan,
mixed, biracial, Eurasian"""

# Common pose suggestions (for tooltip)
POSE_HINTS = """Examples: confident-standing, casual-lean, seated-relaxed, seated-forward,
power-pose, thoughtful, walking, turned-away, arms-crossed, hands-pockets,
seated-elegant, reclining, kneeling, crouching"""

# Genre options for ethnicity/race switching
GENRES = ["realistic", "fantasy"]

# Realistic ethnicities (real-world)
ETHNICITIES_REALISTIC = [
    "NA",
    # East Asian
    "Japanese", "Korean", "Chinese", "Vietnamese", "Thai", "Filipino",
    # South Asian
    "Indian", "Pakistani", "Bangladeshi",
    # Middle Eastern
    "Arab", "Persian", "Turkish", "Kurdish",
    # African
    "Nigerian", "Ethiopian", "Kenyan", "South African", "Egyptian",
    # European
    "British", "Irish", "German", "French", "Italian", "Spanish", "Scandinavian", "Slavic",
    # Americas
    "African American", "Mexican", "Brazilian", "Puerto Rican", "Indigenous American",
    # Pacific
    "Polynesian", "Hawaiian", "Maori",
    # Mixed
    "mixed", "biracial",
    "custom",
]

# Fantasy races
ETHNICITIES_FANTASY = [
    "NA",
    # Core races
    "human", "elf", "high-elf", "wood-elf", "dark-elf", "sea-elf", "sun-elf", "moon-elf",
    "dwarf", "mountain-dwarf", "hill-dwarf",
    "halfling", "gnome",
    "orc", "half-orc", "half-elf",
    "tiefling", "dragonborn", "aasimar",
    # Genasi
    "genasi-fire", "genasi-water", "genasi-earth", "genasi-air",
    # Beastfolk
    "tabaxi", "kenku", "lizardfolk",
    # Goblinoids
    "goblin", "hobgoblin", "kobold",
    "custom",
]

# Combined for server-side validation (ComfyUI needs all valid options)
ETHNICITIES_ALL = list(dict.fromkeys(ETHNICITIES_REALISTIC + ETHNICITIES_FANTASY))
