import os
import subprocess

OUTPUT_FOLDER = "cut_audio"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def cut_audio(audio_path, start_time, end_time):

    print("\n" + "=" * 60)
    print("Cutting audio...")
    print("=" * 60)

    if not os.path.isfile(audio_path):
        print("ERROR: Audio file not found.")
        return

    try:
        filename = os.path.basename(audio_path)
        name, extension = os.path.splitext(filename)

        output_path = os.path.join(
            OUTPUT_FOLDER,
            f"{name}_cut{extension}"
        )

        command = [
            "ffmpeg",
            "-y",
            "-i",
            audio_path,
            "-ss",
            start_time,
            "-to",
            end_time,
            "-c",
            "copy",
            output_path
        ]

        subprocess.run(command, check=True)

        print("\n" + "=" * 60)
        print("AUDIO CUT COMPLETED")
        print("=" * 60)
        print(f"Output: {os.path.abspath(output_path)}")
        print("=" * 60)

    except subprocess.CalledProcessError:
        print("\nFFmpeg failed to process the audio.")

    except Exception as e:
        print(f"\nError: {e}")


def main():

    print("=" * 60)
    print("               AUDIO CUTTER")
    print("=" * 60)
    print("Type 'exit' at any prompt to close.")
    print("=" * 60)

    while True:

        audio_path = input("\nEnter audio path: ").strip()

        if audio_path.lower() in ["exit", "quit", "q"]:
            break

        if not audio_path:
            print("Please enter an audio path.")
            continue

        start_time = input("Start time (HH:MM:SS): ").strip()

        if start_time.lower() in ["exit", "quit", "q"]:
            break

        end_time = input("End time (HH:MM:SS): ").strip()

        if end_time.lower() in ["exit", "quit", "q"]:
            break

        cut_audio(
            audio_path,
            start_time,
            end_time
        )

        print("\nWaiting for next audio...")


if __name__ == "__main__":
    main()