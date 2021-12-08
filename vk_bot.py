# Import built-in python packages
import sqlite3
import random
import os

# Import downloaded python packages
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

con = sqlite3.connect('db/sendlist.sqlite')
CUR = con.cursor()

# Command list: (List can be increased by the time)
# variable = {'name': command_name,
#             'description': command_description}
#             if need:
#             'positive_answer': command_positive_answer,
#             'negative_answer': command_negative_answer}

add_list = {'name': '!Подписаться *класс*',
            'description': 'подписаться на ежедневную рассылку расписания уроков. Например, !Подписаться 1А',
            'positive_answer': 'Вы были успешно подписались на рассылку расписания!',
            'negative_answer': 'Вы уже были записаны на рассылку!'}

remove_list = {'name': '!Отписаться',
               'description': 'отписаться от ежедневной рассылки.',
               'positive_answer': 'Вы успешно отписались от рассылки расписания',
               'negative_answer': 'Вы не были записаны на рассылку'}

bot_help = {'name': '!Помощь',
            'description': 'вывести все команды бота.'}


def command_help() -> str:
    """Returns a text with bot commands"""

    text = f'Команды бота-рассыльщика:\n' \
           f"{add_list['name']} - {add_list['description']}\n" \
           f"{remove_list['name']} - {remove_list['description']}\n" \
           f"{bot_help['name']} - {bot_help['description']}"
    return text


def add_person(person_id: int, person_grade: str) -> bool:
    """Adds id and grade of the person to the sendlist.
     In the future, people from the sendlist will be aware of the schedule update."""

    request = f"INSERT INTO id_list (person_id, person_grade) VALUES ({person_id}, '{person_grade}')"
    result = CUR.execute(f"SELECT * FROM id_list WHERE person_id = {person_id}").fetchall()

    if result:
        return False
    else:
        CUR.execute(request).fetchall()
        con.commit()
        return True


def remove_person(person_id: int) -> bool:
    """Removes id and grade of the person from the sendlist.
    In the future, the person will not receive a notification about the schedule update."""

    request = f"DELETE FROM id_list WHERE person_id = {person_id}"
    result = CUR.execute(f"SELECT * FROM id_list WHERE person_id = {person_id}").fetchall()

    if result:
        CUR.execute(request).fetchall()
        con.commit()
        return True
    else:
        return False


def get_community_info() -> dict:
    d = {
        'community_id': None,
        'token': None
    }

    community_id_request = 'SELECT value FROM settings WHERE [key] = "community_id"'
    community_id = CUR.execute(community_id_request).fetchall()[0][0]
    d['community_id'] = community_id

    token_request = 'SELECT value FROM settings WHERE [key] = "vktoken"'
    token = CUR.execute(token_request).fetchall()[0][0]
    d['token'] = token

    return d


def main():
    """Main code of VkBot that
    Connecting to VK:
    get_community_info()

    Modifying database (soon):
    create_table()
    delete_table()

    Checks messages, that group receives and replies, depending on the command:
    add_person()
    remove_person()
    command_help()
    """

    com_info = get_community_info()

    vk_session = vk_api.VkApi(token=com_info['token'])
    longpoll = VkBotLongPoll(vk_session, com_info['community_id'])

    print('VkBot is ready to work!')  # Print line to know if bot is ready

    # Add the proccess id to kill it when the program is gonna be closed
    request = f"""UPDATE settings SET value = '{os.getpid()}' WHERE "key" = 'proccess_id';"""
    CUR.execute(request).fetchall()
    con.commit()

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            reply = ''
            console_reply = None
            text = event.obj.message['text'].split()

            if len(text) == 2 and text[0] == add_list['name']:  # add_list(dict), add_person(func)
                status = add_person(event.obj.message['from_id'], text[1])
                console_reply = 'add_person'

                if status:
                    reply = add_list['positive_answer']
                else:
                    reply = add_list['negative_answer']

            elif len(text) == 1 and text[0] == remove_list['name']:  # remove_list(dict), remove_person(func)
                status = remove_person(event.obj.message['from_id'])
                console_reply = 'remove_person'

                if status:
                    reply = remove_list['positive_answer']
                else:
                    reply = remove_list['negative_answer']

            elif len(text) == 1 and text[0] == bot_help['name']:  # bot_help(dict), command_help(func)
                reply = command_help()
                console_reply = 'command_help'

            else:  # Handle an exception where the user didn't use any commands
                reply = "Sorry, I didn't understood your request"

            print(f"{event.obj.message['from_id']}\t{console_reply}")  # Print lines to get info about bot activity

            vk = vk_session.get_api()
            vk.messages.send(user_id=event.obj.message['from_id'], message=reply,
                             # Don't really know, what I should put here, so I put there a random num
                             random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()