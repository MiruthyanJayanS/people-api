import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from requests.sessions import merge_cookies

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
def update_contacts(service):
    
    service.people().updateContact( resourceName="people/c6520683945250739135",updatePersonFields=('Names'),body={
        
        "etag":"%EgcBAgkuNz0+GgQBAgUHIgwxcjErd2pzY014ST0=",
        "names": [
            {
                "givenName": "Jaswant k"
            }
        ]
        
        }).execute()
service=get_service()
update_contacts(service)
