import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.implicitly_wait(5)
    driver.get('https://b2c.passport.rt.ru')
    yield driver
    driver.quit()


def test_empty_fields(driver: WebDriver):
    submit = move_to_register_page(driver)

    submit.click()
    assert get_input_error_block(driver, 'input[name="firstName"]').text \
           == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
    assert get_input_error_block(driver, 'input[name="lastName"]').text \
           == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
    assert get_input_error_block(driver, '#address').text \
           == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
    assert get_input_error_block(driver, '#password').text \
           == 'Длина пароля должна быть не менее 8 символов'
    assert get_input_error_block(driver, '#password-confirm').text \
           == 'Длина пароля должна быть не менее 8 символов'


def test_wrong_password(driver: WebDriver):
    submit = move_to_register_page(driver)

    fill_name_and_email(driver)
    driver.find_element(By.ID, 'password').send_keys('qwertyuioa')
    driver.find_element(By.ID, 'password-confirm').send_keys('qwertyuioa')
    submit.click()

    assert get_input_error_block(driver, '#password').text \
           == 'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру'
    assert get_input_error_block(driver, '#password-confirm').text \
           == 'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру'


def test_wrong_confirm_password(driver: WebDriver):
    submit = move_to_register_page(driver)

    fill_name_and_email(driver)
    driver.find_element(By.ID, 'password').send_keys('qwertyuIoa1')
    driver.find_element(By.ID, 'password-confirm').send_keys('aoiuytrrIwq1')
    submit.click()

    assert get_input_error_block(driver, '#password-confirm').text \
           == 'Пароли не совпадают'


def test_success(driver: WebDriver):
    submit = move_to_register_page(driver)
    fill_name_and_email(driver)
    driver.find_element(By.ID, 'password').send_keys('qwertyZ-A123456')
    driver.find_element(By.ID, 'password-confirm').send_keys('qwertyZ-A123456')

    submit.click()

    assert driver.find_element(By.TAG_NAME, 'h1').text == 'Подтверждение email'


def move_to_register_page(driver) -> WebElement:
    driver.find_element(By.ID, 'kc-register').click()
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'Регистрация'

    return driver.find_element(By.CSS_SELECTOR, 'button[name="register"]')


def get_input_error_block(driver, selector: str):
    return driver.find_element(
        By.CSS_SELECTOR,
        '.rt-input:has(> ' + selector + ') + .rt-input-container__meta--error'
    )


def fill_name_and_email(driver: WebDriver):
    driver.find_element(By.CSS_SELECTOR, 'input[name="firstName"]').send_keys('Джон')
    driver.find_element(By.CSS_SELECTOR, 'input[name="lastName"]').send_keys('Доу')
    driver.find_element(By.ID, 'address').send_keys('example@test.dev')
    pass
