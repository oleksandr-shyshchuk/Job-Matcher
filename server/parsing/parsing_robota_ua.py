from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def parsing_robota_ua(url, driver):
    result = pd.DataFrame(columns=['Position', 'Company', 'Salary', 'Location', 'Benefits', 'Labels', 'Time', 'URL'])

    driver.get(url)
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "html/body/app-root/div/alliance-jobseeker-vacancies-root-page"))
    )

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    section = driver.find_element(by=By.TAG_NAME, value='section')

    for a in section.find_elements(By.TAG_NAME, value='a'):
        text = a.text
        if 'Відгукнутись' in text:
            labels = a.find_elements(by=By.TAG_NAME, value='alliance-vac-list-status-label')
            name = a.find_element(by=By.TAG_NAME, value='h2').text
            company = a.find_element(by=By.XPATH, value='div/div[2]/div/div[2]/span[1]').text
            try:
                salary = a.find_element(by=By.XPATH, value='div/div[2]/div/div[1]/span[1]').text
            except:
                salary = ''
            try:
                location = a.find_element(by=By.XPATH, value='div/div[2]/div/div[2]/span[2]').text
            except:
                location = ''
            benefits = a.find_elements(by=By.XPATH, value='div/div[3]/div')
            time_t = text.split('\n')[-1]

            benefits_text = ''
            labels_text = ''
            for label in labels:
                if len(labels_text) > 0:
                    labels_text += ', '
                labels_text += label.text

            for benefit in benefits:
                if len(benefits_text) > 0:
                    benefits_text += ', '
                benefits_text += benefit.text

            row = pd.DataFrame(data=[[name, company, salary, location, benefits_text, labels_text, time_t, a.get_attribute('href')]],
                               columns=['Position', 'Company', 'Salary', 'Location', 'Benefits', 'Labels', 'Time', 'URL'])
            result = pd.concat([result, row], ignore_index=True)

    return result


if __name__ == '__main__':
    driver = webdriver.Firefox()

    url = 'https://robota.ua/zapros/data-scientist/ukraine'

    res = parsing_robota_ua(url, driver)
    
    print(res)


    driver.quit()
