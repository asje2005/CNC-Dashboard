import os
import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_FOLDER = "data/raw_logs"
OUTPUT_DB = "output/cnc_data.db"

class CNCLogHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".txt") or event.src_path.endswith(".csv"):
            print(f"New file detected: {event.src_path}")
            self.process_file(event.src_path)

    def process_file(self, filepath):
        try:
            df = pd.read_csv(filepath)  # Adjust for your log format
            # Add parsing logic here (e.g., extract program name, cycle time)
            df.to_sql("cnc_logs", sqlite3.connect(OUTPUT_DB), if_exists="append", index=False)
            print(f"Data saved to {OUTPUT_DB}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    event_handler = CNCLogHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()
    print(f"Monitoring {WATCH_FOLDER} for new CNC logs...")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()