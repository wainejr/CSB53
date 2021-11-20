from grammy.html import download_and_save_html
from grammy.metacritic import (
    InfoMetacritic,
    MetacriticURL,
    get_filename_metacritic_album_html,
    get_filename_metacritic_data_all_years,
)


def main():
    filename_csv = get_filename_metacritic_data_all_years("csv")
    metacritic_infos = InfoMetacritic.read_from_csv(filename_csv)
    metacritic_urls = [
        MetacriticURL(artist=m.artist, album=m.album, url=m.link_album) for m in metacritic_infos
    ]

    total = len(metacritic_urls)
    not_found = 0
    for metacritic_url in metacritic_urls:
        url = metacritic_url.url
        filename_save_html = get_filename_metacritic_album_html(url)
        try:
            download_and_save_html(url, "", filename_save_html)
        except Exception as e:
            not_found += 1
            print(f"Unable to download from url {url!r}")
    print()
    print(f"Unable to download {not_found} out of {total}")


if __name__ == "__main__":
    main()
