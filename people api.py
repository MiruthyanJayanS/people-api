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
def create_contacts(service,name,phoneNumber,emailAddresses):
    
    # CREATING CONTACTSSSSSSSS
    service.people().createContact( body={
        "names": [
            {
                "givenName": name
            }
        ],
        "phoneNumbers": [
            {
                'value': phoneNumber
            }
        ],
        "emailAddresses": [
            {
                'value': emailAddresses 
            }
        ]
    }).execute()

service=get_service()

