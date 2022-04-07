from selenium import webdriver
from time import sleep
import json

def getData(url, n_button):
    browser.get(url)
    sleep(5)

    button_showmore = browser.find_element_by_id('gsc_bpf_more')

    for i in range(n_button):
        button_showmore.click()
        sleep(5)


    paper_list = browser.find_elements_by_class_name('gsc_a_tr')

    for paper in paper_list:
        title = paper.find_element_by_class_name('gsc_a_at')
        authors = paper.find_element_by_class_name('gs_gray')
        # article_link = .get_attribute('href')

        print("__________===___________")
        print(title.text)
        print(authors.text)
        # print(article_link)

        data['root'].append({
            'title': title.text,
            'authors': authors.text
            })

    with open('NgoDucThanh.json', 'w') as f:
        json.dump(data, f, indent = 3)
    print(len(data['root']))

    browser.close()


data = {}
data['root'] = []


browser = webdriver.Chrome(executable_path='./chromedriver.exe')

url = 'https://scholar.google.com/citations?hl=vi&user=I8bNZakAAAAJ'
n_button = 1

getData(url, n_button=n_button)
