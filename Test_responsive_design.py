import time
import pytest
from selenium import webdriver
from Test_login_logout import test_valid_login
from selenium.webdriver.common.by import By



@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# TC1
def test_screen_size(driver):
    test_valid_login(driver)  # Assuming this logs in and navigates to the correct page

    # Helper function to verify visibility and presence of critical elements
    def verify_elements_visibility():
        elements_to_check = [
            "//a[text()='Home']",
            "//a[text()='About']",
            "//a[text()='Menu']",
            "//a[text()='Trace Order']",
            "//a[text()='My Order']",
            "//a[text()='Chefs']",
            "//li[@class='scroll-to-section']/a[text()='Contact Us']",
            "//a[@href='/cart']/i[@class='fa fa-shopping-cart']",
            "//button[contains(text(), 'Công Huy')]",
        ]

        all_elements_visible = True

        for xpath in elements_to_check:
            try:
                # Wait for the element to be visible
                element = driver.find_element(By.XPATH, xpath)

                if element.is_displayed():
                    print(f"Element with XPath {xpath} is visible.")
                else:
                    print(f"Element with XPath {xpath} exists but is not visible.")
                    all_elements_visible = False
            except Exception as e:
                print(f"Element with XPath {xpath} failed to load or display: {e}")
                all_elements_visible = False

        return all_elements_visible

    # Test with different screen sizes
    screen_sizes = [(800, 600), (1920, 1080), (800, 600)]

    for width, height in screen_sizes:
        print(f"\nTesting with screen size: {width}x{height}")
        driver.set_window_size(width, height)
        time.sleep(1)

        if verify_elements_visibility():
            print(f"All elements are visible at {width}x{height}.\n")
        else:
            print(f"Some elements are not visible at {width}x{height}.\n")