import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    WebDriverWait(driver, 15).until(EC.url_to_be("http://127.0.0.1:8000/redirects"))
    driver.find_element(By.XPATH, "//span[@class='menu-title' and text()='Orders']").click()
    driver.find_element(By.CSS_SELECTOR, "i.menu-arrow").click()
    complete_orders_link = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.nav-link[href='/orders-complete']"))
    )
    assert complete_orders_link.is_displayed()
    complete_orders_link.click()
    WebDriverWait(driver, 15).until(EC.url_to_be("http://127.0.0.1:8000/orders-complete"))
def test_details_order(driver):
    driver.get("http://127.0.0.1:8000")
    driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
    driver.find_element(By.ID, "password").send_keys("123456789")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 15).until(EC.url_to_be("http://127.0.0.1:8000/redirects"))
    driver.find_element(By.XPATH, "//span[@class='menu-title' and text()='Orders']").click()
    driver.find_element(By.CSS_SELECTOR, "i.menu-arrow").click()
    driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/orders-complete']").click()
    WebDriverWait(driver, 15).until(EC.url_to_be("http://127.0.0.1:8000/orders-complete"))
    details_link = driver.find_element(By.CSS_SELECTOR, "a.badge.badge-outline-primary[href='http://127.0.0.1:8000/invoice/details/58fsclp4']")
    details_link.click()
    WebDriverWait(driver, 15).until(EC.url_to_be("http://127.0.0.1:8000/invoice/details/58fsclp4"))






