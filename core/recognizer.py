import cv2
import json
import numpy as np
from PIL import ImageGrab, ImageStat

from utils.screenshot import capture_region

with open("config.json", "r", encoding="utf-8") as file:
  config = json.load(file)

SCREEN_REGION = config.get("screen_region", [0, 0, 1920, 1080])
OFFSET_X, OFFSET_Y, WIDTH, HEIGHT = (
  SCREEN_REGION[0], SCREEN_REGION[1], SCREEN_REGION[2], SCREEN_REGION[3]
)


def match_template(template_path, region=None, threshold=0.85):
  # Get screenshot
  if region:
    left = OFFSET_X + region[0]
    top = OFFSET_Y + region[1]
    right = left + region[2]
    bottom = top + region[3]
    screen = np.array(ImageGrab.grab(bbox=(left, top, right, bottom)))
  else:
    screen = np.array(
      ImageGrab.grab(bbox=(OFFSET_X, OFFSET_Y, OFFSET_X + WIDTH, OFFSET_Y + HEIGHT))
    )
  screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

  # Load template
  template = cv2.imread(template_path, cv2.IMREAD_COLOR)  # safe default
  if template.shape[2] == 4:
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
  result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
  loc = np.where(result >= threshold)

  h, w = template.shape[:2]
  boxes = [(x, y, w, h) for (x, y) in zip(*loc[::-1])]

  return deduplicate_boxes(boxes)


def deduplicate_boxes(boxes, min_dist=5):
  filtered = []
  for x, y, w, h in boxes:
    cx, cy = x + w // 2, y + h // 2
    if all(abs(cx - (fx + fw // 2)) > min_dist or abs(cy - (fy + fh // 2)) > min_dist
        for fx, fy, fw, fh in filtered):
      filtered.append((x, y, w, h))
  return filtered

def is_infirmary_active(REGION):
  screenshot = capture_region(REGION)
  grayscale = screenshot.convert("L")
  stat = ImageStat.Stat(grayscale)
  avg_brightness = stat.mean[0]

  # Treshold infirmary btn
  return avg_brightness > 150
