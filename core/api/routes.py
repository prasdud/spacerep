import datetime
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import os, json
import logging as log
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db
from db.models import Event
from db.crud import get_events, add_event


router = APIRouter()

@router.get("/")
async def root():
    return "Root"

@router.get("/ping")
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

# Redirect to Google for consent
@router.get("/auth")
def auth():
    authorization_url, state = flow.authorization_url(
        access_type="offline", # request refresh token
        prompt="consent",   # force consent screen to show for returning users
    )
    log.info(f"Authorization URL: {authorization_url}")
    return RedirectResponse(authorization_url)

# Google redirects back with code; exchange it for tokens
@router.get("/auth/callback")
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
        json.dump(tokens, f, indent=2)
    return JSONResponse({"status": "ok", "message": "Google Calendar connected"})

# Use stored tokens to call Calendar API
@router.get("/calendar")
def get_calendar_events():

    creds = None
    with open("tokens.json") as f:
        tokens = json.load(f)
    creds = Credentials(**tokens)

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        response = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            log.info(start, event["summary"])
            response.append({"start": start, "summary": event["summary"]})
        
        return JSONResponse(response)

    except HttpError as error:
        print(f"An error occurred: {error}")


@router.get("/events")
async def read_events(session: AsyncSession = Depends(get_db)):
    return await get_events(session)

@router.post("/events")
async def create_event(event: Event, session: AsyncSession = Depends(get_db)):
    await add_event(session, event)
    return {"status": "ok"}
