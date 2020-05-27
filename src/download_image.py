import os
import time
import pandas as pd
import urllib.error
import urllib.request

download_dir = "../data/"

def get_urls():
    df = pd.read_csv("../https_list.csv", index_col=0)
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
    for i, url in enumerate(urls):
        print(i, url[0])
        download_file(url[0], download_dir + "sailor_{:0=4}.png".format(i))
        time.sleep(1)

def main():
    urls = get_urls()
    download_images(urls)

if __name__ == "__main__":
    main()