import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/contacts']

def get_service():
    
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('people', 'v1', credentials=creds)
    return service 
def create_contacts(service,name,phoneNumber1,phoneNumber2,emailAddresses1,emailAddresses2,homeAddresses,workAddresses,link):
    
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

service=get_service()
def list_contacts(service):
# Call the People API
    print('List 100 connection names')
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=1000,
        personFields='names,emailAddresses').execute()
    connections = results.get('connections', [])

    for person in connections:
        names = person.get('names', [])
        name = names[0].get('displayName')
        resourceName = person.get('resourceName',[])
        etag = person.get('etag', [])
        contact_info =[]
        contact_info =(name,resourceName,etag)
        print(contact_info)
list_contacts(service)
