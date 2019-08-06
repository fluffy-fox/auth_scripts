#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests.exceptions import ConnectionError
import time

url = "https://site.site.ru/"

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
options.add_experimental_option("prefs", prefs)
options.add_argument('--disable-logging')
options.add_argument('--disable-gpu-sandbox')
options.add_argument('--disable-setuid-sandbox')
options.add_argument('--no-sandbox')
options.add_argument('--disable-images')
options.add_argument('--disable-application-cache')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)
driver.implicitly_wait(1)

### Параметры для входа и проверки ###

login_box = "ID"
login = "test"
password_box = "ID"
password = "pass"
login_button = "x-path"
check_box = "x-path"
check_box_content = u'Петров Пётр Петрович'
logout_button = "x-path"

### Ответы при ошибках ###

success = 0 # "We can login, check content in check_box and logout"
wrong_check_box = 1 # "We can login but compare in check_box incorrect"
check_run_fail = 2 #"Failed to run checking"
bad_response = 3 #"Response code is not 200"
bad_url = 4 #"Failed to open url."
anknown_error = 5 #Really anknown error

try:
    a = requests.get(url, timeout=10)
    a = a.status_code
    if a == 200:
        try:
            driver.get(url)
            time.sleep(5)
            login_field = driver.find_element_by_id(login_box)
            login_field.send_keys(login)
            password_field = driver.find_element_by_id(password_box)
            password_field.send_keys(password)
            button_login = driver.find_element_by_xpath(login_button)
            button_login.click()
            time.sleep(5)
            check_element = driver.find_element_by_xpath(check_box)
            compare_element = check_box_content

            if check_element.text == compare_element:
                button_logout = driver.find_element_by_xpath(check_box)
                button_logout.click()
                button_logout2 = driver.find_element_by_xpath(logout_button)
                button_logout2.click()
                driver.quit()
                print(success)
            else:
                print(wrong_check_box)
                driver.quit()
        except:
            print(check_run_fail)
            driver.quit()

    else:
        print(bad_response)
        driver.quit()
except ConnectionError:
    print(bad_url)
    driver.quit()
driver.quit()
