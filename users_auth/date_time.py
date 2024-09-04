import time
from datetime import datetime

def get_date_at_midnight():
    """
    Continuously checks the current time and returns the date and time as a string
    formatted as "YYYY-MM-DD HH:MM:SS" when it is exactly midnight (00:00:00).
    
    The function runs an infinite loop, checking the time every second.
    """
    while True:
        now = datetime.now()  # Get the current date and time
        # Check if the current time is exactly midnight
        if now.hour == 0 and now.minute == 0 and now.second == 0:
            # Return the date and time as a formatted string
            return now.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(1)  # Wait for 1 second before checking again