import os
import subprocess
import json
import re

OUTPUT_FOLDER = "mixed_audio"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def run_command(command):
    """
    Run a command and return True if successful.
    """
    try:
        subprocess.run(command, check=True)
        return True

    except subprocess.CalledProcessError:
        return False


def get_audio_duration(audio_path):
    """
    Get audio duration using ffprobe.
    Returns duration in seconds.
    """

    command = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        audio_path
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        data = json.loads(result.stdout)

        return float(data["format"]["duration"])

    except Exception:
        return None


def time_to_seconds(time_string):
    """
    Convert:

    HH:MM:SS
    HH:MM:SS.ms
    MM:SS
    seconds

    into seconds.
    """

    time_string = time_string.strip()

    try:

        # Plain number
        if re.fullmatch(r"\d+(\.\d+)?", time_string):
            return float(time_string)

        parts = time_string.split(":")

        if len(parts) == 2:

            minutes = float(parts[0])
            seconds = float(parts[1])

            return minutes * 60 + seconds

        elif len(parts) == 3:

            hours = float(parts[0])
            minutes = float(parts[1])
            seconds = float(parts[2])

            return hours * 3600 + minutes * 60 + seconds

    except ValueError:
        pass

    return None


def format_time(seconds):
    """
    Convert seconds into HH:MM:SS format.
    """

    seconds = int(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def ask_yes_no(question):

    while True:

        answer = input(f"{question} (y/n): ").strip().lower()

        if answer in ["y", "yes"]:
            return True

        if answer in ["n", "no"]:
            return False

        print("Please enter y or n.")


def ask_float(question, minimum=None, maximum=None):

    while True:

        value = input(question).strip()

        try:

            value = float(value)

            if minimum is not None and value < minimum:
                print(f"Value must be at least {minimum}.")
                continue

            if maximum is not None and value > maximum:
                print(f"Value must be at most {maximum}.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number.")


# ============================================================
# SONG INFORMATION
# ============================================================

def get_song_information(song_number):

    print("\n" + "=" * 60)
    print(f"SONG {song_number}")
    print("=" * 60)

    while True:

        audio_path = input("Enter audio path: ").strip()

        if not os.path.isfile(audio_path):
            print("ERROR: Audio file not found.")
            continue

        break

    duration = get_audio_duration(audio_path)

    if duration is None:

        print("Could not determine audio duration.")
        return None

    print(f"\nAudio duration: {format_time(duration)}")

    use_full_length = ask_yes_no("Use full length")

    if use_full_length:

        start_time = 0
        end_time = duration

    else:

        while True:

            start_input = input(
                "Start time (HH:MM:SS or MM:SS): "
            ).strip()

            start_time = time_to_seconds(start_input)

            if start_time is None:
                print("Invalid start time.")
                continue

            if start_time < 0 or start_time >= duration:
                print("Start time is outside the audio duration.")
                continue

            break

        while True:

            end_input = input(
                "End time (HH:MM:SS or MM:SS): "
            ).strip()

            end_time = time_to_seconds(end_input)

            if end_time is None:
                print("Invalid end time.")
                continue

            if end_time <= start_time:
                print("End time must be greater than start time.")
                continue

            if end_time > duration:
                print("End time is outside the audio duration.")
                continue

            break

    clip_duration = end_time - start_time

    print(
        f"\nSelected clip: "
        f"{format_time(start_time)} → "
        f"{format_time(end_time)}"
    )

    print(f"Clip duration: {format_time(clip_duration)}")

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------

    print("\nVolume")

    volume = ask_float(
        "Volume percentage (0-200): ",
        minimum=0,
        maximum=200
    )

    # --------------------------------------------------------
    # FADE IN
    # --------------------------------------------------------

    fade_in = 0

    if ask_yes_no("\nAdd fade-in"):

        max_fade = min(10, clip_duration / 2)

        fade_in = ask_float(
            f"Fade-in duration in seconds (0-{max_fade:.2f}): ",
            minimum=0,
            maximum=max_fade
        )

    # --------------------------------------------------------
    # FADE OUT
    # --------------------------------------------------------

    fade_out = 0

    if ask_yes_no("\nAdd fade-out"):

        max_fade = min(10, clip_duration / 2)

        fade_out = ask_float(
            f"Fade-out duration in seconds (0-{max_fade:.2f}): ",
            minimum=0,
            maximum=max_fade
        )

    return {
        "path": os.path.abspath(audio_path),
        "start": start_time,
        "end": end_time,
        "duration": clip_duration,
        "volume": volume / 100,
        "fade_in": fade_in,
        "fade_out": fade_out
    }


# ============================================================
# TRANSITION SELECTION
# ============================================================

def ask_transition(song_a, song_b, transition_number):

    print("\n" + "-" * 60)
    print(
        f"TRANSITION {transition_number}: "
        f"Song {song_a} → Song {song_b}"
    )
    print("-" * 60)

    print("""
1. None
2. Fade
3. Crossfade
""")

    while True:

        choice = input("Choose transition (1-3): ").strip()

        if choice in ["1", "2", "3"]:
            break

        print("Please choose 1, 2 or 3.")

    if choice == "1":

        return {
            "type": "none",
            "duration": 0
        }

    elif choice == "2":

        print("\nFade transition selected.")

        duration = ask_float(
            "Fade duration in seconds: ",
            minimum=0.1,
            maximum=10
        )

        return {
            "type": "fade",
            "duration": duration
        }

    else:

        print("\nCrossfade selected.")

        while True:

            duration = ask_float(
                "Crossfade duration in seconds: ",
                minimum=0.1,
                maximum=30
            )

            break

        return {
            "type": "crossfade",
            "duration": duration
        }


# ============================================================
# FILTER GRAPH
# ============================================================

def build_filter_graph(songs, transitions):

    filters = []

    # --------------------------------------------------------
    # CREATE INDIVIDUAL CLIPS
    # --------------------------------------------------------

    for i, song in enumerate(songs):

        start = song["start"]
        end = song["end"]

        volume = song["volume"]

        fade_in = song["fade_in"]
        fade_out = song["fade_out"]

        clip_duration = song["duration"]

        filter_chain = []

        # Trim
        filter_chain.append(
            f"atrim=start={start}:end={end}"
        )

        # Reset timestamps
        filter_chain.append(
            "asetpts=PTS-STARTPTS"
        )

        # Standardize audio
        filter_chain.append(
            "aresample=44100"
        )

        filter_chain.append(
            "aformat=sample_fmts=fltp:channel_layouts=stereo"
        )

        # Volume
        if volume != 1:

            filter_chain.append(
                f"volume={volume}"
            )

        # Fade in
        if fade_in > 0:

            filter_chain.append(
                f"afade=t=in:st=0:d={fade_in}"
            )

        # Fade out
        if fade_out > 0:

            fade_start = max(
                0,
                clip_duration - fade_out
            )

            filter_chain.append(
                f"afade=t=out:st={fade_start}:d={fade_out}"
            )

        filter_string = ",".join(filter_chain)

        filters.append(
            f"[{i}:a]{filter_string}[a{i}]"
        )

    # --------------------------------------------------------
    # MIX / TRANSITIONS
    # --------------------------------------------------------

    current_label = "[a0]"

    accumulated_duration = songs[0]["duration"]

    for i, transition in enumerate(transitions):

        next_label = f"[a{i + 1}]"

        output_label = f"[mix{i + 1}]"

        transition_type = transition["type"]
        transition_duration = transition["duration"]

        # ----------------------------------------------------
        # NO TRANSITION
        # ----------------------------------------------------

        if transition_type == "none":

            filters.append(
                f"{current_label}{next_label}"
                f"concat=n=2:v=0:a=1"
                f"{output_label}"
            )

            accumulated_duration += songs[i + 1]["duration"]

        # ----------------------------------------------------
        # FADE
        # ----------------------------------------------------

        elif transition_type == "fade":

            fade_duration = min(
                transition_duration,
                songs[i]["duration"] / 2,
                songs[i + 1]["duration"] / 2
            )

            # Fade out previous clip
            fade_out_start = max(
                0,
                songs[i]["duration"] - fade_duration
            )

            faded_previous = f"[fadeout{i}]"
            faded_next = f"[fadein{i}]"

            filters.append(
                f"{current_label}"
                f"afade=t=out:"
                f"st={fade_out_start}:"
                f"d={fade_duration}"
                f"{faded_previous}"
            )

            # Fade in next clip
            filters.append(
                f"{next_label}"
                f"afade=t=in:"
                f"st=0:"
                f"d={fade_duration}"
                f"{faded_next}"
            )

            # Concatenate
            filters.append(
                f"{faded_previous}{faded_next}"
                f"concat=n=2:v=0:a=1"
                f"{output_label}"
            )

            accumulated_duration += songs[i + 1]["duration"]

        # ----------------------------------------------------
        # CROSSFADE
        # ----------------------------------------------------

        elif transition_type == "crossfade":

            crossfade_duration = min(
                transition_duration,
                songs[i]["duration"] - 0.01,
                songs[i + 1]["duration"] - 0.01
            )

            if crossfade_duration <= 0:
                crossfade_duration = 0.1

            filters.append(
                f"{current_label}{next_label}"
                f"acrossfade="
                f"d={crossfade_duration}:"
                f"c1=tri:"
                f"c2=tri"
                f"{output_label}"
            )

            accumulated_duration += (
                songs[i + 1]["duration"]
                - crossfade_duration
            )

        current_label = output_label

    return filters, current_label


# ============================================================
# CREATE MIX
# ============================================================

def create_mix(songs, transitions, output_path):

    print("\n" + "=" * 60)
    print("BUILDING AUDIO MIX")
    print("=" * 60)

    filters, final_label = build_filter_graph(
        songs,
        transitions
    )

    filter_complex = ";".join(filters)

    command = [
        "ffmpeg",
        "-y"
    ]

    # --------------------------------------------------------
    # INPUT FILES
    # --------------------------------------------------------

    for song in songs:

        command.extend([
            "-i",
            song["path"]
        ])

    # --------------------------------------------------------
    # FILTER
    # --------------------------------------------------------

    command.extend([
        "-filter_complex",
        filter_complex,
        "-map",
        final_label,
        "-c:a",
        "libmp3lame",
        "-b:a",
        "320k",
        output_path
    ])

    print("\nProcessing...")

    try:

        subprocess.run(
            command,
            check=True
        )

        print("\n" + "=" * 60)
        print("AUDIO MIX COMPLETED")
        print("=" * 60)
        print(f"Output: {os.path.abspath(output_path)}")
        print("=" * 60)

        return True

    except subprocess.CalledProcessError:

        print("\n" + "=" * 60)
        print("ERROR")
        print("=" * 60)
        print("FFmpeg failed to create the mix.")
        print("Check the audio files and transition settings.")
        print("=" * 60)

        return False


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("                    AUDIO MIXER")
    print("=" * 60)
    print("Create multi-song mixes directly from the terminal.")
    print("=" * 60)

    # --------------------------------------------------------
    # NUMBER OF SONGS
    # --------------------------------------------------------

    while True:

        try:

            song_count = int(
                input("\nHow many songs do you want to mix? ").strip()
            )

            if song_count < 1:

                print("You need at least 1 song.")
                continue

            break

        except ValueError:

            print("Please enter a valid number.")

    # --------------------------------------------------------
    # SONGS
    # --------------------------------------------------------

    songs = []

    for i in range(song_count):

        song = get_song_information(i + 1)

        if song is None:
            print("Could not add this song.")
            return

        songs.append(song)

    # --------------------------------------------------------
    # TRANSITIONS
    # --------------------------------------------------------

    transitions = []

    if song_count > 1:

        print("\n" + "=" * 60)
        print("                    TRANSITIONS")
        print("=" * 60)

        for i in range(song_count - 1):

            transition = ask_transition(
                i + 1,
                i + 2,
                i + 1
            )

            transitions.append(transition)

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("                    OUTPUT")
    print("=" * 60)

    output_name = input(
        "Output filename (without extension): "
    ).strip()

    if not output_name:

        output_name = "audio_mix"

    output_name = os.path.splitext(output_name)[0]

    output_path = os.path.join(
        OUTPUT_FOLDER,
        f"{output_name}.mp3"
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("                    MIX SUMMARY")
    print("=" * 60)

    for i, song in enumerate(songs):

        print(
            f"\nSong {i + 1}: "
            f"{os.path.basename(song['path'])}"
        )

        print(
            f"  Clip: "
            f"{format_time(song['start'])} → "
            f"{format_time(song['end'])}"
        )

        print(
            f"  Volume: "
            f"{song['volume'] * 100:.0f}%"
        )

        print(
            f"  Fade in: "
            f"{song['fade_in']} sec"
        )

        print(
            f"  Fade out: "
            f"{song['fade_out']} sec"
        )

    if transitions:

        print("\nTransitions:")

        for i, transition in enumerate(transitions):

            print(
                f"  {i + 1} → {i + 2}: "
                f"{transition['type'].upper()} "
                f"({transition['duration']} sec)"
            )

    print(
        f"\nOutput: {os.path.abspath(output_path)}"
    )

    # --------------------------------------------------------
    # CONFIRM
    # --------------------------------------------------------

    print()

    if not ask_yes_no("Create this mix"):

        print("\nMix cancelled.")
        return

    # --------------------------------------------------------
    # CREATE
    # --------------------------------------------------------

    create_mix(
        songs,
        transitions,
        output_path
    )

    print("\nWaiting for next mix...")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()