from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
import io
import requests
import PIL
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


QUERY_STRING = 'dog'
NUMBER_OF_IMAGE_TO_SAVE = 100


def scroll_to_bottom():
    last_height = browser.execute_script('return document.body.scrollHeight')
    sleep(3)

    while True:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        sleep(3)
        new_height = browser.execute_script('return document.body.scrollHeight')
        sleep(3)

        # expect to see 'See more results" button
        try:
            btnSeeMore = browser.find_element(by=By.XPATH, value='/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[2]/div[2]/input')
            btnSeeMore.click()
            sleep(3)

        except:
            pass

        # check if we have reached the bottom of the page
        if new_height == last_height:
            break

        last_height = new_height


# Create browser object
browser = webdriver.Chrome(service=Service('./chromedriver.exe'))
browser.maximize_window()
browser.get('https://images.google.com')
sleep(1)

# Finding the search box
box = browser.find_element(by=By.XPATH, value='//*[@id="sbtc"]/div/div[2]/input')

# Type the search query in the search box
box.send_keys('dog')
sleep(2)

# Pressing enter
box.send_keys(Keys.ENTER)
sleep(1)

# Auto scrolling to the bottom of the page
scroll_to_bottom()

"""After we reached the bottom of the page, 
    we need to loop through all of image and save them"""

for i in range(NUMBER_OF_IMAGE_TO_SAVE):
    try:
        img = browser.find_element(by=By.XPATH,
                                   value='//*[@id="islrg"]/div[1]/div['+str(i+1)+']/a[1]/div[1]/img')
        img.screenshot('./images/' + QUERY_STRING + str(i+1) + '.png')
        sleep(0.5)
    except:
        pass

print('Done')
sleep(2)
# Close browser
browser.close()
