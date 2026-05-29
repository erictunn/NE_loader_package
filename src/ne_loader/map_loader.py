"""Handles downloading and fetching of NE data."""

import logging
import zipfile
from pathlib import Path
from typing import Optional, Union

import geopandas as gpd
import requests

from .cacher import PathLike, get_cache_dir
from .error_handler import ErrorMode, error_handler, validate_error_mode


def build_ne_filename(name: str, res: str = "10m", suffix: str = ".zip") -> str:
    """Build a Natural Earth dataset filename."""
    return f"ne_{res}_{name}{suffix}"


def build_ne_url(category: str, name: str, res: str = "10m") -> str:
    """Build the download URL for a Natural Earth vector dataset."""
    return (
        f"https://naciscdn.org/naturalearth/{res}/{category}/"
        f"{build_ne_filename(name, res)}"
    )


def build_ne_zip_path(data_dir: PathLike, name: str, res: str = "10m") -> Path:
    """Build the local cache path for a Natural Earth zip file."""
    return Path(data_dir) / build_ne_filename(name, res)


def build_ne_extract_dir(data_dir: PathLike, name: str, res: str = "10m") -> Path:
    """Build the local extraction directory for a Natural Earth dataset."""
    return Path(data_dir) / build_ne_filename(name, res, suffix="")


def build_ne_shp_path(data_dir: PathLike, name: str, res: str = "10m") -> Path:
    """Build the local shapefile path for an extracted Natural Earth dataset."""
    extract_dir: Path = build_ne_extract_dir(data_dir, name, res)
    return extract_dir / build_ne_filename(name, res, suffix=".shp")


def get_natural_earth(
    category: str,
    name: str,
    res: str = "10m",
    dir_override: Optional[PathLike] = None,
    error_mode: ErrorMode = "raise",
) -> Union[gpd.GeoDataFrame, Exception, None]:
    """Download, cache, and load a Natural Earth vector dataset.

    Args:
        category: Natural Earth data category, e.g. "cultural" or
            "physical".
        name: Dataset name without the ``ne_{res}_`` prefix, e.g.
            "admin_0_countries".
        res: Natural Earth resolution. "10m", "50m" and "110m" are accepted.
            However, not all datasets will have all 3 resolutions available.
        dir_override: Optional cache directory override. This takes precedence over the
            ``NATURAL_EARTH_CACHE_DIR`` environment variable.
        error_mode: Error handling mode. Default is raise.
            ``"ignore"`` returns None,
            ``"raise"`` raises the error,
            and ``"return"`` returns the exception object.

    Returns:
        A GeoPandas ``GeoDataFrame`` loaded from the cached shapefile.

    """
    try:
        validate_error_mode(error_mode)
        logger: logging.Logger = logging.getLogger(__name__)

        data_dir: Path = get_cache_dir(dir_override)
        data_dir.mkdir(parents=True, exist_ok=True)

        url: str = build_ne_url(category, name, res)
        zip_path: Path = build_ne_zip_path(data_dir, name, res)
        extract_dir: Path = build_ne_extract_dir(data_dir, name, res)
        shp_file: Path = build_ne_shp_path(data_dir, name, res)

        _download_ne_data(
            url=url,
            extract_dir=extract_dir,
            name=name,
            res=res,
            zip_path=zip_path,
            shp_file=shp_file,
            logger=logger,
        )

        return gpd.read_file(shp_file)
    except Exception as error:
        return error_handler(error, error_mode)


def _download_ne_data(
    url: str,
    extract_dir: Path,
    name: str,
    res: str,
    zip_path: Path,
    shp_file: Path,
    logger: logging.Logger,
) -> None:
    """Download and extract a dataset when the expected shapefile is absent."""
    if shp_file.exists():
        return

    print(f"ne-loader: Downloading {name} ({res})...")

    try:
        response: requests.Response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        with zip_path.open("wb") as zip_file:
            chunk: bytes
            for chunk in response.iter_content(chunk_size=8192):
                zip_file.write(chunk)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        zip_path.unlink()
        return None

    except requests.exceptions.HTTPError as error:
        logger.error(
            "ne-loader: A HTTP error occurred while attempting to fetch data: %s\n"
            "This may cause an error when attempting to load the data.",
            error,
        )
        print(f"A HTTP error occurred while attempting to fetch data: {error}")
        raise
    except requests.exceptions.RequestException as error:
        logger.error(
            "ne-loader: A request error occurred while attempting to fetch data: %s\n"
            "This may cause an error when attempting to load the data.",
            error,
        )
        print(f"A request error occurred while attempting to fetch data: {error}")
        raise
