from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parsing_djinni(url, driver):
    driver.get(url)

    if (driver.current_url != url) and (driver.current_url != url[:-7]):
        return 'Кінець'

    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]"))
    )

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    jobs = driver.find_elements(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/main/ul[1]/li/div")

    if len(jobs) == 0:
        return 'Нове'

    result = pd.DataFrame(
        columns=['Position', 'Company', 'Salary', 'Attributes', 'Description', 'Views', 'Reviews', 'Time', 'URL'])

    for job in jobs:
        name_element = job.find_element(By.XPATH, "header/div[2]/div/a")
        name = name_element.text
        link = name_element.get_attribute("href")

        company_element = job.find_element(By.XPATH, "header/div[1]/div/a")
        company = company_element.text

        attributes_elements = job.find_element(By.XPATH, "header/div[3]")
        attributes = attributes_elements.text

        try:
            salary_element = job.find_element(By.XPATH, 'header/div[2]/div/strong/span')
            salary = salary_element.text
        except:
            salary = ''

        description_elements = job.find_element(By.XPATH, 'div[1]/span')
        description = description_elements.text

        time_element = job.find_element(By.XPATH, 'header/div[1]/span[2]/span/span[1]')
        time = time_element.text

        seeker_element = job.find_element(By.XPATH, 'header/div[1]/span[2]/span/span[2]/span[1]')
        seeker = seeker_element.text

        reviews_element = job.find_element(By.XPATH, 'header/div[1]/span[2]/span/span[2]/span[2]')
        reviews = reviews_element.text

        row = pd.DataFrame(data=[[name, company, salary, attributes, description, seeker, reviews, time, link]],
                           columns=['Position', 'Company', 'Salary', 'Attributes', 'Description', 'Views', 'Reviews',
                                    'Time', 'URL'])
        result = pd.concat([result, row], ignore_index=True)

    return result


if __name__ == '__main__':
    url = 'https://djinni.co/jobs/?all-keywords=data+science&keywords=data+science'
    driver = webdriver.Firefox()

    result = parsing_djinni(url, driver)
    print(result)

    driver.quit()
