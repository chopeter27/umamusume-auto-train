import json
import pyautogui

with open("config.json", "r", encoding="utf-8") as file:
  config = json.load(file)

GAME_REGION = tuple(config.get("screen_region", [0, 0, 1920, 1080]))


def ura():
  race_btn = pyautogui.locateCenterOnScreen(
    "assets/ura/ura_race_btn.png", confidence=0.8, minSearchTime=0.2, region=GAME_REGION
  )
  if race_btn:
    pyautogui.click(race_btn)

