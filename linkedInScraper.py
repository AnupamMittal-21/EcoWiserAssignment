import os
import time
import numpy as np
import pickle
import pandas as pd
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import undetected_chromedriver as uc


class LinkedInScraper(uc.Chrome):

    def __init__(self, driver_path=None):
        self.driver_path = driver_path

        # Creating a new DataFrame for each user query
        self.df = pd.DataFrame()
        self.firstName = "First"
        self.lastName = "Last"
        self.count = 0

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
            emailInputText = self.find_element(By.CSS_SELECTOR, "input#username")
            emailInputText.send_keys(USER_NAME)

            # Sending Password to the input field.
            passwordInputText = self.find_element(By.CSS_SELECTOR, "input#password")
            passwordInputText.send_keys(PASSWORD)

            # Clicking on the login button.
            login_button = self.find_element(By.CSS_SELECTOR, "button.btn__primary--large.from__button--floating")
            login_button.click()

        except Exception as e:
            print("Error in Login...")

    def getPersonList(self, first_name, last_name):

        # Used to check for the names of the person. and storing the file name.
        self.firstName = first_name
        self.lastName = last_name

        time.sleep(5)
        # Storing the links of individuals that appears on search page.

        links = []

        try:
            self.implicitly_wait(2)
            self.get(f"https://www.linkedin.com/search/results/people/?keywords={first_name}%20{last_name}&origin=GLOBAL_SEARCH_HEADER")

            self.implicitly_wait(5)

            personList = self.find_elements(By.CSS_SELECTOR, "li.reusable-search__result-container")
            print("Total Person with this name on the current page are : ", len(personList))

            for person in personList:
                # Extracting link of all the profiles of the people.
                link = person.find_element(By.CSS_SELECTOR, "a.app-aware-link").get_attribute("href")
                links.append(link)

        except Exception as e:
            print("Error in getting the person list.")

        return links

    def getName(self):
        try:
            name = self.find_element(By.CSS_SELECTOR, "h1").text
        except:
            name = np.NAN
            print("No Name Found")

        return name

    def getSummary(self):
        try:
            summary = self.find_element(By.CSS_SELECTOR,
                                        "h2.top-card-layout__headline.break-words.font-sans.leading-open.text-color-text").text
        except:
            try:
                summary = self.find_element(By.CSS_SELECTOR, "div.text-body-medium.break-words").text
            except:
                summary = np.NAN
                print("No summary Found.")

        return summary

    def getAbout(self):
        self.implicitly_wait(5)
        try:
            # This is to get the second sibling of the div with ID = about
            about_container = self.find_element(By.XPATH, "//div[@id='about']/following-sibling::*[2]")
            about_text = about_container.find_element(By.CSS_SELECTOR, "span.visually-hidden").text
        except:
            about_text = np.NAN
            print("No About Found.")

        return about_text

    def getActivities(self):
        self.implicitly_wait(5)
        # Extracting activities
        activity_list = []
        try:
            try:
                activities = self.find_elements(By.CSS_SELECTOR,
                                                "li.profile-creator-shared-feed-update__mini-container")
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
                print("Activities : ")
                print(activity_dict)
        except:
            print("No Activities found.")

        # Converting to string to store in DataFrame
        activity_list_str = [str(activity) for activity in activity_list]
        return activity_list_str

    def getEducation(self):
        self.implicitly_wait(5)
        education_list = []
        try:
            # Fetching second sibling of the div with id = education
            education_div = self.find_element(By.XPATH, "//div[@id='education']/following-sibling::*[2]")
            education_list_container = education_div.find_elements(By.CSS_SELECTOR, "li")
            for education in education_list_container:
                education_dict = {}

                try:
                    education_center = education.find_element(By.CSS_SELECTOR, "div.justify-space-between")

                    try:
                        education_link = education_center.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    except:
                        education_link = np.NAN

                    try:
                        education_institute = education_center.find_element(By.CSS_SELECTOR, "div.display-flex ").text
                    except:
                        education_institute = np.NAN

                    try:
                        education_detail_container = education_center.find_elements(By.CSS_SELECTOR,
                                                                                    "span.t-14.t-normal")

                        education_branch = education_detail_container[0].text
                        education_timeline = education_detail_container[1].text
                    except:
                        education_branch = np.NAN
                        education_timeline = np.NAN

                except:
                    print("No Education Container found.")
                    education_link = np.NAN
                    education_institute = np.NAN
                    education_branch = np.NAN
                    education_timeline = np.NAN

                education_dict['Link'] = education_link
                education_dict['Institute'] = education_institute
                education_dict['Domain'] = education_branch
                education_dict['Timeline'] = education_timeline
                education_list.append(education_dict)
                print("Education : ")
                print(education_dict)
        except:
            education_list = []
            print("No Education Found")

        education_list_str = [str(activity) for activity in education_list]
        return education_list_str

    def getExperience(self):
        experience_list = []
        try:
            experience_div = self.find_element(By.XPATH, "//div[@id='education']/following-sibling::*[2]")
            experience_list_container = experience_div.find_elements(By.CSS_SELECTOR, "li")
            for experience in experience_list_container:
                experience_dict = {}

                try:
                    experience_center = experience.find_element(By.CSS_SELECTOR, "div.justify-space-between")

                    try:
                        experience_link = experience_center.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    except:
                        experience_link = np.NAN

                    try:
                        experience_name = experience_center.find_element(By.CSS_SELECTOR, "div.display-flex ").text
                    except:
                        experience_name = np.NAN

                    try:
                        education_detail_container = experience_center.find_elements(By.CSS_SELECTOR,
                                                                                     "span.t-14.t-normal")

                        experience_timeline = education_detail_container[0].text
                        experience_location = education_detail_container[1].text
                    except:
                        experience_location = np.NAN
                        experience_timeline = np.NAN

                except:
                    print("N0 Experience Container found.")
                    experience_link = np.NAN
                    experience_name = np.NAN
                    experience_location = np.NAN
                    experience_timeline = np.NAN

                experience_dict['Link'] = experience_link
                experience_dict['Institute'] = experience_name
                experience_dict['Domain'] = experience_location
                experience_dict['Timeline'] = experience_timeline
                experience_list.append(experience_dict)
                print("Experience : ")
                print(experience_dict)
        except:
            print("No Experience Found")

        experience_list_str = [str(activity) for activity in experience_list]
        return experience_list_str

    def checkName(self, name):
        name = name.split(" ")
        first_name = name[0].strip(' ')
        last_name = name[1].strip(' ')
        if self.lastName == last_name and self.firstName == first_name:
            return True
        return False

    def getPersonInfo(self, link):
        self.get(link)
        self.implicitly_wait(10)

        # Extracting Name
        name = self.getName()

        if not self.checkName(name):
            return

        # Extracting summary
        summary = self.getSummary()

        # Extracting about
        about_text = self.getAbout()

        # Extracting activities
        activity_str = self.getActivities()

        # Extracting education
        education_str = self.getEducation()

        # Extracting experience
        experience_str = self.getExperience()

        # Extracting LinkedIn URL
        try:
            linkedIn_url = self.current_url
        except:
            linkedIn_url = np.NAN

        information_dict = {'profile_link': linkedIn_url, 'username': name, 'summary': summary, 'about': about_text,
                            'activity': activity_str, 'experience': experience_str, 'education': education_str}

        print("Each Detail of a User is ", information_dict)
        information_dict = pd.DataFrame([information_dict])
        self.df = pd.concat([self.df, information_dict], ignore_index=True)
        self.count += 1

    def saveDf(self):
        temp_df_dict = self.df.to_dict()
        with open('df.pickle', 'wb') as handle:
            pickle.dump(temp_df_dict, handle)
        self.df.to_csv(f'{self.firstName} {self.lastName}.csv', index=False)