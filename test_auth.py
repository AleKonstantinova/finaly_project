import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.implicitly_wait(15)
    driver.get('https://b2c.passport.rt.ru')
    yield driver
    driver.quit()


def test_error_auth_by_phone(driver: WebDriver):
    tab = driver.find_element(By.ID, 't-btn-tab-phone')
    tab.click()

    login(driver, '+79110000000')


def test_error_auth_by_email(driver: WebDriver):
    tab = driver.find_element(By.ID, 't-btn-tab-mail')
    tab.click()

    login(driver, 'example@test.com')


def test_error_auth_by_login(driver: WebDriver):
    tab = driver.find_element(By.ID, 't-btn-tab-login')
    tab.click()

    login(driver, 'test-login')


def test_error_auth_by_ls(driver: WebDriver):
    tab = driver.find_element(By.ID, 't-btn-tab-ls')
    tab.click()

    login(driver, '111111111111', )


def login(driver: WebDriver, username: str):
    username_input = driver.find_element(By.ID, 'username')
    username_input.send_keys(username)
    username_input = driver.find_element(By.ID, 'password')
    username_input.send_keys('password')

    captcha = driver.find_element(By.ID, 'captcha')
    if captcha:
        captcha.send_keys('12345')

    submit_button = driver.find_element(By.ID, 'kc-login')
    submit_button.click()

    error_block = driver.find_element(By.ID, 'form-error-message')
    if captcha:
        assert error_block.text == 'Неверно введен текст с картинки'
    else:
        assert error_block.text == 'Неверный логин или пароль'
