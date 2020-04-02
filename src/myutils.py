import requests

def download_steam(url,savepath,chunk=2048):
    r = requests.get(url, stream=True)
    with open(savepath, "wb") as f:
        for chunk in r.iter_content(chunk_size=chunk):
            if chunk:
                f.write(chunk)
                # time.sleep(0.1) # speed limit TODO
