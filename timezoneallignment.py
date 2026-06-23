from datetime import datetime
import pytz

# ClickBank timestamps are usually in US Pacific Time
clickbank_tz = pytz.timezone('US/Pacific')

# Your local time zone (e.g., London)
local_tz = pytz.timezone('Europe/London')

# Example timestamp from ClickBank
cb_time_str = "2025-10-20 14:30:00"

# Parse and convert
cb_time = clickbank_tz.localize(datetime.strptime(cb_time_str, "%Y-%m-%d %H:%M:%S"))
local_time = cb_time.astimezone(local_tz)

print("ClickBank Time:", cb_time.strftime("%Y-%m-%d %H:%M:%S %Z"))
print("Local Time:", local_time.strftime("%Y-%m-%d %H:%M:%S %Z"))
