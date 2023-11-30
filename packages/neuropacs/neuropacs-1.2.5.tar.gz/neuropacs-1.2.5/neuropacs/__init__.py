# __init__.py
from .sdk import neuropacs

PACKAGE_VERSION = "1.2.5"

def init(api_key, server_url):
    return neuropacs(api_key=api_key, server_url=server_url)


