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

    request = "SELECT value FROM timer WHERE setting = 'timer_enable'"
    result = CUR.execute(request).fetchall()[0][0]

    if result == 'ON':
        return True
    elif result == 'OFF':
        return False


def timer_enable() -> bool:
    """Turns on the timer
    Sets the value of timer_enable to 'ON' """

    # If we need to check the status (ON/OFF)
    request = "UPDATE timer SET value = 'ON' WHERE setting = 'timer_enable'"

    CUR.execute(request).fetchall()
    con.commit()

    return True


def timer_disable() -> bool:
    """Turns on the timer
    Sets the value of timer_enable to 'OFF'"""

    # If we need to check the status (ON/OFF)
    request = "UPDATE timer SET value = 'OFF' WHERE setting = 'timer_enable'"

    CUR.execute(request).fetchall()
    con.commit()

    return True


def update_delay(unit: int) -> bool:  # Sooner, this func will be re refactored
    """Sets the update_minutes to {minutes}"""

    request = f"UPDATE timer SET value = '{unit}' WHERE setting = 'update_times\'"

    CUR.execute(request).fetchall()
    con.commit()

    return True


def get_delay() -> int:
    """Returns a timer delay"""

    request = "SELECT value FROM timer WHERE setting = 'update_time'"
    update_time = CUR.execute(request).fetchall()[0][0]

    return update_time * get_delay_type()


def change_delay_type(delay_type: str) -> bool:
    """Sets the delay_type to {delay_type}"""

    request = f'UPDATE timer SET value = "{delay_type}" WHERE setting = "delay_type"'

    CUR.execute(request).fetchall()
    con.commit()

    return True


def get_delay_type() -> int:
    """Returns a time unit multiplier
    SECONDS - 1, MINUTES - 60, HOURS - 3600, DAYS - 86400"""

    request = "SELECT value FROM timer WHERE setting = 'delay_type'"  # Not finished

    result = CUR.execute(request).fetchall()[0][0]

    if result == 'SECONDS':
        return 1
    elif result == 'MINUTES':
        return 1 * 60
    elif result == 'HOURS':
        return 1 * 60 * 60
    elif result == 'DAYS':
        return 1 * 60 * 60 * 24


def timer():
    """Actual timer of shedule updating. Uses:
    timer_status()
    get_delay()
    """

    print(timer_status())
    print(timer_enable())
    print(timer_disable())

    print(update_delay(1))
    print(get_delay())
    print(change_delay_type('SECONDS'))
    print(get_delay_type())


if __name__ == '__main__':
    timer()