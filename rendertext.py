from PIL import Image, ImageDraw, ImageFont

def getlength(text, font_size):
    temp_img = Image.new('RGB', (1, 1), color='white')
    draw = ImageDraw.Draw(temp_img)
    font = ImageFont.truetype('font.ttf', font_size)
    return draw.textlength(text, font=font)

def maxfont(text, length):
    fsize = 4
    while getlength(text, fsize) < length:
        fsize += 1
    return fsize - 1

import easyocr
reader = easyocr.Reader(['en'])
print('reading now')
result = reader.readtext('out.jpg')
image = Image.open('out.jpg')

colours = []
for pos, text, conf in result:
    if conf < 0.05: continue
    if not text.isascii(): continue
    c1 = image.getpixel(tuple(pos[0]))
    c2 = image.getpixel(tuple(pos[1]))
    c3 = image.getpixel(tuple(pos[2]))
    c4 = image.getpixel(tuple(pos[3]))
    color = tuple((a + b + c + d) // 3 for a, b, c, d in zip(c1, c2, c3, c4))
    colours.append(c1) # NOTE!!! im choosing to use the top left corner bcos it works better

draw = ImageDraw.Draw(image)
for pos, text, conf in result:
    if conf < 0.05: continue
    if not text.isascii(): continue
    length = abs(pos[0][0] - pos[1][0])
    fsize = maxfont(text, length)
    print(f'{text}: confidence = {conf}, length = {length}')
    # draw rectangle
    color = colours.pop(0)
    draw.rectangle([tuple(pos[0]), tuple(pos[2])], fill=color)
    # write text
    font = ImageFont.truetype('font.ttf', size=fsize)
    draw.text(pos[0], text, font=font, fill=(255, 0, 0))
image.show()
