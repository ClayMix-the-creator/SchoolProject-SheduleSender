# Import built-in python packages
import sqlite3
from datetime import datetime
import time
import random

# Import downloaded python packages
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# Import project files
from vk_bot import get_community_info
from data.info_updater import refresh_lessons


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


def to_seconds(hours: int=0, minutes: int=0, seconds: int=0) -> int:
    return hours * 3600 + minutes * 60 + seconds


def people_to_send(class_name: str) -> list:
    request = f'SELECT person_id FROM id_list WHERE person_grade = "{class_name}"'
    result = [i[0] for i in CUR.execute(request).fetchall()]

    return result


def update_text(class_name: str) -> str:
    text = 'Посмотри, появилось обновление школьного расписания для тебя!\n'
    request = f'SELECT ALL lessons FROM [{class_name}]'
    lessons = [i[0] for i in CUR.execute(request)]

    for i in range(len(lessons)):
        text += f'{i + 1}. {lessons[i]}\n'

    return text


def timer():
    """Actual timer of shedule updating. Uses:
    timer_status()
    get_delay()
    """

    com_info = get_community_info()

    try:
        vk_session = vk_api.VkApi(token=com_info['token'])
        longpoll = VkBotLongPoll(vk_session, com_info['community_id'])

        vk = vk_session.get_api()
    except Exception as e:
        print(e)
        return

    while True:
        now = datetime.now()
        if timer_status() and (17 <= now.hour < 24 or 0 <= now.hour < 8):
            classes_to_send = refresh_lessons()
            print(classes_to_send)

            for i in classes_to_send:
                for j in people_to_send(i):
                    vk.messages.send(user_id=j, message=update_text(i),
                                     # Don't really know, what I should put here, so I put there a random num
                                     random_id=random.randint(0, 2 ** 64))

        # Means that current time between 8:00 and 17:00
        # 17:00 is time when usually schedule uploads
        else:
            cur_time = to_seconds(hours=now.hour, minutes=now.minute, seconds=now.second)
            delta = to_seconds(hours=17) - cur_time

            time.sleep(to_seconds(delta))

        time.sleep(get_delay())


if __name__ == '__main__':
    timer()