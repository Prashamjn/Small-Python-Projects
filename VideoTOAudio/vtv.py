import os
import subprocess


OUTPUT_FOLDER = "converted_audio"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


def convert_mp4_to_mp3(video_path):

    print("\n" + "=" * 60)
    print("             MP4 → MP3 CONVERTER")
    print("=" * 60)

    # --------------------------------------------------------
    # Check file
    # --------------------------------------------------------

    if not os.path.isfile(video_path):

        print("\nERROR: File not found.")
        return

    # --------------------------------------------------------
    # Check extension
    # --------------------------------------------------------

    extension = os.path.splitext(
        video_path
    )[1].lower()

    if extension != ".mp4":

        print(
            "\nERROR: Please provide an MP4 file."
        )

        return

    # --------------------------------------------------------
    # Ask output name
    # --------------------------------------------------------

    while True:

        filename = input(
            "\nEnter output file name "
            "(without extension): "
        ).strip()

        if not filename:

            print(
                "Please enter a file name."
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

        break

    output_path = os.path.join(
        OUTPUT_FOLDER,
        filename + ".mp3"
    )

    # --------------------------------------------------------
    # FFmpeg command
    # --------------------------------------------------------

    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-vn",
        "-codec:a",
        "libmp3lame",
        "-b:a",
        "320k",
        output_path
    ]

    print("\nConverting MP4 → MP3...")
    print("Please wait...\n")

    try:

        subprocess.run(
            command,
            check=True
        )

        print("\n" + "=" * 60)
        print("             CONVERSION COMPLETE")
        print("=" * 60)

        print(
            f"\nMP3 saved at:\n"
            f"{os.path.abspath(output_path)}"
        )

        print("=" * 60)

    except subprocess.CalledProcessError:

        print("\nFFmpeg failed to convert the file.")

    except FileNotFoundError:

        print(
            "\nERROR: FFmpeg was not found."
        )

        print(
            "Make sure FFmpeg is installed "
            "and added to PATH."
        )

    except Exception as e:

        print(
            f"\nUnexpected error: {e}"
        )


def main():

    print("=" * 60)
    print("                MP4 → MP3")
    print("=" * 60)

    print(
        "\nType 'exit' to close the program."
    )

    while True:

        video_path = input(
            "\nEnter MP4 file path: "
        ).strip()

        # Remove quotes from copied Windows paths
        video_path = (
            video_path
            .strip('"')
            .strip("'")
        )

        if video_path.lower() in [
            "exit",
            "quit",
            "q"
        ]:

            print("\nGoodbye!")
            break

        if not video_path:

            print(
                "Please enter an MP4 file path."
            )

            continue

        convert_mp4_to_mp3(
            video_path
        )

        print(
            "\nWaiting for next MP4..."
        )


if __name__ == "__main__":
    main()