import yaml
import json


def load_yaml_config(file_path):
    """Load a YAML configuration file."""
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def load_json_config(file_path):
    """Load a JSON configuration file."""
    with open(file_path, "r") as file:
        return json.load(file)


def parse_fsm_config(file_path, file_type="yaml"):
    """Load FSM configuration (YAML or JSON)."""
    if file_type == "yaml":
        return load_yaml_config(file_path)
    elif file_type == "json":
        return load_json_config(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
