import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/contacts']


def get_service():
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('people', 'v1', credentials=creds)
    return service    
service=get_service()
def create_contacts(service,contact_creation_info):
    name,phoneNumber1,phoneNumber2,emailAddresses1,emailAddresses2,link=contact_creation_info
    #contact creation.
    service.people().createContact( body={
        "names": [
            {
                "givenName": name
            }
        ],
        "phoneNumbers": [
          {
           "type": "home",
           "value": phoneNumber1
          },
          {
          "type": "work",
          "value": phoneNumber2
          }
        ],
        "emailAddresses": [
        {
         "type": "home",
         "value": emailAddresses1
        },
        {
         "type": "work",
         "value": emailAddresses2
        }
        ],
        "urls": [
         {
         "type": "work",
         "value": link
         }
        ]
    }).execute()
def list_contacts(service):
    #listing contacts for updation.
    results = service.people().connections().list(
            resourceName='people/me',
            pageSize=10,
            personFields='names,emailAddresses').execute()
    connections = results.get('connections', [])
    name_list,resource_Name_list,etag_list = [],[],[]
    for person in connections:
        names = person.get('names', [])
        name_list.append(names[0].get('displayName'))
        resource_Name_list.append(person.get('resourceName',[]))
        etag_list.append(person.get('etag', []))
        
    return name_list,resource_Name_list,etag_list
# list_contacts(service)
def update_contacts(service,resource_Name,etag):
    #updating contacts.
    # name,phonenumber,emailaddresses,urls=get_contacts(service,resource_Name)
    service.people().updateContact( resourceName=resource_Name,updatePersonFields=('urls'),body={
        
        "etag":etag,
        "urls": [
         {
         "type": "work",
         "value": "google.com"
         }
        ]
        }).execute()
#update_contacts(service)
def get_contacts(service,resourceName):
    #getting contacts for updation.
    results = service.people().connections().list(
            resourceName='people/me',
            pageSize=10,
            personFields='names,emailAddresses,phoneNumbers,addresses,urls').execute()
    connections = results.get('connections', [])

    for person in connections:
        
        names = person.get('names', [])
        name = names[0].get('displayName')
        
        emailAddresses = person.get('emailAddresses', [])
        emailaddresses=[]
        for i in range (len(emailAddresses)):
            emailaddresses.append(emailAddresses[i]['value'])
        
        phoneNumbers=person.get('phoneNumbers',)
        phonenumber=[]
        for i in range (len(phoneNumbers)):
            phonenumber.append(phoneNumbers[i]['value'])
        
        
        urls=person.get('urls',[])
        
        get_info =[name,emailaddresses,phonenumber,urls]
        return get_info
        
#get_contacts(service)        


def merge_contacts(all_contacts,create_contact):
    #merging the contacts
    all_contacts_name,all_contacts_resource_Name,all_contacts_etag_list = all_contacts
    for i in range(len(all_contacts_name)):
        if all_contacts_name[i] == create_contact:
            return update_contacts(service,all_contacts_resource_Name[i],all_contacts_etag_list[i])
    if create_contact not in  all_contacts:
        return create_contacts(service)
all_contacts = list_contacts(service)
name = ''
merge_contacts(all_contacts,name)
