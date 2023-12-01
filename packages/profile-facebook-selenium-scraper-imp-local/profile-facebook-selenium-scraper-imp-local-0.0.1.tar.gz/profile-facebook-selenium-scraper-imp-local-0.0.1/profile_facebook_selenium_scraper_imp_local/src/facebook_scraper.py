"""
FacebookScraper Class:

This class defines a Facebook scraper to gather information about friends on Facebook.
It uses Selenium for web scraping and provides methods for logging in, 
extracting data about friends.
"""
import time
from typing import Optional
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class FacebookScraper:
    """
    Class for scraping Facebook friends' information.
    """

    def __init__(self) -> None:
        """
        Initializes the FacebookScraper class.
        """
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 10)

    def login(self, email: str, password: str) -> None:
        """
        Login to the account by given username and password
        """
        self.driver.get('https://www.facebook.com/')
        time.sleep(5)

        email_input = self.driver.find_element(By.ID, 'email')
        password_input = self.driver.find_element(By.ID, 'pass')

        email_input.send_keys(email)
        password_input.send_keys(password)
        password_input.submit()

        self.wait.until(EC.url_contains('facebook.com'))
        time.sleep(5)

    def extract_and_cast_to_int(self, input_string: str) -> Optional[int]:
        """
        Extracts and casts the first integer from the given input string.
        """
        number = [int(s) for s in input_string.split() if s.isdigit()]
        return number[0] if number else None

    def get_num_friends(self) -> Optional[int]:
        """
        Gets the number of friends from the Facebook friends list.
        """
        self.driver.get('https://www.facebook.com/friends/list')
        time.sleep(5)
        num_friends_css_selector = 'div.xu06os2:nth-child(3) > div:nth-child(1) >\
             div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) >\
                 h2:nth-child(1) > span:nth-child(1) > span:nth-child(1)'
        num_of_friends = self.driver.find_element(By.CSS_SELECTOR, num_friends_css_selector).text
        num_of_friends = self.extract_and_cast_to_int(num_of_friends)
        return num_of_friends


    def click_friend(self, j: int) -> None:
        """
        Clicks on the friend with the specified index.
        """
        friend_css_selector = f'.x135pmgq > div:nth-child({j}) > a:nth-child(1) >\
             div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)\
                 > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)\
                     > span:nth-child(1)'
        friend = self.driver.find_element(By.CSS_SELECTOR, friend_css_selector)
        friend.click()
        time.sleep(5)

    def get_friend_name(self) -> str:
        """
        Gets the name of the current friend.
        """
        friend_name_css_selector = '.x14qwyeo > h1:nth-child(1)'
        friend_name = self.driver.find_element(By.CSS_SELECTOR, friend_name_css_selector).text
        return friend_name

    def click_about_friend(self) -> None:
        """
        Clicks on the 'About' section of the current friend's profile.
        """
        about_friend_css_selector = '.x879a55 > div:nth-child(1) > div:nth-child(1) >\
             div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) >\
                 a:nth-child(3) > div:nth-child(1) > span:nth-child(1)'
        about_friend = self.driver.find_element(By.CSS_SELECTOR, about_friend_css_selector)
        about_friend.click()
        time.sleep(5)

    def get_work_place(self) -> Optional[str]:
        """
        Gets the work place information of the current friend.
        """
        try:
            work_place_css_selector = '.xqmdsaz > div:nth-child(1) > div:nth-child(1) >\
                 div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) >\
                     div:nth-child(1) > span:nth-child(1) > a:nth-child(1) > span:nth-child(1) >\
                         span:nth-child(1)'
            work_place = self.driver.find_element(By.CSS_SELECTOR, work_place_css_selector).text
            return work_place
        except NoSuchElementException:
            return None

    def get_went_to(self) -> Optional[str]:
        """
        Gets the 'Went to' information of the current friend.
        """
        try:
            went_to_css_selector = 'div.x1hq5gj4:nth-child(3) > div:nth-child(1) >\
                 div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)'
            went_to = self.driver.find_element(By.CSS_SELECTOR, went_to_css_selector).text
            return went_to
        except NoSuchElementException:
            return None

    def get_residential_location(self) -> Optional[str]:
        """
        Gets the residential location information of the current friend.
        """
        try:
            residential_location_css_selector = 'div.x1hq5gj4:nth-child(4) > div:nth-child(1) >\
                 div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1) >\
                     a:nth-child(1) > span:nth-child(1) > span:nth-child(1)'
            residential_location = self.driver.find_element(
                By.CSS_SELECTOR, residential_location_css_selector).text
            return residential_location
        except NoSuchElementException:
            return None

    def click_about_basic_info_friend(self) -> None:
        """
        Clicks on the 'About' section and then the 'Basic Info' subsection 
        of the current friend's profile.
        """
        self.click_about_friend()

        basic_info_css_selector = 'div.x1e56ztr:nth-child(5)'
        basic_info = self.driver.find_element(By.CSS_SELECTOR, basic_info_css_selector)
        basic_info.click()
        time.sleep(5)

    def get_gender_type(self) -> Optional[str]:
        """
        Gets the gender information of the current friend.
        """
        self.click_about_basic_info_friend()
        try:
            gender_css_selector = '.xqmdsaz > div:nth-child(3) > div:nth-child(1) >\
                 div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) >\
                     div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) >\
                         div:nth-child(1) > span:nth-child(1)'
            gender = self.driver.find_element(By.CSS_SELECTOR, gender_css_selector).text
            return gender
        except NoSuchElementException:
            return None

    def convert_to_date(self, date_string: str) -> Optional[datetime]:
        """
        Converts a date string to a datetime object.        
        """
        default_date_format = "%B %d %Y"
        try:
            date_object = datetime.strptime(date_string, default_date_format)
            return date_object
        except ValueError as e:
            print(f"Error: {e}")
            return None

    def get_birth_date(self) -> Optional[datetime]:
        """
        Gets the birth date of the current friend.        
        """
        self.click_about_basic_info_friend()
        try:
            birth_date_css_selector = 'div.xat24cr:nth-child(3) > div:nth-child(1) >\
                 div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) >\
                     div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'
            birth_date = self.driver.find_element(By.CSS_SELECTOR, birth_date_css_selector).text
            birth_year_css_selector = 'div.xat24cr:nth-child(3) > div:nth-child(1) >\
                 div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) >\
                     div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'
            birth_year = self.driver.find_element(By.CSS_SELECTOR, birth_year_css_selector).text
            birth_date = birth_date + " " + birth_year
            return self.convert_to_date(birth_date)
        except NoSuchElementException:
            return None

    def scrape_friends(self) -> None:
        """
        Scrapes information about the friends and inserts it into the database.        
        """
        num_of_friends = self.get_num_friends()

        frind_css_selector_index = 4

        for _ in range(num_of_friends):
            self.click_friend(frind_css_selector_index)
            friend_name = self.get_friend_name()

            self.click_about_friend()
            work_place = self.get_work_place()
            went_to = self.get_went_to()
            residential_location = self.get_residential_location()
            gender_type = self.get_gender_type()
            birth_date = self.get_birth_date()

            frind_css_selector_index += 1

            friend_data = {
                'friend_name': friend_name,
                'work_place': work_place,
                'went_to': went_to,
                'residential_location': residential_location,
                'gender_type': gender_type,
                'birth_date': birth_date,
            }
            print(friend_data)

        print("--------------end--------------")
        time.sleep(120)
        self.driver.quit()


if __name__ == "__main__":
    fb_scraper = FacebookScraper()

    EMAIL = "neomi.b@circ.zone"
    PASSWORD = "Neo1Bas2Circ3!"

    fb_scraper.login(EMAIL, PASSWORD)
    fb_scraper.scrape_friends()
