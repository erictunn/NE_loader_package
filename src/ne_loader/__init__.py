"""Natural Earth Loader package.

See map_loader.py for public API entrypoint.
"""

from .map_loader import get_natural_earth, Resolution

__all__ = ["get_natural_earth", "Resolution"]
