import os
from PIL import Image

OUTPUT_FOLDER = "pdf_output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def convert_image_to_pdf(image_path):
    print("\n" + "=" * 60)
    print("Converting image to PDF...")
    print("=" * 60)

    if not os.path.isfile(image_path):
        print("ERROR: File not found.")
        return

    try:
        image = Image.open(image_path)

        # Convert to RGB because PDF does not support all image modes
        if image.mode != "RGB":
            image = image.convert("RGB")

        filename = os.path.basename(image_path)
        name = os.path.splitext(filename)[0]

        output_path = os.path.join(
            OUTPUT_FOLDER,
            f"{name}.pdf"
        )

        image.save(output_path, "PDF", resolution=100.0)

        print("\n" + "=" * 60)
        print("CONVERSION COMPLETED")
        print("=" * 60)
        print(f"Input  : {image_path}")
        print(f"Output : {os.path.abspath(output_path)}")
        print("=" * 60)

    except Exception as e:
        print("\n" + "=" * 60)
        print("CONVERSION FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        print("=" * 60)


def main():

    print("=" * 60)
    print("             IMAGE → PDF CONVERTER")
    print("=" * 60)
    print("Enter an image path.")
    print("Type 'exit' to close.")
    print("=" * 60)

    while True:

        image_path = input("\nEnter image path: ").strip()

        if not image_path:
            print("Please enter an image path.")
            continue

        if image_path.lower() in ["exit", "quit", "q"]:
            print("\nGoodbye!")
            break

        convert_image_to_pdf(image_path)

        print("\nWaiting for next image...")


if __name__ == "__main__":
    main()