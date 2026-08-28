import barcode
import os

from barcode.writer import ImageWriter

# Create output folder
output_folder = "Generated Barcodes"
os.makedirs(output_folder, exist_ok=True)

# Get data from user
data = input("Enter the data to encode in the barcode: ")

# Generate barcode
output_path = os.path.join(output_folder, "barcode")

barcode.get("code128", data, writer=ImageWriter()).save(output_path)

print(f"Barcode generated and saved in '{output_folder}/barcode.png'")
