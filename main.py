import os
from dotenv import load_dotenv
from linkedInScraper import LinkedInScraper

if __name__ == "__main__":
    load_dotenv("data.env")
    driver_path_name = os.environ.get("DRIVER_PATH")

    with LinkedInScraper(driver_path_name) as bot:
        bot.getUrl("https://in.linkedin.com/")
        bot.login()
        # bot.searchGlobally()
        links = bot.getPersonList()
        for link in links:
            bot.getPersonInfo(link)
        # link = "https://www.linkedin.com/in/ankit-kumar-pm/"
        # link = "https://www.linkedin.com/in/anupam-mittal-877a271a2/"
        # bot.getPersonInfo(link)

        bot.saveDf()
        bot.loadDf("df.pickle")