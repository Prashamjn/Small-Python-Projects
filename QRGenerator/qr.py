import qrcode
import os

# Create output folder
output_folder = "Generated QR Codes"
os.makedirs(output_folder, exist_ok=True)

# Get data from user
data = input("ENTER TEXT OR LINK: ")

# Generate QR code
img = qrcode.make(data)

# Save QR code
output_path = os.path.join(output_folder, "img.png")
img.save(output_path)

# Open generated QR code
img.show()

print(f"QRCODE GENERATED AND SAVED IN '{output_folder}/img.png' !!!")
