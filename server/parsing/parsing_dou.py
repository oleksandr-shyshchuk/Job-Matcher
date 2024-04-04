from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def parsing_dou(url, driver):
    driver.get(url)

    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div[1]"))
    )

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    button = driver.find_elements(By.XPATH, '//*[@id="vacancyListId"]/div/a')
    button_available = True
    while button_available:
        try:
            button[0].click()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            button = driver.find_elements(By.XPATH, '//*[@id="vacancyListId"]/div/a')
        except:
            button_available = False


    jobs = driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/ul/li")

    result = pd.DataFrame(columns=['Position', 'Company', 'Salary', 'Location', 'Description', 'URL'])

    for job in jobs:
        name_element = job.find_element(By.XPATH, "div[2]/a")
        name = name_element.text
        link = name_element.get_attribute("href")

        company_element = job.find_element(By.XPATH, "div[2]/strong/a")
        company = company_element.text

        try:
            place_element = job.find_element(By.XPATH, "div[2]/span[2]")
            place = place_element.text

            salary_element = job.find_element(By.XPATH, "div[2]/span[1]")
            salary = salary_element.text
        except:
            place_element = job.find_element(By.XPATH, "div[2]/span[1]")
            place = place_element.text

            salary = ''

        description_element = job.find_element(By.XPATH, "div[3]")
        description = description_element.text

        row = pd.DataFrame(data=[[name, company.strip(), salary, place, description, link]],
                           columns=['Position', 'Company', 'Salary', 'Location', 'Description', 'URL'])
        result = pd.concat([result, row], ignore_index=True)

    return result


if __name__ == '__main__':
    url = 'https://jobs.dou.ua/vacancies/?search=python'
    driver = webdriver.Firefox()

    result = parsing_dou(url, driver)

    print(result)

    driver.quit()

