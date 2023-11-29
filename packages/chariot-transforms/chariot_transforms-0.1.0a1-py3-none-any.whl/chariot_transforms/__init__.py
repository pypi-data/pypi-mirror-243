from importlib import metadata

try:
    __version__ = metadata.version("chariot_transforms")
except Exception:
    __version__ = "0.0.0-dev"
del metadata
