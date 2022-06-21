from infi.systray import SysTrayIcon
from PIL import Image, ImageDraw,ImageFont
import time

image_name = "volume_tray.ico"
font_type = ImageFont.truetype("arial.ttf", 55)
systray = None

def set_icon_text(icon_image_name: str, text: int):
  new_img = Image.new('RGBA', (65, 65), color = (255, 255, 255, 0))
  drawed = ImageDraw.Draw(new_img)
  drawed.text((5, 5), f"{text}", fill=(255,255,255), font = font_type)
  new_img.save(icon_image_name)

def update_systray(icon_image_name: str):
  if not systray:
    systray = SysTrayIcon("volume_tray.ico", "Example tray icon", ())
    systray.start()
  else:
    systray.update(icon=icon_image_name)
