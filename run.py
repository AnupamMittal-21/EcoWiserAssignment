import streamlit as st
import pickle
from main import main
st.title('LinkedIn Profile Scraper')
firstName = st.text_input('Enter First Name')
lastName = st.text_input('Enter Last Name')
button = st.button('Get Details')

st.write(f"Searching profiles for {firstName} {lastName}...")

if button:
    main(firstName,lastName)
    with open("df.pickle", 'rb') as handle:
        df = pickle.load(handle)
    st.dataframe(df)


st.write("Made with ❤️ by Anupam Mittal")