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

add_person_dict = {'name': '!Подписаться *класс*',
                   'description': 'подписаться на ежедневную рассылку расписания уроков. Например, "!Подписаться 1А"',
                   'positive_answer': 'Вы были успешно подписались на рассылку расписания!',
                   'negative_answer': 'Вы уже были записаны на рассылку!'}

remove_person_dict = {'name': '!Отписаться',
                      'description': 'отписаться от ежедневной рассылки.',
                      'positive_answer': 'Вы успешно отписались от рассылки расписания',
                      'negative_answer': 'Вы не были записаны на рассылку'}

command_help_dict = {'name': '!Помощь',
                     'description': 'вывести все команды бота.'}

# Extra commands for Admins
add_class_dict = {'name': '!Добавить класс *класс*',
                  'description': 'добавить в базу данных таблицу с уроками данного класса. Например, "!Добавить класс 1А"',
                  'positive_answer': 'Таблица была успешно добавлена в базу данных',
                  'negative_answer': 'Произошла ошибка при добавлении таблицы в базу данных'}

remove_class_dict = {'name': '!Удалить класс *класс*',
                     'description': 'убрать из базы данных таблицу с уроками данного класса. Например, "!Удалить класс 1А"',
                     'positive_answer': 'Таблица была успешно удалена из базы данных',
                     'negative_answer': 'Произошла ошибка при удалении таблицы из базы данных'}


def change_vktoken(token: str) -> bool:
    request = f"UPDATE settings SET value = '{token}' WHERE [key] = 'vktoken'"

    CUR.execute(request).fetchall()
    con.commit()

    return True


def change_community_id(community_id: str) -> bool:
    request = f"UPDATE settings SET value = '{community_id}' WHERE [key] = 'community_id'"

    CUR.execute(request).fetchall()
    con.commit()

    return True


def command_help_func() -> str:
    """Returns a text with bot commands"""

    text = f'Команды бота-рассыльщика:\n' \
           f"{add_person_dict['name']} - {add_person_dict['description']}\n" \
           f"{remove_person_dict['name']} - {remove_person_dict['description']}\n" \
           f"{command_help_dict['name']} - {command_help_dict['description']}"
    return text


def admin_command_help_func() -> str:
    text = f"\nКоманды АДминистратора:\n" \
           f"{add_class_dict['name']} - {add_class_dict['description']}\n" \
           f"{remove_class_dict['name']} - {remove_class_dict['description']}"
    return text


def add_person_func(person_id: int, person_grade: str) -> bool:
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


def remove_person_func(person_id: int) -> bool:
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


def get_admins() -> set:
    request = 'SELECT user_id FROM administrators'

    admins = CUR.execute(request).fetchall()

    for i in range(len(admins)):
        admins[i] = admins[i][0]

    return set(admins)


def add_admin_func(user_id) -> bool:
    if user_id in get_admins():
        return False

    request = f'INSERT INTO administrators (user_id) VALUES ({user_id})'

    CUR.execute(request).fetchall()
    con.commit()

    return True


def remove_admin_func(user_id) -> bool:
    if user_id in get_admins():
        request = f'DELETE FROM administrators WHERE user_id = {user_id}'

        CUR.execute(request).fetchall()
        con.commit()

        return True

    return False


def add_class_func(table_name: str) -> bool:
    max_lessons_amount = 8
    try:
        request = f'SELECT * FROM [{table_name}]'
        CUR.execute(request).fetchall()

        return False
    except Exception as e:
        request = f'CREATE TABLE [{table_name}] (id INTEGER PRIMARY KEY AUTOINCREMENT, lesson STRING)'
        CUR.execute(request)
        con.commit()

        request = f'INSERT INTO [{table_name}] (lesson) VALUES (NULL)'
        for i in range(max_lessons_amount):
            CUR.execute(request).fetchall()
        con.commit()

        return True


def remove_class_func(table_name: str) -> bool:
    try:
        request = f'SELECT * FROM [{table_name}]'
        CUR.execute(request).fetchall()

        request = f'DROP TABLE [{table_name}]'
        CUR.execute(request).fetchall()

        con.commit()

        return True
    except Exception as e:
        return False


def main():
    """Main code of VkBot that
    Connecting to VK:
    get_community_info()

    Has VK administrators:
    get_admins()
    add_admin()
    remove_admin()

    Modifying database:
    add_class_func()
    remove_class_func()

    Checks messages, that group receives and replies, depending on the command:
    add_person_func()
    remove_person_func()
    command_help_func()
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
            user_id = event.obj.message['from_id']
            text = event.obj.message['text'].split()

            if len(text) == 2 and text[0] == add_person_dict['name'].split()[0]:  # add_person_dict, add_person_func
                status = add_person_func(event.obj.message['from_id'], text[1])
                console_reply = 'add_person -> '

                if status:
                    reply = add_person_dict['positive_answer']
                    console_reply += 'OK'
                else:
                    reply = add_person_dict['negative_answer']
                    console_reply += 'Error'

            elif len(text) == 1 and text[0] == remove_person_dict['name'].split()[0]:  # remove_person_dict, remove_person_func
                status = remove_person_func(event.obj.message['from_id'])
                console_reply = 'remove_person -> '

                if status:
                    reply = remove_person_dict['positive_answer']
                    console_reply += 'OK'
                else:
                    reply = remove_person_dict['negative_answer']
                    console_reply += 'Error'

            elif len(text) == 1 and text[0] == command_help_dict['name']:  # command_help_dict, command_help_func
                reply = command_help_func()
                console_reply = 'command_help'

                if user_id in get_admins():
                    reply += admin_command_help_func()
                    console_reply = 'admin.' + console_reply

            elif len(text) == 3 and [text[0], text[1]] == add_class_dict['name'].split()[0:2]:  # add_class_dict, add_class_func
                if user_id in get_admins():
                    status = add_class_func(text[2])
                    console_reply = 'admin.add_class -> '

                    if status:
                        reply = add_class_dict['positive_answer']
                        console_reply += 'OK '
                    else:
                        reply = add_class_dict['negative_answer']
                        console_reply += 'Error '
                    console_reply += f'name: {text[2]}'

                else:
                    reply = 'Вы не имеете достаточно прав, для использования данной команды'
                    console_reply = 'user.add_class -> access denied'

            elif len(text) == 3 and [text[0], text[1]] == remove_class_dict['name'].split()[0:2]:  # remove_class_dict, remove_class_func
                if user_id in get_admins():
                    status = remove_class_func(text[2])
                    console_reply = 'admin.remove_class -> '

                    if status:
                        reply = remove_class_dict['positive_answer']
                        console_reply += 'OK '
                    else:
                        reply = remove_class_dict['negative_answer']
                        console_reply += 'Error'
                    console_reply += f'name: {text[2]}'

                else:
                    reply = 'Вы не имеете достаточно прав, для использования данной команды'

            else:  # Handle an exception where the user didn't use any commands
                reply = "Простите, не понял вашу команду"

            print(f"{event.obj.message['from_id']}\t{console_reply}")  # Print lines to get info about bot activity

            vk = vk_session.get_api()
            vk.messages.send(user_id=user_id, message=reply,
                             # Don't really know, what I should put here, so I put there a random num
                             random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    # change_vktoken()
    # change_community_id()
    # add_admin_func()
    main()
