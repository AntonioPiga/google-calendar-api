from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import uuid

def main(args):

    try:
        redirect_uris = args.get('REDIRECT_URIS_0'), args.get('REDIRECT_URIS_1')

        web_client_info = {
            "web": {
                "client_id": args.get('CLIENT_ID'),
                "project_id": args.get('PROJECT_ID'),
                "auth_uri": args.get('AUTH_URI'),
                "token_uri": args.get('TOKEN_URI'),
                "auth_provider_x509_cert_url": args.get('AUTH_PROVIDER_X509_CERT_URL'),
                "client_secret": args.get('CLIENT_SECRET'),
                "redirect_uris": redirect_uris, 
                "javascript_origins": args.get('JAVASCRIPT_ORIGINS_0')
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
            print('No events today.')
        for event in events:
            print(event)

        return {
            'body': {
            'output': events,
            'state': str(uuid.uuid4()),
            'display': 'json'
            }
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        raise(e)
