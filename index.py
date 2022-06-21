import sys
from infi.systray import SysTrayIcon
from infi.systray.traybar import PostMessage, WM_CLOSE
from PIL import Image, ImageDraw,ImageFont
import subprocess
import time

# Constants
mute_command = "$obj = new-object -com wscript.shell; $obj.SendKeys([char]173)"
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

def mute(_):
  subprocess.run(["powershell", "-Command", mute_command], capture_output=True)

def get_volume_level():
  out = subprocess.check_output('powershell ./get_volume.ps1', shell=True, encoding='utf8').strip()
  return int(float(out.replace(',', '.')) * 100)

def custom_shutdown(self):
  if not self._hwnd:
      return
  PostMessage(self._hwnd, WM_CLOSE, 0, 0)


def main():
  default_icon_name = "volume_tray.ico"
  set_icon_text(default_icon_name, 25)
  menu_options = (("Toggle mute", None, mute),)
  systray = None
  SysTrayIcon.shutdown = custom_shutdown
  def on_quit(self):
    systray.shutdown()
    raise SystemExit(0)

  systray = SysTrayIcon(default_icon_name, "", menu_options, on_quit=on_quit)
  systray.start()
  print(get_volume_level())
  while True:
    # systray.update(icon=default_icon_name)
    time.sleep(0.5)

main()
