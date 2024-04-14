from bs4 import BeautifulSoup
import requests
import pandas as pd


def parsing_work_ua(url):
    """
        Function to scrape job listings from work.ua.

        Args:
            url (str): The URL of the work.ua page with the job listings.

        Returns:
            DataFrame or str: Pandas DataFrame containing the scraped job data if jobs are found,
                              otherwise returns 'Немає' indicating no jobs found.

                Columns:
                    - 'Position': Job position/title.
                    - 'Company': Name of the hiring company.
                    - 'Salary': Salary information (if available).
                    - 'Location': Job location.
                    - 'Description': Job description.
                    - 'Time': Time since job posting.
                    - 'URL': URL to the job listing.
    """

    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    if 'вакансій поки немає.' in soup.text:
        return 'Немає'

    css_selector = '#pjax-jobs-list > div'

    jobs = soup.select(css_selector)
    result = pd.DataFrame(columns=['Position', 'Company', 'Salary', 'Location', 'Description', 'Time', 'URL'])

    for job in jobs:
        job_name_element = job.select_one('div.add-bottom > h2 > a')
        if not job_name_element:
            continue
        name = job_name_element.text.strip()

        salary_element = job.select_one('div:nth-child(3) > span')
        salary = ''
        if salary_element:
            salary = salary_element.text.strip().replace(' ', ' ').replace(' ', ' ').replace(' ', ' ')

        company_name_element = job.select_one('div.add-top-xs > span:nth-child(1) > span')
        company = company_name_element.text.strip()

        place_element = job.select_one('div.add-top-xs > span:nth-child(3)')
        place = ''
        if place_element:
            place = place_element.text.strip().replace(' ', ' ')
            if place.endswith(','):
                place = place[:-1]

        description_element = job.select_one('p')
        description = description_element.text.strip().replace('\n', ' ').replace('\xa0', ' ')
        description = ' '.join(description.split()).replace('…', ' ').strip()

        time_element = job.select_one('div.flex.flex-align-center.flex-wrap > span')
        time = ''
        if time_element:
            time = time_element.text.strip()

        url = 'https://www.work.ua' + job_name_element.attrs['href']

        row = pd.DataFrame(data=[[name, company, salary, place, description, time, url]],
                           columns=['Position', 'Company', 'Salary', 'Location', 'Description', 'Time', 'URL'])
        result = pd.concat([result, row], ignore_index=True)

    return result


if __name__ == '__main__':
    url = 'https://www.work.ua/jobs/?ss=1'
    # url = 'https://www.work.ua/jobs-frontend/?page=10'

    result = parsing_work_ua(url)

    print(result)
