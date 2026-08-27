import os
import shutil
import subprocess
import sys
import tempfile


OUTPUT_FOLDER = "extracted_audio"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# ============================================================
# CHECK DEMUCS
# ============================================================

def check_demucs():

    try:

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "demucs",
                "--help"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return result.returncode == 0

    except Exception:

        return False


# ============================================================
# GET FILE PATH
# ============================================================

def get_song_path():

    while True:

        path = input(
            "\nEnter song/audio path: "
        ).strip()

        path = (
            path
            .strip('"')
            .strip("'")
        )

        if path.lower() in [
            "exit",
            "quit",
            "q"
        ]:

            return None

        if not path:

            print(
                "Please enter a file path."
            )

            continue

        if not os.path.isfile(path):

            print(
                "\nERROR: File not found."
            )

            continue

        return path


# ============================================================
# SEPARATE AUDIO
# ============================================================

def separate_audio(
    song_path,
    work_folder
):

    print("\n" + "=" * 60)
    print("SEPARATING AUDIO")
    print("=" * 60)

    print(
        "\nThis may take some time."
    )

    print(
        "The song is being separated into vocals "
        "and instrumental audio...\n"
    )

    command = [
        sys.executable,
        "-m",
        "demucs",
        "--two-stems=vocals",
        "-n",
        "htdemucs",
        "-o",
        work_folder,
        song_path
    ]

    try:

        subprocess.run(
            command,
            check=True
        )

    except subprocess.CalledProcessError:

        print(
            "\nERROR: Audio separation failed."
        )

        return None

    # --------------------------------------------------------
    # Find Demucs output
    # --------------------------------------------------------

    song_name = os.path.splitext(
        os.path.basename(song_path)
    )[0]

    separated_folder = os.path.join(
        work_folder,
        "htdemucs",
        song_name
    )

    vocals_path = os.path.join(
        separated_folder,
        "vocals.wav"
    )

    music_path = os.path.join(
        separated_folder,
        "no_vocals.wav"
    )

    if not os.path.isfile(
        vocals_path
    ):

        print(
            "\nERROR: Vocal stem was not created."
        )

        return None

    if not os.path.isfile(
        music_path
    ):

        print(
            "\nERROR: Music stem was not created."
        )

        return None

    print("\n✓ Separation completed.")

    return vocals_path, music_path


# ============================================================
# ASK OUTPUT NAME
# ============================================================

def ask_filename(prompt):

    while True:

        filename = input(
            prompt
        ).strip()

        if not filename:

            print(
                "Please enter a filename."
            )

            continue

        filename = os.path.splitext(
            filename
        )[0]

        invalid_chars = '<>:"/\\|?*'

        if any(
            char in filename
            for char in invalid_chars
        ):

            print(
                'Invalid filename. '
                'Avoid: < > : " / \\ | ? *'
            )

            continue

        return filename


# ============================================================
# CONVERT WAV → MP3
# ============================================================

def convert_to_mp3(
    input_path,
    output_path
):

    command = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-codec:a",
        "libmp3lame",
        "-b:a",
        "320k",
        output_path
    ]

    try:

        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return True

    except subprocess.CalledProcessError:

        return False


# ============================================================
# SAVE VOCALS
# ============================================================

def save_vocals(
    vocals_path
):

    filename = ask_filename(
        "\nEnter vocal output name: "
    )

    output_path = os.path.join(
        OUTPUT_FOLDER,
        filename + ".mp3"
    )

    print(
        "\nCreating vocal MP3..."
    )

    if convert_to_mp3(
        vocals_path,
        output_path
    ):

        print(
            "\n✓ Vocals saved:"
        )

        print(
            os.path.abspath(
                output_path
            )
        )

    else:

        print(
            "\nERROR: Could not save vocals."
        )


# ============================================================
# SAVE MUSIC
# ============================================================

def save_music(
    music_path
):

    filename = ask_filename(
        "\nEnter music output name: "
    )

    output_path = os.path.join(
        OUTPUT_FOLDER,
        filename + ".mp3"
    )

    print(
        "\nCreating music MP3..."
    )

    if convert_to_mp3(
        music_path,
        output_path
    ):

        print(
            "\n✓ Music saved:"
        )

        print(
            os.path.abspath(
                output_path
            )
        )

    else:

        print(
            "\nERROR: Could not save music."
        )


# ============================================================
# SAVE OPTIONS
# ============================================================

def save_options(
    vocals_path,
    music_path
):

    print("\n" + "=" * 60)
    print("SAVE OPTIONS")
    print("=" * 60)

    print("""
1. Save vocals and music
2. Save vocals only
3. Save music only
4. Don't save
""")

    while True:

        choice = input(
            "Choose option: "
        ).strip()

        if choice in [
            "1",
            "2",
            "3",
            "4"
        ]:

            break

        print(
            "Please choose 1, 2, 3, or 4."
        )

    if choice == "1":

        save_vocals(
            vocals_path
        )

        save_music(
            music_path
        )

    elif choice == "2":

        save_vocals(
            vocals_path
        )

    elif choice == "3":

        save_music(
            music_path
        )

    else:

        print(
            "\nNothing was saved."
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("               VOCAL EXTRACTOR")
    print("=" * 60)

    print("""
Separate a song into:

• Vocals
• Instrumental / Music

The final files are saved as MP3.
""")

    # --------------------------------------------------------
    # Check Demucs
    # --------------------------------------------------------

    if not check_demucs():

        print(
            "\nERROR: Demucs is not installed "
            "or cannot be started."
        )

        print(
            "\nInstall it with:"
        )

        print(
            "pip install demucs"
        )

        return

    while True:

        # ----------------------------------------------------
        # Input
        # ----------------------------------------------------

        song_path = get_song_path()

        if song_path is None:

            print(
                "\nGoodbye!"
            )

            break

        # ----------------------------------------------------
        # Temporary working directory
        # ----------------------------------------------------

        with tempfile.TemporaryDirectory(
            prefix="vocal_extractor_"
        ) as work_folder:

            result = separate_audio(
                song_path,
                work_folder
            )

            if result is None:

                print(
                    "\nWaiting for next song..."
                )

                continue

            vocals_path, music_path = result

            # ------------------------------------------------
            # Save
            # ------------------------------------------------

            save_options(
                vocals_path,
                music_path
            )

        print(
            "\n" + "=" * 60
        )

        print(
            "Waiting for next song..."
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()