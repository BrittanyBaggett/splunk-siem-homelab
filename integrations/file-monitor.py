from watchdog.events import FileSystemEventHandler
from watchdog.events import FileModifiedEvent
from watchdog.observers import Observer
import logging
import time


# ----------------------------------------
# File Modification Event Handler
# ----------------------------------------

# Inherit from FileSystemEventHandler to handle filesystem events.
class MyEventHandler(FileSystemEventHandler):

    # Called automatically when Watchdog detects a modification.
    def on_modified(self, event: FileModifiedEvent):

        # Ignore directory changes and log file modifications only.
        if event.is_directory == False:
            logging.info(f"{event.src_path} | File Modified")


# ----------------------------------------
# Observer Configuration
# ----------------------------------------

# Create an instance of the custom event handler.
event_handler = MyEventHandler()

# Create an observer to monitor the specified directory.
observer = Observer()

# Define the directory to monitor.
path = "C:\Lab\MonitoredFiles"

# Schedule monitoring without including subdirectories.
observer.schedule(event_handler, path, recursive=False)


# ----------------------------------------
# Logging Configuration
# ----------------------------------------

# Configure logging to record timestamps, severity, and file paths.
logging.basicConfig(
    level=logging.INFO,
    filename="file_monitor.log",
    format='%(asctime)s %(levelname)s: %(message)s'
)


# ----------------------------------------
# Start File Monitoring
# ----------------------------------------

# Start the observer and automatically stop it when the context exits.
with observer:

    # Keep the program running while Watchdog monitors the directory.
    while True:

        # Pause the main thread to prevent unnecessary CPU usage.
        time.sleep(1)
