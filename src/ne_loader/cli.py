"""Provides basic command line functionality."""

import click
from pathlib import Path
import geopandas as gpd

from . import map_loader
from .cacher import get_cache_dir


@click.group()
def main() -> None:
    """Entry point for the ne-loader CLI."""


@main.command("download-get")
@click.argument("category")
@click.argument("name")
@click.option("--res", default="10m", help="NE dataset resolution (default: 10m)")
def cli_get_natural_earth(category: str, name: str, res: map_loader.Resolution) -> None:
    """Download a Natural Earth dataset and load it into GeoPandas."""
    map_loader.get_natural_earth(category, name, res)

@main.command("where")
def cli_where_cache() -> None:
    """Locates where the cached NE data is."""
    cache_dir = get_cache_dir()
    click.echo(cache_dir)
