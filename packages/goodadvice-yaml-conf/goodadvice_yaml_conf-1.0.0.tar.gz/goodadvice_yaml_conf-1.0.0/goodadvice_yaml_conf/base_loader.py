from .api.request import EndPoint, make_request

from typing import Any, AnyStr, Callable, Union, TypedDict

import re
import os


class BaseSearcher:
    def __init__(self, name: str, loader: "BaseLoader"):
        self.name = name
        self.loader = loader
        self._regex = None 

    def _construct_regex(self) -> AnyStr:
        """
            Construct a regex for searching.
            Format: 
                "$name:value"
        """
        if self._regex:
            return self._regex
        regex = r"\$(?P<name>%(name)s):(?P<value>.*)" % {'name': self.name}
        self._regex = re.compile(regex)
        return self._regex
    
    regex = property(_construct_regex)

    def execute(self, name: str, value: Any) -> Any:
        raise NotImplementedError()
    
    def __call__(self, value: Any) -> Union[dict, None]:
        try:
            match = self.regex.match(value)
            if match:
                return self.execute(match['name'], match["value"].strip())
        except re.error as e:
            raise ValueError(f"Error parsing {value} with transformer {self.name}: {e}")
        return value
    
class AttrDict(dict):
    def __getattr__(self, key):
        v = self[key]
        if isinstance(v, dict):
            return AttrDict(v)
        return v
    
    def __setattr__(self, key, value):
        self[key] = value
    
class EndpointData(AttrDict):
    def __init__(self, endpoint, data):
        super().__init__(data)
        self.endpoint = endpoint

    def __repr__(self):
        return f"{self.__class__.__name__}(endpoint={self.endpoint}, data={self.data})"

class EndpointSearcher(BaseSearcher):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._endpoints: TypedDict[str, EndpointData] = {}

    def fetch_data(self, name: str = None) -> list[EndpointData] | EndpointData:
        if not name:
            for endpoint in self.loader._endpoints.values():
                decoded, _ = make_request(endpoint)
                endpoint_data = EndpointData(endpoint, decoded)
                self._endpoints[endpoint.name] = endpoint_data
            return list(self._endpoints.values())
        
        endpoint = self.loader.get_endpoint(name)
        decoded, _ = make_request(endpoint)
        endpoint_data = EndpointData(endpoint, decoded)
        self._endpoints[name] = endpoint_data
        return endpoint_data


    def execute(self, name: str, value: Any) -> Union[dict, None]:
        if name in self._endpoints:
            endpoint = self._endpoints[name]
        else:
            endpoint = self.fetch_data(name)
        return endpoint[value]
    
class EnvSearcher(BaseSearcher):
    def execute(self, name: str, value: Any) -> Union[dict, None]:
        return os.environ.get(value)

class BaseLoader:
    def __getitem__(self, key):
        return self.transform_value(self.data[key])
    
    def __getattr__(self, key):
        return self.__getitem__(key)
    
    def __iter__(self):
        return iter(self.data)
    
    def __len__(self):
        return len(self.data)
    
    def __contains__(self, key):
        return key in self.data
    
    def __repr__(self):
        return f"{self.__class__.__name__}(source={self.source})"

    def __init__(self, source: AnyStr):
        self.source = source
        self._data: Any = None
        self._endpoints: TypedDict[str, EndPoint] = {}
        self.transformers: list[Callable] = self.get_default_transformers()

    def get_default_transformers(self) -> list[Callable]:
        return [
            EnvSearcher("environ", self),
        ]

    def _init_endpoints(self):
        endpoint = self._data.get('endpoint')
        if endpoint:
            kwargs = self.transform_dict(endpoint_kwargs)
            name = kwargs.pop('name')
            self._endpoints[name] = EndPoint(**kwargs)
            self.transformers.append(
                EndpointSearcher(name, self),
            )

        endpoints = self._data.get('endpoints', {})
        for name, endpoint_kwargs in endpoints.items():
            # We want to evaluate the endpoint kwargs as we do all other values
            kwargs = self.transform_dict(endpoint_kwargs)
            self._endpoints[name] = EndPoint(**kwargs)
            self.transformers.append(
                EndpointSearcher(name, self),
            )

    def load(self) -> Any:
        if self._data is None:
            data = self.load_data(str(self.source))
            self.init_data(data)
        return self._data
    
    data = property(load)
    
    def init_data(self, data):
        self._data = data
        self._init_endpoints()

    def keys(self):
        return self.data.keys()
    
    def values(self):
        return self.data.values()
    
    def items(self):
        return self.data.items()
    
    def get(self, key, default=None):
        try:
            data = self.data
            data = data.get(key, default)
        except:
            data = default
        return self.transform_value(data)

    def endpoints(self):
        return self._endpoints.items()

    def load_data(self, source: str) -> Any:
        raise NotImplementedError()
    
    def transform_value(self, value: Any) -> Any:
        if isinstance(value, str):
            return self.transform_string(value)
        elif isinstance(value, dict) or hasattr(value, 'items'):
            return self.transform_dict(value)
        elif isinstance(value, (list, tuple)):
            return self.transform_list(value)
        return value

    def transform_string(self, value: AnyStr) -> Any:
        for transformer in self.transformers:
            value = transformer(value)
            if isinstance(value, (dict, list)):
                break
        return value
    
    def transform_dict(self, value: dict) -> dict:
        for key, val in value.items():
            key = self.transform_string(key)
            value[key] = self.transform_value(val)
        return AttrDict(value)
    
    def transform_list(self, value: list) -> list:
        for i, val in enumerate(value):
            value[i] = self.transform_value(val)
        return value

    def get_endpoint(self, name: str) -> EndPoint:
        endpoint = self._endpoints.get(name)
        if not endpoint:
            raise ValueError(f"Endpoint {name} not found")
        return endpoint


