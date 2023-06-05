from PIL import Image
import piexif

image = Image.open('img_from_bytes.jpeg')

exif_ifd = {piexif.ExifIFD.UserComment: 'some data'.encode()}

exif_dict = {"0th": {}, "Exif": exif_ifd, "1st": {},
         "thumbnail": None, "GPS": {}}
exif_dat = piexif.dump(exif_dict)
image.save('img_with_exif.jpeg',  exif=exif_dat)
