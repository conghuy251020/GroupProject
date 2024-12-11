import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_navigation_order(driver):
    driver.get("http://127.0.0.1:8000")
    driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
    driver.find_element(By.ID, "password").send_keys("123456789")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[@class='menu-title' and text()='Orders']").click()
    driver.find_element(By.CSS_SELECTOR, "i.menu-arrow").click()
    time.sleep(3)
    complete_orders_link = driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/orders-complete']")
    assert complete_orders_link.is_displayed()
    complete_orders_link.click()
    time.sleep(5)
def test_details_order(driver):
    driver.get("http://127.0.0.1:8000")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
    time.sleep(1)
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
    driver.find_element(By.ID, "password").send_keys("123456789")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, "a.nav-link[data-toggle='collapse'][href='#ui-basic']").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/orders-complete']").click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "a.badge.badge-outline-primary[href*='/invoice/details/']").click()
    time.sleep(2)
    assert "details" in driver.current_url, "Không điều hướng tới trang chi tiết"






