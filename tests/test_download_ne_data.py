"""Tests for natural earth data downloader functions."""

import io
import zipfile
import logging
import pytest
import requests
from pathlib import Path

from ne_loader.map_loader import download_ne_data, build_ne_filename

def _mock_zip_bytes(name: str, res: str) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr(build_ne_filename(name, res, suffix=".shp"), b"mock shp content")
    return buffer.getvalue()



def test_download_ne_data_success(tmp_path: Path) -> None:
    """Tests that download_ne_data function works when HTTP response succeeds."""
    name = "admin_0_countries"
    res = "10m"

    mocked_bytes = _mock_zip_bytes(name, res)

    class MockResponse:
        """Mock a response, to be fed to download_ne_data by monkeypatch."""

        def __init__(self, data: bytes):
            self.data = data

        def raise_for_status(self) -> None:
            return None

        def iter_content(self, chunk_size: int = 8192):
            for i in range (0, len(self.data), chunk_size):
                yield self.data[i : i + chunk_size]

    def mock_get(*args, **kwargs):
        return MockResponse(mocked_bytes)

    pytest.MonkeyPatch().setattr(requests, "get", lambda *a **k: mock_get)

    base = tmp_path / "ne-cache"
    extract_dir = base / build_ne_filename(name, res, suffix="")
    zip_path = base / build_ne_filename(name, res)
    shp_file = extract_dir / build_ne_filename(name, res, suffix=".shp")

    download_ne_data(
        url="www.thisisnotarealurl.org/file.zip",
        extract_dir=extract_dir,
        name=name,
        res=res,
        zip_path=zip_path,
        shp_file=shp_file,
        logger=logging.getLogger("testing")
    )

    assert shp_file.exists()
    assert extract_dir.exists()
    assert not zip_path.exists()
