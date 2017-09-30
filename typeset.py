from PIL import Image
from PIL import ImageDraw


def flow_into_box(text, w, min_word_on_line=.3):
    dimg = Image.new("RGB", (100, 100))
    d = ImageDraw.Draw(dimg)
    lines = []
    idx = 0
    line = ""
    while idx < len(text):
        running_width = d.textsize(line)[0]
        next_token = text.find(" ", idx + 1)
        if next_token != -1:
            c_text = text[idx:next_token]
        else:
            c_text = text[idx:]
        print c_text
        c_width = d.textsize(c_text)[0]
        proportion_of_fit = (w - running_width) // c_width

        if proportion_of_fit >= 1:
            pass  # We're good
        elif proportion_of_fit > min_word_on_line:
            split = int(proportion_of_fit * len(c_text))
            c_text = c_text[:split]
        else:
            if line:
                lines.append(line)
                line = ""
            else:
                lines.append(c_text)
                idx += len(c_text)
            continue

        line += c_text
        idx += len(c_text)

    return "\n".join(lines)


def typeset_blurb(img, blurb):
    pass
