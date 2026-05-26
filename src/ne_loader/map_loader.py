import os
import requests
import zipfile
import geopandas as gpd
from .cacher import get_cache_dir

# TODO: Typehint, improve documentation.

def get_natural_earth(category, name, res="10m", dir_override=None):
    """
    Downloads, unzips, and loads Natural Earth vector data.
    Categories: 'cultural', 'physical'
    """

    data_dir = get_cache_dir(dir_override)

    os.makedirs(data_dir, exist_ok=True)


    base_url = f"https://naciscdn.org/naturalearth/{res}/{category}/"
    filename = f"ne_{res}_{name}.zip"
    url = base_url + filename

    zip_path = os.path.join(data_dir, filename)
    extract_dir = os.path.join(data_dir, f"ne_{res}_{name}")

    shp_file = os.path.join(extract_dir, f"ne_{res}_{name}.shp")

    _download_ne_data(url, extract_dir, name, res, zip_path, shp_file)

    return gpd.read_file(shp_file)

def _download_ne_data(url, extract_dir, name, res, zip_path, shp_file):
    if not os.path.exists(shp_file): 

        print(f"Downloading {name} ({res})...")

        r = requests.get(url, stream=True, timeout=10)

        with open(zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        os.remove(zip_path)
