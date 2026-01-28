"""
Z-Forge - Randomization Logic
Generates random values for person fields.
"""
import random
from typing import Dict, Any

from .presets import (
    BODY_TYPES_ALL,
    ETHNICITIES_FANTASY,
    ETHNICITIES_REALISTIC,
    GENDERS,
    TIMES,
    FRAMINGS,
    CAMERA_ANGLES,
    WEATHERS,
)

# Random value pools

AGES = [
    "early 20s", "mid 20s", "late 20s",
    "early 30s", "mid 30s", "late 30s",
    "early 40s", "mid 40s", "late 40s",
    "early 50s", "mid 50s", "late 50s",
    "early 60s", "mid 60s",
    "18", "21", "25", "28", "32", "35", "38", "42", "45", "50", "55"
]

ETHNICITIES = [
    # European
    "British", "Irish", "German", "French", "Italian", "Spanish",
    "Swedish", "Norwegian", "Russian", "Polish", "Greek", "Portuguese",
    # Asian
    "Japanese", "Korean", "Chinese", "Vietnamese", "Thai", "Filipino",
    "Indian", "Pakistani",
    # African
    "Nigerian", "Ethiopian", "Kenyan", "South African", "Ghanaian",
    # Middle Eastern
    "Arab", "Persian", "Turkish", "Lebanese",
    # Americas
    "African American", "Mexican", "Brazilian", "Colombian", "Puerto Rican",
    # Pacific
    "Polynesian", "Samoan", "Hawaiian",
    # Mixed
    "mixed", "biracial", "Eurasian",
]

HAIR_COLORS = [
    "black", "dark brown", "brown", "light brown", "auburn", "red",
    "strawberry blonde", "blonde", "platinum blonde", "silver", "grey",
    "white", "pink", "blue", "purple", "green",
]

HAIR_LENGTHS = [
    "very short", "short", "chin-length", "shoulder-length",
    "medium-length", "long", "very long", "waist-length",
]

HAIR_STYLES = [
    "straight", "wavy", "curly", "coily", "braided", "in a bun",
    "in a ponytail", "slicked back", "messy", "windswept",
    "with bangs", "parted in the middle", "parted to the side",
    "natural", "textured", "layered",
]

EXPRESSIONS = [
    "confident", "contemplative", "joyful", "serene", "defiant",
    "vulnerable", "amused", "intense", "melancholic", "fierce",
    "tender", "mysterious", "weary", "playful", "stoic",
    "thoughtful", "determined", "relaxed", "surprised", "curious",
    "knowing", "wistful", "proud", "gentle", "fierce",
]

GAZES = [
    "direct at camera", "direct at viewer", "looking into camera",
    "off-camera left", "off-camera right", "looking down",
    "looking up", "looking into distance", "eyes closed",
    "looking over shoulder", "sidelong glance", "downcast eyes",
]

HAND_POSITIONS = [
    "relaxed at sides", "one hand on hip", "both hands on hips",
    "arms crossed", "hands in pockets", "one hand touching face",
    "hands clasped", "one hand raised", "gesturing",
    "holding an object", "fingers interlaced", "hands on knees",
    "one hand on chest", "hands behind back",
]

SKIN_TEXTURES = [
    "smooth", "natural", "matte", "dewy", "weathered",
    "sun-kissed", "porcelain", "glowing",
]

SKIN_DETAILS_OPTIONS = [
    "freckles", "light freckles across nose", "freckles on cheeks and shoulders",
    "beauty mark near lip", "small mole on cheek", "laugh lines",
    "crow's feet", "smile lines", "faint acne scars",
    "stretch marks", "cellulite visible", "visible pores",
    "tattoo on arm", "small tattoo on wrist", "tattoo sleeve",
    "pierced ears", "nose piercing", "scar on eyebrow",
    "", "", "",  # Empty options for variety
]

POSES = [
    "standing confidently", "casual lean against wall", "seated relaxed",
    "seated forward", "power pose", "thoughtful stance",
    "walking", "turned away, looking over shoulder", "arms crossed",
    "hands in pockets", "seated elegantly", "reclining",
    "kneeling", "crouching", "mid-stride", "stretching",
]

# Realistic locations (modern/real-world)
LOCATIONS_REALISTIC = [
    "urban street", "coffee shop", "modern apartment", "rooftop",
    "beach at sunset", "forest clearing", "mountain overlook",
    "art gallery", "library", "restaurant", "bar",
    "train station", "airport", "hotel room", "garden",
    "park bench", "city skyline background", "industrial warehouse",
    "studio with seamless backdrop", "vintage diner",
    "luxury penthouse", "cozy cabin", "botanical garden",
]

# Fantasy locations - cinematic realism (Lord of the Rings / Witcher / Game of Thrones aesthetic)
LOCATIONS_FANTASY = [
    # ANCIENT FORESTS (12)
    "ancient forest with massive gnarled oaks draped in heavy moss, shafts of cold morning light cutting through mist, fallen logs covered in fungus, damp earth and rotting leaves underfoot, the air thick and still",
    "dense woodland in autumn, towering trees with golden and copper leaves, soft diffused light filtering through the canopy, a carpet of fallen leaves on the forest floor, cold crisp air",
    "dark pine forest at dusk, tall straight trunks disappearing into shadow, patches of snow on the ground, weak grey light barely penetrating the thick canopy, an oppressive silence",
    "primeval forest with trees so old their branches block out the sky, twisted roots breaking through rocky soil, thick fog clinging to the ground, everything damp and ancient",
    "foggy woodland at dawn, bare birch trees with peeling white bark, ground frost on dead grass, pale weak sunlight struggling through the haze, breath visible in the cold air",
    "ancient forest with towering oak trees centuries old, thick trunks covered in deep green moss and lichen, shafts of pale morning light cutting through dense fog, forest floor carpeted in fallen leaves and ferns, damp earthy atmosphere",
    "dark pine forest on a mountainside, tall straight trunks disappearing into low-hanging clouds, thick mist obscuring visibility beyond thirty feet, wet black soil and exposed roots, overcast diffused light creating flat shadows",
    "autumnal forest at dawn, massive beech trees with golden and copper leaves, cold mist rising from the forest floor, weak sunlight filtering through the canopy, fallen leaves covering an old stone path",
    "primeval forest with trees so large their roots form caverns, dense canopy blocking most light, rare beams of sun illuminating floating dust and pollen, humid still air heavy with the smell of decay and growth",
    "forest clearing after rainfall, water dripping from every leaf and branch, muddy ground with pooled water reflecting grey sky, low clouds visible through the gap in the canopy, everything glistening wet",
    "dead forest in winter twilight, leafless black trees against a pale grey sky, thin layer of snow on frozen ground, cold blue light fading to darkness, absolute silence and stillness",
    "forest of massive redwoods in morning fog, trunks like cathedral pillars disappearing upward into white mist, ferns covering the forest floor, soft diffused light with no visible sun, sense of immense scale",

    # MOUNTAINS & HIGHLANDS (12)
    "rocky mountain pass at sunset, jagged peaks silhouetted against an orange sky, a narrow path winding between massive boulders, cold wind whipping through the gap, patches of old snow in shadowed crevices",
    "highland moor under grey overcast skies, endless rolling hills of heather and brown grass, standing stones weathered by centuries, distant rain sweeping across the landscape",
    "mountain fortress carved into sheer cliff face, ancient stonework blackened by age, narrow switchback path leading to iron-bound gates, banners tattered by harsh winds",
    "alpine meadow at the tree line, wildflowers among rocky outcrops, snow-capped peaks towering above, a cold clear stream cutting through the grass, thin crisp air",
    "volcanic highlands with black rock and ash-grey soil, steam venting from cracks in the earth, an orange glow on the horizon from distant lava flows, acrid smell of sulfur",
    "mountain pass at high altitude, jagged granite peaks dusted with snow rising into clouds, narrow rocky path carved into the cliff face, cold wind visible in swirling snow, harsh overcast light",
    "highland moor under stormy skies, rolling hills of heather and rough grass stretching to the horizon, dark clouds threatening rain, standing stones weathered by centuries on a distant ridge, cold wind bending the grass",
    "volcanic landscape at dusk, black rocky terrain with cracks revealing orange magma beneath, steam venting from fissures, dark ash clouds on the horizon, hellish red glow reflecting off low clouds",
    "mountain fortress ruins at dawn, crumbling stone walls built into a cliff face, centuries of weather erosion visible in the stonework, snow on the peaks above, first golden light catching the highest towers",
    "alpine valley in early morning, frost covering the grass, breath visible in cold air, massive mountains on either side still in shadow, thin mist hanging over a glacial river, pristine untouched wilderness",
    "rocky mountain peak above the clouds, barren windswept stone at extreme altitude, sea of white clouds below, intense blue sky above, harsh direct sunlight casting sharp shadows, sense of isolation and exposure",
    "mountain lake at sunset, perfectly still water reflecting snow-capped peaks and orange sky, dark pine forest along the shoreline, last warm light of day on the highest summits, approaching darkness in the valleys",

    # RUINS & ANCIENT STRUCTURES (13)
    "crumbling stone ruins overgrown with ivy and moss, broken columns and fallen archways, weeds pushing through cracked flagstones, the remains of what was once a great hall open to grey skies",
    "abandoned fortress on a hilltop, walls breached and towers collapsed, grass growing in the courtyard, rusty iron gates hanging from broken hinges, crows circling overhead",
    "ancient temple deep in the forest, massive stone blocks fitted without mortar, roots growing over and through the structure, shafts of light illuminating dust and decay within",
    "ruined watchtower on a coastal cliff, half collapsed into the sea below, weathered stone stairs leading nowhere, the constant crash of waves against rocks, salt spray in the air",
    "overgrown cemetery with tilted headstones and collapsed crypts, iron fences rusted and bent, dead trees with bare branches, thick fog obscuring the older graves",
    "ruined stone keep overtaken by forest, massive trees growing through collapsed walls, roots cracking ancient stonework, moss and ivy covering every surface, overcast light filtering through the broken roof",
    "abandoned great hall with collapsed timber roof, stone walls blackened by ancient fire, weeds growing between cracked floor tiles, shafts of light through holes in the ceiling illuminating floating dust, centuries of neglect",
    "crumbling stone bridge over a deep gorge, ancient weathered construction missing sections, thick fog obscuring the depths below, wet stone surfaces, overcast grey sky, sense of danger and decay",
    "ruined temple in dense jungle, massive stone blocks carved with worn reliefs, strangler figs consuming the architecture, humid air thick with moisture, dappled light through the jungle canopy above",
    "ancient stone circle on a windswept hill, massive standing stones weathered smooth by millennia, lichen covering the surfaces, grey overcast sky, long grass bending in the wind, sense of prehistoric mystery",
    "collapsed cathedral in an abandoned city, Gothic arches open to the sky, vegetation reclaiming the nave, rubble and debris covering the floor, pigeons nesting in the high stonework, melancholy afternoon light",
    "fortress built into a sea cliff, stone walls battered by centuries of storms, waves crashing against the rocks below, salt spray in the air, grey sky and grey sea merging at the horizon, isolated and weatherbeaten",
    "ancient watchtower on a border ridge, simple stone construction worn by weather, wooden door long rotted away, commanding view of wild lands in every direction, cold wind and racing clouds",

    # SETTLEMENTS & DWELLINGS (12)
    "medieval village at dawn, thatched roof cottages with smoke rising from chimneys, muddy unpaved streets, wooden carts and hanging shop signs, warm light spilling from tavern windows",
    "fortified town with high stone walls, guards patrolling the ramparts, crowded streets of timber-frame buildings, market stalls with canvas awnings, the smell of woodsmoke and livestock",
    "harbor town in grey weather, wooden docks with fishing boats tied up, nets hanging to dry, seagulls circling, salt-worn buildings with slate roofs, cold spray off choppy waters",
    "mountain stronghold built into the rock, massive stone walls with iron-reinforced gates, torches burning in brackets, armored guards at the entrance, banners hanging limp in still air",
    "forest settlement of wooden longhouses, smoke rising through central roof holes, muddy paths between buildings, livestock penned nearby, woodpiles stacked against walls",
    "medieval village at dawn, timber and thatch buildings along a muddy street, smoke rising from chimneys, frost on the rooftops, warm candlelight in a few windows, mist hanging in the air",
    "isolated farmstead in rolling hills, stone cottage with thick walls and small windows, livestock pen with rough wooden fencing, vegetable garden beside the house, woodsmoke rising into grey sky",
    "fishing village on a rocky northern coast, weathered wooden buildings on stilts above the tide line, fishing boats pulled up on the shore, grey sea and grey sky, smell of salt and fish",
    "blacksmith's forge in a village square, open-sided wooden structure with a roaring coal fire, iron tools hanging on every beam, anvil worn smooth by generations of use, orange firelight against overcast day",
    "mountain monastery built on an impossible ledge, ancient stone buildings clinging to the cliff face, narrow stairs carved into the rock, clouds drifting below, cold thin air at high altitude",
    "abandoned mining town in a narrow valley, wooden buildings in various states of collapse, rusted equipment left where it stood, mine entrance dark in the hillside, overcast sky and dead silence",
    "lord's manor house in autumn, grey stone building with tall chimneys, formal gardens overgrown and wild, fallen leaves covering the gravel drive, smoke from one chimney suggesting occupation, melancholy faded grandeur",

    # INTERIORS (5)
    "great hall of a medieval castle, long wooden tables lit by fire and candlelight, smoke-stained stone walls hung with faded tapestries, hounds sleeping near the hearth, cold drafts from high windows",
    "ancient library with towering wooden shelves, leather-bound books thick with dust, weak light from narrow windows, a heavy oak table covered in scrolls and maps, candles guttering in iron holders",
    "forge interior with roaring fire in the furnace, tools hanging on soot-blackened walls, the ring of hammer on anvil, sparks flying, sweat and heat and the smell of hot metal",
    "throne room of weathered grey stone, faded banners hanging from high rafters, an iron throne on a raised dais, cold light from tall narrow windows, echoing emptiness",
    "tavern interior with low timber ceiling blackened by smoke, rough wooden tables scarred by knife marks, a fire crackling in a stone hearth, the smell of ale and roasting meat",

    # WATER & COASTLINES (13)
    "misty lake at dawn, still grey water reflecting bare trees on the shore, a wooden dock with a small boat tied up, reeds along the waterline, the call of unseen birds",
    "river crossing at an old stone bridge, moss-covered arches over dark water, willows trailing branches in the current, a muddy path leading to and from the bridge",
    "coastal cliffs in a storm, grey waves crashing against black rocks far below, rain driving sideways, a narrow path along the cliff edge, sea spray mixing with rain",
    "swamp at dusk, dark water between hummocks of grass, dead trees rising from the murk, the buzz of insects, mist curling over the surface, uncertain footing everywhere",
    "waterfall in a rocky gorge, white water thundering down into a churning pool, spray soaking the mossy rocks, ferns growing from every crevice, the roar drowning all other sound",
    "hidden cove at low tide, dark wet sand and exposed rocks covered in seaweed, sea cave entrance visible in the cliff, grey sky reflected in tidal pools, smell of salt and kelp",
    "river ford at a forest crossing, shallow water flowing over smooth stones, ancient road visible on both banks, overhanging trees creating a tunnel of green, dappled afternoon light on the water surface",
    "sea stack at sunset, massive pillar of rock isolated offshore, waves breaking around its base, nesting seabirds circling, dramatic orange and purple sky, last light of day catching the stone",
    "frozen lake in deep winter, thick ice covered in wind-blown snow, dark pine forest surrounding the shore, mountains in the distance, flat grey overcast light, absolute silence and cold",
    "marsh at dawn, still water between reed beds, thick mist limiting visibility, silhouettes of dead trees, soft pink light beginning to show on the horizon, frogs and birds beginning to call",
    "underground river in a vast cave system, black water flowing silently through a passage of pale limestone, torch light the only illumination, absolute darkness beyond the light's reach, cold damp air",
    "fjord at midday, steep cliff walls rising from dark water, waterfall cascading from a hanging valley, low clouds clinging to the peaks, small fishing boat providing sense of immense scale",

    # BATTLEFIELDS & DARK PLACES (11)
    "aftermath of a battle, churned muddy earth littered with broken weapons and shields, crows picking at the fallen, smoke rising from burned siege equipment, grey overcast sky",
    "dark cave mouth in a hillside, cold air flowing out from the darkness within, bones scattered near the entrance, claw marks on the stone, an animal smell",
    "gallows hill outside a town, wooden scaffold weathered grey by rain, crows perched on the crossbeam, dead grass and bare earth, a cold wind from the north",
    "burned village still smoldering, collapsed roofs and blackened walls, smoke rising from the ruins, personal belongings scattered in the mud, no sign of survivors",
    "ancient burial mound at twilight, grass-covered dome of earth, a dark entrance framed by standing stones, the wind making a low moan across the opening",
    "ancient battlefield now overgrown, rusted swords and broken shields visible in the long grass, burial mounds on a distant hill, crows circling overhead, overcast sky and cold wind, sense of old violence",
    "mass grave site in a forest clearing, disturbed earth in long rows, simple wooden markers weathered and leaning, fallen leaves covering the ground, grey light filtering through bare branches, sombre and haunting",
    "execution ground on a hill outside a city, wooden gallows weathered by years of use, crows perched on the crossbeam, muddy path worn by countless feet, view of city walls in the distance, grim overcast day",
    "abandoned siege line outside a fortress, collapsed wooden siege towers rotting in the mud, trenches filled with stagnant water, rusted weapons scattered in the grass, walls still standing in the distance",
    "haunted moor at twilight, flat boggy ground with treacherous pools, wisps of marsh gas drifting in the fading light, distant hills barely visible through the haze, sense of being watched, dangerous and lonely",

    # CAVES & UNDERGROUND (6)
    "cave entrance in a mountainside, dark opening framed by weathered rock, cold air flowing from within, bones of animals scattered near the entrance, overgrown path suggesting long abandonment",
    "vast underground cavern with a still black lake, natural limestone formations rising from the water, absolute darkness beyond torch range, dripping water echoing in the silence, ancient and untouched",
    "dwarf-carved hall deep underground, massive stone pillars in geometric rows, dust covering intricate floor patterns, some pillars collapsed and broken, faint light from a distant shaft, abandoned grandeur",
    "narrow cave passage with walls of glittering quartz, natural crystal formations catching torchlight, tight squeeze between rock walls, darkness ahead and behind, claustrophobic and beautiful",
    "underground tomb with stone sarcophagi in rows, dust and cobwebs covering carved lids, faded paintings on the walls, stale air undisturbed for centuries, flickering torchlight casting long shadows",
    "hot springs in a volcanic cave, steam rising from mineral-rich water, orange and yellow deposits around the pools, warmth in contrast to cold stone surroundings, dim light from the cave entrance",

    # ROADS & JOURNEYS (6)
    "ancient road through a forest, stone paving cracked and heaved by roots, overgrown but still passable, milestone with worn inscription, late afternoon light slanting through the trees",
    "mountain path in a snowstorm, narrow trail on a steep slope, visibility reduced to meters, snow accumulating quickly, dangerous drop into whiteness below, desperate conditions",
    "crossroads at dusk, four dirt roads meeting at a weathered signpost, old oak tree with thick trunk, long shadows stretching across the grass, decision point with unknown destinations",
    "coastal path along high cliffs, narrow trail with sheer drop to crashing waves below, sea spray in the air, grey sky meeting grey sea, wind pulling at clothes, exhilarating and terrifying",
    "forest road after heavy rain, deep muddy ruts from cart wheels, puddles reflecting grey sky, dripping trees on either side, difficult slow travel, saturated earth",
    "stone causeway across a marsh, raised path of ancient fitted stones, dark water on either side, mist obscuring the far end, croaking frogs, sense of vulnerability on the exposed path",

    # WILD PLACES (5)
    "windswept heath stretching to the horizon, low scrubby vegetation and scattered boulders, dark clouds rolling in from the west, a single twisted tree bent by constant wind",
    "frozen northern waste, endless white snow under a pale sky, distant mountains barely visible through ice haze, the crunch of boots on hard-packed snow, brutal cold",
    "dense thicket of thorns and brambles, no clear path through, weak light barely reaching the ground, the scratch and catch of branches on clothing, slow difficult progress",
    "river delta at low tide, channels of water between mudflats, wading birds picking through the shallows, the smell of salt and rotting seaweed, grey sky reflecting in still pools",
    "old growth forest after rain, everything dripping and glistening, mushrooms sprouting from fallen logs, rich smell of wet earth and decay, mist rising as weak sun breaks through",

    # MYSTICAL BUT GROUNDED (6)
    "stone circle at winter solstice dawn, massive standing stones casting long shadows, frost covering the ground, first light of sun aligned with the central stone, cold still air, ancient astronomical precision",
    "sacred grove of ancient yew trees, gnarled trunks thousands of years old, filtered green light through dense foliage, moss covering fallen branches, profound silence and stillness, sense of age and reverence",
    "healing spring in a forest hollow, clear water bubbling from rocks, offerings of cloth tied to surrounding branches, worn stone basin collecting the water, dappled sunlight, folk tradition and faith",
    "hermit's cave on a cliff face, simple dwelling carved into rock, wooden platform extending over the drop, smoke from a small fire within, commanding view of wild valleys below, isolation and contemplation",
    "ruined oracle's temple in mountain heights, cracked stone floor over a deep fissure, vapors rising from below, collapsed columns and scattered masonry, thin air and howling wind, abandoned prophecy",
    "burial barrow on a windswept plain, grass-covered mound with stone entrance visible, sheep grazing nearby, grey sky stretching to the horizon, sense of ancestors sleeping beneath, quietly sacred",

    # ELVEN & ANCIENT CIVILISATIONS (8)
    "hidden valley sanctuary carved into white limestone cliffs, elegant arched bridges spanning a rushing river below, waterfalls cascading from hanging gardens, autumn trees in gold and red, soft morning mist, timeless and serene",
    "abandoned elven city reclaimed by forest, graceful stone architecture with organic flowing lines, tree roots embracing fallen columns, shafts of light through the canopy illuminating moss-covered statues, melancholy beauty",
    "great library hall with towering shelves carved into living rock, dust motes floating in light from high windows, leather-bound tomes stacked on ancient oak tables, silence broken only by distant dripping water",
    "white stone city built in tiers up a mountainside, morning sun catching the highest towers, banners hanging limp in still air, cypress trees lining the climbing roads, Mediterranean warmth and ancient grandeur",
    "tree-platform settlement high in enormous ancient oaks, rope bridges connecting dwelling platforms, morning mist below obscuring the forest floor, wood smoke rising from hidden hearths, dappled green light",
    "palace courtyard with reflecting pools and geometric gardens, white marble walkways between still dark water, mountains visible beyond the walls, clear blue sky, formal and peaceful",
    "canyon city carved into red sandstone cliffs, facades of ancient temples emerging from the rock face, narrow gorge approach with walls towering overhead, warm afternoon light on rose-coloured stone",
    "ruins of a great hall with soaring ribbed ceiling partly collapsed, tall windows now empty of glass, vines climbing the walls, birds nesting in the high corners, grandeur faded but still evident",

    # NORTHERN & VIKING INSPIRED (8)
    "longhouse in a fjord settlement, turf roof thick with grass, woodsmoke rising into grey sky, wooden boats pulled up on the rocky shore, steep mountains plunging into dark water on either side",
    "frozen harbour with longships locked in winter ice, snow covering the decks and rigging, dark wooden buildings along the shore, mountains lost in low cloud, blue twilight of arctic winter",
    "great mead hall with massive timber beams and a central firepit, flames casting dancing shadows on carved wooden pillars, smoke gathering beneath the high roof, shields and weapons mounted on walls",
    "coastal watchtower on a windswept headland, dry-stone construction weathered by salt spray, iron brazier for signal fires on the roof, grey sea stretching to the horizon, gulls wheeling overhead",
    "burial ship on a pyre at water's edge, flames beginning to catch the oil-soaked timbers, mourners as silhouettes against the fire, smoke rising into overcast sky, fjord waters still and dark",
    "mountain stronghold built into a granite cliff face, wooden scaffolding and stairs zigzagging up the rock, snow on the peaks above, defensive walls following the natural contours, impregnable and isolated",
    "hot spring pool steaming in a snowy landscape, dark water against white snow banks, steam rising into cold air, distant mountains under heavy grey sky, volcanic warmth in frozen wilderness",
    "stave church in a mountain valley, dark tarred wood with dragon-headed carvings on the roofline, graveyard with weathered headstones, pine forest pressing close, overcast light and light rain",

    # DARK MEDIEVAL & GOTHIC (8)
    "plague village with doors marked in white paint, empty streets with personal belongings abandoned, crows gathering on rooftops, grey overcast light, smoke from burning pyres beyond the village edge",
    "torture chamber in a castle dungeon, iron implements hanging on damp stone walls, straw on the floor dark with old stains, single torch providing flickering light, drain in the centre of the floor",
    "gibbet cage hanging at a crossroads, rusted iron containing old bones, crows perched on the frame, muddy road stretching in four directions, grey sky and bare winter trees",
    "witch trial pyre in a town square, stake with chains and kindling prepared, townspeople's windows shuttered, cobblestones wet from recent rain, heavy atmosphere of fear and accusation",
    "leper colony outside city walls, ramshackle wooden shelters behind a ditch, warning bells hanging at the boundary, figures in hooded robes at a distance, isolation and suffering",
    "battlefield surgery tent, canvas walls splattered with blood, surgical tools on a wooden table, straw pallets for the wounded, surgeons working by lantern light, screams from outside",
    "mass burial during plague, lime-covered bodies in a deep pit, gravediggers with cloth masks over their faces, priest reading last rites, rain falling into the open grave, desperation and death",
    "abandoned asylum on a hilltop, Victorian Gothic architecture with barred windows, overgrown grounds with rusted gates, broken glass and peeling paint, crows nesting in the bell tower, disturbing history",

    # SLAVIC & EASTERN EUROPEAN (8)
    "witch's hut in a birch forest, crooked timber construction on wooden supports, animal skulls hanging from the eaves, herb garden overgrown and wild, thin smoke from a chimney, deep snow all around",
    "fortified monastery on a river island, white walls and golden onion domes, wooden dock with fishing boats, ice forming at the river edges, grey winter sky, bells ringing in the tower",
    "peasant village in autumn harvest, thatched wooden houses along a dirt track, haystacks in the fields, geese wandering free, smoke from cooking fires, golden afternoon light on turning leaves",
    "haunted manor in overgrown estate, baroque architecture falling into decay, windows dark and empty, wild garden with toppled statues, iron gates rusted open, crows calling from dead trees",
    "battlefield in a wheat field, trampled golden crops revealing dark earth, abandoned weapons and standards, bodies being collected onto carts, smoke from a burning farmhouse on the horizon",
    "forest shrine at a crossroads, weathered wooden structure with offerings of food and cloth, icons faded by weather, wildflowers growing at the base, dappled light through birch canopy",
    "swamp village on wooden platforms, houses on stilts above dark water, rope bridges connecting structures, mist rising from the marsh, fishing nets drying on poles, isolated and self-sufficient",
    "abandoned border fort in tall grass, earthwork walls overgrown with wildflowers, wooden watchtowers leaning dangerously, wide sky over flat landscape, wind bending the grass in waves",

    # DESERT & ANCIENT NEAR EAST (8)
    "desert canyon city with dwellings carved into cliff faces, ladders connecting levels, smoke from cooking fires emerging from rock-cut chimneys, afternoon shadows filling the canyon floor",
    "ruined ziggurat rising from desert sands, massive stepped structure of mud brick weathered by millennia, sand dunes encroaching on the base, harsh midday sun casting sharp shadows",
    "oasis town with mud-brick walls, palm trees providing shade over a spring-fed pool, market stalls with colourful awnings, camels resting in the shade, heat shimmer on distant dunes",
    "desert fortress on a rocky outcrop, thick walls with few windows against the heat, watchtower scanning empty horizons, well in the central courtyard, refuge in hostile wilderness",
    "ancient tomb entrance cut into a cliff, massive stone door flanked by weathered guardian statues, hieroglyphs worn almost smooth by sandstorms, dark interior promising secrets",
    "abandoned caravanserai on a desert trade route, roofless rooms around a central courtyard, well now dry, sand drifting through empty doorways, ghosts of commerce past",
    "sandstorm approaching a desert camp, wall of brown dust on the horizon, tents being hastily secured, camels kneeling with backs to the wind, sky turning orange and dark",
    "cliff dwelling village in a desert canyon, multi-storey structures built into natural alcoves, ancient and abandoned, pottery fragments in the dust, silence and dry preservation",

    # JUNGLE & TROPICAL (8)
    "temple pyramid emerging from jungle canopy, massive stone structure with steep stairs, tree roots cracking the masonry, howler monkeys calling from surrounding trees, humid green light",
    "jungle river at dawn, mist rising from warm water, dense vegetation to the waterline, colourful birds taking flight, wooden dugout canoe beached on muddy bank, sounds of waking forest",
    "ruined palace in monsoon rains, stone lions guarding a flooded courtyard, rain hammering ancient tiles, vegetation pushing through every crack, grey sky and sheets of water",
    "jungle cenote with crystal clear water, natural sinkhole with sheer limestone walls, tree roots hanging down from above, ancient offerings visible in the depths, sacred and hidden",
    "overgrown temple complex, multiple structures being consumed by strangler figs, stone faces emerging from root masses, moss covering carved reliefs, humid oppressive heat",
    "bamboo forest in mountain fog, tall straight stems disappearing into white mist, narrow path between the groves, dripping moisture, filtered grey-green light, meditative silence",
    "terraced rice paddies in mountain highlands, flooded fields reflecting grey sky, farmers working in knee-deep water, small huts on the ridges between terraces, ancient agricultural engineering",
    "volcanic island with black sand beaches, palm trees bent by constant wind, smoking peak visible through clouds, rough surf crashing on dark shore, dramatic and primal",

    # SEAS & SHIPS (8)
    "medieval harbour at dawn, trading vessels with furled sails, dock workers beginning the day's labour, warehouses along the waterfront, morning mist on the water, smell of tar and fish",
    "ship graveyard at low tide, rotting hulls of wooden vessels exposed on mudflats, ribs of keels like whale skeletons, salvagers picking through debris, grey overcast sky, end of voyages",
    "lighthouse on a storm-battered rock, waves crashing against the base, beam of light cutting through rain and spray, small keeper's cottage huddled beside the tower, violence of nature",
    "pirate cove hidden behind sea stacks, natural harbour with a crescent of sand, wooden structures built against the cliff, captured ship at anchor, smoke from cooking fires, outlaw refuge",
    "frozen ship trapped in pack ice, rigging heavy with frost, crew's footprints in snow leading to nearby camp, pressure ridges of ice surrounding the hull, arctic survival situation",
    "sea battle aftermath at sunset, burning ships on the horizon, debris and bodies in the water, surviving sailors clinging to wreckage, orange sky reflecting on oil-slicked waves, devastation",
    "fishing fleet returning at dusk, small boats with lanterns lit, harbour lights welcoming them home, families waiting on the dock, smell of the day's catch, end of honest labour",
    "ghost ship emerging from fog bank, ragged sails hanging limp, no crew visible on deck, barnacles covering the waterline, drifting without purpose, unexplained and unsettling",

    # MYSTICAL NATURAL PLACES (8)
    "ancient oak in a forest clearing, trunk so wide a door has been carved into it, gnarled branches spreading over the entire clearing, offerings left at the roots, meeting place for centuries",
    "tidal island accessible only at low tide, ruined priory on the rocky summit, causeway of wet sand connecting to mainland, pilgrims crossing before the waters return, liminal and sacred",
    "waterfall shrine behind the cascade, small cave altar visible through the curtain of water, rainbow in the spray, pilgrims' ribbons tied to nearby branches, natural temple",
    "meteorite crater lake, perfectly circular body of dark water, no vegetation on the inner slopes, sense of cosmic violence preserved in the landscape, still and mysterious",
    "petrified forest at sunset, stone tree trunks casting long shadows, ancient wood turned to colourful mineral, desert landscape of frozen time, amber light on crystalline surfaces",
    "geothermal valley with boiling mud pools, steam vents hissing from cracks in the earth, mineral deposits in vivid yellows and oranges, boardwalk path through dangerous terrain, hellish beauty",
    "sea cave at high tide, waves surging into a vast cavern, natural light from the entrance illuminating the interior, thunder of water echoing off walls, salt spray filling the air",
    "aurora over a frozen lake, green and purple lights rippling across the sky, perfect reflection in the ice, snow-covered pines along the shore, absolute silence, natural wonder",

    # CELTIC & MYTHIC BRITAIN (8)
    "iron age hillfort at dawn, concentric earthwork ditches and wooden palisade walls, roundhouses with conical thatched roofs, morning cook fires sending smoke into grey sky, cattle grazing on the slopes below",
    "drowned forest at low tide, ancient oak stumps exposed on a beach, preserved by peat for millennia, grey waves lapping at blackened wood, storm clouds gathering offshore, remnant of a lost landscape",
    "crannog dwelling on a misty loch, circular wooden house on an artificial island, timber causeway connecting to shore, fishing nets drying on poles, smoke rising through the roof, bronze age isolation",
    "chalk giant carved into a hillside, ancient figure cut through turf to white bedrock, sheep grazing around the outline, overcast sky stretching to distant downs, mysterious origin and purpose",
    "tin mine on a moorland hillside, stone engine house with crumbling chimney stack, spoil heaps of pale waste rock, rusted winding gear, gorse and heather reclaiming the workings, industrial archaeology",
    "holy well in a forest hollow, stone basin collecting spring water, clouties tied to overhanging branches, worn steps leading down to the water, dappled light through oak leaves, folk devotion",
    "passage tomb at winter solstice, grass-covered mound with stone entrance passage, dawn light beginning to penetrate the interior, frost on the surrounding grass, five thousand years of waiting",
    "cliff monastery on a sea stack, beehive stone cells clinging to impossible rock, wooden ladders the only access, atlantic waves crashing below, grey sky and wheeling seabirds, extreme devotion",

    # NORDIC & ICELANDIC (8)
    "turf farmstead in a glacial valley, traditional longhouse with grass-covered roof blending into hillside, sheep scattered on surrounding slopes, glacier visible at valley head, isolation and endurance",
    "black sand beach with basalt sea stacks, dark volcanic sand against white surf, columnar basalt formations like frozen organ pipes, low grey clouds, wind-driven rain, alien and dramatic",
    "geothermal rift valley, steam rising from cracks in dark volcanic rock, milky blue hot spring pools, orange and yellow mineral deposits, mountains on either side, tectonic forces visible",
    "viking assembly site on a flat plain, natural amphitheatre formed by rock walls, law rock where speakers stood, river running through the site, historical weight of decisions made here",
    "glacial lagoon with floating icebergs, chunks of blue-white ice calved from glacier tongue, still grey water reflecting the ice, black volcanic sand shore, seals hauled out on the bergs",
    "moss-covered lava field stretching to horizon, lumpy green terrain of ancient volcanic flow, no trees breaking the endless green, low clouds and soft light, otherworldly and silent",
    "abandoned turf church in a remote valley, wooden door hanging open, interior dark and damp, graveyard with leaning headstones, mountains closing in on all sides, faith at the edge of habitation",
    "waterfall plunging behind a walking path, curtain of white water with cave passage behind, spray soaking everything, rainbow in the mist when sun breaks through, hidden viewpoint",

    # GERMANIC & CENTRAL EUROPEAN (8)
    "walled medieval town at market day, half-timbered buildings around a cobbled square, market stalls with produce and crafts, town well at the centre, church spire rising above steep rooftops",
    "castle on a river bend, stone walls rising directly from the water, round towers at each corner, vineyards on the slopes behind, morning mist on the river surface, strategic and picturesque",
    "charcoal burner's camp deep in the forest, smouldering mound covered in turf, simple shelter of branches, soot-blackened worker tending the burn, smoke filtering through the trees, solitary trade",
    "salt mine entrance in a mountainside, timber-framed tunnel mouth with rail tracks emerging, mine carts loaded with white crystal, workers in leather aprons, wealth drawn from the earth",
    "monastery brewery courtyard, copper vessels visible through open doors, monks in brown robes rolling barrels, herb garden providing flavourings, steam rising from the brewhouse, industrious contemplation",
    "plague column in a town square, baroque stone monument to pandemic dead, carved saints and angels weathered by time, cobblestones worn smooth around the base, memorial to catastrophe",
    "hanging houses over a river gorge, medieval buildings cantilevered over the drop, wooden balconies overlooking the chasm, river visible far below, engineering confidence of another age",
    "forest glassworks in a clearing, furnace glowing orange through open doors, workers blowing and shaping molten glass, stacks of finished vessels, sand and ash raw materials piled nearby",

    # MEDITERRANEAN & CLASSICAL RUINS (8)
    "roman aqueduct spanning a valley, massive stone arches marching across the landscape, some collapsed into the river below, wildflowers growing on the top channel, engineering for eternity",
    "amphitheatre overgrown with grass, stone seating tiers visible beneath vegetation, arena floor now a meadow, goats grazing where gladiators fought, afternoon sun warming ancient stone",
    "temple columns standing alone in a field, marble pillars with capitals still intact, building they supported long collapsed, olive trees surrounding the site, cicadas loud in summer heat",
    "roman bath complex in ruins, mosaic floors exposed to sky, hypocaust pillars visible in excavated sections, wildflowers growing in the cold plunge pool, faded luxury",
    "cliff-face tombs carved into limestone, decorated facades weathered by millennia, dark doorways leading to burial chambers, goat track winding between the tombs, city of the dead",
    "sunken city visible through clear water, street grid and building foundations below the surface, fish swimming through doorways, boat floating above the ruins, subsidence and time",
    "volcanic ruins preserved in ash, excavated streets with stepping stones, frescoed walls still showing colour, plaster casts of victims, tourists walking where romans walked, frozen catastrophe",
    "byzantine chapel on a rocky island, simple stone structure with faded frescoes inside, fishermen's boats pulled up on the shore, crystal clear water, whitewash bright against blue sea",

    # FORTIFICATIONS & WARFARE (8)
    "star fort from above, geometric bastions designed for artillery defence, moat filled with stagnant green water, grass growing on the earthworks, military mathematics made landscape",
    "siege tower abandoned against castle walls, massive wooden structure burnt and broken, scaling ladders still leaning on the stonework, bodies cleared but weapons remaining, assault failed",
    "trebuchet on a hillside overlooking a fortress, massive timber throwing arm cocked and loaded, stone ammunition piled nearby, crew preparing for the next shot, medieval artillery",
    "battlefield after snowfall, white covering hiding the carnage beneath, broken weapons protruding from the snow, crows gathering despite the cold, peaceful surface over violence",
    "border wall stretching across moorland, stone construction following the ridgeline, milecastles at regular intervals, soldiers patrolling the walkway, empire's edge marked in stone",
    "breached city wall with rubble spilling inward, gap where artillery finally broke through, burnt buildings visible beyond, victorious soldiers entering the breach, moment of conquest",
    "military cemetery in neat rows, simple wooden crosses marking fresh graves, larger memorial at the head of the field, rain falling on the raw earth, organised grief",
    "watchtower on fire at night, flames visible for miles, signal passed to the next tower on the horizon, alarm spreading across the frontier, invasion warning system activated",

    # HARSH ENVIRONMENTS (8)
    "mountain hermitage carved into a sheer cliff, wooden platforms and ladders providing access, prayer flags snapping in the wind, clouds below the level of the dwelling, extreme isolation",
    "arctic hunting camp on sea ice, skin tents weighted with stones, dog teams staked nearby, seal carcass being butchered, hunters silhouetted against vast white expanse, survival skills",
    "desert well surrounded by date palms, stone-lined pit with rope and bucket, camel caravan watering before continuing, precious water in hostile land, life at the oasis",
    "highland shieling in summer pasture, simple stone shelter for seasonal herders, cattle grazing on mountain grass, distant view of glens below, transhumance tradition",
    "peat cutting on a windswept bog, rectangular pools where fuel has been extracted, cut blocks drying in stacks, crofter working with traditional tool, landscape as fuel source",
    "ice cave inside a glacier, blue light filtering through the frozen ceiling, meltwater stream running along the floor, walls of compressed ice showing annual layers, inside the frozen river",
    "storm shelter in a mountain pass, rough stone walls and turf roof, barely visible against the hillside, built to save lives in sudden weather, refuge in dangerous terrain",
    "salt flat stretching to every horizon, cracked white surface with distant mountains shimmering in heat haze, perfect geometric patterns in the dried crust, blinding brightness at midday",

    # INDUSTRIAL & WORKING LANDSCAPES (8)
    "iron bloomery in a forest clearing, clay furnace glowing with charcoal heat, bellows being worked by apprentices, raw iron being extracted and hammered, birth of metal",
    "quarry cut deep into a hillside, massive stone blocks being levered and lifted, crane powered by human treadmill, dust hanging in the air, cathedral stone being born",
    "water mill on a fast-flowing stream, wooden wheel turning steadily, grain sacks waiting to be ground, miller dusted white with flour, mechanical power from nature",
    "rope walk stretching between buildings, workers twisting hemp fibres into cordage, long covered shed protecting the process, maritime industry supporting fleets, skilled repetitive labour",
    "tannery beside a river, hides soaking in foul-smelling pits, workers scraping and treating leather, wooden frames with stretched skins drying, necessary but noisome trade",
    "pottery workshop with drying racks, clay vessels in various stages of completion, kiln smoking in the yard, potter at the wheel shaping with wet hands, ancient craft continuing",
    "shipyard at low tide, wooden hull taking shape on the slipway, workers swarming over the skeleton frame, smell of tar and fresh timber, vessel being born for the sea",
    "fulling mill processing wool cloth, water-powered hammers pounding fabric, workers hanging wet cloth to dry on frames, stream running milky with lanolin, textile finishing",

    # SACRED & SPIRITUAL PLACES (8)
    "pilgrimage church at journey's end, grand facade after weeks of walking, pilgrims kneeling in the square, scallop shell symbols everywhere, destination achieved at last",
    "hermit's cell built against a boulder, tiny stone structure with single window, vegetable garden scratched from poor soil, path worn by those seeking wisdom, chosen solitude",
    "monastery scriptorium with high windows, desks arranged to catch the light, monks bent over manuscripts, ink and gold leaf and vellum, knowledge preserved through dark ages",
    "baptistry with sunken pool, octagonal building with domed roof, light entering through high windows, still water awaiting the faithful, architecture of transformation",
    "charnel house with stacked bones, skulls arranged in decorative patterns, femurs forming walls, memento mori made physical, medieval death acceptance",
    "leper chapel outside city walls, small stone building with separate entrance for the afflicted, alms window in the wall, bell to warn of approach, care at a distance",
    "wayside shrine at a dangerous crossing, small roofed structure protecting a carved figure, candles and flowers left by travellers, prayers for safe passage, faith at the roadside",
    "ruined abbey in a river valley, gothic arches open to the sky, grass growing in the nave, sheep grazing in the cloister, dissolution and decay of religious power",
]

# Keep LOCATIONS as alias for backwards compatibility
LOCATIONS = LOCATIONS_REALISTIC

ATMOSPHERES = [
    "intimate", "dramatic", "peaceful", "tense", "melancholic",
    "joyful", "mysterious", "romantic", "contemplative",
    "energetic", "serene", "moody", "vibrant", "nostalgic",
    "ethereal", "raw", "warm", "cool", "cinematic",
]

LIGHTINGS = [
    "soft natural light", "harsh sunlight", "overcast diffused light",
    "warm lamp light", "cool blue light", "neon lights",
    "candlelight", "firelight", "studio lighting",
    "rim lighting", "backlit", "side lighting",
    "dramatic chiaroscuro", "soft window light", "dappled light through leaves",
]

# ═══════════════════════════════════════════════════════════════════════════
#                           REALISTIC OUTFITS
# ═══════════════════════════════════════════════════════════════════════════
OUTFITS_CASUAL = [
    "fitted t-shirt and jeans",
    "oversized sweater and leggings",
    "sundress",
    "button-down shirt, sleeves rolled up",
    "hoodie and joggers",
    "tank top and shorts",
    "casual blazer over t-shirt",
    "flowy blouse and skirt",
    "denim jacket and dress",
]

OUTFITS_FORMAL = [
    "elegant black dress",
    "tailored suit",
    "evening gown",
    "cocktail dress",
    "sharp blazer and trousers",
    "silk blouse and pencil skirt",
    "tuxedo",
    "fitted dress with heels",
]

OUTFITS_ATHLETIC = [
    "sports bra and leggings",
    "running outfit",
    "yoga wear",
    "gym clothes",
    "athletic tank and shorts",
    "compression wear",
]

ACCESSORIES_REALISTIC = [
    "simple necklace", "layered necklaces", "statement earrings",
    "small hoop earrings", "stud earrings", "bracelet",
    "watch", "rings", "sunglasses", "glasses",
    "scarf", "hat", "headband", "hair clips",
    "", "", "",  # Empty for variety
]

FOOTWEAR_REALISTIC = [
    "sneakers", "heels", "boots", "sandals", "loafers",
    "bare feet", "flats", "ankle boots", "running shoes",
    "", "",  # Empty for variety
]

# ═══════════════════════════════════════════════════════════════════════════
#                           FANTASY OUTFITS
# ═══════════════════════════════════════════════════════════════════════════
OUTFITS_FANTASY_COMMON = [
    "simple tunic and trousers",
    "rough-spun peasant clothes",
    "traveling cloak over simple garments",
    "leather vest and breeches",
    "homespun dress with apron",
    "patched traveler's outfit",
    "woodsman's garb",
    "village worker's attire",
]

OUTFITS_FANTASY_NOBLE = [
    "elegant elven robes with silver embroidery",
    "royal gown with flowing sleeves",
    "ornate court dress with gold trim",
    "noble's doublet and fine breeches",
    "silk robes with arcane patterns",
    "velvet cloak over fine garments",
    "ceremonial armor with decorative filigree",
    "high-collared mage robes",
]

OUTFITS_FANTASY_WARRIOR = [
    "battle-worn leather armor",
    "chainmail shirt over padded gambeson",
    "plate armor with clan insignia",
    "ranger's hooded cloak and leather gear",
    "barbarian furs and war paint",
    "knight's surcoat over armor",
    "mercenary's mismatched armor pieces",
    "scout's dark leather outfit",
]

OUTFITS_FANTASY_MAGIC = [
    "flowing wizard robes with star patterns",
    "druid's earth-toned vestments",
    "necromancer's dark hooded robes",
    "enchanter's shimmering garments",
    "alchemist's stained work clothes",
    "seer's veiled ceremonial dress",
    "warlock's leather and cloth ensemble",
    "mystic's rune-covered wrappings",
]

ACCESSORIES_FANTASY = [
    "amulet on leather cord", "pendant with glowing gem", "silver circlet",
    "ear cuffs with elven design", "enchanted rings", "arm bands with runes",
    "leather bracers", "feathered hair ornament", "bone jewelry",
    "crystal pendant", "clan brooch", "holy symbol on chain",
    "gemstone earrings", "woven friendship bracelet", "seer's eye pendant",
    "", "", "",  # Empty for variety
]

FOOTWEAR_FANTASY = [
    "leather boots", "elven soft-soled shoes", "armored greaves",
    "wrapped cloth foot bindings", "fur-lined winter boots",
    "bare feet", "ornate sandals", "riding boots",
    "forest moccasins", "enchanted slippers",
    "", "",  # Empty for variety
]

# Backwards compatibility aliases
ACCESSORIES_OPTIONS = ACCESSORIES_REALISTIC
FOOTWEAR_OPTIONS = FOOTWEAR_REALISTIC


def random_hair() -> str:
    """Generate random hair description."""
    color = random.choice(HAIR_COLORS)
    length = random.choice(HAIR_LENGTHS)
    style = random.choice(HAIR_STYLES)
    return f"{length} {color} hair, {style}"


def random_outfit(genre: str = "realistic") -> str:
    """Generate random outfit based on genre."""
    if genre == "fantasy":
        category = random.choice(["common", "common", "noble", "warrior", "magic"])
        if category == "common":
            return random.choice(OUTFITS_FANTASY_COMMON)
        elif category == "noble":
            return random.choice(OUTFITS_FANTASY_NOBLE)
        elif category == "warrior":
            return random.choice(OUTFITS_FANTASY_WARRIOR)
        else:
            return random.choice(OUTFITS_FANTASY_MAGIC)
    else:
        category = random.choice(["casual", "casual", "formal", "athletic"])
        if category == "casual":
            return random.choice(OUTFITS_CASUAL)
        elif category == "formal":
            return random.choice(OUTFITS_FORMAL)
        else:
            return random.choice(OUTFITS_ATHLETIC)


def randomize_subject(genre: str = "realistic") -> Dict[str, Any]:
    """
    Generate random values for all subject fields.

    Args:
        genre: "realistic" for real-world ethnicities, "fantasy" for fantasy races

    Returns:
        Dictionary with randomized field values
    """
    # Filter out NA and custom from body types for random selection
    valid_body_types = [bt for bt in BODY_TYPES_ALL if bt not in ("NA", "custom")]

    # Filter out NA and custom from genders
    valid_genders = [g for g in GENDERS if g not in ("NA", "custom")]

    # Select genre-appropriate options
    if genre == "fantasy":
        ethnicity_choices = [e for e in ETHNICITIES_FANTASY if e not in ("NA", "custom")]
        accessories_choices = ACCESSORIES_FANTASY
        footwear_choices = FOOTWEAR_FANTASY
    else:
        ethnicity_choices = [e for e in ETHNICITIES_REALISTIC if e not in ("NA", "custom")]
        accessories_choices = ACCESSORIES_REALISTIC
        footwear_choices = FOOTWEAR_REALISTIC

    return {
        "age": random.choice(AGES),
        "gender": random.choice(valid_genders),
        "ethnicity": random.choice(ethnicity_choices),
        "body_type": random.choice(valid_body_types),
        "body_type_custom": "",
        "hair": random_hair(),
        "face": "",  # Leave for user - too complex to randomize well
        "expression": random.choice(EXPRESSIONS),
        "gaze": random.choice(GAZES),
        "hands": random.choice(HAND_POSITIONS),
        "skin_texture": random.choice(SKIN_TEXTURES),
        "skin_details": random.choice(SKIN_DETAILS_OPTIONS),
        "extras": "",  # Leave for user
        "outfit": random_outfit(genre=genre),
        "accessories": random.choice(accessories_choices),
        "footwear": random.choice(footwear_choices),
        "pose": random.choice(POSES),
    }


def randomize_scene(genre: str = "realistic") -> Dict[str, Any]:
    """
    Generate random values for scene fields.

    Args:
        genre: "realistic" for real-world locations, "fantasy" for magical locations

    Returns:
        Dictionary with randomized scene values
    """
    # Filter out NA and custom from dropdowns
    valid_times = [t for t in TIMES if t not in ("NA", "custom")]
    valid_weathers = [w for w in WEATHERS if w not in ("NA", "custom")]
    valid_framings = [f for f in FRAMINGS if f not in ("NA", "custom")]
    valid_angles = [a for a in CAMERA_ANGLES if a not in ("NA", "custom")]

    # Select location based on genre
    if genre == "fantasy":
        location = random.choice(LOCATIONS_FANTASY)
        era = "fantasy"
    else:
        location = random.choice(LOCATIONS_REALISTIC)
        era = "modern"

    return {
        "location": location,
        "time": random.choice(valid_times),
        "weather": random.choice(valid_weathers),
        "atmosphere": random.choice(ATMOSPHERES),
        "props": "",  # Leave for user
        "background": "",  # Leave for user
        "era": era,
        "action": "",  # Leave for user
        "story": "",  # Leave for user
        "lighting": random.choice(LIGHTINGS),
        "framing": random.choice(valid_framings),
        "camera_angle": random.choice(valid_angles),
    }
