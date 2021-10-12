from pathlib import Path


def create_folder(foldername: str):
    Path(foldername).mkdir(parents=True, exist_ok=True)


def create_folders_for_file(filename: str):
    create_folder(Path(filename).resolve().parent)
