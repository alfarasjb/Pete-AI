import requests
import json
from typing import Dict, List

from src.definitions.credentials import Credentials

# NOTE: Calendly does not have an endpoint to support scheduling events.
# Must use a different option
# https://developer.calendly.com/frequently-asked-questions


class Calendly:
    def __init__(self):
        self._api_key = Credentials.calendly_api_key()
        self.base_url = 'https://api.calendly.com'
        self.headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }
        self.user_uri = self.get_user_uri()
        self.last_recorded_customer_name = ""
        self.last_recorded_meeting_date = ""

    def get_user_uri(self):
        endpoint = self.base_url + "/users/me"
        response = requests.get(endpoint, headers=self.headers)
        return response.json()['resource']['uri']

    def list_user_availability_schedules(self):
        endpoint = self.base_url + "/user_availability_schedules"
        params = {"user": self.user_uri}
        response = requests.get(endpoint, params=params, headers=self.headers)
        if response.status_code == 200:
            response_json = response.json()
            available_schedule = {}
            schedules = response_json['collection'][0]['rules']
            timezone = response_json['collection'][0]['timezone']
            for schedule in schedules:
                if len(schedule['intervals']) == 0:
                    continue
                available_schedule[schedule['wday']] = schedule['intervals']
            # return self.to_readable_schedule(available_schedule, timezone)
            return available_schedule
        else:
            print("Something went wrong")

    def to_readable_schedule(self, schedule: Dict[str, any], timezone: str):
        schedules = [f"Timezone: {timezone}"]
        for day, times in schedule.items():
            schedules.append(day)
            for time in times:
                schedules.append(f" - {time['from']} - {time['to']}")
        return '\n'.join(schedules)

    def get_user_event_types(self):
        endpoint = self.base_url + "/event_types"
        params = {"user": self.user_uri}
        response = requests.get(endpoint, headers=self.headers, params=params)
        if response.status_code:
            event_uri = response.json()['collection'][0]['uri']

        print(json.dumps(response.json(), indent=4))

    def set_meeting(self, meeting_date: str, customer_name: str):
        # Ignore empty inputs
        if meeting_date == "" or customer_name == "":
            return
        # Ignore repeat requests
        if self.last_recorded_meeting_date == meeting_date:
            return
        if self.last_recorded_customer_name == customer_name:
            return
        self.last_recorded_meeting_date = meeting_date
        self.last_recorded_customer_name = customer_name
        print(f"Setting calendly meeting for: {customer_name} on {meeting_date}")
