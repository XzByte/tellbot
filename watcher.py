# filepath: /e:/work/tellbot/src/watcher.py
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script, python_path):
        self.script = script
        self.python_path = python_path
        self.process = subprocess.Popen([self.python_path, self.script])

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            self.process.terminate()
            self.process = subprocess.Popen([self.python_path, self.script])

if __name__ == "__main__": 
    path = "."
    script = os.path.join(os.getcwd(), "src", "bot.py")
    python_path = os.path.join(os.getcwd(), "Scripts", "python.exe")  # Adjust if your venv is in a different location
    event_handler = ChangeHandler(script, python_path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()