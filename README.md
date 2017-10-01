# manga-translator

Automatically translates manga pages from Japanese to English.

# How it works

* Find text bubbles using OpenCV contour manipulations
* OCR the text bubbles with Tesseract
* Send the text to Google Translate
* Typeset the translated text back into the text bubbles

# Example

![untranslated][untranslated]
![translated][translated]

[untranslated]: img/opm-5.jpg
[translated]: translation-example.jpg

# Dependencies

* Python 2.7
* [Tesseract](https://github.com/tesseract-ocr)
* [OpenCV](http://opencv.org/) with Python wrapper
* [Node.js](https://nodejs.org)
* [google-translate-api](https://www.npmjs.com/package/google-translate-api)
* [pytesseract](https://pypi.python.org/pypi/pytesseract)
* NumPy, SciPy, some other Python packages


