from nuqi.io.download import download_mauritania_pbf

if __name__ == "__main__":
    path = download_mauritania_pbf()
    print(f"Downloaded to: {path}")