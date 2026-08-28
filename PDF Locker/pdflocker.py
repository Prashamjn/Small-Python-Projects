from pypdf import PdfReader,PdfWriter
reader = PdfReader("TG105.pdf")
writer = PdfWriter()

writer.append(reader)
writer.encrypt("12345")

with open("protected.pdf","wb") as file:
    writer.write(file)
