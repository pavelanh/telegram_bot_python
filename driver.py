import logging

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def __get_chrome_options() -> Options:
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    return options


driver = webdriver.Chrome(options=__get_chrome_options())


def open_page(url):
    logging.info(f'opening page: {url}..')
    driver.implicitly_wait(10)
    driver.get(url)


def open_new_tab():
    logging.info('creating new tab..')
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')


def click_elem(elem_xpath):
    logging.info(f'clicking on element {elem_xpath}..')
    try:
        driver.find_element(By.XPATH, elem_xpath).click()
    except NoSuchElementException:
        logging.info("element was not found")


def get_text_from_element(elem_xpath):
    logging.info(f'getting text from element {elem_xpath}..')
    element_text = driver.find_element(By.XPATH, elem_xpath).text
    logging.info(f'element text: {element_text}')
    return element_text


def tear_down():
    logging.info('closing web driver..')
    driver.close()
