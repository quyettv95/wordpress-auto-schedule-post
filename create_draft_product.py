import time
import string
import random
from selenium import webdriver
import chromedriver_autoinstaller
from dotenv import dotenv_values
from selenium.webdriver.common.by import By

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}


chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

WP_URL = config['WP_URL']
driver = webdriver.Chrome()
driver.get(WP_URL + "/wp-login.php")
username = driver.find_element(By.ID, "user_login")
username.send_keys('admin')
password = driver.find_element(By.ID, "user_pass")
password.send_keys('admin')

buttonLogin = driver.find_element(By.ID, "wp-submit")
buttonLogin.click()
for i in range(100):
    driver.get(WP_URL + "/wp-admin/post-new.php?post_type=product")

    letters = string.ascii_lowercase
    randtext = ''.join(random.choice(letters) for i in range(10))
    product_title = driver.find_element(By.ID, "title")
    product_title.send_keys("Sample product: " + randtext)
    product_content = driver.find_element(By.ID, "save-post")
    product_content.click()
time.sleep(5)
