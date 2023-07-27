import qrcode

for i in range(125,135):
    image = qrcode.make(f"http://localhost:8100/home?room={i}")
    image.save(f"backend/scripts/qrcodes/room{i}.png")
    