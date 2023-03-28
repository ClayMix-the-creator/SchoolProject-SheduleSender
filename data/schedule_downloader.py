# Import built-in packages
import requests


def download(datetime: str, school_url: str) -> list or False:
    today_url = school_url + '_' + datetime

    # Doing classes 1-4 and 5-11 cause of specific schedule placement
    classes_1to4 = '_1-4.xls'
    classes_5to11 = '_5-11.xls'

    try:
        # downloading shedule for 1-11 classes
        response_1to4 = requests.get(today_url + classes_1to4)
        response_5to11 = requests.get(today_url + classes_5to11)

        if response_1to4 and response_5to11:
            file_names = []
            # Filling excel file for 1-4 classes

            file = f'Schedule/schedule_{datetime}{classes_1to4}'
            with open(file, 'wb') as f:
                f.write(response_1to4.content)
                f.close()
            file_names.append(file)

            # Filling excel file for 5-11 classes

            file = f'Schedule/schedule_{datetime}{classes_5to11}'
            with open(file, 'wb') as f:
                f.write(response_5to11.content)
                f.close()
            file_names.append(file)

            return file_names
        return False

    except Exception as e:
        print(e)
        return False

# Example
# download('day_month_year', 'some_url')
