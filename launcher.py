import subprocess
import sys
import os

index_file = 'index.py'
if getattr(sys, 'frozen', False):
  application_path = sys._MEIPASS
else:
  application_path = os.path.dirname(os.path.abspath(__file__))

index_path = os.path.join(application_path, index_file)
subprocess.call('python ' + index_path, shell=True)