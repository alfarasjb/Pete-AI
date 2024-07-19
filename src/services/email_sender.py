import requests


class Email:
    def __init__(self):
        self.url = ''

    def send_email(self, name: str, email_address: str, message: str):
        data = {
            "name": name,
            "email": email_address,
            "message": message
        }

        response = requests.post(self.url, data=data)
        print(response.status_code)

if __name__ == "__main__":
    service = Email()