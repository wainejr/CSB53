import os
from typing import Dict

import requests

from grammy.utils import create_folders_for_file

# This header is added, because otherwise most sites block the request
REQUEST_HEADERS = {
    "Content-Type": "text/html",
    "Accept-Charset": "utf-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 OPR/79.0.4143.73",
}


def download_and_save_html(
    url_path: str, html_params: str, filename: str, only_if_not_downloaded: bool = True
):
    if only_if_not_downloaded and os.path.exists(filename):
        return

    html_save = download_html(url_path, html_params)
    create_folders_for_file(filename)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_save)


def download_html(url_path: str, params: Dict[str, str]) -> str:
    req = requests.get(url_path, params=params, headers=REQUEST_HEADERS, allow_redirects=True)
    if req.status_code < 400:
        return req.text
    raise Exception(f"Unable to get from {req.url}, status {req.status_code}\n{req.text}")
