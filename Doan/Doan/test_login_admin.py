import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_login_admin(driver):
    driver.get("http://127.0.0.1:8000")
    login_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".text-sm.text-gray-700.underline")))
    login_link.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("123456789")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/redirects"))
    assert driver.current_url == "http://127.0.0.1:8000/redirects"
