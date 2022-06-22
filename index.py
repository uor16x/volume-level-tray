import sys
from PIL import Image, ImageDraw,ImageFont
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import wx.adv
import wx
import time


class Audio:
  def __init__(self):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    self.volume = cast(interface, POINTER(IAudioEndpointVolume))

  def getVolume(self):
    return int(round(self.volume.GetMasterVolumeLevelScalar() * 100))


class TaskBarIcon(wx.adv.TaskBarIcon):
    tray_icon = 'volume_tray.ico'
    font_type = ImageFont.truetype("arial.ttf", 55)

    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.update()

    @staticmethod
    def refresh_icon(volume):
      new_img = Image.new('RGBA', (65, 65), color = (255, 255, 255, 0))
      drawed = ImageDraw.Draw(new_img)
      drawed.text((5, 5), f"{volume}", fill=(255,255,255), font = TaskBarIcon.font_type)
      new_img.save(TaskBarIcon.tray_icon)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        exitItem = wx.MenuItem(menu, -1, 'Exit')
        menu.Bind(wx.EVT_MENU, self.on_exit, id=exitItem.GetId())
        menu.Append(exitItem)
        return menu

    def update(self):
      icon = wx.Icon(TaskBarIcon.tray_icon)
      self.SetIcon(icon, '')

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()
        sys.exit(0)

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        self.icon = TaskBarIcon(frame)
        audio = Audio()
        while True:
          currVolume = audio.getVolume()
          TaskBarIcon.refresh_icon(currVolume)
          self.icon.update()
          time.sleep(.5)

def main():
  app = App(False)
  app.MainLoop()

main()
