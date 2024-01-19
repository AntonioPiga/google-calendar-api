from google_auth_oauthlib.flow import InstalledAppFlow
import os.path
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta


credentials_path = './client-web-google.json'

scopes = ['https://www.googleapis.com/auth/calendar']

token_pickle_path = 'token.pickle'
creds = None

if os.path.exists(token_pickle_path):
    with open(token_pickle_path, 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path, scopes)
        creds = flow.run_local_server(port=8080)

    with open(token_pickle_path, 'wb') as token:
        pickle.dump(creds, token)

print(f'refresh_token: {creds.refresh_token}')
service = build('calendar', 'v3', credentials=creds)

now = datetime.utcnow()

start_of_today = datetime(now.year, now.month, now.day, 0, 0, 0)

end_of_today = start_of_today + timedelta(days=1)

start_time = start_of_today.isoformat() + 'Z'
end_time = end_of_today.isoformat() + 'Z'

# today events
events_result = service.events().list(
    calendarId='primary', 
    timeMin=start_time,
    timeMax=end_time,
    maxResults=10
).execute()

events = events_result.get('items', [])
if not events:
    print('No events today.')
for event in events:
    print(event)