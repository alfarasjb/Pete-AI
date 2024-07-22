from src.services.google import GoogleAPI

TIME = "2024-07-26T09:00:00+08:00"
END = "2024-07-26T09:30:00+08:00"

if __name__ == "__main__":
    google = GoogleAPI()
    # print(google.existing_events(TIME))
    google.create_meeting(TIME, END)