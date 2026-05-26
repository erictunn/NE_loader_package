"""Resolve the cache directory used for downloaded Natural Earth data."""

import os
from pathlib import Path
from typing import Optional, Union

from platformdirs import user_cache_dir


PathLike = Union[str, Path]


def get_cache_dir(path_override: Optional[PathLike] = None) -> Path:
    """Return the directory used to cache Natural Earth downloads.

    Cache directory in order of precedence:

    1. Explicit function argument 'path_override'
    2. ``NATURAL_EARTH_CACHE_DIR`` environment variable.
    3. Platform-specific user cache directory.

    Args:
        path_override: Optional cache directory 

    Returns:
        A ``pathlib.Path`` pointing to the cache directory.
    """

    if path_override:
        return Path(path_override).expanduser()

    env_path: Optional[str] = os.getenv("NATURAL_EARTH_CACHE_DIR")
    if env_path:
        return Path(env_path).expanduser()

    default_cache_dir: str = user_cache_dir(appname="ne-loader", appauthor="erictunn")
    return Path(default_cache_dir)
