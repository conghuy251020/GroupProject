import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)  # Set implicit wait globally
    yield driver
    driver.quit()


def test_navigate_food_menu(driver):
    driver.get("http://127.0.0.1:8000")
    driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
    driver.find_element(By.ID, "password").send_keys("123456789")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    assert driver.current_url == "http://127.0.0.1:8000/redirects"
    driver.get("http://127.0.0.1:8000/admin/food-menu")
    assert driver.current_url == "http://127.0.0.1:8000/admin/food-menu"
    food_menu_list = driver.find_elements(By.CSS_SELECTOR, ".food-menu-item")
    assert len(food_menu_list) > 0


def test_edit_food_item(driver):
    driver.get("http://127.0.0.1:8000")
    driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
    driver.find_element(By.ID, "password").send_keys("123456789")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    driver.get("http://127.0.0.1:8000/admin/food-menu")
    food_card = driver.find_element(By.XPATH, "//div[@class='card-body']/h5[contains(text(), 'Chocolate Cake')]")
    assert food_card.is_displayed()
    edit_button = driver.find_element(By.XPATH, "//a[contains(@href, 'edit/1')]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_button)
    edit_button.click()
    assert driver.current_url == "http://127.0.0.1:8000/menu/edit/1"
    edit_form_title = driver.find_element(By.XPATH, "//h1[contains(text(), 'Edit Menu Item')]")
    assert edit_form_title.is_displayed()


def test_edit_price_food_item(driver):
    driver.get("http://127.0.0.1:8000")
    driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
    driver.find_element(By.ID, "password").send_keys("123456789")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    driver.get("http://127.0.0.1:8000/admin/food-menu")
    food_card = driver.find_element(By.XPATH, "//div[@class='card-body']/h5[contains(text(), 'Chocolate Cake')]")
    assert food_card.is_displayed()
    edit_button = driver.find_element(By.XPATH, "//a[contains(@href, 'edit/1')]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_button)
    edit_button.click()
    price_input = driver.find_element(By.ID, "exampleInputPassword4")
    price_input.clear()
    price_input.send_keys("218")
    update_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary')]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", update_button)
    update_button.click()
    updated_price = driver.find_element(By.XPATH, "//p[contains(text(), 'Price')]").text
    assert "218 Tk" in updated_price
