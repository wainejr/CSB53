import os

METACRITIC_BEST_ALBUNS = {
    "save_path": "downloads/metacritic/",
}


def get_filename_metacritic_best_albuns(year: int) -> str:
    return os.path.join(METACRITIC_BEST_ALBUNS["save_path"], f"best_albuns_{year}.html")
