import os
import pickle
import datetime

from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.discovery import build
from openai import OpenAI
from dotenv import load_dotenv
from roles.calendar_utils import get_calendar_service, update_event

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SCOPES = ["https://www.googleapis.com/auth/calendar"]
REDIRECT_URI = "http://localhost:8000/calendar/auth"

def fetch_upcoming_events():
    service = get_calendar_service()
    if isinstance(service, dict):
        return service

    now = datetime.datetime.utcnow().isoformat() + "Z"
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True, orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    return events

def explain_calendar():
    events = fetch_upcoming_events()
    if isinstance(events, dict):  # User hasn't authorized yet
        return events

    summary = "\n".join([
        f"- {e.get('summary', 'No Title')} with {', '.join([att.get('email', 'No Attendees') for att in e.get('attendees', [])])} at {e['start'].get('dateTime', e['start'].get('date'))}"
        for e in events
    ]) or "No upcoming events."

    prompt = f"""You are a calendar assistant. Here's a user's upcoming schedule:
{summary}

Explain these events in plain English. Suggest if there are any time conflicts or improvements for productivity."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content

def modify_event(event_id, updates):
    service = get_calendar_service()
    if isinstance(service, dict):
        return service  # authorization URL or error

    result = update_event(service, event_id, updates)
    return result
