import qrcode

for i in range(100, 105):
    image = qrcode.make(f"http://localhost:8100/signin?room={i}")
    image.save(f"qrcodes/room{i}.png")