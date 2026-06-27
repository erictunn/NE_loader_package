"""Provides basic command line functionality."""

import click
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
    """Locate the cache directory."""
    cache_dir = get_cache_dir()
    click.echo(cache_dir)

@main.command("list")
def cli_list_cached_files() -> None:
    """List all cached NE files within the cache dir."""
    cache_dir = get_cache_dir()
    sub_folders = [f.name for f in cache_dir.iterdir() if f.is_dir()]
    click.echo(", ".join(sub_folders))
