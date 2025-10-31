from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os, json, dotenv

app = FastAPI()
dotenv.load_dotenv()

@app.get("/")
async def root():
    return "Root"

@app.get("/ping")
async def health_check():
    return "pong"


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # For local dev only

client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

flow = Flow.from_client_config(
    {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [redirect_uri],
        }
    },
    scopes=["https://www.googleapis.com/auth/calendar.events"],
)
flow.redirect_uri = redirect_uri  # Set the redirect_uri on the flow object

# Step 1: Redirect to Google for consent
@app.get("/auth")
def auth():
    authorization_url, state = flow.authorization_url(
        access_type="offline", prompt="consent", include_granted_scopes="true"
    )
    return RedirectResponse(authorization_url)

# Step 2: Google redirects back with code; exchange it for tokens
@app.get("/auth/callback")
def auth_callback(request: Request):
    flow.fetch_token(authorization_response=str(request.url))
    credentials = flow.credentials
    tokens = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
    # In production: store this in your DB, tied to the authenticated user
    with open("tokens.json", "w") as f:
        json.dump(tokens, f)
    return JSONResponse({"status": "ok", "message": "Google Calendar connected"})

# Step 3: Use stored tokens to call Calendar API
@app.get("/calendar")
def get_calendar_events():
    with open("tokens.json") as f:
        tokens = json.load(f)
    creds = Credentials(**tokens)
    service = build("calendar", "v3", credentials=creds)
    events = service.events().list(calendarId="primary").execute()
    return events
