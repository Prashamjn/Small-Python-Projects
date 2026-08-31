from __future__ import annotations

from dataclasses import dataclass
from typing import List

from auth import get_youtube_service
from youtube_api import (
    create_playlist,
    add_video_to_playlist,
    search_videos,
)


# ================================================================
# DATA MODEL
# ================================================================

@dataclass
class SelectedSong:
    video_id: str
    title: str
    channel: str


# ================================================================
# UI HELPERS
# ================================================================

def print_header(title: str) -> None:
    print("\n" + "=" * 72)
    print(title.center(72))
    print("=" * 72)


def print_small_line() -> None:
    print("-" * 72)


# ================================================================
# SEARCH RESULT SELECTION
# ================================================================

def choose_search_result(results: list[dict]) -> dict | None:
    print_header("YOUTUBE SEARCH RESULTS")

    for i, item in enumerate(results, start=1):
        print(f"\n[{i}] {item['title']}")
        print(f"    Channel : {item['channel']}")
        print(f"    Video ID: {item['video_id']}")

    print("\n[0] Cancel")

    while True:
        choice = input("\nChoose a result: ").strip()

        if choice == "0":
            return None

        try:
            index = int(choice)
        except ValueError:
            print("Please enter a number.")
            continue

        if 1 <= index <= len(results):
            return results[index - 1]

        print(f"Choose a number from 0 to {len(results)}.")


# ================================================================
# SHOW CURRENT SONGS
# ================================================================

def show_songs(songs: List[SelectedSong]) -> None:
    print_header("CURRENT PLAYLIST")

    if not songs:
        print("No songs added yet.")
        return

    for i, song in enumerate(songs, start=1):
        print(f"{i:02d}. {song.title}")
        print(f"    {song.channel}")

    print_small_line()
    print(f"Total songs: {len(songs)}")


# ================================================================
# CREATE PLAYLIST
# ================================================================

def build_playlist() -> None:

    print_header("CREATE YOUTUBE PLAYLIST")

    # ------------------------------------------------------------
    # AUTHENTICATION
    # ------------------------------------------------------------

    print("Connecting to your YouTube account...")
    print("If this is your first run, your browser will open for")
    print("Google authorization.")
    print()

    try:
        youtube = get_youtube_service()

    except Exception as exc:
        print_header("GOOGLE AUTHENTICATION FAILED")

        print(f"Error: {exc}")

        print_small_line()

        print("Make sure:")
        print("1. client_secret.json is beside main.py")
        print("2. YouTube Data API v3 is enabled")
        print("3. Your OAuth client is a Desktop app")
        print("4. You have completed Google authorization")

        return

    print("\n✓ YouTube account connected successfully.")

    # ------------------------------------------------------------
    # PLAYLIST NAME
    # ------------------------------------------------------------

    playlist_name = input("\nPlaylist name: ").strip()

    if not playlist_name:
        print("Playlist name cannot be empty.")
        return

    # ------------------------------------------------------------
    # SONG LIST
    # ------------------------------------------------------------

    songs: List[SelectedSong] = []

    print("\nAdd songs by typing their names.")

    print_small_line()

    print("Commands:")
    print("  list       Show songs currently selected")
    print("  remove N   Remove song number N")
    print("  clear      Remove all selected songs")
    print("  stop       Finish adding songs")

    print_small_line()

    # ------------------------------------------------------------
    # SONG INPUT LOOP
    # ------------------------------------------------------------

    while True:

        raw = input(f"\nSong {len(songs) + 1}: ").strip()

        if not raw:
            print("Please enter a song name or command.")
            continue

        command = raw.lower()

        # --------------------------------------------------------
        # STOP
        # --------------------------------------------------------

        if command == "stop":
            break

        # --------------------------------------------------------
        # LIST
        # --------------------------------------------------------

        if command == "list":
            show_songs(songs)
            continue

        # --------------------------------------------------------
        # CLEAR
        # --------------------------------------------------------

        if command == "clear":
            songs.clear()
            print("\n✓ Playlist draft cleared.")
            continue

        # --------------------------------------------------------
        # REMOVE
        # --------------------------------------------------------

        if command.startswith("remove "):

            parts = raw.split(maxsplit=1)

            if len(parts) != 2:
                print("Usage: remove N")
                continue

            number_text = parts[1].strip()

            try:
                number = int(number_text)

                if number < 1 or number > len(songs):
                    print(
                        f"Invalid song number. "
                        f"Choose between 1 and {len(songs)}."
                    )
                    continue

                removed = songs.pop(number - 1)

                print(f"\n✓ Removed: {removed.title}")

            except ValueError:
                print("Please enter a valid song number.")

            continue

        # --------------------------------------------------------
        # SEARCH YOUTUBE
        # --------------------------------------------------------

        print(f"\nSearching YouTube for: {raw}")

        try:

            # IMPORTANT:
            #
            # search_videos() requires:
            #
            # search_videos(youtube, query, max_results)
            #
            # The previous version incorrectly called:
            #
            # search_videos(raw, max_results=5)
            #
            results = search_videos(
                youtube,
                raw,
                max_results=5
            )

        except Exception as exc:

            print("\nSearch failed:")
            print(f"Error: {exc}")

            continue

        # --------------------------------------------------------
        # NO RESULTS
        # --------------------------------------------------------

        if not results:

            print("\nNo YouTube video results found.")

            continue

        # --------------------------------------------------------
        # CHOOSE VIDEO
        # --------------------------------------------------------

        selected = choose_search_result(results)

        if selected is None:

            print("\nSearch cancelled.")

            continue

        # --------------------------------------------------------
        # DUPLICATE CHECK
        # --------------------------------------------------------

        if any(
            song.video_id == selected["video_id"]
            for song in songs
        ):

            print(
                "\nThat video is already in your playlist."
            )

            continue

        # --------------------------------------------------------
        # ADD SONG
        # --------------------------------------------------------

        songs.append(
            SelectedSong(
                video_id=selected["video_id"],
                title=selected["title"],
                channel=selected["channel"],
            )
        )

        print(f"\n✓ Added: {selected['title']}")

    # ============================================================
    # FINISHED ADDING SONGS
    # ============================================================

    if not songs:

        print("\nNo songs were selected.")

        print("Nothing to create.")

        return

    # ============================================================
    # REVIEW PLAYLIST
    # ============================================================

    show_songs(songs)

    print("\n")

    print_small_line()

    confirm = input(
        "Create this playlist on YouTube? [Y/n]: "
    ).strip().lower()

    if confirm not in ("", "y", "yes"):

        print("\nPlaylist creation cancelled.")

        return

    # ============================================================
    # CREATE YOUTUBE PLAYLIST
    # ============================================================

    print("\nCreating YouTube playlist...")

    try:

        playlist_id = create_playlist(
            youtube,
            title=playlist_name,
            description="Created with YouTube Playlist Builder",
            privacy_status="private",
        )

        print(f"\n✓ Playlist created: {playlist_name}")

        print(f"  Playlist ID: {playlist_id}")

        # --------------------------------------------------------
        # ADD SONGS
        # --------------------------------------------------------

        print("\nAdding songs...")

        added = 0

        for index, song in enumerate(songs, start=1):

            try:

                add_video_to_playlist(
                    youtube,
                    playlist_id=playlist_id,
                    video_id=song.video_id,
                )

                added += 1

                print(
                    f"✓ [{index}/{len(songs)}] "
                    f"{song.title}"
                )

            except Exception as exc:

                print(
                    f"✗ [{index}/{len(songs)}] "
                    f"{song.title}"
                )

                print(f"  Error: {exc}")

        # ========================================================
        # COMPLETE
        # ========================================================

        print_header("PLAYLIST COMPLETE")

        print(f"Name  : {playlist_name}")

        print(f"Added : {added}/{len(songs)}")

        print(
            "URL   : "
            f"https://www.youtube.com/playlist?list={playlist_id}"
        )

    except Exception as exc:

        print_header("PLAYLIST CREATION FAILED")

        print(f"Error: {exc}")


# ================================================================
# MAIN MENU
# ================================================================

def main() -> None:

    print_header("YOUTUBE PLAYLIST BUILDER")

    print("Build a real YouTube playlist from song names.")

    print()

    print("1. Create new playlist")
    print("2. Exit")

    while True:

        choice = input("\nChoose: ").strip()

        # --------------------------------------------------------
        # CREATE
        # --------------------------------------------------------

        if choice == "1":

            build_playlist()

            print("\nReturning to main menu...")

        # --------------------------------------------------------
        # EXIT
        # --------------------------------------------------------

        elif choice == "2" or choice.lower() in {
            "q",
            "quit",
            "exit",
        }:

            print("\nGoodbye!")

            break

        # --------------------------------------------------------
        # INVALID
        # --------------------------------------------------------

        else:

            print("Please choose 1 or 2.")


# ================================================================
# PROGRAM ENTRY POINT
# ================================================================

if __name__ == "__main__":
    main()
