from pathlib import Path


def create_folder(foldername: str):
    Path(foldername).mkdir(parents=True, exist_ok=True)


def create_folders_for_file(filename: str):
    create_folder(Path(filename).resolve().parent)


def only_ascii(s: str) -> str:
    return s.encode("ascii", "ignore").decode("ascii")


def normalize_url_str(s: str) -> str:
    char_remove = [":", "&", "'", ".", ",", "?", "/"]
    for c in char_remove:
        s = s.replace(c, "")
    s = s.lower()
    s = s.replace("(deluxe)", "")
    s = s.strip()

    # Avoid problems as "1 - 2", generating "1---2"
    s = s.replace(" ", "-")
    while "--" in s:
        s = s.replace("--", "-")
    return s
