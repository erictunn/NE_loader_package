import logging
import zipfile
from pathlib import Path
from typing import Optional

import geopandas as gpd
import requests

from .cacher import PathLike, get_cache_dir


def get_natural_earth(
    category: str,
    name: str,
    res: str = "10m",
    dir_override: Optional[PathLike] = None,
) -> gpd.GeoDataFrame:
    """Download, cache, and load a Natural Earth vector dataset.

    Args:
        category: Natural Earth data category, e.g. "cultural" or
            "physical".
        name: Dataset name without the ``ne_{res}_`` prefix, e.g.
            "admin_0_countries".
        res: Natural Earth resolution. "10m", "50m" and "110m" are accepted.
            however, not all datasets will have all 3 resolutions available.
        dir_override: Optional cache directory override. This takes precedence over the
            ``NATURAL_EARTH_CACHE_DIR`` environment variable.

    Returns:
        A GeoPandas ``GeoDataFrame`` loaded from the cached shapefile.
    """
    logger: logging.Logger = logging.getLogger(__name__)

    data_dir: Path = get_cache_dir(dir_override)
    data_dir.mkdir(parents=True, exist_ok=True)

    base_url: str = f"https://naciscdn.org/naturalearth/{res}/{category}/"
    filename: str = f"ne_{res}_{name}.zip"
    url: str = base_url + filename

    zip_path: Path = data_dir / filename
    extract_dir: Path = data_dir / f"ne_{res}_{name}"
    shp_file: Path = extract_dir / f"ne_{res}_{name}.shp"

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

    print(f"Downloading {name} ({res})...")

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

    except requests.exceptions.HTTPError as error:
        logger.error(
            "A HTTP error occurred while attempting to fetch data: %s\n"
            "This may cause an error when attempting to load the data.",
            error,
        )
        print(f"A HTTP error occurred while attempting to fetch data: {error}")
    except requests.exceptions.RequestException as error:
        logger.error(
            "A request error occurred while attempting to fetch data: %s\n"
            "This may cause an error when attempting to load the data.",
            error,
        )
        print(f"A request error occurred while attempting to fetch data: {error}")
