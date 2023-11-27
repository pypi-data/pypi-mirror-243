from .base_loader import BaseLoader
from typing import Any
import json

try:
    from yaml import safe_load as load

    def load_yaml(file):
        with open(file, 'r') as f:
            return load(f)

    class YamlLoader(BaseLoader):
        def load_data(self, source: str) -> Any:
            return load_yaml(source)
except ImportError:
    class YamlLoader(BaseLoader):
        def load_data(self, source: str) -> Any:
            raise ImportError("PyYAML is not installed")
        
class JsonLoader(BaseLoader):
    def load_data(self, source: str) -> Any:
        with open(source, 'r') as f:
            return json.load(f)

def _extract(value: str) -> str:
    """
        Extract a value from the environment.
        The value might be quoted, or end with a comment.
        Example:
            extract("hello # comment") -> "hello"
            extract("'hello # comment'") -> "'hello # comment'"
    """
    value = value.strip()
    opener = value[0]

    if opener in ["'", '"']:
        i = 1
        while i < len(value):
            if value[i] == opener and value[i - 1] != '\\':
                return value[:i + 1]
            i += 1
        return value  # Return as is if closing quote is not found
    else:
        return value.split('#', 1)[0].strip()
        
class EnvLoader(BaseLoader):
    def load_data(self, source: str) -> Any:
        data = {}
        with open(source, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                data[key] = _extract(value)
        return data
    
    def get_list(self, key):
        return self.data.get(key, '').split(' ')
    

