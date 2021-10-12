import os
from typing import Dict

import requests

from grammy.utils import create_folders_for_file

# This header is added, because otherwise most sites block the request
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}


def download_and_save_html(
    url_path: str, html_params: str, filename: str, only_if_not_downloaded: bool = True
):
    if only_if_not_downloaded and os.path.exists(filename):
        return

    html_save = download_html(url_path, html_params)
    create_folders_for_file(filename)

    with open(filename, "w") as f:
        f.write(html_save)


def download_html(url_path: str, params: Dict[str, str]) -> str:
    req = requests.get(url_path, params=params, headers=REQUEST_HEADERS)
    if req.status_code < 400:
        return req.text
    raise Exception(f"Unable to get from {req.url}, status {req.status_code}\n{req.text}")
