import os
import time
import random
import numpy as np
import pickle
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import undetected_chromedriver as uc


class LinkedInScraper(uc.Chrome):

    def __init__(self, driver_path=None):
        self.driver_path = driver_path

        # Creating a new DataFrame for each user query
        self.df = pd.DataFrame()

        # Loading env file to get the path of the driver
        load_dotenv('data.env')

        driver_path_name = os.environ.get("DRIVER_PATH")
        os.environ['PATH'] += driver_path_name

        options = uc.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        # Setting our default browser as dummy browser so that authentication problem is solved
        options.add_argument(r'--user-data-dir=C:\Users\anupa\AppData\Local\Google\Chrome\User Data\Default')

        user_path_name = os.environ.get("USER_PATH")
        options.add_argument(user_path_name)
        super(LinkedInScraper, self).__init__(options=options)
        self.maximize_window()

    def __exit__(self, exc_type, exc_value, traceback):
        self.quit()

    def random_delay(self):
        time.sleep(random.uniform(1.0, 3.0))

    def getUrl(self, url):
        self.get(url)
        time.sleep(5)

    # We need to do manual login in order to retrieve the data.
    def login(self):
        # Getting Username and Password from env file.
        USER_NAME = os.environ.get('USER_NAME')
        PASSWORD = os.environ.get('PASSWORD')

        self.implicitly_wait(3)
        try:
            # Sending Email/Phone to the input field.
            emailInputText = self.find_element(By.CSS_SELECTOR, "input#session_key")
            emailInputText.send_keys(USER_NAME)
            self.implicitly_wait(1)

            # Sending Password to the input field.
            passwordInputText = self.find_element(By.CSS_SELECTOR, "input#session_password")
            passwordInputText.send_keys(PASSWORD)

            # Clicking on the login button.
            login_button = self.find_element(By.CSS_SELECTOR, "button[data-id='sign-in-form__submit-btn']")
            login_button.click()
            self.implicitly_wait(10)

        except Exception as e:
            self.implicitly_wait(2)
            print("Email, Password fields not found on LinkedIn Page. Trying another way to login.")

            try:
                self.get("https://www.linkedin.com/login")

                # Sending Email/Phone to the input field.
                emailInputText = self.find_element(By.CSS_SELECTOR, "input#username")
                emailInputText.send_keys(USER_NAME)

                # Sending Password to the input field.
                passwordInputText = self.find_element(By.CSS_SELECTOR, "input#password")
                passwordInputText.send_keys(PASSWORD)

                # Clicking on the login button.
                login_button = self.find_element(By.CSS_SELECTOR, "button.btn__primary--large.from__button--floating")
                login_button.click()

            except Exception as e:
                print("Error in sending the email and password.")

    def searchGlobally(self):
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
        personList = self.find_elements(By.CSS_SELECTOR, "ul.reusable-search__entity-result-list.list-style-none>li")
        for person in personList:
            print(person.text)

    def getPersonList(self, first_name, last_name):

        time.sleep(15)

        # Storing the links of individuals that appears on search page.
        links = []

        try:
            self.implicitly_wait(2)
            self.get(f"https://www.linkedin.com/search/results/people/?keywords={first_name}%20{last_name}&origin=GLOBAL_SEARCH_HEADER")
            self.implicitly_wait(5)
            personList = self.find_elements(By.CSS_SELECTOR, "li.reusable-search__result-container")
            print(len(personList))
            for person in personList:
                # Extracting link of all the profiles of the people.
                link = person.find_element(By.CSS_SELECTOR, "a.app-aware-link").get_attribute("href")
                links.append(link)

        except Exception as e:
            print("Error in getting the person list.")

        return links

    def getPersonInfo(self, link):
        self.get(link)
        self.implicitly_wait(10)

        # If option to sign up comes, then close it.
        try:
            self.find_element(By.CSS_SELECTOR, "svg.artdeco-icon.lazy-loaded").click()
        except Exception as e:
            print("No close button found.")

        # Extracting Name - Done
        try:
            name = self.find_element(By.CSS_SELECTOR, "h1").text
        except:
            name = np.NAN
            print("No Name Found")

        print(name)

        # Extracting summary - Done
        try:
            summary = self.find_element(By.CSS_SELECTOR, "h2.top-card-layout__headline.break-words.font-sans.leading-open.text-color-text").text
        except:
            try:
                summary = self.find_element(By.CSS_SELECTOR, "div.text-body-medium.break-words").text

            except:
                summary = np.NAN

        print(summary)

        # Extracting about - Done
        # Need to handle show more case
        try:
            about = self.find_element(By.CSS_SELECTOR, "div.core-section-container__content.break-words").text
        except:
            try:
                about = self.find_element(By.CSS_SELECTOR, "div.display-flex.ph5.pv3>div.inline-show-more-text--is-collapsed-with-line-clamp>span.visually-hidden").text
            except:
                about = np.NAN

        print(about)

        # Extracting skills
        try:
            skills = self.find_element(By.CSS_SELECTOR, "div.display-flex.align-items-center.t-14.t-normal").text
        except:
            skills = np.NAN

        print(skills)

        # Extracting activities
        activity_list = []
        try:
            # profile-creator-shared-feed-update__mini-container
            try:
                activities = self.find_elements(By.CSS_SELECTOR, "li.profile-creator-shared-feed-update__mini-container")
            except:
                try:
                    activities = self.find_elements(By.CSS_SELECTOR, "ul[data-test-id='activities__list']>li")
                except:
                    activities = []
                    print("No activities Found")

            for activity in activities:
                activity_dict = {}
                try:
                    activity_a = activity.find_element(By.CSS_SELECTOR, "a")
                except:
                    activity_a = None
                    print("No Activity Link found.")

                try:
                    activity_text = activity_a.text
                except:
                    print("No activity description found")
                    activity_text = np.NAN

                try:
                    activity_link = activity_a.get_attribute("href")
                except:
                    print("No Activity Link found.")
                    activity_link = np.NAN

                activity_dict['Text'] = activity_text
                activity_dict['Link'] = activity_link
                activity_list.append(activity_dict)
                print(activity_text, activity_link)
        except:
            activites = []

        # Extracting experience
        self.implicitly_wait(3)
        experiences_list = []
        try:
            experiences = self.find_elements(By.CSS_SELECTOR, "ul.experience__list>li")
            for experience in experiences:
                experience_dict = {}
                try:
                    experience_link = experience.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                except:
                    experience_link = np.NAN
                    print("No Experience Link found.")

                try:
                    experience_post = experience.find_element(By.CSS_SELECTOR, "span.experience-item__title").text
                except:
                    experience_post = np.NAN
                    print("No Experience Post found.")

                try:
                    experience_company = experience.find_element(By.CSS_SELECTOR, "span.experience-item__subtitle").text
                except:
                    experience_company = np.NAN
                    print("No Experience Company found.")

                # Iske aage ke abhi sahi nhi h.
                try:
                    experience_timeline = experience.find_elements(By.CSS_SELECTOR, "p.experience-item__meta-item")[
                        0].text
                except:
                    experience_timeline = np.NAN
                    print("No Experience Timeline found.")

                try:
                    experience_location = experience.find_elements(By.CSS_SELECTOR, "p.experience-item__meta-item")[
                        1].text
                except:
                    experience_location = np.NAN
                    print("No Experience Location found.")

                try:
                    experience_detail = experience.find_element(By.CSS_SELECTOR,
                                                                "p.show-more-less-text__text--more").text
                except:
                    experience_detail = np.NAN
                    print("No Experience Detail found.")

                experience_dict['Link'] = experience_link
                experience_dict['Post'] = experience_post
                experience_dict['Company'] = experience_company
                experience_dict['Timeline'] = experience_timeline
                experience_dict['Location'] = experience_location
                experience_dict['Detail'] = experience_detail

                print(experience_dict)
                experiences_list.append(experience_dict)
        except:
            experiences_list = []
            print("No Experience Found.")

        # Extracting education
        education_list = []
        try:
            educationList = self.find_elements(By.CSS_SELECTOR, "ul.education__list>li")
            for education in educationList:
                education_dict = {}

                try:
                    education_link = education.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                except:
                    print("No Education Link found")
                    education_link = np.NAN

                try:
                    education_institute = education.find_element(By.CSS_SELECTOR,
                                                                 "span.education-item__school-name").text
                except:
                    education_institute = np.NAN
                    print("No Education Institute found.")

                education_dict['Link'] = education_link
                education_dict['Institute'] = education_institute
                education_list.append(education_dict)
                print(education.text)
        except:
            education_list = []
            print("No Education Found")

        try:
            linkedIn_url = self.current_url
        except:
            linkedIn_url = np.NAN

        print(linkedIn_url, name, summary, about, activity_list, experiences_list, education_list)
        information_dict = {'profile_link': linkedIn_url, 'username': name, 'summary': summary, 'about': about,
                            'activity': activity_list, 'experience': experiences_list, 'education': education_list}

        print("Each Detail of a User is ", information_dict)
        information_dict = pd.DataFrame([information_dict])
        self.df = pd.concat([self.df, information_dict], ignore_index= True)


    def saveDf(self):
        temp_df_dict = self.df.to_dict()
        with open('df.pickle', 'wb') as handle:
            pickle.dump(temp_df_dict, handle)

    def loadDf(self, file_name):
        with open(file_name, 'rb') as handle:
            b = pickle.load(handle)

        print(b)