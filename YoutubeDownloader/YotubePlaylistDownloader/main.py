# This only works for Public Youtube Playlist !!

import os
import yt_dlp

DOWNLOAD_FOLDER = "downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def download_playlist(url):
    print("\n" + "=" * 70)
    print("          YOUTUBE PLAYLIST → MP3 DOWNLOADER")
    print("=" * 70)
    print("Reading playlist information...")
    print("=" * 70)

    options = {
        # Download best available audio
        "format": "bestaudio/best",

        # Create a separate folder for each playlist
        "outtmpl": os.path.join(
            DOWNLOAD_FOLDER,
            "%(playlist_title)s",
            "%(playlist_index)02d - %(title)s.%(ext)s"
        ),

        # Convert downloaded audio to MP3
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],

        # IMPORTANT: Allow playlist downloading
        "noplaylist": False,

        # Show progress
        "quiet": False,
        "no_warnings": False,

        # Don't stop the whole playlist if one video fails
        "ignoreerrors": True,

        # Continue downloading if some files already exist
        "continuedl": True,

        # Don't overwrite existing downloaded files
        "overwrites": False,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:

            info = ydl.extract_info(url, download=True)

            if not info:
                print("\nCould not retrieve playlist information.")
                return False

            playlist_title = info.get(
                "title",
                "Unknown Playlist"
            )

            entries = info.get("entries", [])

            # Count successfully processed videos
            total = len(entries)

            print("\n" + "=" * 70)
            print("              PLAYLIST DOWNLOAD COMPLETED")
            print("=" * 70)

            print(f"Playlist : {playlist_title}")
            print(f"Videos   : {total}")
            print(
                f"Location : "
                f"{os.path.abspath(DOWNLOAD_FOLDER)}"
            )

            print("=" * 70)

            return True

    except Exception as e:

        print("\n" + "=" * 70)
        print("              PLAYLIST DOWNLOAD FAILED")
        print("=" * 70)

        print(f"Error: {e}")

        print("=" * 70)

        return False


def main():

    print("=" * 70)
    print("             YOUTUBE PLAYLIST → MP3")
    print("=" * 70)

    print("Paste a YouTube playlist URL below.")
    print("Every video in the playlist will be")
    print("downloaded and converted to MP3.")
    print()
    print("MP3 Quality: 320 kbps")
    print("Type 'exit' to close the program.")
    print("=" * 70)

    while True:

        url = input("\nEnter YouTube Playlist URL: ").strip()

        if not url:
            print("Please enter a playlist URL.")
            continue

        if url.lower() in ["exit", "quit", "q"]:

            print("\nExiting program. Goodbye!")

            break

        download_playlist(url)

        print("\nWaiting for next playlist...")


if __name__ == "__main__":
    main()
