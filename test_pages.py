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
    yield driver
    driver.quit()


def test_page_reset_password(driver: WebDriver):
    # Auth page
    driver.get('https://b2c.passport.rt.ru')
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'Авторизация'

    # Reset password page
    driver.find_element(By.ID, 'forgot_password').click()
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'Восстановление пароля'


def test_page_register(driver: WebDriver):
    driver.get('https://b2c.passport.rt.ru')
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'Авторизация'

    # Register page
    driver.find_element(By.ID, 'kc-register').click()
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'Регистрация'


def test_pages_agreement(driver: WebDriver):
    driver.get('https://b2c.passport.rt.ru')
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'Авторизация'

    # License agreement
    driver.find_element(By.CSS_SELECTOR, '.auth-policy a').click()

    p = driver.current_window_handle
    for w in driver.window_handles:
        if w != p:
            driver.switch_to.window(w)
            break

    assert driver.find_element(By.TAG_NAME, 'h1').text \
           == 'Публичная оферта о заключении Пользовательского соглашения на использование Сервиса «Ростелеком ID»'
