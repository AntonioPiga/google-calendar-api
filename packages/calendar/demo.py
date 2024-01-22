from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import uuid

def main():
    try:
        auth_url = start_auth()
        return {
            'body': {
                'output': auth_url,
                'state': str(uuid.uuid4()),
                'display': 'json'
            }
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e

def start_auth():
    web_client_info = {
        "web": {
            "client_id": "xxx",
            "project_id": "xxx",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "xxx",
            "redirect_uris": ["http://localhost:8080/"],
            "javascript_origins": ["http://localhost"]
        }
    }

    scopes = ['https://www.googleapis.com/auth/calendar']

    flow = Flow.from_client_config(
        web_client_info, scopes,
        redirect_uri='https://nuvolaris.dev/api/v1/web/antoniopiga/callback/callback')

    authorization_url, _ = flow.authorization_url(prompt='consent')
    
    print('auth url is')
    print(authorization_url)
    
    return authorization_url

# Test
main()
