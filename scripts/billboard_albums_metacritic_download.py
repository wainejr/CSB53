from grammy.html import download_and_save_html
from grammy.metacritic import (
    MetacriticURL,
    get_filename_metacritic_album_html,
    get_filename_metacritic_billboard_urls_treated,
)


def main():
    filename_csv = get_filename_metacritic_billboard_urls_treated("csv")
    metacritic_urls = MetacriticURL.read_from_csv(filename_csv)
    total = len(metacritic_urls)
    not_found = []
    for metacritic_url in metacritic_urls:
        url = metacritic_url.url
        filename_save_html = get_filename_metacritic_album_html(url)
        if metacritic_url.artist.lower() in ("various artists", "soundtrack"):
            continue
        try:
            download_and_save_html(url, "", filename_save_html)
        except Exception as e:
            not_found.append(metacritic_url)
            print(f"Unable to download from url {url!r}")
    print()
    print(f"Unable to download {len(not_found)} out of {total}")
    MetacriticURL.save_to_csv("unable_to_download.csv", not_found)


if __name__ == "__main__":
    main()
