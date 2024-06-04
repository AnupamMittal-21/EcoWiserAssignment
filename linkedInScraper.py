import time

import numpy as np
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import Keys

from selenium.webdriver.common.by import By
import os


class LinkedInScraper(webdriver.Chrome):

    def __init(self, driver_path):
        self.driver_path = driver_path

        load_dotenv('data.env')

        driver_path_name = os.environ.get("DRIVER_PATH")
        os.environ['PATH'] += driver_path_name
        options = webdriver.ChromeOptions()
        user_path_name = os.environ.get("USER_PATH")
        options.add_argument(user_path_name)
        self.maximize_window()
        super(LinkedInScraper, self).__init__(options=options)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # if self.teardown:
        self.quit()

    # Username: ankitnitj3@gmail.com
    # Password: ankitnitj3

    def getUrl(self, url):
        self.get(url)
        time.sleep(5)

    # We need to do manual login in order to retrieve the data.
    def login(self):
        self.implicitly_wait(3)

        try:
            # Sending Email/Phone to the input field.
            emailInputText = self.find_element(By.CSS_SELECTOR, "input#session_key")
            emailInputText.send_keys("ankitnitj3@gmail.com")

            # Sending Password to the input field.
            passwordInputText = self.find_element(By.CSS_SELECTOR, "input#session_password")
            passwordInputText.send_keys("ankitnitj3")

        except Exception as e:
            print("Error in sending the email and password.")

        try:
            # Clicking on the login button.
            login_button = self.find_element(By.CSS_SELECTOR, "button[data-id='sign-in-form__submit-btn']")
            login_button.click()

        except Exception as e:
            print("Error in clicking the login button.")

    def searchGLobally(self):
        # ankitnitj3@gmail.com
        # ankitnitj3

        try:
            # Searching for the people globally.
            searchInput = self.find_element(By.CSS_SELECTOR, "input.search-global-typeahead__input")
            searchInput.send_keys("Ankit Kumar")
            searchInput.send_keys(Keys.ENTER)
            time.sleep(3)

        except Exception as e:
            print("Error in searching globally.")

        try:
            # Clicking on See all people option.
            self.implicitly_wait(5)
            seeAllPeople = self.find_element(By.CSS_SELECTOR, "a.app-aware-link")
            seeAllPeople.click()

        except Exception as e:
            print("Error in clicking on see all people option.")

        self.implicitly_wait(5)
        personList = self.find_elements(By.CSS_SELECTOR, "ul.reusable-search__entity-result-list list-style-none>li")
        for person in personList:
            print(person.text)

    # Example of an good profile to scrap : "https://www.linkedin.com/in/ankit-kumar-035379191/"
    def getPersonList(self):
        links = []

        try:
            self.implicitly_wait(2)
            self.get("https://www.linkedin.com/search/results/people/?keywords=Ankit%20Kumar&origin=GLOBAL_SEARCH_HEADER")
            self.implicitly_wait(5)
            personList = self.find_elements(By.CSS_SELECTOR, "li.reusable-search__result-container")
            print(len(personList))
            for person in personList:
                link = person.find_element(By.CSS_SELECTOR, "a.app-aware-link").get_attribute("href")
                links.append(link)

        except Exception as e:
            print("Error in getting the person list.")

        return links


    def getPersonInfo(self, link):
        self.get(link)

        try:
            heading = self.find_element(By.CSS_SELECTOR, "div.text-body-medium.break-words").text
        except:
            heading = np.NAN

        try:
            experience_nav_list = self.find_element(By.CSS_SELECTOR, "ul.pv-text-details__right-panel").text
        except:
            experience_nav_list = np.NAN

        try:
            about = self.find_element(By.CSS_SELECTOR, "div.display-flex.ph5.pv3").text
        except:
            about = np.NAN

        try:
            activites = self.find_elements(By.CSS_SELECTOR, "li.profile-creator-shared-feed-update__mini-container")
            for activity in activites:
                print(activity.text)
        except:
            activites = []

        print(heading, experience_nav_list, about)
