import os
from dotenv import load_dotenv
from linkedInScraper import LinkedInScraper


def main(firstName, lastName):
    load_dotenv("data.env")
    driver_path_name = os.environ.get("DRIVER_PATH")

    with LinkedInScraper(driver_path_name) as bot:
        bot.getUrl("https://www.linkedin.com/login")
        bot.login()
        # bot.searchGlobally()
        links = bot.getPersonList(firstName, lastName)
        for link in links:
            bot.getPersonInfo(link)

        # link = "https://www.linkedin.com/in/ankit-kumar-pm/"
        # link = "https://www.linkedin.com/in/anupam-mittal-877a271a2/"
        # link = "https://www.linkedin.com/in/ravinder-chadha/"
        # link = "https://www.linkedin.com/in/shubhankar-shandilya-/"
        # bot.getPersonInfo(link)

        bot.saveDf()
        bot.loadDf("df.pickle")
