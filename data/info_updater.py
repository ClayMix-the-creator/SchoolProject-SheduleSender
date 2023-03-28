# Import built-in packages
import sqlite3

# Import project files
from data.get_class_info import get_lessons

con = sqlite3.connect('db/sendlist.sqlite')
CUR = con.cursor()


def class_exists(class_name: str) -> bool:
    request = f'SELECT classes FROM classes_table WHERE classes = "{class_name}"'
    result = CUR.execute(request).fetchone()

    if result:
        return True
    return False


def change_lessons(class_name: str, lessons: list) -> bool:
    if class_exists(class_name):
        for i in range(len(lessons)):
            request = f'UPDATE [{class_name}] SET lessons = "{lessons[i]}" WHERE id = {i + 1}'
            CUR.execute(request)
        con.commit()
        return True
    return False


def refresh_lessons() -> list:
    classes_lessons = get_lessons()

    to_send = []

    for cur_class in classes_lessons:
        class_name, lessons = cur_class[0], cur_class[1:]
        if not class_exists(class_name):
            continue
        request = f'SELECT * FROM [{class_name}]'
        db_lessons = [i[1] for i in CUR.execute(request)]

        for i in range(len(lessons)):
            if db_lessons[i] != lessons[i]:
                to_send.append(class_name)
                change_lessons(class_name, lessons)
                break

    return to_send


