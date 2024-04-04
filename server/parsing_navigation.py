import string

from selenium import webdriver

from parsing.parsing_work_ua import parsing_work_ua
from parsing.parsing_robota_ua import parsing_robota_ua
from parsing.parsing_dou import parsing_dou
from parsing.parsing_djinni import parsing_djinni

import pandas as pd


def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def forming_link(request, source, page=1):
    request = remove_punctuation(request)

    if source == 'work.ua':
        result = '+'.join(request.split())
        result = 'https://www.work.ua/jobs-' + result + '/?page=' + str(page)
        return result

    if source == 'robota.ua':
        result = '-'.join(request.split())
        result = 'https://robota.ua/zapros/' + result + '/ukraine?page=' + str(page)
        return result

    if source == 'dou':
        result = '+'.join(request.split())
        result = 'https://jobs.dou.ua/vacancies/?search=' + result
        return result

    if source == 'djinni':
        result = '+'.join(request.split())
        result = 'https://djinni.co/jobs/?all-keywords=' + result + '&keywords=' + result + '&page=' + str(page)
        return result


def get_table_by_request(request, source, driver):
    if source == 'work.ua':
        table = 1
        i = 1
        result = pd.DataFrame(columns=['Position', 'Company', 'Salary', 'Location', 'Description', 'Time', 'URL'])

        while not isinstance(table, str):
            url = forming_link(request, source, page=i)
            table = parsing_work_ua(url)

            if not isinstance(table, str):
                result = pd.concat([result, table], ignore_index=True)
            i += 1
        return result

    if source == 'robota.ua':
        i = 1
        result = pd.DataFrame(columns=['Position', 'Company', 'Salary', 'Location', 'Description', 'Time', 'URL'])
        while True:
            url = forming_link(request, source, page=i)
            table = parsing_robota_ua(url, driver)

            if table.empty:
                break

            result = pd.concat([result, table], ignore_index=True)
            i += 1

        return result

    if source == 'dou':
        url = forming_link(request, source)
        table = parsing_dou(url, driver)
        return table

    if source == 'djinni':
        table = 1
        i = 1
        result = pd.DataFrame(columns=['Position', 'Company', 'Salary', 'Location', 'Description', 'Time', 'URL'])

        while not isinstance(table, str):
            url = forming_link(request, source, page=i)
            table = parsing_djinni(url, driver)

            if not isinstance(table, str):
                result = pd.concat([result, table], ignore_index=True)
            i += 1
        return result


if __name__ == '__main__':
    driver = webdriver.Firefox()
    print(get_table_by_request('tqdmtqmd', 'djini', driver))
    driver.quit()
