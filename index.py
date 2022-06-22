from infi.systray import SysTrayIcon
from infi.systray.traybar import PostMessage, WM_CLOSE
from PIL import Image, ImageDraw,ImageFont
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import subprocess
import time

# Constants
font_type = ImageFont.truetype("arial.ttf", 55)

class Audio:
  def __init__(self):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    self.volume = cast(interface, POINTER(IAudioEndpointVolume))

  def getVolume(self):
    return int(round(self.volume.GetMasterVolumeLevelScalar() * 100))

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


def get_volume_level():
  out = subprocess.check_output('powershell ./get_volume.ps1', shell=True, encoding='utf8').strip()
  return int(float(out.replace(',', '.')) * 100)

def custom_shutdown(self):
  if not self._hwnd:
      return
  PostMessage(self._hwnd, WM_CLOSE, 0, 0)


def main():
  audio = Audio()
  default_icon_name = "volume_tray.ico"
  set_icon_text(default_icon_name, 25)
  menu_options = (("Toggle mute", None, None),)
  systray = None
  SysTrayIcon.shutdown = custom_shutdown
  def on_quit(self):
    systray.shutdown()
    raise SystemExit(0)

  systray = SysTrayIcon(default_icon_name, "", menu_options, on_quit=on_quit)
  systray.start()
  print(get_volume_level())
  volume = init_audio()
  while True:
    # systray.update(icon=default_icon_name)
    time.sleep(0.5)

main()
