from PIL import Image, ImageEnhance
import json
import mss
import numpy as np

with open("config.json", "r", encoding="utf-8") as file:
  config = json.load(file)

SCREEN_REGION = config.get("screen_region", [0, 0, 1920, 1080])
OFFSET_X, OFFSET_Y = SCREEN_REGION[0], SCREEN_REGION[1]


def enhanced_screenshot(region=(0, 0, 1920, 1080)) -> Image.Image:
  with mss.mss() as sct:
    monitor = {
      "left": OFFSET_X + region[0],
      "top": OFFSET_Y + region[1],
      "width": region[2],
      "height": region[3],
    }
    img = sct.grab(monitor)
    img_np = np.array(img)
    img_rgb = img_np[:, :, :3][:, :, ::-1]
    pil_img = Image.fromarray(img_rgb)

  pil_img = pil_img.resize((pil_img.width * 2, pil_img.height * 2), Image.BICUBIC)
  pil_img = pil_img.convert("L")
  pil_img = ImageEnhance.Contrast(pil_img).enhance(1.5)

  return pil_img


def capture_region(region=(0, 0, 1920, 1080)) -> Image.Image:
  with mss.mss() as sct:
    monitor = {
      "left": OFFSET_X + region[0],
      "top": OFFSET_Y + region[1],
      "width": region[2],
      "height": region[3],
    }
    img = sct.grab(monitor)
    img_np = np.array(img)
    img_rgb = img_np[:, :, :3][:, :, ::-1]
    return Image.fromarray(img_rgb)