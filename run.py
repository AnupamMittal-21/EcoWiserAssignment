import streamlit as st
import pickle
from main import main
st.title('LinkedIn Profile Scraper')
firstName = st.text_input('Enter First Name')
lastName = st.text_input('Enter Last Name')
button = st.button('Get Details via Web Scraping')
api_button = st.button('Get Details via API')

st.write(f"Searching profiles for {firstName} {lastName}...")

if button:
    main(firstName,lastName)
    with open("df.pickle", 'rb') as handle:
        df = pickle.load(handle)
    st.dataframe(df)

if api_button:
    main(firstName,lastName, api=True)
    # with open("df_api.pickle", 'rb') as handle:
    #     df2 = pickle.load(handle)
    # st.dataframe(df2)
st.write("Made with ❤️ by Anupam Mittal")