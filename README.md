# NE Loader

A simple, robust Python package to download and load Natural Earth map data using GeoPandas.

## Features

- Download and cache Natural Earth datasets
- Load shapefiles as GeoDataFrames

## Installation

```bash
pip install ne-loader
```

## Usage

```python
from ne_loader import map_loader
world = map_loader.get_natural_earth('cultural', 'admin_0_countries')
```

## CLI

```bash
ne-loader --help
```

## License

MIT
