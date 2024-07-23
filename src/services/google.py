import json
import logging
from datetime import datetime
from dateutil import parser

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.definitions.credentials import Credentials as Creds

logger = logging.getLogger(__name__)


class GoogleAPI:
    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/calendar"]
        self._credentials = self._authenticate()
        self.calendar = build(serviceName="calendar", version="v3", credentials=self._credentials)

    def _authenticate(self):
        """
        Authenticate
        """
        try:
            token_json = json.loads(Creds.google_token())
            creds = Credentials.from_authorized_user_info(token_json, scopes=self.scopes)
            return creds
        except Exception as e:
            logger.error(f"GoogleAPI Authentication failed. Error: {e}")

    def existing_events(self, time: str) -> bool:
        """
        Checks for existing events

        Args:
            time: str - time in ISO8601 format
        """
        try:
            events_result = self.calendar.events().list(
                calendarId="primary",
                timeMin=time,
                maxResults=1,
                singleEvents=True,
                orderBy="startTime"
            ).execute()

            events = events_result.get("items", [])
            if not events:
                logger.info("No upcoming events found.")
                return False
            target = parser.isoparse(time)
            for event in events:
                event_start = parser.isoparse(event['start']['dateTime'])
                event_end = parser.isoparse(event['end']['dateTime'])
                if event_end >= target >= event_start:
                    logger.info("Cannot set meeting. An event already exists.")
                    return True
            return False
        except HttpError as error:
            # TODO: LLM needs to handle this with an error message
            logger.error(f"Failed to get existing events on Google Calendar. An error occurred: {error}")

    def generate_token_from_credentials(self):
        """
        Generates token.json from credentials.json. Only call this locally.

        Copy token.json into .env
        """
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=self.scopes)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    def create_meeting(self, meeting_start: str, meeting_end: str):
        """
        Creates a meeting on Google Calendar
        Args:
             meeting_start: str - Meeting start time in ISO8601 format
             meeting_end: str - Meeting end time in ISO8601 format
        """
        # Check for conflicts. Return failed to set meeting if there are conflicts
        conflicts = self.existing_events(meeting_start)
        if conflicts:
            logging.error(f"Failed to create a meeting on Google Calendar. Meeting conflicts found: {conflicts}")
            return False
        try:
            event = {
                "summary": "30 minute Consultancy Call",
                "description": "PioneerDevAI Consulting Call",
                "colorId": 6,
                "start": {
                    "dateTime": meeting_start,
                    "timeZone": "Asia/Singapore"
                },
                "end": {
                    "dateTime": meeting_end,
                    "timeZone": "Asia/Singapore"
                },
                "attendees": [
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
            # Set the event
            event = self.calendar.events().insert(calendarId="primary", body=event, conferenceDataVersion=1).execute()
            success = event['conferenceData']['createRequest']['status']['statusCode'] == 'success'
            logger.info(f"Meeting result: {success}")
            # {'kind': 'calendar#event', 'etag': '"3443281977610000"', 'id': '9km30ljt52k10dq52miit9tne8', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=OWttMzBsanQ1MmsxMGRxNTJtaWl0OXRuZTggamF5YWxmYXJhc0Bt', 'created': '2024-07-22T09:36:28.000Z', 'updated': '2024-07-22T09:36:28.805Z', 'summary': 'Google Event', 'description': 'Some random description', 'location': 'Somewhere online', 'colorId': '6', 'creator': {'email': 'jayalfaras@gmail.com', 'self': True}, 'organizer': {'email': 'jayalfaras@gmail.com', 'self': True}, 'start': {'dateTime': '2024-07-23T09:00:00+08:00', 'timeZone': 'Asia/Singapore'}, 'end': {'dateTime': '2024-07-23T10:00:00+08:00', 'timeZone': 'Asia/Singapore'}, 'iCalUID': '9km30ljt52k10dq52miit9tne8@google.com', 'sequence': 0, 'attendees': [{'email': 'alfarasjb@gmail.com', 'responseStatus': 'needsAction'}, {'email': 'jayalfaras@gmail.com', 'organizer': True, 'self': True, 'responseStatus': 'needsAction'}], 'hangoutLink': 'https://meet.google.com/pfu-brgs-isa', 'conferenceData': {'createRequest': {'requestId': 'some-random-string', 'conferenceSolutionKey': {'type': 'hangoutsMeet'}, 'status': {'statusCode': 'success'}}, 'entryPoints': [{'entryPointType': 'video', 'uri': 'https://meet.google.com/pfu-brgs-isa', 'label': 'meet.google.com/pfu-brgs-isa'}], 'conferenceSolution': {'key': {'type': 'hangoutsMeet'}, 'name': 'Google Meet', 'iconUri': 'https://fonts.gstatic.com/s/i/productlogos/meet_2020q4/v6/web-512dp/logo_meet_2020q4_color_2x_web_512dp.png'}, 'conferenceId': 'pfu-brgs-isa'}, 'reminders': {'useDefault': True}, 'eventType': 'default'}
            return success
        except HttpError as error:
            logger.error(f"Failed to create meeting on Google Calendar. Error: {error}") 
            return False


