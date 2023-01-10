import qrcode

# Create the QR code image
img = qrcode.make("https://classroom.google.com")

# Save the image to a file
img.save("qr_code.png")
