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

  def get_volume(self):
    return int(round(self.volume.GetMasterVolumeLevelScalar() * 100))

  def is_muted(self):
    return self.volume.GetMute()

  def toggle_mute(self):
    self.volume.SetMute(not self.is_muted(), None)

class TaskBarIcon(wx.adv.TaskBarIcon):
    tray_icon = 'volume_tray.ico'
    font_type = ImageFont.truetype("arial.ttf", 45)
    size = 50

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
    def refresh_icon(volume, is_muted):
      new_img = Image.new('RGBA', (TaskBarIcon.size, TaskBarIcon.size), color = (255, 255, 255, 0))
      drawed = ImageDraw.Draw(new_img)
      if is_muted:
        drawed.line([(0, 0), (TaskBarIcon.size, TaskBarIcon.size)], fill = (255,0,0,150), width = 8)
        drawed.line([(0, TaskBarIcon.size), (TaskBarIcon.size, 0)], fill = (255,0,0,150), width = 8)
      drawed.text((0, 0), f"{volume}", fill=(255,255,255), font = TaskBarIcon.font_type)
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
        currVolume = self.audio.get_volume()
        is_muted = self.audio.is_muted()
        TaskBarIcon.refresh_icon(currVolume, is_muted)
        self.icon.update_icon()
        time.sleep(.2)

class App(wx.Frame):
    def __init__(self):
      wx.Frame.__init__(self, None, wx.ID_ANY, "", size=(1,1))
      wx.Panel(self)
      self.Bind(wx.EVT_CLOSE, self.on_close)

      self.icon = TaskBarIcon(self)
      self.audio = Audio()
      self.icon.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.mute)
      IconUpdateThread(self.icon, self.audio)

    def mute(self, event):
      self.audio.toggle_mute()
      
    def on_close(self, event):
      self.icon.RemoveIcon()
      self.icon.Destroy()
      self.Destroy()

if __name__ == "__main__":
  wxApp = wx.App()
  App()
  wxApp.MainLoop()
