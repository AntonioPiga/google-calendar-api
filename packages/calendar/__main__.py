from flask import Flask, request, redirect, session
from google_auth_oauthlib.flow import Flow

app = Flask(__name__)

@app.route('/')
def index():
    return get_authorization_url()

@app.route('/get_authorization_url')
def get_authorization_url():
    
    web_client_info = {
       {
        "web": {
            "client_id": "xxx",
            "project_id": "xxx",
            "auth_uri": "xxx",
            "token_uri": "xxx",
            "auth_provider_x509_cert_url": "xxx",
            "client_secret": "xxx",
            "redirect_uris": ["xxx"],
            "javascript_origins": ["xxx"]
        }
    }
}


    scopes = ['https://www.googleapis.com/auth/calendar']

    flow = Flow.from_client_config(
        web_client_info, scopes,
        redirect_uri='https://nuvolaris.dev/api/v1/web/antoniopiga/callback/callback')

    authorization_url, _ = flow.authorization_url(prompt='consent')

    return redirect(authorization_url)

@app.route('/callback')
def callback():
    
    authorization_code = request.args.get('code')

    web_client_info = {
       {
        "web": {
            "client_id": "xxx",
            "project_id": "xxx",
            "auth_uri": "xxx",
            "token_uri": "xxx",
            "auth_provider_x509_cert_url": "xxx",
            "client_secret": "xxx",
            "redirect_uris": ["xxx"],
            "javascript_origins": ["xxx"]
        }
    }

    }

    scopes = ['https://www.googleapis.com/auth/calendar']

    flow = Flow.from_client_config(
        web_client_info, scopes,
        redirect_uri='http://localhost:8080/callback')

    token = flow.fetch_token(
        authorization_response=request.url)

    print(token)
    

    return 'Consensi concessi con successo! ' + str(token)

if __name__ == '__main__':
    app.run(port=8080)
