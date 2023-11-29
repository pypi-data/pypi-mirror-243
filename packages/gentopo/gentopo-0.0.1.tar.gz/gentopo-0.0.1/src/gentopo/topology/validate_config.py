from yaml import safe_load
from glob import glob
from jsonschema import validate


schema = {
    "type": "object",
    "properties": {
        "project": {"type": "string"},
        "topology": {
            "type": "object",
            "properties": {
                "family": {
                    "default": "complete",
                    "enum": ["complete", "random", "small_world", "lattice"],
                },
                "n": {
                    "type": "number",
                    # TODO: Combine with and statement for range of accepted n values
                },
            },
            "required": ["family", "n", "connected", "directed"],
            "allOf": [
                {
                    "if": {
                        "properties": {
                            "family": {"const": "small_world"},
                        },
                    },
                    "then": {
                        "properties": {
                            "params": {
                                "type": "object",
                                "properties": {
                                    "omega_range": {
                                        "type": "array",
                                        "items": {"type": "number"},
                                    },
                                },
                                "required": ["omega_range"],
                            },
                        },
                        "required": ["params"],
                    },
                },
            ],
        },
        "interactions": {"type": "object"},
    },
    "required": ["project", "topology", "interactions"],
}


def validate_config(study_name):
    """Validate config.yml files in the studies directory.

    Args:
        study_name (str): lowercase name of study

    Returns:
        config: dict of config details for generating topologies
    """
    with open(f"studies/{study_name}/config.yml") as file:
        config = safe_load(file)
        validate(instance=config, schema=schema)

    return config
