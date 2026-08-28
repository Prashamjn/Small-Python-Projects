from pypdf import PdfReader, PdfWriter
import os

# Create output folder
output_folder = "Locked PDFs"
os.makedirs(output_folder, exist_ok=True)

print("================================")
print("         PDF LOCKER")
print("================================")

# Ask for PDF file
pdf_path = input("\nEnter the PDF file path: ")

# Check if PDF exists
if not os.path.exists(pdf_path):
    print("\nPDF file not found!")
    exit()

# Ask for password
password = input("Enter the password: ")

# Ask for output filename
filename = input("Enter the name for the locked PDF: ")

# Add .pdf if user didn't enter it
if not filename.lower().endswith(".pdf"):
    filename += ".pdf"

# Create output path
output_path = os.path.join(output_folder, filename)

# Read PDF
reader = PdfReader(pdf_path)

# Create PDF writer
writer = PdfWriter()

# Copy all pages
writer.append(reader)

# Encrypt PDF
writer.encrypt(password)

# Save protected PDF
with open(output_path, "wb") as file:
    writer.write(file)

print("\n================================")
print("PDF LOCKED SUCCESSFULLY!")
print(f"Saved at: {output_path}")
print("================================")
