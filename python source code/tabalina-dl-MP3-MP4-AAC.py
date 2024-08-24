import sys
import yt_dlp as youtube_dl  
import os
import time
from urllib.parse import urlparse

ITALIC = '\x1b[3m'
RESET = '\x1b[0m'

print(r"""
  _____  
 /     \   [I]=======================================[I]
| () () |  [I]         Download MP4, MP3, AAC        [I]
 \  ^  /   [I]          by: {}Jayrold Tabalina{}         [I]
  |||||    [I]=======================================[I]
  |||||

""".format(ITALIC, RESET))

def get_download_options(option, custom_filename):
    options = {
        "format": "bestvideo[height<=1080]+bestaudio/best" if option == 1 else (
            "bestvideo[height<=720]+bestaudio/best" if option == 2 else (
                "bestvideo[height<=480]+bestaudio/best" if option == 3 else (
                    "bestvideo[height<=360]+bestaudio/best" if option == 4 else (
                        "bestvideo[height<=180]+bestaudio/best" if option == 5 else (
                            "best" if option == 6 else "bestaudio/best"
                        )
                    )
                )
            )
        ),
        "outtmpl": f"{custom_filename}.%(ext)s",
        "verbose": True
    }

    if option in [7, 8]:
        codec = "aac" if option == 7 else "mp3"
        options["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": codec,
            "preferredquality": "192",
        }]
        options["postprocessor_args"] = ["-t", "600"]

    return options

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

try:
    url = input("Enter the Link/URL to be downloaded: ")

    if not is_valid_url(url):
        print("Invalid URL. Please enter a valid URL.")
        print("This window will close in 3 seconds.")
        time.sleep(3)
        sys.exit(1)

    custom_filename = input("Type the filename you want (without extension): ").strip()

    print("Choose format and resolution:")
    print("1. 1080p(HD)")
    print("2. 720p")
    print("3. 480p(SD)")
    print("4. 360p")
    print("5. 180p")
    print("6. Any available resolution")
    print("7. Audio only (AAC)")
    print("8. Audio only (MP3)")

    option = int(input("Enter your option (1 - 8): "))
    if option not in range(1, 9):
        print("Option not available")
        sys.exit(1)

    
    if os.name == 'nt':  # For Windows
        download_path = os.path.join(os.environ['USERPROFILE'], 'Videos')
    else:  # For Unix-like systems
        download_path = os.path.join(os.path.expanduser('~'), 'Videos')

    os.makedirs(download_path, exist_ok=True)  
    os.chdir(download_path)

    ydl_opts = get_download_options(option, custom_filename)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading........." + url)
        ydl.download([url])

    print("Download and conversion completed. Look for it in Videos FOLDERS.")
    time.sleep(5)

except youtube_dl.utils.DownloadError as e:
    print(f"Download Error: {e}")
    time.sleep(3)
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    time.sleep(3)
    sys.exit(1)
