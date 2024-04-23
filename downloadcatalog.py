import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_html(url):
    response = requests.get(url)
    time.sleep(3)
    return response.text
def parse_course_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    courses_offered= []
    for course in soup.find_all('div', class_='course-info'):
        title = course.find('h3', class_='title').text.strip()
        number = course.find('span', class_ ='course-number').text.strip()
        desc = course.find('p', class_ ='description').text.strip()
        prerequesites = course.find('p', class_ = 'prerequisites')
        if prerequesites:
            prerequesites = prerequesites.text.strip()
        else:
            prerequesites = ''
        courses_offered.append({
            'title': title,
            'number': number,
            'desc': desc,
            'prerequesites': prerequesites,
        })
    return courses_offered

def main():
    base_url = 'http://collegecatalog.uchicago.edu/'
    department_url = base_url + 'thecollege/datascience/'
    start_page = get_html(department_url)
    course_data = parse_course_data(start_page)
    df = pd.DataFrame(course_data)
    df.to_csv('departments.csv', index =False)
if __name__ == '__main__':
    main()