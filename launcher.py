import subprocess

independent_process = subprocess.Popen(
    'python ./index.py',
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
)