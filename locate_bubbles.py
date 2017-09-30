#!/usr/bin/python

from PIL import Image

import numpy as np
import cv2


import pytesseract

if __name__ == '__main__':
  img = cv2.imread("img/opm-1.jpg")

  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img_gray = cv2.bitwise_not(cv2.adaptiveThreshold(img_gray, 255, cv2.THRESH_BINARY, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 75, 10))

  kernel = np.ones((2,2),np.uint8)
  img_gray = cv2.erode(img_gray, kernel,iterations = 2)
  img_gray = cv2.bitwise_not(img_gray)
  im2, contours, hierarchy = cv2.findContours(img_gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

  pruned_contours = []
  mask = np.zeros_like(img)
  mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
  height, width, channel = img.shape

  for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 100 and area < ((height / 4) * (width / 4)):
      pruned_contours.append(cnt)

  # find contours for the mask for a second pass after pruning the large and small contours
  cv2.drawContours(mask, pruned_contours, -1, (255,255,255), 1)
  im2, contours2, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

  final_mask = cv2.cvtColor(np.zeros_like(img), cv2.COLOR_BGR2GRAY)
  for cnt in contours2:
    area = cv2.contourArea(cnt)
    if area > 1000 and area < ((height / 4) * (width / 4)):
      draw_mask = cv2.cvtColor(np.zeros_like(img), cv2.COLOR_BGR2GRAY)
      approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
      cv2.fillPoly(draw_mask, [approx], (255,0,0))
      cv2.fillPoly(final_mask, [approx], (255,0,0))
      image = cv2.bitwise_and(draw_mask, cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
      pil_image = Image.fromarray(image)
      pil_image.show()
      text = pytesseract.image_to_string(pil_image, lang="jpn_vert")
      print "Ateempt: " + text

Image.fromarray(final_mask).show()
