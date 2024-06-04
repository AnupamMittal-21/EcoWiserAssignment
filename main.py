import os
from dotenv import load_dotenv
from linkedInScraper import LinkedInScraper

if __name__ == "__main__":
    load_dotenv("data.env")
    driver_path_name = os.environ.get("DRIVER_PATH")

    with LinkedInScraper() as bot:
        bot.getUrl("https://in.linkedin.com/")
        bot.login()
        # bot.searchGLobally()
        links = bot.getPersonList()
        for link in links:
            bot.getPersonInfo(link)
