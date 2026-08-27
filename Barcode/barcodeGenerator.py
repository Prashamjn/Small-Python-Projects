import barcode

from barcode.writer import ImageWriter

data = input("Enter the data to encode in the barcode: ")

barcode.get('code128', data, writer=ImageWriter()).save("barcode")

print("Barcode generated and saved as 'barcode.png'")