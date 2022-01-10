import streamlit as st
from quickstart import *


def update_contacts(service,name):
    service= get_service()
    gc_name,gc_emailaddresses,gc_phonenumber,gc_urls = get_contacts(service,list_contacts(service)[1][0])
    with st.form(key='my_form'):
        name = st.text_input('Name',gc_name)
        phoneNumber1 =  st.text_input('phoneNumber_home',gc_phonenumber)
        phoneNumber2 =  st.text_input('phoneNumber_work')
        emailAddresses1 = st.text_input('emailAddress_home',gc_emailaddresses)
        emailAddresses2 = st.text_input('emailAddress_work')
        link = st.text_input('Url',gc_urls)
        submit_button = st.form_submit_button(label='Submit')


    if submit_button:
        service=get_service()
        merge_contacts(service,name)
	
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
        merge_contacts(service,name)
	
	

def check_option():
    option = st.selectbox(
     'Select Function',
     ('Select a Function','create a contact','update a contact'))
    if option == 'create a contact':
        create_contacts(service,name)
    elif option == 'update a contact':
        update_contacts(service,name)
    

check_option()
