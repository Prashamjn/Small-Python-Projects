import os
import yt_dlp


# ============================================================
# CONFIGURATION
# ============================================================

DOWNLOAD_FOLDER = "downloads"
MP3_QUALITY = "320"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# ============================================================
# SEARCH YOUTUBE
# ============================================================

def search_youtube(query, number_of_results=5):

    print("\n" + "=" * 70)
    print("Searching YouTube...")
    print("=" * 70)

    search_options = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
    }

    search_query = f"ytsearch{number_of_results}:{query}"

    try:

        with yt_dlp.YoutubeDL(search_options) as ydl:

            result = ydl.extract_info(
                search_query,
                download=False
            )

        if not result:
            return []

        entries = result.get("entries", [])

        return [
            video
            for video in entries
            if video
        ]

    except Exception as error:

        print(f"\nSearch failed: {error}")

        return []


# ============================================================
# SHOW SEARCH RESULTS
# ============================================================

def show_results(results):

    print("\n" + "=" * 70)
    print("                     SEARCH RESULTS")
    print("=" * 70)

    for index, video in enumerate(results, start=1):

        title = video.get(
            "title",
            "Unknown title"
        )

        channel = video.get(
            "channel",
            video.get("uploader", "Unknown channel")
        )

        duration = video.get(
            "duration_string",
            ""
        )

        print(f"\n[{index}] {title}")
        print(f"    Channel : {channel}")

        if duration:
            print(f"    Duration: {duration}")

    print("\n[0] Cancel")

    print("=" * 70)


# ============================================================
# DOWNLOAD SELECTED SONG
# ============================================================

def download_song(video):

    title = video.get(
        "title",
        "Unknown Song"
    )

    webpage_url = video.get(
        "webpage_url"
    )

    # For extract_flat search results, construct URL if needed
    if not webpage_url:

        video_id = video.get("id")

        if not video_id:
            print("Could not determine video URL.")
            return False

        webpage_url = (
            f"https://www.youtube.com/watch?v={video_id}"
        )

    print("\n" + "=" * 70)
    print("                    DOWNLOADING")
    print("=" * 70)

    print(f"Song: {title}")
    print("=" * 70)

    options = {

        # Best available audio
        "format": "bestaudio/best",

        # Save directly inside downloads
        "outtmpl": os.path.join(
            DOWNLOAD_FOLDER,
            "%(title)s.%(ext)s"
        ),

        # Convert to MP3
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": MP3_QUALITY,
            }
        ],

        "noplaylist": True,

        "quiet": False,
        "no_warnings": False,

        # Don't overwrite existing files
        "overwrites": False,

        # Continue interrupted downloads
        "continuedl": True,
    }

    try:

        with yt_dlp.YoutubeDL(options) as ydl:

            ydl.download([webpage_url])

        print("\n" + "=" * 70)
        print("                  DOWNLOAD COMPLETE")
        print("=" * 70)

        print(f"Song     : {title}")
        print(
            f"Location : "
            f"{os.path.abspath(DOWNLOAD_FOLDER)}"
        )

        print("=" * 70)

        return True

    except Exception as error:

        print("\n" + "=" * 70)
        print("                  DOWNLOAD FAILED")
        print("=" * 70)

        print(f"Error: {error}")

        print("=" * 70)

        return False


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("              YOUTUBE SONG → MP3")
    print("=" * 70)

    print("Type the name of the song you want.")
    print()
    print("Example:")
    print("  Tum Hi Ho Arijit Singh")
    print()
    print("The program will search YouTube and show")
    print("the top 5 results.")
    print()
    print("Type 'exit' to close.")
    print("=" * 70)


    while True:

        query = input("\nSong name: ").strip()

        # ----------------------------------------------------
        # EMPTY INPUT
        # ----------------------------------------------------

        if not query:

            print("Please enter a song name.")

            continue


        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if query.lower() in [
            "exit",
            "quit",
            "q"
        ]:

            print("\nGoodbye!")

            break


        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        results = search_youtube(query)


        if not results:

            print("\nNo results found.")

            continue


        # ----------------------------------------------------
        # SHOW RESULTS
        # ----------------------------------------------------

        show_results(results)


        # ----------------------------------------------------
        # USER SELECTION
        # ----------------------------------------------------

        while True:

            choice = input(
                "\nSelect a song (1-5): "
            ).strip()

            if choice == "0":

                print("\nCancelled.")

                break


            try:

                selected_index = int(choice)

                if 1 <= selected_index <= len(results):

                    selected_video = results[
                        selected_index - 1
                    ]

                    download_song(
                        selected_video
                    )

                    break

                else:

                    print(
                        f"Please enter a number "
                        f"between 1 and {len(results)}."
                    )

            except ValueError:

                print("Please enter a valid number.")


        print("\nReady for another song...")


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()
