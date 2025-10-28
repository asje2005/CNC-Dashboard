import os

import time
import pandas as pd
import sqlite3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_FOLDER = "data/raw_logs"
OUTPUT_DB = "output/cnc_data.db"

class CNCLogHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".csv"):
            print(f"New file detected: {event.src_path}")
            process_file(event.src_path)

def process_file(filepath):
    try:
        df = pd.read_csv(filepath)
        df['timestamp'] = pd.to_datetime(df['timestamp'])  # Optional: normalize time
        conn = sqlite3.connect(OUTPUT_DB)
        df.to_sql("cnc_logs", conn, if_exists="append", index=False)
        conn.close()
        print(f"Saved {filepath} to database.")
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