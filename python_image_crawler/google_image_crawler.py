from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
import io
import requests
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import *

QUERY_STRING = 'ChiPu'
NUMBER_OF_IMAGE_TO_SAVE = 500

# Create browser object
browser = webdriver.Chrome(service=Service('./chromedriver.exe'))
browser.maximize_window()
browser.get('https://images.google.com')
sleep(1)


# Finding the search box
box = browser.find_element(by=By.XPATH, value='//*[@id="sbtc"]/div/div[2]/input')

# Type the search query in the search box
box.send_keys(QUERY_STRING)
sleep(2)

# Pressing enter
box.send_keys(Keys.ENTER)
sleep(1)

# we need to hide the windows
browser.set_window_position(-10000, 0)


# Auto scrolling to the bottom of the page
scroll_to_bottom(browser)

"""After we reached the bottom of the page,
    we need to loop through all of image and save them"""
browser.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.CONTROL + Keys.HOME)

urls = get_image_urls(browser, number_of_image=NUMBER_OF_IMAGE_TO_SAVE)
print(urls)
os.makedirs(os.path.join(os.getcwd(), QUERY_STRING), exist_ok=True)
for i, url in enumerate(urls):
    download_images('./' + QUERY_STRING + '/', url, QUERY_STRING + str(i + 1) + '.jpg')
sleep(2)

# Close browser
# browser.close()
browser.quit()
