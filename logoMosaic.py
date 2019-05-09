#! python3
# makeBrazil.py

import sys, shutil, os
from PIL import Image

white = (255, 255, 255)
black = (0, 0, 0)

original = Image.open(sys.argv[1])
print(original.size)
mosaic = Image.new('RGB', (original.size[0]*200, original.size[1]*200), color=(255,255,255))

path = ('C:\\test\\LKDlogos\\')
logoList = os.listdir(path)

nextImage = 0

for c in range(0,original.size[0]):
    for r in range(0,original.size[1]):
        pixel = original.getpixel((c,r))
        if pixel == 0:
            logo = Image.open(path+logoList[nextImage]).resize((200, 200))
            nextImage += 1
            mosaic.paste(logo, (c*200, r*200))

mosaic.save("C:\\test\\mosaic.png")