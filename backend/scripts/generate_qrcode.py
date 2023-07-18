import qrcode

for i in range(125,128):
    image = qrcode.make(f"http://localhost:8100/classroom/{i}")
    image.save(f"backend/scripts/qrcodes/room{i}.png")