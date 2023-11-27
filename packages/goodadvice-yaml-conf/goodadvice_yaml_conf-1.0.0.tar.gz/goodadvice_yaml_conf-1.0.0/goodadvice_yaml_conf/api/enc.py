import json
import yaml
import base64

encode_choices = {
    'json': json.dumps,
    'yaml': yaml.dump,
    'base64': base64.b64encode,
}

decode_choices = {
    'json': json.loads,
    'yaml': yaml.safe_load,
    'base64': base64.b64decode,
}

def _strip_for_chaining(s: str) -> list[str]:
    if not s:
        return []
    if isinstance(s, (list, tuple)):
        return s
    a = []
    for i in s.split(';'):
        i = i.strip()
        if i:
            a.append(i)
    return a

def encode_chain(s: str, encodings: str) -> str:
    """
        Encode a string using a chain of encodings.
        Example:
            encode_chain('hello', 'json; base64') -> 'aGVsbG8='
    """
    encodings = _strip_for_chaining(encodings)
    for encoding in encodings:
        s = encode_choices[encoding](s)
    return s

def decode_chain(s: str, encodings: str) -> (dict | list):
    """
        Decode a string using a chain of encodings.
        Example:
            decode_chain('aGVsbG8=', 'json; base64') -> 'hello'
    """
    encodings = _strip_for_chaining(encodings)
    for encoding in reversed(encodings):
        s = decode_choices[encoding](s)
    return s



