import streamlit as st
import pickle

st.title('LinkedIn Profile Scraper')
firstName = st.text_input('Enter First Name')
lastName = st.text_input('Enter Last Name')

st.write(f'Hello {firstName} {lastName}')
with open("df.pickle", 'rb') as handle:
    df = pickle.load(handle)
st.dataframe(df)