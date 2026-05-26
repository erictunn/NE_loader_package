"""Finds system cache directory for caching of NE data."""

import os
from typing import Optional
from platformdirs import user_cache_dir

def get_cache_dir(path_override: Optional[str] = None):
    """Returns a path to read or write NE data to or from.
    In order of precedence:
    1. Override for the path.
    2. Environment override for the path.
    3. OS cache.

    Args:
        path_override (str | None, optional): _description_. Defaults to None.

    Returns:
        _type_: Path 
    """

    if path_override:
        return path_override

    env_path = os.getenv("NATURAL_EARTH_CACHE_DIR")
    if env_path:
        return env_path

    path = user_cache_dir(appname="ne-loader", appauthor="erictunn")
    return path
