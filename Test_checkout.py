import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from Test_login_logout import test_valid_login
from Test_cart import add_random_product, delete_all_product_in_cart
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# TC1
def test_valid_check_out(driver):
    #condition
    test_valid_login(driver)
    delete_all_product_in_cart(driver)
    add_random_product(driver)

    #main
    driver.find_element(By.XPATH, "//a[@href = '/cart']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[text() = 'Checkout']").click()
    time.sleep(1)
    driver.find_element(By.ID, "cod").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Place Order']").click()
    time.sleep(1)
    driver.find_element(By.ID, "address").send_keys("123 abc")
    driver.find_element(By.ID, "address2").send_keys("123 abc")
    Select(driver.find_element(By.ID, "country")).select_by_value("Bangladesh")
    Select(driver.find_element(By.ID, "state")).select_by_value("Dhaka")
    driver.find_element(By.ID, "zip").send_keys("32")

    driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm order')]").click()
    time.sleep(5)
    assert "confirm_place_order" in driver.current_url

# TC2
def test_checkout_empty_address(driver):
    #condition
    test_valid_login(driver)
    delete_all_product_in_cart(driver)
    add_random_product(driver)

    #main
    driver.find_element(By.XPATH, "//a[@href = '/cart']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[text() = 'Checkout']").click()
    time.sleep(1)
    driver.find_element(By.ID, "cod").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Place Order']").click()
    time.sleep(1)
    address_input = driver.find_element(By.ID, "address")
    address_input.clear()
    driver.find_element(By.ID, "address2").send_keys("123 abc")
    Select(driver.find_element(By.ID, "country")).select_by_value("Bangladesh")
    Select(driver.find_element(By.ID, "state")).select_by_value("Dhaka")
    driver.find_element(By.ID, "zip").send_keys("32")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm order')]").click()

    #Check blank input
    check_blank = None
    try:
        check_blank = address_input.get_attribute("validationMessage")
        print("Blank error is: ", check_blank)
    except StaleElementReferenceException:
        print("Blank error is displayed unsuccessfully")
    time.sleep(2)

    assert check_blank is not None