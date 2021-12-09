# Import built-in python packages
import sqlite3
import time

# Import downloaded python packages
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


con = sqlite3.connect('db/sendlist.sqlite')
CUR = con.cursor()


def timer_status() -> bool:
    """Returns timer's bool status.
    ON - True, OFF - False"""

    request = "SELECT value FROM settings WHERE [key] = 'timer_enable'"
    result = CUR.execute(request).fetchall()[0][0]

    if result == 'ON':
        return True
    elif result == 'OFF':
        return False


def timer_enable() -> bool:
    """Turns on the timer
    Sets the value of timer_enable to 'ON' """

    # If we need to check the status (ON/OFF)
    request = "UPDATE settings SET value = 'ON' WHERE [key] = 'timer_enable'"

    CUR.execute(request).fetchall()
    con.commit()

    return True


def timer_disable() -> bool:
    """Turns on the timer
    Sets the value of timer_enable to 'OFF'"""

    # If we need to check the status (ON/OFF)
    request = "UPDATE settings SET value = 'OFF' WHERE [key] = 'timer_enable'"

    CUR.execute(request).fetchall()
    con.commit()

    return True


def update_minutes(minutes: int) -> bool:
    """Sets the update_minutes to {minutes}"""

    request = f"UPDATE settings SET value = '{minutes}' WHERE [key] = 'timer_enable'"

    CUR.execute(request).fetchall()
    con.commit()

    return True


def get_minutes_pause() -> int:
    """Returns a timer delay in minutes from database"""

    request = "SELECT value FROM settings WHERE [key] = 'update_minutes'"
    minutes = CUR.execute(request).fetchall()[0][0]

    return minutes


def timer():
    """Actual timer of shedule updating. Uses:
    timer_status()
    get_minutes_pause()
    """

    while True:
        if timer_status():
            time.sleep(get_minutes_pause() * 60)
            print('YES')
        else:
            print('NO')


if __name__ == '__main__':
    timer()