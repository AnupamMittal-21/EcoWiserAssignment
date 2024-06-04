import streamlit as st

st.title('LinkedIn Profile Scraper')
firstName = st.text_input('Enter First Name')
lastName = st.text_input('Enter Last Name')

st.write(f'Hello {firstName} {lastName}')