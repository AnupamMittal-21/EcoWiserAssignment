import os
from dotenv import load_dotenv
from linkedInScraper import LinkedInScraper
from api import run_api
import pandas as pd
import pickle


def main(firstName, lastName, api=False):
    load_dotenv("data.env")
    driver_path_name = os.environ.get("DRIVER_PATH")

    with LinkedInScraper(driver_path_name) as bot:
        bot.getUrl("https://www.linkedin.com/login")
        bot.login()
        links = bot.getPersonList(firstName, lastName)

        if api:
            load_dotenv("data.env")
            PROXYCURL_API_KEY = os.environ.get("PROXY_CURL_API_KEY")
            print(PROXYCURL_API_KEY)

            df2= pd.DataFrame()
            cnt = 0
            for link in links:
                cnt += 1
                if cnt==3:
                    break

                json_data = run_api(PROXYCURL_API_KEY, link)
                # json_data =  {
                #   "public_identifier": "ankitkumarshrivastava",
                #   "profile_pic_url": "https://s3.us-west-000.backblazeb2.com/proxycurl/person/ankitkumarshrivastava/profile?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=0004d7f56a0400b0000000001%2F20240607%2Fus-west-000%2Fs3%2Faws4_request&X-Amz-Date=20240607T221858Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=53069b43362e81e390ff16e3cdc1fb7edd05824eb691404899503113771093c5",
                #   "background_cover_image_url": "",
                #   "first_name": "Ankit",
                #   "last_name": "Kumar",
                #   "full_name": "Ankit Kumar",
                #   "occupation": "Technical Sales - Brand Specialist for SAARC region at IBM",
                #   "headline": "Technical sales specialising in Network Performance Management",
                #   "summary": "- PRINCE2 + PMI-ACP + ITIL V3 foundation certified\n\n- Experience in managed services, service delivery, project management, deployment and solution designing\n\n- Worked for Not-for-profit organization (www.praja.org)\n\nSpecialties: PCRF, OTA, SMSC, SMPP, HTTP, Diameter, Gx, VAS, GPRS Roaming Exchange ( GRX ) Expert, GPRS, IN Ericsson CS3.0, Solution designing, Non-profits, GPS (global positioning system), social networking, ICT, ITIL, Joomla, PHP, Python, Website management, SQL, Bash scripting, Linux, Switches and networking",
                #   "country_full_name": "India",
                #   "city": "Mumbai",
                #   "state": "Maharashtra",
                #   "experiences": [
                #     {
                #       "starts_at": {
                #         "day": 1,
                #         "month": 8,
                #         "year": 2022
                #       },
                #       "ends_at": "",
                #       "company": "IBM",
                #       "company_linkedin_profile_ur": "https://www.linkedin.com/company/ibm/",
                #       "company_facebook_profile_url": "",
                #       "title": "Technical Sales - Brand Specialist for SAARC region",
                #       "description": "",
                #       "location": "Mumbai, Maharashtra, India",
                #       "logo_url": "https://s3.us-west-000.backblazeb2.com/proxycurl/company/ibm/profile?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=0004d7f56a0400b0000000001%2F20240607%2Fus-west-000%2Fs3%2Faws4_request&X-Amz-Date=20240607T221859Z&X-Amz-Expires=1800&X-Amz-SignedHeaders=host&X-Amz-Signature=883a3fce44a505395a853b7816f0774ddfbdfc6e45c78f2321cbd49476f4195d"
                #     }
                #   ]
                # }

                data = {}
                data['LinkedIn URL'] = json_data['public_identifier']
                data['Profile Pic URL'] = json_data['profile_pic_url']
                data['Name'] = json_data['full_name']
                data['Occupation'] = json_data['occupation']
                data['About'] = json_data['headline']
                data['Summary'] = json_data['summary']
                data['Country'] = json_data['country_full_name']
                data['City'] = json_data['city']
                data['State'] = json_data['state']
                data['Experience'] = json_data['experiences']

                print(data)

                data_df = pd.DataFrame([data])
                df2 = pd.concat([df2, data_df], ignore_index=True)

            temp_df_dict = df2.to_dict()
            with open('df2.pickle', 'wb') as handle:
                pickle.dump(temp_df_dict, handle)
            df2.to_csv(f'{firstName} {lastName}2.csv', index=False)
        else:
            for link in links:
                bot.getPersonInfo(link)
            bot.saveDf()