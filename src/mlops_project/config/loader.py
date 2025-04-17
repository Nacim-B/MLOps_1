import os
import yaml

def load_config(env: str = "dev") -> dict:
    base_path = os.path.dirname(__file__)
    config_path = os.path.join(base_path, f"{env}.yaml")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config