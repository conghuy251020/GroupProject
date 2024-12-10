import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
# from condition_function import *

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


valid_email = "conghuy251020@gmail.com"
valid_pass = ("123456789")


# TC1
def test_valid_login(driver):
    # main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//a[@class = 'text-sm text-gray-700 underline']").click()
    time.sleep(1)
    driver.find_element(By.ID, "email").send_keys(valid_email)
    driver.find_element(By.ID, "password").send_keys(valid_pass)
    driver.find_element(By.TAG_NAME, "button").click()

    time.sleep(3)
    assert "Công Huy" == driver.find_element(By.XPATH, "//span[@class = 'inline-flex rounded-md']").text

# TC2
def test_wrong_pass(driver):
    #main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//a[@class = 'text-sm text-gray-700 underline']").click()
    time.sleep(1)
    driver.find_element(By.ID, "email").send_keys(valid_email)
    driver.find_element(By.ID, "password").send_keys("wrong")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    check_pass = driver.find_element(By.XPATH, "//div[@class = 'font-medium text-red-600']").text == "Whoops! Something went wrong."

    print("Check invalid Password: ", check_pass)
    time.sleep(3)
    assert check_pass

# TC3
def test_wrong_Email(driver):
    #main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//a[@class = 'text-sm text-gray-700 underline']").click()

    time.sleep(1)
    driver.find_element(By.ID, "email").send_keys("conghuy@gmail.com")
    driver.find_element(By.ID, "password").send_keys(valid_pass)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    check_email = driver.find_element(By.XPATH, "//div[@class = 'font-medium text-red-600']").text == "Whoops! Something went wrong."

    print("Check invalid Email: ", check_email)
    time.sleep(3)
    assert check_email

# TC4
def test_SQL_injection_password(driver):
    #main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//a[@class = 'text-sm text-gray-700 underline']").click()
    time.sleep(1)
    driver.find_element(By.ID, "email").send_keys(valid_email)
    driver.find_element(By.ID, "password").send_keys("' OR '1'='1")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    check_pass = driver.find_element(By.XPATH, "//div[@class = 'font-medium text-red-600']").text == "Whoops! Something went wrong."

    print("Check sql injection - Password: ", check_pass)
    time.sleep(3)
    assert check_pass

# TC5
def test_SQL_injection_email(driver):
    #main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//a[@class = 'text-sm text-gray-700 underline']").click()
    time.sleep(1)
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys("' OR '1'='1")
    driver.find_element(By.ID, "password").send_keys(valid_pass)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    check_email_input = None
    try:
        check_email_input = email_input.get_attribute("validationMessage")
        print("Error is: ", check_email_input)
    except StaleElementReferenceException:
        print("Invalid email error is displayed unsuccessfully")

    print("Check sql injection - Email: ", check_email_input)
    time.sleep(3)
    assert check_email_input is not None

# TC6
def test_valid_logout(driver):
    #condition
    test_valid_login(driver)

    #main
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[@class ='inline-flex rounded-md']").find_element(By.TAG_NAME, "button").click()
    driver.find_element(By.XPATH, "//*[text() = 'Log Out']").click()
    time.sleep(3)
    try:
        driver.find_element(By.XPATH, "//*[text()='Log in']")
        print("Log out successfully")
        assert True
    except NoSuchElementException:
        print("Log out unsuccessfully")
        assert False