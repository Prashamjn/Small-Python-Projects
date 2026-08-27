import os
import yt_dlp

DOWNLOAD_FOLDER = "downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def download_mp3(url):
    print("\n" + "=" * 60)
    print("Starting download...")
    print("=" * 60)

    options = {
        "format": "bestaudio/best",

        "outtmpl": os.path.join(
            DOWNLOAD_FOLDER,
            "%(title)s.%(ext)s"
        ),

        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],

        "noplaylist": True,

        # Makes yt-dlp show useful progress information
        "quiet": False,
        "no_warnings": False,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)

            title = info.get("title", "Unknown")

            print("\n" + "=" * 60)
            print("TASK COMPLETED")
            print("=" * 60)
            print(f"Title    : {title}")
            print(f"Location : {os.path.abspath(DOWNLOAD_FOLDER)}")
            print("=" * 60)

            return True

    except Exception as e:
        print("\n" + "=" * 60)
        print("DOWNLOAD FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        print("=" * 60)

        return False


def main():
    print("=" * 60)
    print("        YOUTUBE → MP3 DOWNLOADER")
    print("=" * 60)
    print("Paste a YouTube URL below.")
    print("Type 'exit' to close the program.")
    print("=" * 60)

    while True:
        url = input("\nEnter YouTube URL: ").strip()

        if not url:
            print("Please enter a URL.")
            continue

        if url.lower() in ["exit", "quit", "q"]:
            print("\nExiting program. Goodbye!")
            break

        download_mp3(url)

        print("\nWaiting for next URL...")


if __name__ == "__main__":
    main()