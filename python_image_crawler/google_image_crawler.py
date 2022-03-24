from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
import io
import requests
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

QUERY_STRING = 'ChiPu'
NUMBER_OF_IMAGE_TO_SAVE = 50


def scroll_to_bottom():
    last_height = browser.execute_script('return document.body.scrollHeight')
    sleep(1)
    while True:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        sleep(1)
        new_height = browser.execute_script('return document.body.scrollHeight')
        sleep(1)
        # expect to see 'See more results" button
        try:
            btnSeeMore = browser.find_element(by=By.XPATH, value='/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[2]/div[2]/input')
            btnSeeMore.click()
            sleep(1)
        except:
            pass
        # check if we have reached the bottom of the page
        if new_height == last_height:
            break
        last_height = new_height


def download_images(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name
        with open(file_path, 'wb') as file:
            image.save(file, 'JPEG')
        print('Download ' + file_name + ' successfully!')
    except Exception as e:
        print('FAILED - ', e)


def scroll_down(_browser):
    _browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    sleep(1)


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

# Auto scrolling to the bottom of the page
scroll_to_bottom()

"""After we reached the bottom of the page,
    we need to loop through all of image and save them"""
browser.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.CONTROL + Keys.HOME)


def get_image_urls():
    image_urls = set()
    flag = True
    while flag:
        scroll_down(browser)
        thumbnails = browser.find_elements(by=By.CLASS_NAME, value='Q4LuWd')
        for img in thumbnails:
            try:
                img.click()
                sleep(0.2)
            except:
                continue
            images = browser.find_elements(by=By.CLASS_NAME, value='n3VNCb')
            for image in images:
                print("==>" + image.get_attribute('src') if 'http' in image.get_attribute('src') else None)
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                if len(image_urls) >= NUMBER_OF_IMAGE_TO_SAVE:
                    return image_urls


urls = get_image_urls()
print(urls)

os.makedirs(os.path.join(os.getcwd(), QUERY_STRING), exist_ok=True)
for i, url in enumerate(urls):
    download_images('./'+QUERY_STRING+'/', url, QUERY_STRING + str(i+1) + '.jpg')
sleep(2)

# Close browser
# browser.close()
browser.quit()
