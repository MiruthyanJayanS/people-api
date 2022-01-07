import streamlit as st
from quickstart import *

with st.form(key='my_form'):
    name = st.text_input(label='Name')
    phoneNumber =  st.text_input(label='phoneNumber')
    emailAddresses = st.text_input(label='emailAddress')
    submit_button = st.form_submit_button(label='Submit')


if submit_button:
    service=get_service()
    create_contacts(service,name,phoneNumber,emailAddresses)
    st.success('Contact Has Been Created!')
