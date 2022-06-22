from PIL import Image, ImageDraw,ImageFont
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from threading import Thread
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
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame
        self.update_icon()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        exitItem = wx.MenuItem(menu, -1, 'Exit')
        menu.Bind(wx.EVT_MENU, self.on_exit, id=exitItem.GetId())
        menu.Append(exitItem)
        return menu

    @staticmethod
    def refresh_icon(volume):
      new_img = Image.new('RGBA', (65, 65), color = (255, 255, 255, 0))
      drawed = ImageDraw.Draw(new_img)
      drawed.text((5, 5), f"{volume}", fill=(255,255,255), font = TaskBarIcon.font_type)
      new_img.save(TaskBarIcon.tray_icon)

    def update_icon(self):
        icon = wx.Icon(wx.Bitmap(TaskBarIcon.tray_icon))
        self.SetIcon(icon, 'Volume level')

    def on_exit(self, event):
        self.frame.Close()

class IconUpdateThread(Thread):
    def __init__(self, icon, audio):
        Thread.__init__(self)
        self.daemon = True

        self.audio = audio
        self.icon = icon
        self.start()
    def run(self):
        while True:
          currVolume = self.audio.getVolume()
          TaskBarIcon.refresh_icon(currVolume)
          self.icon.update_icon()
          time.sleep(.5)

class App(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "", size=(1,1))
        wx.Panel(self)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.icon = TaskBarIcon(self)
        self.audio = Audio()
        IconUpdateThread(self.icon, self.audio)
      
    def onClose(self, evt):
        self.icon.RemoveIcon()
        self.icon.Destroy()
        self.Destroy()

if __name__ == "__main__":
    wxApp = wx.App()
    App()
    wxApp.MainLoop()
