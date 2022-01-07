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
    # created automatically when the authorization flow completes for the first
    # time.
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
    name,phoneNumber1,phoneNumber2,emailAddresses1,emailAddresses2,homeAddresses,workAddresses,link=contact_creation_info
    # CREATING CONTACTSSSSSSSS
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
        "addresses": [
        {
         "type": "Addresses_home",
         "streetAddress": homeAddresses
        },
        {
         "type": "Addresses_work",
         "streetAddress": workAddresses
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
    results = service.people().connections().list(
            resourceName='people/me',
            pageSize=10,
            personFields='names,emailAddresses').execute()
    connections = results.get('connections', [])

    for person in connections:
        names = person.get('names', [])
        name = names[0].get('displayName')
        resource_Name = person.get('resourceName',[])
        etag = person.get('etag', [])
        
        return name,resource_Name,etag
#list_contacts(service)

def merge_contacts():
    name=list_contacts(service)
    for name in list_contacts:
        if name == create_contacts:
            update_contacts(service)
    if create_contacts not in  list_contacts:
        create_contacts(service)
#merge_contacts()        

def update_contacts(service):
    resource_Name,etag=list_contacts()
    name,phonenumber,emailaddresses,urls=get_contacts(service)
    service.people().updateContact( resourceName=resource_Name,updatePersonFields=('Names','phoneNumbers','emailAddresses','addresses','urls'),body={
        
        "etag":etag,
        "names": [
            {
                "givenName": name
            }
        ],
        "phoneNumbers": [
          {
           "type": "home",
           "value": phonenumber[0]
          },
          {
          "type": "work",
          "value": phonenumber[1]
          }
        ],
        "emailAddresses": [
        {
         "type": "home",
         "value": emailaddresses[0]
        },
        {
         "type": "work",
         "value": emailaddresses[1]
        }
        ],
        
        "urls": [
         {
         "type": "work",
         "value": urls
         }
        ]
        }).execute()
#update_contacts(service)

def get_contacts(service):
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
        
get_contacts(service)    
