import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "http://collegecatalog.uchicago.edu/"

response = requests.get(base_url + 'thecollege/programsofstudy/')
soup = BeautifulSoup(response.text, 'html.parser')

department_links = [a['href'] for a in soup.find_all('a', href=True) \
                     if "/thecollege/" in a['href']]
courses = []
for link in department_links:
    department_response = requests.get(base_url + link)
    department_soup = BeautifulSoup(department_response.text, 'html.parser')
    for course_block in department_soup.find_all('div', class_='courseblock'):
        title_text = course_block.find('p', class_='courseblocktitle').get_text(strip=True)
        course_number = title_text.split(' ')[0]
        course_title = title_text

        desc = course_block.find('p', class_='courseblockdesc').get_text(strip=True)
        terms_offered = [term.text.strip() for term in 
            course_block.find_all('li', class_='term')] \
                if course_block.find('li', class_='term') else []
        credits = course_block.find('span', class_='credits').text.strip() \
            if course_block.find('span', class_='credits') else 'Varies'
        courses.append({
            'Course Number': course_number,
            'Title': course_title,
            'Description': desc,
            'Terms Offered': terms_offered,
            'Credits': credits,
            'Department': link
        })
df = pd.DataFrame(courses)
df.to_csv('departments.csv', index=False)

total_classes = df.shape[0]
deduped_df = df.drop_duplicates(subset=['Course Number', 'Department'])  
deduped_classes_count = deduped_df.shape[0]
department_counts = deduped_df['Department'].value_counts()
most_classes_department = department_counts.idxmax()
most_classes_count = department_counts.max()
department_counts.to_csv('department_class_counts.csv')

print(f"Department w the most: {most_classes_department},{most_classes_count}")
print("Total", total_classes)
print('Deduped classes', deduped_classes_count)