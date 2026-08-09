import os
import json
class Argument:
    def __init__(self, args_path):
        self.args_dict = self._load_json_config(args_path)
        for key, value in self.args_dict.items():
            setattr(self, key, value)

    def _load_json_config(self, args_path):
        if os.path.exists(args_path):
            with open(args_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"Config file not found: {config_path}")
class Metrics:
    def __init__(self):
        self.metrics = {}

