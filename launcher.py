import subprocess
import sys
import os

index_file = 'index.py'

# if app is running inside of an executable container,
# application path is inside of the container,
# else it is in the same directory as the executable
if getattr(sys, 'frozen', False):
  application_path = sys._MEIPASS
else:
  application_path = os.path.dirname(os.path.abspath(__file__))

# index_path is application path + index_file
index_path = os.path.join(application_path, index_file)
# call the subprocess with python and index_path,
# which leads to index.py being executed in the background.
subprocess.call('python ' + index_path, shell=True)