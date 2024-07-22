import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes=SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired.creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials_oauth.json", scopes=SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": "Google Event",
            "location": "Somewhere online",
            "description": "Some random description",
            "colorId": 6,
            "start": {
                "dateTime": "2024-07-23T09:00:00+02:00",
                "timeZone": "Europe/Vienna"
            },
            "end": {
                "dateTime": "2024-07-23T10:00:00+02:00",
                "timeZone": "Europe/Vienna"
            },
            "attendees": [
                {"email": "alfarasjb@gmail.com"},
                {"email": "jayalfaras@gmail.com"}
            ],
            "conferenceData": {
                "createRequest": {
                    "conferenceSolutionKey": {
                        "type": "hangoutsMeet"
                    },
                    "requestId": "some-random-string"  # Unique identifier for the request
                }
            }
        }

        event = service.events().insert(calendarId="primary", body=event, conferenceDataVersion=1).execute()
        print(f"Event Created {event.get('htmlLink')}")

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
