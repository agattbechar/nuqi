from pathlib import Path
import hashlib
import httpx
from nuqi.config import RAW_DIR

MAURITANIA_PBF_URL = "https://download.geofabrik.de/africa/mauritania-latest.osm.pbf"

def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def download_mauritania_pbf(force: bool = False) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out = RAW_DIR / "mauritania-latest.osm.pbf"
    if out.exists() and not force:
        return out

    print(f"Downloading: {MAURITANIA_PBF_URL}")
    with httpx.stream("GET", MAURITANIA_PBF_URL, timeout=120.0, follow_redirects=True) as r:
        r.raise_for_status()
        with out.open("wb") as f:
            for chunk in r.iter_bytes():
                f.write(chunk)

    print(f"Saved: {out} (sha256={_sha256(out)[:12]}...)")
    return out