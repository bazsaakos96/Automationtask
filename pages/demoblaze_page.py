import random
import re
import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from data.test_data import random_username, random_password
from locators.demoblaze_locators import DemoblazePageLocators as L, DemoblazePageLocators
from data.test_data import static_data

class DemoblazePage:

    locators_list=[L.CONTACT_EMAIL,
                L.CONTACT_NAME,
                L.MESSAGE]


    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def is_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()

    # NAVBAR
    def is_element_displayed(self,logo=None):
        if "logo" in logo:
            return self.is_visible(L.NAVBAR_ID_LOGO)
        elif "login" in logo:
            return self.is_visible(L.WELCOME_USERNAME_FIELD)
        else:
            return    self.is_visible(L.PRODUCTS_CARDS)
    # AUTH


    def is_login(self,method):
        self.click(L.LOGIN_BUTTON)
        if "valid" in method:
            self.type(L.LOGIN_USERNAME,static_data[0])
            self.type(L.LOGIN_PASSWORD,static_data[1])
        self.type(L.LOGIN_USERNAME,random_username())
        self.type(L.LOGIN_PASSWORD,random_password())
        self.click(L.LOGIN_FORM_BUTTON)

    def is_sign_up(self, username, password):
        self.click(L.SIGN_UP_BUTTON)
        self.type(L.USERNAME_FIELD, username)
        self.type(L.PASSWORLD_FIELD, password)
        self.click(L.REGISTER_BUTTON)

    def is_products_cards_visible(self):
        return self.is_visible(L.PRODUCTS_CARDS)

    def next_page(self):
        self.click(L.NEXT_BUTTON)

    def get_side_item(self):
        self.click(L.SIDE_BAR)


    def get_price(self):
        price_text = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(L.PRICE)
        ).text
        return int(price_text.replace("$", "").split()[0])

    def open_product_and_buy(self, product_locator):
        product = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(product_locator)
        )
        product.click()
        time.sleep(1)
        price = self.get_price()

        self.click(L.BUY_BUTTON)

        WebDriverWait(self.driver, 5).until(
            EC.alert_is_present()
        ).accept()

        return price



    def buy_things(self):

        price1 = self.open_product_and_buy(L.PRODUCTS_CARDS2)
        self.driver.get("https://www.demoblaze.com")
        time.sleep(1)

        price2 = self.open_product_and_buy(L.PRODUCTS_CARDS3)
        total_price = price1 + price2
        return total_price

    def check_price(self):
        self.driver.get("https://www.demoblaze.com")
        self.click(L.CART_BUTTON)
        time.sleep(1)
        price = int(self.driver.find_element(*L.PRICE_INFO).text.replace("$", "").split()[0])
        return price

    def contact(self):
        self.click(L.CONTACT)

    def contact_values(self,data,email=None):
        if "empty" in data:
            for locator in self.locators_list:
                actual_content=self.driver.find_element(*locator).get_attribute("value")
                if len(actual_content) == 0:
                    continue
        if "partially" in data:
                username = random_username()
                locator=random.choice(self.locators_list)
                self.type(locator, username)
        if "full" in data:

            for locator in self.locators_list:
                if email and locator==self.locators_list[0]:
                    self.type(locator, email)
                elif locator!=self.locators_list[0]:
                    username = random_username()
                    self.type(locator, username)
                actual_content=self.driver.find_element(*locator).get_attribute("value")
                if len(actual_content) >0:
                    self.validate_email()

        return None

    def validate_email(self):
        email_locator = self.locators_list[0]
        email = self.driver.find_element(*email_locator).get_attribute("value")

        pattern = r"^[\w\.-]+@[\w\.-]+\.com$"

        assert email, "Email field is empty"
        assert re.match(pattern, email), f"Invalid email format (must end with .com): {email}"

    def send_message(self):
        self.click(L.SEND_MESSAGE)

    def is_about(self):
        self.click(L.ABOUT_US)
        return self.is_visible(L.VIDEO)