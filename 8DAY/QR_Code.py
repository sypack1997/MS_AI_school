import qrcode

qr_data = 'www.naver.com'
qr_img = qrcode.make(qr_data)

qr_img.save(qr_data + '.png')