# Import downloaded packages
import pandas as pd
import datetime
import sqlite3

# Import project files
from data.schedule_downloader import download

con = sqlite3.connect('db/sendlist.sqlite')
CUR = con.cursor()


def get_today() -> str:
    today = datetime.datetime.today()
    return f'{today.day}-{today.month}-{today.year}'


def next_day() -> str:
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    return f'{tomorrow.day}-{tomorrow.month}-{tomorrow.year}'


def get_url() -> str:
    request = 'SELECT value FROM timer WHERE setting = "school_url"'
    result = CUR.execute(request).fetchone()

    return result[0]


# Time to shitcode
def schedule_1to4(sheet) -> list:
    classes = []
    i = 0
    tmp = []

    while i < len(sheet):
        cur_row = sheet[i][2:]

        if 0 <= i < 6:
            if i == 0:
                tmp = [[j.split()[0].upper()] for j in cur_row]
            else:
                for j in range(len(tmp)):
                    if str(cur_row[j]) != 'nan':
                        tmp[j].append(cur_row[j])
                    else:
                        tmp[j].append('-')

        elif 7 <= i < 13:
            if i == 7:
                tmp = [[j.split()[0].upper()] for j in cur_row[:-1]]
            else:
                for j in range(len(tmp)):
                    if str(cur_row[j]) != 'nan':
                        tmp[j].append(cur_row[j])
                    else:
                        tmp[j].append('-')

        elif 15 <= i < 22:
            if i == 15:
                tmp = [[j.split()[0].upper()] for j in cur_row[:-2]]
            else:
                for j in range(len(tmp)):
                    if str(cur_row[j]) != 'nan':
                        tmp[j].append(cur_row[j])
                    else:
                        tmp[j].append('-')

        elif 26 <= i < 33:
            if i == 26:
                tmp = [[j.split()[0].upper()] for j in cur_row]
            else:
                for j in range(len(tmp)):
                    if str(cur_row[j]) != 'nan':
                        tmp[j].append(cur_row[j])
                    else:
                        tmp[j].append('-')

        elif 34 <= i < 41:
            if i == 34:
                tmp = [[j.split()[0].upper()] for j in cur_row[:-1]]
            else:
                for j in range(len(tmp)):
                    if str(cur_row[j]) != 'nan':
                        tmp[j].append(cur_row[j])
                    else:
                        tmp[j].append('-')
        else:
            if tmp:
                classes.extend(tmp)
                tmp.clear()
        i += 1

    return classes


def schedule_5to11(sheet) -> list:
    classes = []
    i = 0
    tmp = []
    while i < len(sheet):
        cur_row = sheet[i][2:]

        if 0 <= i < 8:
            if i == 0:
                tmp = [[j.split()[0].upper()] for j in cur_row]
            else:
                for j in range(len(tmp)):
                    if str(cur_row[j]) != 'nan':
                        tmp[j].append(cur_row[j])
                    else:
                        tmp[j].append('-')

        elif 9 <= i < 18:
            if i == 9:
                tmp = [[j.split()[0].upper()] for j in cur_row[:-1]]
            else:
                for j in range(len(tmp)):
                    if str(cur_row[j]) != 'nan':
                        tmp[j].append(cur_row[j])
                    else:
                        tmp[j].append('-')

        elif 19 <= i < 29:
            if i == 19:
                tmp = [[j.split()[0].upper()] for j in cur_row[:-1]]
            else:
                for j in range(len(tmp)):
                    if str(cur_row[j]) != 'nan':
                        tmp[j].append(cur_row[j])
                    else:
                        tmp[j].append('-')

        elif 30 <= i < 39:
            if i == 30:
                tmp = [[j.split()[0].upper()] for j in cur_row[:-1]]
            else:
                for j in range(len(tmp)):
                    if str(cur_row[j]) != 'nan':
                        tmp[j].append(cur_row[j])
                    else:
                        tmp[j].append('-')

        elif 40 <= i < 49:
            if i == 40:
                tmp = [[j.split()[0].upper()] for j in cur_row[:-1]]
            else:
                for j in range(len(tmp)):
                    if str(cur_row[j]) != 'nan':
                        tmp[j].append(cur_row[j])
                    else:
                        tmp[j].append('-')

        elif 53 <= i < 61:
            if i == 53:
                tmp = [[j.split()[0].upper()] for j in cur_row[:-1]]
            else:
                for j in range(len(tmp)):
                    if str(cur_row[j]) != 'nan':
                        tmp[j].append(cur_row[j])
                    else:
                        tmp[j].append('-')

        else:
            if tmp:
                classes.extend(tmp)
                tmp.clear()
        i += 1

    return classes


def get_lessons() -> list:
    today = datetime.datetime.today()

    if 17 <= today.hour < 24:
        request_datetime = next_day()

    else:  # 0 <= today.hour < 8:
        request_datetime = get_today()

    request_url = get_url()
    result = download(request_datetime, request_url)

    if result:
        classes_1to4 = result[0]
        classes_5to11 = result[1]

        excel_1to4 = pd.ExcelFile(classes_1to4)
        excel_5to11 = pd.ExcelFile(classes_5to11)

        sheet = excel_1to4.parse(excel_1to4.sheet_names[0])
        sheet = sheet.values[9:52]

        classes_1to4 = schedule_1to4(sheet)

        sheet = excel_5to11.parse(excel_5to11.sheet_names[0])
        sheet = sheet.values[9:72]

        classes_5to11 = schedule_5to11(sheet)

        all_classes = []
        all_classes.extend(classes_1to4)
        all_classes.extend(classes_5to11)

        return all_classes


get_lessons()
