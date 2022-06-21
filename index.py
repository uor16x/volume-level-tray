from infi.systray import SysTrayIcon
from PIL import Image, ImageDraw,ImageFont
import time

font_type = ImageFont.truetype("arial.ttf", 55)

def set_icon_text(icon_image_name: str, text: int):
  new_img = Image.new('RGBA', (65, 65), color = (255, 255, 255, 0))
  drawed = ImageDraw.Draw(new_img)
  drawed.text((5, 5), f"{text}", fill=(255,255,255), font = font_type)
  new_img.save(icon_image_name)

def update_systray(icon_image_name: str):
  if systray is None:
    systray = SysTrayIcon(icon_image_name, "Example tray icon", ())
    systray.start()
  else:
    systray.update(icon=icon_image_name)

def main():
  default_icon_name = "volume_tray.ico"
  set_icon_text(default_icon_name, 25)
  systray = SysTrayIcon(default_icon_name, "", ())
  systray.start()
  while True:
    systray.update(icon=default_icon_name)
    time.sleep(5)

main()
