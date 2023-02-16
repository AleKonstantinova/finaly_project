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
    driver.implicitly_wait(5)
    driver.get('https://b2c.passport.rt.ru')
    yield driver
    driver.quit()


def test_reset_by_phone(driver: WebDriver):
    move_to_reset_page(driver)
    tab = driver.find_element(By.ID, 't-btn-tab-phone')
    tab.click()

    fill(driver, '+79110000000')


def test_reset_by_email(driver: WebDriver):
    move_to_reset_page(driver)
    tab = driver.find_element(By.ID, 't-btn-tab-mail')
    tab.click()

    fill(driver, 'example@test.com')


def test_reset_by_login(driver: WebDriver):
    move_to_reset_page(driver)
    tab = driver.find_element(By.ID, 't-btn-tab-login')
    tab.click()

    fill(driver, 'test-login')


def test_reset_by_ls(driver: WebDriver):
    move_to_reset_page(driver)
    tab = driver.find_element(By.ID, 't-btn-tab-ls')
    tab.click()

    fill(driver, '111111111111')


def move_to_reset_page(driver):
    driver.find_element(By.ID, 'forgot_password').click()
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'Восстановление пароля'


def fill(driver: WebDriver, username: str):
    username_input = driver.find_element(By.ID, 'username')
    username_input.send_keys(username)

    captcha = driver.find_element(By.ID, 'captcha')
    captcha.send_keys('12345')

    submit_button = driver.find_element(By.ID, 'reset')
    submit_button.click()

    error_block = driver.find_element(By.ID, 'form-error-message')
    assert error_block.text == 'Неверный логин или текст с картинки'
