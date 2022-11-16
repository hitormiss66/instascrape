import os, os.path
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


driver = webdriver.Firefox(executable_path='path')


def login(myusername, mypassword, username):
    driver.get("https://www.instagram.com")
    WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.NAME, 'username')))
    driver.find_element(By.NAME, 'username').send_keys(myusername)
    driver.find_element(By.NAME, 'password').send_keys(mypassword)
    driver.find_element(By.CSS_SELECTOR, '.L3NKy').click()
    time.sleep(5)
    try:
        driver.find_element(By.ID, 'slfErrorAlert')
        print(driver.find_element(By.ID, 'slfErrorAlert').text)
        driver.quit()
    except Exception as login_error:
        print(login_error)
        try:
            getmedia(username)
        except Exception as mainloop_error:
            print(mainloop_error)


def getmedia(username):
    stories = []
    scrapestories(username, stories)
    downloadmedia(stories, username)


def scrapestories(username, stories):
    story_page = "https://www.instagram.com/stories" + "/" + username + "/"
    driver.get(story_page)
    try:
        WebDriverWait(driver, 3).until(ec.element_to_be_clickable((By.CSS_SELECTOR, '._acan')))
        driver.find_element(By.CSS_SELECTOR, '._acan').click()
    finally:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        count_stories = soup.find_all('div', '_ac3n')
        print(len(count_stories), 'stories')
        for story in range(len(count_stories)):
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for elem in soup.find_all('source') or soup.find_all('img'):
                if elem.attrs.get('src'):
                    url = elem.attrs.get('src')
                    if url not in stories:
                        stories.append(url)
            driver.find_element(By.CLASS_NAME, '_9zm2').click()
            time.sleep(0.5)
        driver.quit()
        # stories.pop(1)
        # removes profile picture from the result


def downloadmedia(array, username):
    cwd = os.getcwd()
    newpath = cwd + '\\' + username
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    try:
        count = 1
        for link in range(len(array)):
            filename = username + '_story' + str(count)
            filepath = './' + username + '/' + filename
            print(f'downloading {filename}')
            with requests.get(array[link], stream=True) as r:
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=30720):
                        if chunk:
                            f.write(chunk)
            count += 1
    except Exception as e:
        print(e)
