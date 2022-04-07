from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import json

browser = webdriver.Chrome(executable_path='./chromedriver')

FILE = open('account.txt','r')
LINES = FILE.readlines()

if len(LINES) > 0:
    LINES = [line.strip() for line in LINES]
    ID, PASS = LINES[0], LINES[1]


    browser.get('https://www.facebook.com/UIT.Fanpage/posts/4911723612253473')
    # browser.get('https://www.facebook.com/UIT.Fanpage/posts/4924584454300722')
    sleep(3)

    txtUser = browser.find_element_by_id('email')
    txtUser.send_keys(ID)

    txtPass = browser.find_element_by_id('pass')
    txtPass.send_keys(PASS)
    txtPass.send_keys(Keys.ENTER)

    sleep(15)

    cmt_mode = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div/div/div')
    cmt_mode.click()

    sleep(3)


    full_mode = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div[3]')
    full_mode.click()

    sleep(3)
    more_comment = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[4]/div/div/div[2]/div[4]/div/div[2]/span/span')
    more_comment.click()

    sleep(5)
    reply_comment = browser.find_elements_by_xpath("//div[@class='j83agx80 buofh1pr jklb3kyz l9j0dhe7']")
    for reply in reply_comment:
        reply.click()

    sleep(5)
    user_list = browser.find_elements_by_xpath("//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn mdeji52x e9vueds3 j5wam9gi lrazzd5p oo9gr5id']")
    comment_list = browser.find_elements_by_xpath("//div[@class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql']/div")
    Checked = len(user_list) == len(comment_list)

    DATA = []

    if Checked:
        for i in range(len(comment_list)):
            print(f'Poster: {user_list[i].text}')
            print(f'Comment: {comment_list[i].text}')
            print('-'*15)
            data = {
                "id_name": user_list[i].text,
                "comment": comment_list[i].text
            }
            DATA.append(data)
        
        RESULTS = {
            "Facebook": DATA
        }

        json_object = json.dumps(RESULTS, indent = 2, ensure_ascii=False) # UTF-8 fixed

        with open("results2.json", "w") as outfile:
            outfile.write(json_object)
            
            # print(f'Poster: {user_list[i].text}')
            # print(f'Comment: {comment_list[i].text}')
            # print('-'*15)

    # for cmt in comment_list:
    #     content = cmt.text # Get content
    #     print(content)

    # for usr in user_list:
    #     poster = usr.text # Get content
    #     print(poster)
    

    sleep(1000)

browser.close()