from datetime import datetime,timedelta
from time import sleep
from selenium import webdriver
import random
import chromedriver_autoinstaller
from dotenv import dotenv_values
from selenium.webdriver.common.by import By

config = dotenv_values("env.txt")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}


entryDate = datetime.strptime(config['ENTRY_DATETIME'], "%Y-%m-%d %H:%M")
usernameENV = config['USERNAME']
passwordENV = config['PASSWORD']
listMinute = config['RANDOM_MINUTE'].split(",")
chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists

WP_URL = config['WP_URL']
driver = webdriver.Chrome()
driver.get(WP_URL + "/wp-login.php")
username = driver.find_element(By.ID, "user_login")
username.send_keys(usernameENV)
password = driver.find_element(By.ID, "user_pass")
password.send_keys(passwordENV)

buttonLogin = driver.find_element(By.ID, "wp-submit")
buttonLogin.click()
page = 1
driver.get(WP_URL + "/wp-admin/edit.php?post_status=draft&post_type=product&paged=" + str(page))
try:
    totalPage = int(driver.find_element(By.CSS_SELECTOR, ".total-pages").text)
except:
    totalPage = 1
while True:
    driver.get(WP_URL + "/wp-admin/edit.php?post_status=draft&post_type=product")
    page += 1
    productEditUrls = driver.find_elements(By.CSS_SELECTOR, '.row-actions .edit a')
    urls = []
    for productEditUrl in productEditUrls:
        url = productEditUrl.get_attribute('href')
        urls.append(url)

    for productEditUrl in urls:
        randomNumber = int(random.choice(listMinute))
        entryDate = entryDate + timedelta(minutes=randomNumber)
        year = str(entryDate.year)
        month = str(entryDate.month).zfill(2)
        day = str(entryDate.day)
        hour = str(entryDate.hour)
        minute = str(entryDate.minute)

        driver.get(productEditUrl)
        sleep(1)
        productName = driver.find_element(By.ID, "title").get_attribute('value')
        print("Processing product: " + productName)

        driver.find_element(By.CSS_SELECTOR, ".edit-timestamp").click()

        sleep(1)
        mm = driver.find_element(By.ID, "mm")
        mm.send_keys(month)

        jj = driver.find_element(By.ID, "jj")
        jj.clear()
        jj.send_keys(day)

        aa = driver.find_element(By.ID, "aa")
        aa.clear()
        aa.send_keys(year)

        hh = driver.find_element(By.ID, "hh")
        hh.clear()
        hh.send_keys(hour)

        mn = driver.find_element(By.ID, "mn")
        mn.clear()
        mn.send_keys(minute)

        save = driver.find_element(By.CSS_SELECTOR, ".save-timestamp")
        save.click()


        publish = driver.find_element(By.ID, "publish")
        publish.click()

        sleep(1)
        print("Done product: " + productName)
        print("="*20)


    if page > totalPage:
        break