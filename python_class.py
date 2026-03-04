import pywhatkit as kit
import datetime
import time

message = """Good evening friends😊
Online class starting at 7 PM.
Join here:
https://meet.google.com/uhh-yhhu-idr
"""

group_name = "BCA- III Year-BOYS-2026"

while True:
    now = datetime.datetime.now()

    # Check time = 6:55 PM
    if now.hour == 18 and now.minute == 55:
        kit.sendwhatmsg_to_group_instantly(
            group_name,
            message,
            wait_time=15,
            tab_close=True
        )

        print("Message Sent ✅")

        # Prevent multiple sending in same minute
        time.sleep(60)

    time.sleep(10)  # check every 10 seconds