import string
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def generate_random_string(length):
    # Chọn ngẫu nhiên các ký tự từ chữ cái và số
    letters_and_digits = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters_and_digits) for i in range(length))
    return random_string

def enter_registration_info(driver, name, email, number, password):
    driver.find_element(By.ID, "name").send_keys(name)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.CSS_SELECTOR, "input[name='phone']").send_keys(number)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "password_confirmation").send_keys(password)



# TC1
def test_valid_register(driver):
    # main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()
    time.sleep(1)

    name = generate_random_string(8)
    email = generate_random_string(5) + '@gmail.com'
    number = ''.join(random.choice(string.digits) for i in range(10))
    password = generate_random_string(12)

    enter_registration_info(driver, name, email, number, password)

    time.sleep(2)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(2)
    assert "login" in driver.current_url

# TC2
def test_email_exist_register(driver):
    # main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()
    time.sleep(1)

    name = generate_random_string(8)
    number = ''.join(random.choice(string.digits) for _ in range(10))
    password = generate_random_string(12)
    email = "conghuy251020@gmail.com"

    enter_registration_info(driver, name, email, number, password)

    time.sleep(2)
    driver.find_element(By.TAG_NAME, "button").click()

    # Check blank input
    check_exits = None
    try:
        alert_div = driver.find_element(By.CLASS_NAME, "alert")
        check_exits = alert_div.text
        assert "Email already registered" in check_exits, "Error message is incorrect or does not exist!"
        print("Opps! Email already registered!")
    except NoSuchElementException:
        print("Error message not found!")
    time.sleep(2)

    assert check_exits is not None

# TC3
def test_register_empty_name(driver):
    # main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()

    time.sleep(1)
    email = generate_random_string(5) + '@gmail.com'
    number = ''.join(random.choice(string.digits) for i in range(10))
    password = generate_random_string(12)

    name = ""
    enter_registration_info(driver, name, email, number, password)

    time.sleep(1)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    # Check blank input
    check_blank = None
    try:
        name_field = driver.find_element(By.ID, "name")
        check_blank = name_field.get_attribute("validationMessage")
        print("Blank error is: ", check_blank)
    except StaleElementReferenceException:
        print("Blank error is displayed unsuccessfully")
    time.sleep(2)

    assert check_blank is not None

# TC4
def test_register_empty_email(driver):
    # main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()

    time.sleep(1)
    name = generate_random_string(8)
    number = ''.join(random.choice(string.digits) for i in range(10))
    password = generate_random_string(12)
    email = ""

    enter_registration_info(driver, name, email, number, password)

    time.sleep(1)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    # Check blank input
    check_blank = None
    try:
        email_input = driver.find_element(By.ID, "email")
        check_blank = email_input.get_attribute("validationMessage")
        print("Blank error is: ", check_blank)
    except StaleElementReferenceException:
        print("Blank error is displayed unsuccessfully")
    time.sleep(2)

    assert check_blank is not None

# TC5
def test_register_invalid_format_email(driver):
    # main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()

    time.sleep(1)
    name = generate_random_string(8)
    number = ''.join(random.choice(string.digits) for i in range(10))
    password = generate_random_string(12)
    email = generate_random_string(6)

    enter_registration_info(driver, name, email, number, password)

    time.sleep(1)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    # Check email format
    check_format = None
    try:
        email_input = driver.find_element(By.ID, "email")
        check_format = email_input.get_attribute("validationMessage")
        print("Format error is: ", check_format)
    except StaleElementReferenceException:
        print("Format error is displayed unsuccessfully")
    time.sleep(2)

    assert check_format is not None

# TC6
def test_register_exceed_email_input(driver):
    # main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()

    time.sleep(1)
    name = generate_random_string(8)
    number = ''.join(random.choice(string.digits) for i in range(10))
    password = generate_random_string(12)
    email = generate_random_string(1000) + "@gmail.com"

    enter_registration_info(driver, name, email, number, password)

    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    # Check exceeded character count
    check_exceed = None
    try:
        email_input = driver.find_element(By.ID, "email")
        check_exceed = email_input.get_attribute("validationMessage")
        print("Exceed error is: ", check_exceed)
    except StaleElementReferenceException:
        print("Exceed error is displayed unsuccessfully")
    time.sleep(2)

    assert check_exceed is not None

# TC7
def test_register_empty_phone(driver):
    # main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()

    time.sleep(1)
    name = generate_random_string(8)
    number = ''
    password = generate_random_string(12)
    email = generate_random_string(5) + '@gmail.com'

    enter_registration_info(driver, name, email, number, password)

    time.sleep(1)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    # Check blank input
    check_blank = None
    try:
        phone_input = driver.find_element(By.CSS_SELECTOR, "input[name='phone']")
        check_blank = phone_input.get_attribute("validationMessage")
        print("Blank error is: ", check_blank)
    except StaleElementReferenceException:
        print("Blank error is displayed unsuccessfully")
    time.sleep(2)

    assert check_blank is not None

# TC8
def test_register_empty_password(driver):
    # main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()

    time.sleep(1)
    name = generate_random_string(8)
    number = ''.join(random.choice(string.digits) for i in range(10))
    password = ""
    email =  generate_random_string(5) + '@gmail.com'

    enter_registration_info(driver, name, email, number, password)
    driver.find_element(By.ID, "password_confirmation").send_keys("123456789")

    time.sleep(1)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    # Check blank input
    check_blank = None
    try:
        password_input = driver.find_element(By.ID, "password")
        check_blank = password_input.get_attribute("validationMessage")
        print("Blank error is: ", check_blank)
    except StaleElementReferenceException:
        print("Blank error is displayed unsuccessfully")
    time.sleep(2)

    assert check_blank is not None

# TC9
def test_register_empty_password_confirmation(driver):
    # main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()

    time.sleep(1)
    name = generate_random_string(8)
    number = ''.join(random.choice(string.digits) for i in range(10))
    password = ""
    email =  generate_random_string(5) + '@gmail.com'

    enter_registration_info(driver, name, email, number, password)
    driver.find_element(By.ID, "password").send_keys("123456789")

    time.sleep(1)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    # Check blank input
    check_blank = None
    try:
        password_confirmation_input = driver.find_element(By.ID, "password_confirmation")
        check_blank = password_confirmation_input.get_attribute("validationMessage")
        print("Blank error is: ", check_blank)
    except StaleElementReferenceException:
        print("Blank error is displayed unsuccessfully")
    time.sleep(2)

    assert check_blank is not None

# TC10
def test_password_do_not_match(driver):
    # main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()
    time.sleep(1)

    name = generate_random_string(8)
    number = ''.join(random.choice(string.digits) for _ in range(10))
    password = generate_random_string(12)
    email = generate_random_string(5) + '@gmail.com'

    enter_registration_info(driver, name, email, number, password)
    driver.find_element(By.ID, "password_confirmation").send_keys("123456789")

    time.sleep(2)
    driver.find_element(By.TAG_NAME, "button").click()

    # Check blank input
    check_exits = None
    try:
        alert_div = driver.find_element(By.CLASS_NAME, "alert")
        check_exits = alert_div.text
        assert "Password do not match" in check_exits, "Error message is incorrect or does not exist!"
        print("Opps! Password do not match!")
    except NoSuchElementException:
        print("Error message not found!")
    time.sleep(2)

    assert check_exits is not None

# TC11
def test_password_too_short(driver):
    # main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()
    time.sleep(1)

    name = generate_random_string(8)
    number = ''.join(random.choice(string.digits) for _ in range(10))
    password = generate_random_string(5)
    email = generate_random_string(5) + '@gmail.com'

    enter_registration_info(driver, name, email, number, password)

    time.sleep(2)
    driver.find_element(By.TAG_NAME, "button").click()

    # Check blank input
    check_exits = None
    try:
        alert_div = driver.find_element(By.CLASS_NAME, "alert")
        check_exits = alert_div.text
        assert "Password lenght at least 8 words" in check_exits, "Error message is incorrect or does not exist!"
        print("Opps! Password lenght at least 8 words!")
    except NoSuchElementException:
        print("Error message not found!")
    time.sleep(2)

    assert check_exits is not None

# TC12
def test_invalid_phone_format(driver):
    # main
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[text()='Register']").click()
    time.sleep(1)

    name = generate_random_string(8)
    number = '-'+' '.join(random.choice(string.digits) for _ in range(10))
    password = generate_random_string(12)
    email = generate_random_string(5) + '@gmail.com'

    enter_registration_info(driver, name, email, number, password)

    time.sleep(2)
    driver.find_element(By.TAG_NAME, "button").click()

    # Check blank input
    check_exits = None
    try:
        alert_div = driver.find_element(By.CLASS_NAME, "alert")
        check_exits = alert_div.text
        assert "Invalid phone number" in check_exits, "Error message is incorrect or does not exist!"
        print("Opps! Invalid phone number!")
    except NoSuchElementException:
        print("Error message not found!")
    time.sleep(2)

    assert check_exits is not None
