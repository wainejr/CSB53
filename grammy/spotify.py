import json
import os
from typing import Dict

from grammy.defines import DATA_PATH, DOWNLOAD_PATH

_JSON_CREDENTIALS = "env.json"

SPOTIFY_ALBUMS_INFO = {
    "data_path": os.path.join(DATA_PATH, "spotify"),
}


def load_credentials() -> Dict[str, str]:
    with open(_JSON_CREDENTIALS, "r") as f:
        data = json.load(f)
        return {"client_id": data["SPOTIFY_CLIENT_ID"]}


_CREDENTIALS = load_credentials()


def get_filename_spotify_search_albums(ext: str) -> str:
    return os.path.join(SPOTIFY_ALBUMS_INFO["data_path"], f"albums_to_search.{ext}")
