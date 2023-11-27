

def run():

    from pathlib import Path
    import os
    from ..loader import YamlLoader

    path = Path(__file__).parent

    CHECK_IP_URL = "https://checkip.amazonaws.com/"
    CHECK_SECRET_KEY = "What a great secret key!"

    CHECK_URL_A = "https://httpbin.org/get"
    CHECK_URL_B = "https://httpbin.org/post"

    HEADERS_A = {
        "Header-A": "a",
        "Header-B": "b",
        "Header-C": "c",
    }
    HEADERS_B = {
        "Header-D": "d",
        "Header-E": "e",
        "Header-F": "f",
    }

    def get_ip_address():
        import requests
        response = requests.get(CHECK_IP_URL)
        if response.status_code != 200:
            raise ValueError(f"status code is {response.status_code}")
        return response.text.strip()
    
    os.environ["YAML_CONF_DEBUG"] = "True"

    loader = YamlLoader(os.path.join(path, 'test_conf.yaml'))

    settings = loader.settings
    
    secret_key = settings.SECRET_KEY
    yaml_conf_debug = settings.DEBUG

    origin_a = settings.ORIGIN_A
    origin_b = settings.ORIGIN_B
    url_a = settings.URL_A
    url_b = settings.URL_B
    headers_a = settings.HEADERS_A
    headers_b = settings.HEADERS_B

    actual_ip = get_ip_address()
    
    if secret_key != CHECK_SECRET_KEY:
        raise ValueError(f"secret_key is not {CHECK_SECRET_KEY}")
            
    if yaml_conf_debug != "True":
        raise ValueError(f"yaml_conf_debug is not True: {yaml_conf_debug}")

    if origin_a != actual_ip:
        raise ValueError(f"origin_a is not {actual_ip}")
    
    if origin_b != actual_ip:
        raise ValueError(f"origin_b is not {actual_ip}")
    
    if url_a != CHECK_URL_A:
        raise ValueError(f"url_a is not {CHECK_URL_A}")
    
    if url_b != CHECK_URL_B:
        raise ValueError(f"url_b is not {CHECK_URL_B}")

    for key, value in HEADERS_A.items():
        if key not in headers_a:
            raise ValueError(f"headers_a does not contain {key}: {headers_a}")
        if headers_a[key] != value:
            raise ValueError(f"headers_a[{key}] is not {value}: {headers_a[key]}")
    
    for key, value in HEADERS_B.items():
        if key not in headers_b:
            raise ValueError(f"headers_b does not contain {key}: {headers_b}")
        if headers_b[key] != value:
            raise ValueError(f"headers_b[{key}] is not {value}: {headers_b[key]}")
        
    print("All tests passed!")
    print(f"\tsecret_key: \n\t\t{secret_key}")
    print(f"\tyaml_conf_debug: \n\t\t{yaml_conf_debug}")
    print(f"\torigin_a: \n\t\t{origin_a}")
    print(f"\torigin_b: \n\t\t{origin_b}")
    print(f"\turl_a: \n\t\t{url_a}")
    print(f"\turl_b: \n\t\t{url_b}")
    print(f"\theaders_a: \n\t\t{headers_a}")
    print(f"\theaders_b: \n\t\t{headers_b}")