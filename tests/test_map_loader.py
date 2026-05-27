"""Basic tests for map_loader.py constructors."""

from pathlib import Path

from ne_loader.map_loader import (
    build_ne_filename,
    build_ne_shp_path,
    build_ne_url,
    build_ne_zip_path,
)


def test_build_ne_url() -> None:
    """Tests that the Natural Earth website URL is built correctly."""
    assert (
        build_ne_url("cultural", "admin_0_countries", "10m")
        == "https://naciscdn.org/naturalearth/10m/cultural/"
        "ne_10m_admin_0_countries.zip"
    )


def test_build_ne_zip_path() -> None:
    """Tests that the cache zip path builds correctly."""
    assert build_ne_zip_path(
        Path("/tmp/natural-earth-cache"),
        "admin_0_countries",
        "10m",
    ) == Path("/tmp/natural-earth-cache/ne_10m_admin_0_countries.zip")


def test_build_ne_filename() -> None:
    """Tests that the Natural Earth data zip file name is built correctly."""
    assert build_ne_filename("admin_0_countries", "10m") == (
        "ne_10m_admin_0_countries.zip"
    )


def test_build_ne_shp_path() -> None:
    """Tests that the path to the .shp file containing NE data is built correctly."""
    assert build_ne_shp_path(
        Path("/tmp/natural-earth-cache"),
        "admin_0_countries",
        "10m",
    ) == Path(
        "/tmp/natural-earth-cache/ne_10m_admin_0_countries/"
        "ne_10m_admin_0_countries.shp"
    )
