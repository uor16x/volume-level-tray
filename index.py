from PIL import Image, ImageDraw,ImageFont
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from threading import Thread
from os.path import exists
import wx.adv
import wx
import time

class Audio:
  """Class"""
  """Class for sound info retrieval"""
  def __init__(self):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    self.volume = cast(interface, POINTER(IAudioEndpointVolume))

  def get_volume(self):
    """Get integer number with range 0-100 which represents the volume percentage"""
    return int(round(self.volume.GetMasterVolumeLevelScalar() * 100))

  def is_muted(self):
    """Returns 1 if muted, 0 if not"""
    return self.volume.GetMute()

  def toggle_mute(self):
    """Toggles mute"""
    self.volume.SetMute(not self.is_muted(), None)

class TaskBarIcon(wx.adv.TaskBarIcon):
  """Class for taskbar icon"""
  tray_icon = 'volume_tray.ico'
  font_type = ImageFont.truetype("arial.ttf", 45)
  # icon is a square, so its size could be represented by a single number
  size = 50

  def __init__(self, frame):
    wx.adv.TaskBarIcon.__init__(self)
    self.frame = frame
    # if icon is not found, it will be created
    if not exists(TaskBarIcon.tray_icon):
      TaskBarIcon.refresh_icon(0, False)
    # set icon for the first time
    self.update_icon()

  def CreatePopupMenu(self):
    """Generate menu for the taskbar icon"""
    menu = wx.Menu()
    # exit menu item
    exitItem = wx.MenuItem(menu, -1, 'Exit')
    menu.Bind(wx.EVT_MENU, self.on_exit, id=exitItem.GetId())
    menu.Append(exitItem)
    return menu

  @staticmethod
  def refresh_icon(volume, is_muted):
    """Refresh icon with new volume level"""
    new_img = Image.new('RGBA', (TaskBarIcon.size, TaskBarIcon.size), color = (255, 255, 255, 0))
    drawed = ImageDraw.Draw(new_img)
    # if muted, draw a red cross
    if is_muted:
      drawed.line([(0, 0), (TaskBarIcon.size, TaskBarIcon.size)], fill = (255,0,0,150), width = 8)
      drawed.line([(0, TaskBarIcon.size), (TaskBarIcon.size, 0)], fill = (255,0,0,150), width = 8)
    # draw volume level
    drawed.text((0, 0), f"{volume}", fill=(255,255,255), font = TaskBarIcon.font_type)
    # store image as the icon
    new_img.save(TaskBarIcon.tray_icon)

  def update_icon(self):
    """Set the icon for the taskbar icon"""
    icon = wx.Icon(wx.Bitmap(TaskBarIcon.tray_icon))
    self.SetIcon(icon, 'Volume level')

  def on_exit(self, event):
    """Exit the application"""
    self.frame.Close()

class IconUpdateThread(Thread):
  """Class for thread which updates the icon in infinite loop"""
  def __init__(self, icon, audio):
    Thread.__init__(self)
    self.daemon = True

    self.audio = audio
    self.icon = icon
    self.start()
  def run(self):
    while True:
      # get volume level
      currVolume = self.audio.get_volume()
      # get mute status
      is_muted = self.audio.is_muted()
      # refresh icon
      TaskBarIcon.refresh_icon(currVolume, is_muted)
      self.icon.update_icon()
      # pause for 0.2 seconds
      time.sleep(.2)

class App(wx.Frame):
  """Class for main application"""
  def __init__(self):
    wx.Frame.__init__(self, None, wx.ID_ANY, "", size=(1,1))
    wx.Panel(self)
    self.Bind(wx.EVT_CLOSE, self.on_close)

    # create taskbar icon
    self.icon = TaskBarIcon(self)
    # create audio object
    self.audio = Audio()
    # bind left click to mute function
    self.icon.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.mute)
    # create thread which updates the icon
    IconUpdateThread(self.icon, self.audio)

  def mute(self, event):
    """Mute/unmute audio"""
    self.audio.toggle_mute()
    
  def on_close(self, event):
    """Destroy the icon on close"""
    self.icon.RemoveIcon()
    self.icon.Destroy()
    self.Destroy()

if __name__ == "__main__":
  wxApp = wx.App()
  App()
  wxApp.MainLoop()
