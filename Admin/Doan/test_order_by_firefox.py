from selenium import webdriver
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()
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

def test_navigation_order(driver):
    driver.get("http://127.0.0.1:8000")
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "preloader")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".text-sm.text-gray-700.underline"))).click()
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
    driver.find_element(By.ID, "password").send_keys("123456789")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Orders']"))).click()
    driver.find_element(By.CSS_SELECTOR, "i.menu-arrow").click()
    driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/orders-complete']").click()
