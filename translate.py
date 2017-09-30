import subprocess
from ocr import Blurb, TranslatedBlurb


def translate_text(text):
    bs = subprocess.check_output(["node", "translate.js", text])
    return bs


def translate_blurb(blurb):
    translation = translate_text(blurb.text)
    return TranslatedBlurb.as_translated(blurb, translation)
