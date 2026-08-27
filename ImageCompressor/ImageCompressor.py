import os
from PIL import Image

OUTPUT_FOLDER = "compressed"


def format_size(size):
    """Convert bytes into KB / MB / GB."""
    if size < 1024:
        return f"{size} B"
    elif size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 ** 3:
        return f"{size / (1024 ** 2):.2f} MB"
    else:
        return f"{size / (1024 ** 3):.2f} GB"


def compress_image(image_path, quality=75):
    print("\n" + "=" * 60)
    print("Starting compression...")
    print("=" * 60)

    if not os.path.isfile(image_path):
        print("ERROR: File not found.")
        return

    try:
        # Open image
        image = Image.open(image_path)

        # Original file size
        original_size = os.path.getsize(image_path)

        # Create output folder
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        # Get filename
        filename = os.path.basename(image_path)
        name, extension = os.path.splitext(filename)

        # Save as JPG
        output_path = os.path.join(
            OUTPUT_FOLDER,
            f"{name}_compressed.jpg"
        )

        # Convert images with transparency to RGB
        if image.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", image.size, "white")

            if image.mode == "P":
                image = image.convert("RGBA")

            background.paste(
                image,
                mask=image.getchannel("A")
                if image.mode == "RGBA"
                else None
            )

            image = background

        else:
            image = image.convert("RGB")

        # Compress
        image.save(
            output_path,
            "JPEG",
            quality=quality,
            optimize=True
        )

        # New file size
        compressed_size = os.path.getsize(output_path)

        # Calculate savings
        saved = original_size - compressed_size

        if original_size > 0:
            percentage = (saved / original_size) * 100
        else:
            percentage = 0

        print("\n" + "=" * 60)
        print("COMPRESSION COMPLETED")
        print("=" * 60)

        print(f"Original : {format_size(original_size)}")
        print(f"New      : {format_size(compressed_size)}")
        print(f"Saved    : {format_size(saved)}")
        print(f"Reduction: {percentage:.2f}%")

        print(f"\nSaved to:")
        print(os.path.abspath(output_path))

        print("=" * 60)

    except Exception as e:
        print("\n" + "=" * 60)
        print("COMPRESSION FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        print("=" * 60)


def main():

    print("=" * 60)
    print("              IMAGE COMPRESSOR")
    print("=" * 60)

    print("Enter an image path.")
    print("Type 'exit' to close the program.")

    print("=" * 60)

    while True:

        image_path = input("\nEnter image path: ").strip()

        if not image_path:
            print("Please enter an image path.")
            continue

        if image_path.lower() in ["exit", "quit", "q"]:
            print("\nExiting program. Goodbye!")
            break

        compress_image(image_path)

        print("\nWaiting for next image...")


if __name__ == "__main__":
    main()