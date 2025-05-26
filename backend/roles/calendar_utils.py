import os
import pickle
import datetime

from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]
REDIRECT_URI = "http://localhost:8000/calendar/auth"

def get_calendar_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
        else:
            flow = Flow.from_client_secrets_file(
                "credentials.json",
                scopes=SCOPES,
                redirect_uri=REDIRECT_URI
            )
            auth_url, _ = flow.authorization_url(prompt='consent')
            return {"auth_url": auth_url}

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)

def update_event(event_id, updated_fields):
    service = get_calendar_service()
    if isinstance(service, dict):  # User hasn't authorized yet
        return service

    try:
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        for key, value in updated_fields.items():
            event[key] = value

        updated_event = service.events().update(
            calendarId='primary',
            eventId=event_id,
            sendUpdates='all',  # notify all attendees
            body=event
        ).execute()

        return updated_event
    except Exception as e:
        return {"error": str(e)}