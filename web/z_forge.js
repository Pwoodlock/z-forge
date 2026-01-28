/**
 * Z-Forge Widget Updater
 *
 * Handles visual updates to widget fields when randomization occurs.
 * When the node is executed with randomize enabled, the server returns
 * randomized values that this script uses to update the widget display.
 *
 * Also handles dynamic dropdown filtering for genre-based ethnicity options.
 */
import { app } from "../../scripts/app.js";

// Ethnicity preset lists (must match presets.py)
const ETHNICITIES_REALISTIC = [
    "NA",
    // East Asian
    "Japanese", "Korean", "Chinese", "Vietnamese", "Thai", "Filipino",
    // South Asian
    "Indian", "Pakistani", "Bangladeshi",
    // Middle Eastern
    "Arab", "Persian", "Turkish", "Kurdish",
    // African
    "Nigerian", "Ethiopian", "Kenyan", "South African", "Egyptian",
    // European
    "British", "Irish", "German", "French", "Italian", "Spanish", "Scandinavian", "Slavic",
    // Americas
    "African American", "Mexican", "Brazilian", "Puerto Rican", "Indigenous American",
    // Pacific
    "Polynesian", "Hawaiian", "Maori",
    // Mixed
    "mixed", "biracial",
    "custom"
];

const ETHNICITIES_FANTASY = [
    "NA",
    // Core races
    "human", "elf", "high-elf", "wood-elf", "dark-elf", "sea-elf", "sun-elf", "moon-elf",
    "dwarf", "mountain-dwarf", "hill-dwarf",
    "halfling", "gnome",
    "orc", "half-orc", "half-elf",
    "tiefling", "dragonborn", "aasimar",
    // Genasi
    "genasi-fire", "genasi-water", "genasi-earth", "genasi-air",
    // Beastfolk
    "tabaxi", "kenku", "lizardfolk",
    // Goblinoids
    "goblin", "hobgoblin", "kobold",
    "custom"
];

/**
 * Setup dynamic ethnicity dropdown based on genre selection
 * Uses Object.defineProperty to make dropdown values dynamic
 */
function setupGenreBasedEthnicity(node, genreWidgetName, ethnicityWidgetName) {
    const genreWidget = node.widgets.find(w => w.name === genreWidgetName);
    const ethnicityWidget = node.widgets.find(w => w.name === ethnicityWidgetName);

    if (!genreWidget || !ethnicityWidget) return;

    // Make ethnicity dropdown values dynamic based on genre
    Object.defineProperty(ethnicityWidget.options, "values", {
        get: function() {
            return genreWidget.value === "fantasy" ? ETHNICITIES_FANTASY : ETHNICITIES_REALISTIC;
        }
    });

    // When genre changes, reset ethnicity if current value is invalid for new genre
    const originalCallback = genreWidget.callback;
    genreWidget.callback = function(value) {
        if (originalCallback) originalCallback.call(this, value);

        const validOptions = value === "fantasy" ? ETHNICITIES_FANTASY : ETHNICITIES_REALISTIC;
        if (!validOptions.includes(ethnicityWidget.value)) {
            ethnicityWidget.value = "NA";
        }
        app.graph.setDirtyCanvas(true, true);
    };
}

app.registerExtension({
    name: "ZForge.WidgetUpdater",

    async nodeCreated(node) {
        // Handle main prompt builder node
        if (node.comfyClass === "ZForgePromptBuilder") {
            setupWidgetUpdater(node);
            setupGenreBasedEthnicity(node, "genre", "person_1_ethnicity");
        }

        // Handle person nodes
        if (node.comfyClass === "ZForgePerson") {
            setupWidgetUpdater(node);
            setupGenreBasedEthnicity(node, "genre", "ethnicity");
        }
    }
});

/**
 * Set up widget update handling for a node
 */
function setupWidgetUpdater(node) {
    // Store reference to track last randomization
    node._zforge_last_randomized = null;

    // Hook into execution results
    const originalOnExecuted = node.onExecuted;
    node.onExecuted = function(message) {
        // Call original handler if exists
        if (originalOnExecuted) {
            originalOnExecuted.apply(this, arguments);
        }

        // Check if randomized data was returned (comes as array from UI return)
        if (message && message.randomized_values && message.randomized_values.length > 0) {
            const values = message.randomized_values[0];
            if (values && Object.keys(values).length > 0) {
                updateWidgetsFromRandomized(node, values);
            }
        }
    };
}

/**
 * Update widget values from randomized data
 * @param {Object} node - The ComfyUI node
 * @param {Object} values - Object with widget names as keys and new values
 */
function updateWidgetsFromRandomized(node, values) {
    if (!node.widgets || !values) return;

    let updated = false;

    for (const [key, value] of Object.entries(values)) {
        const widget = node.widgets.find(w => w.name === key);
        if (widget && value !== undefined && value !== null) {
            // Handle different widget types
            if (widget.type === "combo") {
                // For dropdowns, check if value is valid option
                if (widget.options?.values?.includes(value)) {
                    widget.value = value;
                    updated = true;
                }
            } else {
                // For text, number, etc.
                widget.value = value;
                updated = true;
            }
        }
    }

    // Trigger canvas redraw if anything changed
    if (updated) {
        node.setDirtyCanvas(true, true);
    }
}

/**
 * Server-to-client message handler for model list updates
 * Used by ZForgeLLMConfig node to refresh model dropdown
 */
app.registerExtension({
    name: "ZForge.ModelRefresh",

    async setup() {
        // Listen for model list updates from server
        app.api.addEventListener("zforge-models-updated", (event) => {
            const { models } = event.detail;
            if (!models) return;

            // Find all LLM Config nodes and update their dropdowns
            for (const node of app.graph._nodes) {
                if (node.comfyClass === "ZForgeLLMConfig") {
                    updateModelDropdown(node, models);
                }
            }
        });
    }
});

/**
 * Update model dropdown with new model list
 * @param {Object} node - The LLM Config node
 * @param {Array} models - List of model names
 */
function updateModelDropdown(node, models) {
    if (!node.widgets) return;

    const modelWidget = node.widgets.find(w => w.name === "model_selection");
    if (modelWidget && modelWidget.options) {
        // Preserve custom model option at start
        const customOption = ">> Custom Model <<";
        modelWidget.options.values = [customOption, ...models];
        node.setDirtyCanvas(true, true);
    }
}
