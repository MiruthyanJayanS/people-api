import streamlit as st
from quickstart import *

def create_contacts(service,name):
    with st.form(key='my_form'):
        name = st.text_input(label='Name')
        phoneNumber1 =  st.text_input(label='phoneNumber_home')
        phoneNumber2 =  st.text_input(label='phoneNumber_work')
        emailAddresses1 = st.text_input(label='emailAddress_home')
        emailAddresses2 = st.text_input(label='emailAddress_work')
        link = st.text_input(label='Url')
        submit_button = st.form_submit_button(label='Submit')


    if submit_button:
        service=get_service()
        create_contacts(service,name)
	
	

