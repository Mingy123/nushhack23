from PIL import Image, ImageDraw, ImageFont
import easyocr
reader = easyocr.Reader(['en'])

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


# returns a pil image
def read(filename, confidence_threshold=0.05):
    result = reader.readtext(filename)
    image = Image.open(filename)

    colours = []
    for pos, text, conf in result:
        if conf < confidence_threshold: continue
        if not text.isascii(): continue
        c1 = image.getpixel(tuple(pos[0]))
        colours.append(c1) # NOTE!!! im using the top left corner bcos it works better

    draw = ImageDraw.Draw(image)
    for pos, text, conf in result:
        if conf < confidence_threshold: continue
        if not text.isascii(): continue
        length = abs(pos[0][0] - pos[1][0])
        fsize = maxfont(text, length)
        # draw rectangle
        color = colours.pop(0)
        draw.rectangle([tuple(pos[0]), tuple(pos[2])], fill=color)
        # write text
        font = ImageFont.truetype('font.ttf', size=fsize)
        draw.text(pos[0], text, font=font, fill=(255-color[0], 255-color[1], 255-color[2]))

    return image
