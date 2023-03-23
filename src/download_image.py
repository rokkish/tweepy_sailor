import os
import time
import pandas as pd
import urllib.error
import urllib.request

download_dir = "../data/100rt/"
download_csv = "../https_list.csv"
filename = "sailor"

def get_urls():
    df = pd.read_csv(download_csv, index_col=0)
    return df.values.tolist()

def download_file(url, savename):

    #DL済み
    if os.path.isfile(savename):
        print("skip")
        return

    try:
        with urllib.request.urlopen(url) as web_file, open(savename, "wb") as local_file:
            local_file.write(web_file.read())
    except urllib.error.URLError as e:
        print(e)

def download_images(urls):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    for i, url in enumerate(urls):
        print(i, url[0])
        download_file(url[0], download_dir + f"{filename}_{i:0=4}.png")
        time.sleep(1)

def main():
    urls = get_urls()
    download_images(urls)

if __name__ == "__main__":
    main()