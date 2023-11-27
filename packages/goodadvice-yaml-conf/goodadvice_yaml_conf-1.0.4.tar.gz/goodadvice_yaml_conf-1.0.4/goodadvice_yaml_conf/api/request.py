import requests
from .enc import encode_chain, decode_chain

class EndPoint:
    def __init__(self, url, method="GET", headers={}, encoding="json", data=None):
        if not url:
            raise ValueError("url cannot be empty")
        if not method:
            raise ValueError("method cannot be empty")
        self.url = url
        self.method = method
        self.headers = headers
        self.encoding = encoding
        self.data = data

    def __repr__(self):
        return f"{self.__class__.__name__}(url={self.url}, method={self.method}, headers={self.headers}, encoding={self.encoding}, data={self.data})"
    
    def encode(self) -> str:
        """
            Encode the data attribute using a chain of encodings.
            Example:
                end_point.encode('json; base64')
        """
        if not self.data:
            raise ValueError("data cannot be empty")
        
        return encode_chain(self.data, self.encoding)

    def decode(self, data) -> (dict | list):
        """
            Decode the data attribute using a chain of encodings.
            Example:
                end_point.decode('json; base64')
        """
        return decode_chain(data, self.encoding)

def make_request(end_point: EndPoint) -> (dict | list, requests.Response):
    """
        Make a request to an end point.
        Example:
            make_request(EndPoint(url='https://example.com', method='GET', headers={}, data={}))
    """
    request_kwargs = {}
    request_kwargs['url'] = end_point.url
    request_kwargs['method'] = end_point.method
    if end_point.headers:
        request_kwargs['headers'] = end_point.headers
    if end_point.data:
        request_kwargs['data'] = end_point.encode()
    response = requests.request(**request_kwargs)
    if response.status_code != 200:
        raise ValueError(f"status code is {response.status_code}")
    
    decoded = end_point.decode(response.text)
    return decoded, response


