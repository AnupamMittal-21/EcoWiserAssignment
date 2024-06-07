import os
from dotenv import load_dotenv
from linkedInScraper import LinkedInScraper
import time
from api import run_api
import json
import pandas as pd
import pickle


def main(firstName, lastName, api=False):
    load_dotenv("data.env")
    driver_path_name = os.environ.get("DRIVER_PATH")

    with LinkedInScraper(driver_path_name) as bot:
        # bot.getUrl("https://www.linkedin.com/login")
        # bot.login()
        links = bot.getPersonList(firstName, lastName)

        if api:
            load_dotenv("data.env")
            PROXYCURL_API_KEY = os.environ.get("PROXY_CURL_API_KEY")
            print(PROXYCURL_API_KEY)

            cnt = 0
            for link in links:
                if cnt==1:
                    break

                json_data = run_api(PROXYCURL_API_KEY, link)
                print(json_data)
                # data_dict = json.loads(json_data)
                # data_df = pd.DataFrame([data_dict])
                # df = pd.concat([df, data_df], ignore_index=True)

                # cnt+=1
            # temp_df_dict = df.to_dict()
            # with open('df_api.pickle', 'wb') as handle:
            #     pickle.dump(temp_df_dict, handle)
        else:
            for link in links:
                bot.getPersonInfo(link)
            bot.saveDf()