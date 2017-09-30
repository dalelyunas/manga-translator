from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from ocr import TranslatedBlurb
import math


def flow_into_box(text, w, font=None, min_word_on_line=.3):
    def text_width(l):
        if l:
            return d.textsize(l, font=font)[0]
        else:
            return 0
    dimg = Image.new("RGB", (100, 100))
    d = ImageDraw.Draw(dimg)
    lines = []
    idx = 0
    line = ""
    while idx < len(text):
        if not line and text[idx] == " ":
            idx += 1
        running_width = text_width(line)
        next_token = text.find(" ", idx + 1)
        if next_token != -1:
            c_text = text[idx:next_token]
        else:
            c_text = text[idx:]
        c_width = text_width(c_text)
        proportion_of_fit = float(w - running_width) / c_width
        if proportion_of_fit > .95:
            line += c_text
            idx += len(c_text)
        elif proportion_of_fit > min_word_on_line:
            split = max(int(proportion_of_fit * len(c_text)), 1)
            c_text = c_text[:split] + "-"
            line += c_text
            idx += len(c_text) - 1
        else:
            if len(line) > 0:
                lines.append(line)
                line = ""
            else:
                split = max(int(proportion_of_fit * len(c_text)), 1)
                c_text = c_text[:split] + "-"
                lines.append(c_text)
                idx += len(c_text) - 1

    if len(line) > 0:
        lines.append(line)

    return "\n".join(lines)


def typeset_blurb(img, blurb):
    if isinstance(blurb, TranslatedBlurb):
        text = blurb.translation
    else:
        text = blurb.text

    area = blurb.w * blurb.h
    fontsize = int(math.sqrt(area) / 10)
    font = ImageFont.truetype(font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=fontsize)
    flowed = flow_into_box(text, blurb.w)
    d = ImageDraw.Draw(img)
    img.paste((255, 255, 255), (blurb.x, blurb.y, blurb.x + blurb.w, blurb.y + blurb.h))
    d.text((blurb.x, blurb.y), flowed.strip(), fill=(0, 0, 0), font=font)
