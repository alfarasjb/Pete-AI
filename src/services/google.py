import json

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.definitions.credentials import Credentials as Creds


class GoogleAPI:
    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/calendar"]
        self._credentials = self._authenticate()

    def _authenticate(self):
        token_json = json.loads(Creds.google_token())
        creds = Credentials.from_authorized_user_info(token_json, scopes=self.scopes)
        return creds

    def generate_token_from_credentials(self):
        # Only call this locally
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=self.scopes)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    def create_meeting(self):
        try:
            service = build(serviceName="calendar", version="v3", credentials=self._credentials)
            event = {
                "summary": "Google Event",
                "location": "Somewhere online",
                "description": "Some random description",
                "colorId": 6,
                "start": {
                    "dateTime": "2024-07-23T09:00:00+08:00",
                    "timeZone": "Asia/Singapore"
                },
                "end": {
                    "dateTime": "2024-07-23T10:00:00+08:00",
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
            event = service.events().insert(calendarId="primary", body=event, conferenceDataVersion=1).execute()
            # {'kind': 'calendar#event', 'etag': '"3443281977610000"', 'id': '9km30ljt52k10dq52miit9tne8', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=OWttMzBsanQ1MmsxMGRxNTJtaWl0OXRuZTggamF5YWxmYXJhc0Bt', 'created': '2024-07-22T09:36:28.000Z', 'updated': '2024-07-22T09:36:28.805Z', 'summary': 'Google Event', 'description': 'Some random description', 'location': 'Somewhere online', 'colorId': '6', 'creator': {'email': 'jayalfaras@gmail.com', 'self': True}, 'organizer': {'email': 'jayalfaras@gmail.com', 'self': True}, 'start': {'dateTime': '2024-07-23T09:00:00+08:00', 'timeZone': 'Asia/Singapore'}, 'end': {'dateTime': '2024-07-23T10:00:00+08:00', 'timeZone': 'Asia/Singapore'}, 'iCalUID': '9km30ljt52k10dq52miit9tne8@google.com', 'sequence': 0, 'attendees': [{'email': 'alfarasjb@gmail.com', 'responseStatus': 'needsAction'}, {'email': 'jayalfaras@gmail.com', 'organizer': True, 'self': True, 'responseStatus': 'needsAction'}], 'hangoutLink': 'https://meet.google.com/pfu-brgs-isa', 'conferenceData': {'createRequest': {'requestId': 'some-random-string', 'conferenceSolutionKey': {'type': 'hangoutsMeet'}, 'status': {'statusCode': 'success'}}, 'entryPoints': [{'entryPointType': 'video', 'uri': 'https://meet.google.com/pfu-brgs-isa', 'label': 'meet.google.com/pfu-brgs-isa'}], 'conferenceSolution': {'key': {'type': 'hangoutsMeet'}, 'name': 'Google Meet', 'iconUri': 'https://fonts.gstatic.com/s/i/productlogos/meet_2020q4/v6/web-512dp/logo_meet_2020q4_color_2x_web_512dp.png'}, 'conferenceId': 'pfu-brgs-isa'}, 'reminders': {'useDefault': True}, 'eventType': 'default'}
            print(event)
        except HttpError as error:
            print(f"An error occurred: {error}")


