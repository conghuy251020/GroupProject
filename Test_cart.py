import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from Test_login_logout import test_valid_login
import time, random, re
from selenium.common.exceptions import NoSuchElementException, TimeoutException


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def delete_all_product_in_cart(driver):
    driver.find_element(By.XPATH, "//a[@href = '/cart']").click()
    out_of_product = False
    while not out_of_product:
        try:
            time.sleep(1)
            driver.find_element(By.XPATH, '//button[@class = "btn btn-danger btn-sm remove-from-cart"]').click()
            time.sleep(1)
            alert = driver.switch_to.alert
            alert.accept()
        except NoSuchElementException:
            out_of_product = True


def add_random_product(driver):
    driver.find_element(By.XPATH, "//a[text()='Home']").click()
    driver.find_element(By.XPATH, ".//input[@value='Browse All']").click()
    random_product = random.randint(3, 8)
    product_list = {}
    for i in range(random_product):
        tr_elements = driver.find_elements(By.XPATH, "//tbody/tr")
        pick = False
        while not pick:
            tr_element = random.choice(tr_elements)
            p_name = tr_element.find_element(By.TAG_NAME, "h2").text
            try:
                if bool(next((product_name for product_name in product_list.keys() if product_name == p_name), "")):
                    continue
            except AttributeError:
                a = 0
            try:
                add_button = tr_element.find_element(By.XPATH, ".//button[text() = 'Add to Cart']")
                pick = True
                price = float(tr_element.find_element(By.TAG_NAME, "h4").text[1:])
                quan = random.randint(1, 10)
                input_e = tr_element.find_element(By.ID, "myNumber")
                input_e.clear()
                input_e.send_keys(quan)
                add_button.click()
                product_list[p_name] = [price, quan]
            except NoSuchElementException:
                a = 0
            time.sleep(1)
    return product_list


# TC1
def test_add_one_product(driver):
    # condition
    test_valid_login(driver)
    delete_all_product_in_cart(driver)

    # main
    driver.find_element(By.XPATH, "//a[text()='Home']").click()
    driver.find_element(By.XPATH, ".//input[@value='Browse All']").click()
    tr_elements = driver.find_elements(By.XPATH, "//tbody/tr")
    in_stock = False
    while not in_stock:
        tr_element = random.choice(tr_elements)
        p_name = tr_element.find_element(By.TAG_NAME, "h2").text
        try:
            add_button = tr_element.find_element(By.XPATH, ".//button[text() = 'Add to Cart']")
            in_stock = True
            price = float(tr_element.find_element(By.TAG_NAME, "h4").text[1:])
            quan = random.randint(1, 10)
            input_e = tr_element.find_element(By.ID, "myNumber")
            input_e.clear()
            input_e.send_keys(quan)
            add_button.click()
            print(p_name, ": ", in_stock, " ", price)
        except NoSuchElementException:
            print(p_name, ": ", in_stock)
        time.sleep(1)

    driver.find_element(By.XPATH, "//a[@href = '/cart']").click()
    cart_td_elements = driver.find_elements(By.XPATH, "//tbody/tr/td")
    check_name = p_name == cart_td_elements[0].text
    check_price = price == float(cart_td_elements[1].text[1:])
    check_quan = quan == float(cart_td_elements[2].text)
    check_sub_total = (price * quan) == float(cart_td_elements[3].text[1:])
    print(f"Check name: {p_name} - {check_name}")
    print(f"Check price: {price} - {check_price}")
    print(f"Check quantity: {quan} - {check_quan}")
    print(f"Check sub_total: {price * quan} - {check_sub_total}")

    time.sleep(5)
    assert check_name and check_price and check_quan and check_sub_total


# TC2
def test_add_negative_quantity_to_cart(driver):
    # condition
    test_valid_login(driver)
    delete_all_product_in_cart(driver)

    # main
    driver.find_element(By.XPATH, "//a[text()='Home']").click()
    driver.find_element(By.XPATH, ".//input[@value='Browse All']").click()
    time.sleep(1)
    tr_elements = driver.find_elements(By.XPATH, "//tbody/tr")
    in_stock = False
    while not in_stock:
        tr_element = random.choice(tr_elements)
        try:
            add_button = tr_element.find_element(By.XPATH, ".//button[text() = 'Add to Cart']")
            in_stock = True
            quan = -1
            input_e = tr_element.find_element(By.ID, "myNumber")
            input_e.clear()
            input_e.send_keys(quan)
            add_button.click()
            error_message = driver.find_element(By.CSS_SELECTOR, "input:invalid")
            check_negative = error_message is not None
            if check_negative:
                print("Error is displayed successfully")
        except NoSuchElementException:
            print("Error is displayed unsuccessfully")
        time.sleep(1)

    driver.find_element(By.XPATH, "//a[@href = '/cart']").click()

    time.sleep(5)
    assert check_negative


# TC3
def test_add_multiple_product(driver):
    # condition
    test_valid_login(driver)
    delete_all_product_in_cart(driver)

    # main
    driver.find_element(By.XPATH, "//a[text()='Home']").click()
    driver.find_element(By.XPATH, ".//input[@value='Browse All']").click()
    random_product = random.randint(3, 8)
    # add random
    print(f"Add {random_product} to cart")
    product_list = {}
    for i in range(random_product):
        tr_elements = driver.find_elements(By.XPATH, "//tbody/tr")
        pick = False
        while not pick:
            tr_element = random.choice(tr_elements)
            p_name = tr_element.find_element(By.TAG_NAME, "h2").text
            try:
                if bool(next((product_name for product_name in product_list.keys() if product_name == p_name), "")):
                    continue
            except AttributeError:
                a = 0
            try:
                add_button = tr_element.find_element(By.XPATH, ".//button[text() = 'Add to Cart']")
                pick = True
                price = float(tr_element.find_element(By.TAG_NAME, "h4").text[1:])
                quan = random.randint(1, 10)
                input_e = tr_element.find_element(By.ID, "myNumber")
                input_e.clear()
                input_e.send_keys(quan)
                add_button.click()
                product_list[p_name] = [price, quan]
            except NoSuchElementException:
                a = 0
            time.sleep(1)

    # Check cart
    driver.find_element(By.XPATH, "//a[@href = '/cart']").click()
    time.sleep(1)
    cart_tr_elements = driver.find_elements(By.XPATH, "//tbody/tr")
    shipping_charge_element = cart_tr_elements[-2].find_elements(By.XPATH, ".//td")[-1]
    VAT_element = cart_tr_elements[-1].find_elements(By.XPATH, ".//td")[-1]
    total = float(shipping_charge_element.text[1:]) + float(VAT_element.text[1:])

    check = True
    for tr_element in cart_tr_elements[:-2]:
        td_element = tr_element.find_elements(By.XPATH, ".//td")
        p_in_cart = next((product_name for product_name in product_list.keys() if product_name == td_element[0].text),
                         "")
        price = product_list[p_in_cart][0]
        quan = product_list[p_in_cart][1]
        sub_total = (price * quan)
        total += sub_total

        check_name = bool(p_in_cart)
        check_price = price == float(td_element[1].text[1:])
        check_quan = quan == float(td_element[2].text)
        check_sub_total = sub_total == float(td_element[3].text[1:])
        print(f'"{p_in_cart}": {check_name}')
        print(f"     price: {price} - {check_price}")
        print(f"     quantity: {quan} - {check_quan}")
        print(f"     sub_total: {price * quan} - {check_sub_total}", "\n")
        check = check and check_name and check_price and check_quan and check_sub_total
    total_text = driver.find_element(By.XPATH, "//td/h5/strong").text
    total_in_web = float(re.search(r'\d+', total_text).group())
    check_total = total == total_in_web
    print(f"Total: {total} - {check_total}")

    time.sleep(5)
    assert check and check_total


# TC4
def test_delete_product_in_cart(driver):
    # condition
    test_valid_login(driver)
    add_random_product(driver)

    # main
    driver.find_element(By.XPATH, "//a[@href = '/cart']").click()
    time.sleep(2)

    cart_tr_elements = driver.find_elements(By.XPATH, "//tbody/tr")
    quantity_before_delete = len(cart_tr_elements) - 2
    product_before_delete = []
    for tr_element in cart_tr_elements[:-2]:
        td_element = tr_element.find_elements(By.XPATH, ".//td")
        product_before_delete.append(td_element[0].text)

    out_of_product = False
    while not out_of_product:
        try:
            time.sleep(1)
            driver.find_element(By.XPATH, '//button[@class = "btn btn-danger btn-sm remove-from-cart"]').click()
            time.sleep(1)
            alert = driver.switch_to.alert
            alert.accept()
        except NoSuchElementException:
            out_of_product = True

    time.sleep(5)

    cart_tr_elements = driver.find_elements(By.XPATH, "//tbody/tr")
    quantity_after_delete = len(cart_tr_elements)

    print("Số lượng sản phẩm trong cart (trước khi xóa): ", quantity_before_delete)
    print("Số lượng sản phẩm trong cart (sau khi xóa): ", quantity_after_delete)

    assert quantity_after_delete == 0


# pytest -s Test_cart.py::test_delete_product_in_cart


# TC5
def test_use_coupon(driver):
    # condition
    test_valid_login(driver)
    delete_all_product_in_cart(driver)
    add_random_product(driver)

    # main
    driver.find_element(By.XPATH, "//a[@href = '/cart']").click()
    driver.find_element(By.ID, "exampleFormControlInput1").send_keys("ED60")
    driver.find_element(By.XPATH, "//tfoot/tr/td/button[text() = 'Apply']").click()
    time.sleep(1)

    total_text = driver.find_element(By.XPATH, "//td/h5/strong[contains(text(), 'Total')]").text
    total = float(re.search(r'\d+', total_text).group())
    discount_text = driver.find_element(By.XPATH, "//td/h5/strong[contains(text(), 'Discount')]").text
    discount = float(re.search(r'\d+', discount_text).group())
    total_discount_text = driver.find_element(By.XPATH, "//td/h3/strong").text
    total_discount = float(re.search(r'\d+', total_discount_text).group())

    cart_tr_elements = driver.find_elements(By.XPATH, "//tbody/tr")
    shipping_charge_element = cart_tr_elements[-2].find_elements(By.XPATH, ".//td")[-1]
    VAT_element = cart_tr_elements[-1].find_elements(By.XPATH, ".//td")[-1]
    total_no_fee = total - float(shipping_charge_element.text[1:]) - float(VAT_element.text[1:])

    check_discount = int(total_no_fee * 0.6) == discount
    check_total_after_discount = (total - discount) == total_discount

    print(f"Check discount: {discount} - {check_discount}")
    print(f"Check total after discount: {total_discount} - {check_total_after_discount}")
    time.sleep(5)
    assert check_discount and check_total_after_discount


# TC6
def test_out_of_stock(driver):
    # condition
    test_valid_login(driver)
    delete_all_product_in_cart(driver)

    # main
    driver.find_element(By.XPATH, "//a[text()='Home']").click()
    driver.find_element(By.XPATH, ".//input[@value='Browse All']").click()
    out_of_stock_products = []
    try:
        tr_elements = driver.find_elements(By.XPATH, "//tbody/tr")
        for tr_element in tr_elements:
            try:
                out_of_stock_element = tr_element.find_element(By.XPATH,
                                                               ".//p[@class='btn btn-danger' and text()='Out of Stock']")
                if out_of_stock_element:
                    product_name = tr_element.find_element(By.TAG_NAME, "h2").text
                    product_price = tr_element.find_element(By.TAG_NAME, "h4").text[1:]  # Giá tiền
                    out_of_stock_products.append({"name": product_name, "price": float(product_price)})
                    out_of_stock_element.click()
                    time.sleep(1)
                    print(f"Product '{product_name}' out of stock!")
            except NoSuchElementException:
                continue
    except Exception as e:
        print(f"Error: {e}")

    driver.find_element(By.XPATH, "//a[@href = '/cart']").click()
    time.sleep(1)
    cart_tr_elements = driver.find_elements(By.XPATH, "//tbody/tr")
    issue_found = False
    for tr_element in cart_tr_elements:
        td_elements = tr_element.find_elements(By.XPATH, ".//td")
        if len(td_elements) < 4:
            continue
        product_name_in_cart = td_elements[0].text
        price_in_cart = float(td_elements[1].text[1:])
        quantity_in_cart = int(td_elements[2].text)
        for product in out_of_stock_products:
            if product["name"] == product_name_in_cart:
                issue_found = True
                print(f"Error: Product '{product_name_in_cart}' out of stock but in cart!")
                print(f"\tPrice: {price_in_cart}, Quantity: {quantity_in_cart}")
    if not issue_found:
        print("No out of stock products appear in the shopping cart.")
    assert not issue_found, "An out-of-stock product has been detected in the shopping cart!"