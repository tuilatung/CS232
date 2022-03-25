from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
import io
import requests
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os


def scroll_to_bottom(browser):
    last_height = browser.execute_script('return document.body.scrollHeight')
    sleep(1)
    while True:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        sleep(1)
        new_height = browser.execute_script('return document.body.scrollHeight')
        sleep(1)
        # expect to see 'See more results" button
        try:
            btnSeeMore = browser.find_element(by=By.XPATH,
                                              value='/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[2]/div[2]/input')
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


def get_image_urls(browser, number_of_image=50):
    def scroll_down(_browser):
        _browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        sleep(1)

    image_urls = set()
    while True:
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
                if len(image_urls) >= number_of_image:
                    return image_urls