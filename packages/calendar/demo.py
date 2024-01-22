from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import uuid
from openai import OpenAI

def main():
    try:
        events = get_today_events()
            
        return( {
            'body': {
            'output': 'ok',
            'state': str(uuid.uuid4()),
            'display': 'json'
            }
        })
    except Exception as e:
        print(f"An error occurred: {e}")
        raise(e)

def get_today_events():

    web_client_info = {
    "web": {
        "client_id": "xxx",
        "project_id": "xxx",
        "auth_uri": "xxx",
        "token_uri": "xxx",
        "auth_provider_x509_cert_url": "xxx",
        "client_secret": "xxx",
        "redirect_uris": "xxx",
        "javascript_origins": ["xxx"]
    }

}

    scopes = ['https://www.googleapis.com/auth/calendar'] 
    
    creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                web_client_info, scopes)
            authorization_url = flow.authorization_url(prompt='consent')
            print('auth url is')
            print(authorization_url)
            flow = InstalledAppFlow.from_client_config(
                web_client_info, scopes)
            creds = flow.run_local_server(port=8080)

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
        events = 'no events today'
    return events    

def send_events_to_ai(events):
    ROLE = "You are an assistant that describe google calendar events from json."
    MODEL = "gpt-3.5-turbo"
    #AI = OpenAI(api_key=args.get('OPEN_AI_KEY'))

    #comp = AI.chat.completions.create(model=MODEL, messages=req(ROLE, events)).choices[0].message.content
   
    return 1


def req(ROLE, events):
    return [{"role": "system", "content": ROLE}, 
            {"role": "user", "content": 'Describe this google calendar events:' + str(events)}]

main()