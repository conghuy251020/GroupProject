from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_navigation_to_coupon(driver):
    driver.get("http://127.0.0.1:8000")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
    time.sleep(1)
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
    driver.find_element(By.ID, "password").send_keys("123456789")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//span[@class='menu-title' and text()='Coupon']").click()
    time.sleep(3)
def test_edit_to_coupon(driver):
    driver.get("http://127.0.0.1:8000")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
    driver.find_element(By.ID, "password").send_keys("123456789")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//span[@class='menu-title' and text()='Coupon']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//a[@href='http://127.0.0.1:8000/admin/coupon/edit/1']").click()
    time.sleep(2)
    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='discount_percentage']"))
    )
    input_field.clear()
    input_field.send_keys("19")
    update_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].btn.btn-primary.me-2"))
    )
    update_button.click()

    time.sleep(3)









