#!/usr/bin/env python3

import sys
import requests
import webbrowser
from requests.exceptions import RequestException, Timeout

CATBOX_URL = "https://litterbox.catbox.moe/resources/internals/api.php"
UPLOAD_TIMEOUT = 10
CATBOX_EXPIRATION = "1h"


def error(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def get_img_data():
    img_data = sys.stdin.buffer.read()
    if not img_data:
        error("no input received on stdin")
    return img_data


def upload_to_catbox(img_data):
    files = {
        "reqtype": (None, "fileupload"),
        "time": (None, CATBOX_EXPIRATION),
        "fileToUpload": ("image.png", img_data, "image/png"),
    }

    try:
        response = requests.post(
            CATBOX_URL,
            files=files,
            timeout=UPLOAD_TIMEOUT,
        )
    except Timeout:
        error("upload timed out")
    except RequestException as e:
        error(f"network error: {e}")

    if response.status_code != 200:
        error(f"catbox returned HTTP {response.status_code}")

    url = response.text.strip()

    if not url.startswith("https://"):
        error(f"catbox error: {url}")

    return url


def open_lens_search(img_url):
    try:
        webbrowser.open_new_tab(f"https://lens.google.com/uploadbyurl?url={img_url}")
    except Exception as e:
        error(f"failed to open browser: {e}")


def main():
    img_data = get_img_data()
    img_url = upload_to_catbox(img_data)

    print(img_url)
    open_lens_search(img_url)


if __name__ == "__main__":
    main()
