from unittest import skipIf

import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.demoblaze_page import DemoblazePage
from data.test_data import TestData


@pytest.fixture(scope="function")
def page():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.demoblaze.com")

    page = DemoblazePage(driver)

    yield page

    driver.quit()

def alert_box(page):
    alert = WebDriverWait(page.driver, 5).until(
        EC.alert_is_present()
    )

    alert_text = alert.text
    return alert_text

def submit_contact_form(page, mode, email=None):
    page.contact()
    page.contact_values(mode, email)
    page.send_message()
    return alert_box(page)

def test_logo_visible(page):
    assert page.is_element_displayed("logo")

@pytest.mark.parametrize("username,password", TestData.SIGNUP_DATA)
def test_signup_valid(page, username, password):
    page.is_sign_up(username, password)
    alert_text=alert_box(page)
    if username =="Akos" and password == "Jelszo123":
        assert alert_text in [
            "Sign up successful" or "This user already exist."
        ]
    assert ("Sign up successful" in alert_text)


def test_login_in(page):
    page.is_login("valid")
    assert page.is_element_displayed("login")

def test_invalid_login(page):
    page.is_login("invalid")
    alert_text=alert_box(page)
    assert "User does not exist." in alert_text

@pytest.mark.parametrize("username,password", TestData.INVALID_SIGNUP_DATA)
def test_signup_invalid(page, username, password):
    page.is_sign_up(username, password)
    alert_text=alert_box(page)
    assert "Please fill out" in alert_text




def test_is_products_cards_appear(page):
    assert page.is_products_cards_visible()

    page.next_page()

    assert page.is_products_cards_visible()


def test_buy_things(page):
    price = page.buy_things()
    check_price = page.check_price()

    assert price == check_price

def test_side_bar_buy(page):
    page.get_side_item()
    assert page.is_element_displayed()

def test_contact_full_empty(page):
    alert_text=submit_contact_form(page, "empty")
    assert "fill out" in alert_text or "missing" in alert_text

def test_contact_partially_empty(page):
    alert_text=submit_contact_form(page, "partially")
    assert "fill out" in alert_text or "missing" in alert_text

@pytest.mark.parametrize("email", [
        "test.user1@gmail.com",
        "akos.nagy99@outlook.com",
        "qa_automatio4!!!@n@company-example.com",
        "invalidemail",
        "test44",
        "akarmi!77",])
def test_contact_full(page, email):
    alert_text=submit_contact_form(page, "full", email=email)
    assert "Thanks for the message" in alert_text

def test_about(page):
    assert page.is_about()