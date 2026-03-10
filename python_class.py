import pywhatkit as kit
import datetime
import time

message = """code check 
"""

group_name = "Kathi sanda veerargal"

while True:
    now = datetime.datetime.now()

    # Check time = 6:55 PM
    if now.hour == 21 and now.minute == 39:
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