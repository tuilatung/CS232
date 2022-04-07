from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import json

browser = webdriver.Chrome(executable_path='./chromedriver')

browser.get('https://baomoi.com/')
sleep(5)

titles = browser.find_elements_by_xpath("//h4[@class='bm_O']/span")


DATA = []

for title in titles:
    data = { 
        "article": title.text
            }
        
    DATA.append(data)
        
    RESULTS = {
        "vnexpress": DATA
    }

    json_object = json.dumps(RESULTS, indent = 2, ensure_ascii=False) # UTF-8 fixed

    with open("results_news.json", "w") as outfile:
        outfile.write(json_object)
            
sleep(3)

browser.close()