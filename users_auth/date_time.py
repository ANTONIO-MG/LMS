import time
from datetime import datetime

def get_date_at_midnight():
    while True:
        now = datetime.now()
        if now.hour == 0 and now.minute == 0 and now.second == 0:
            return now.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(1)  # Check every second