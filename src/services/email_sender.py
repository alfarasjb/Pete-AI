import requests


def send_email(name: str, message: str):
    url = 'https://formspree.io/f/xvgpzpdd'  # Replace with your form endpoint URL
    data = {
        'name': name,
        'message': message
    }
    print(f"Send Email")
    # response = requests.post(url, data=data)

    # if response.status_code == 200:
    #     print("Form submitted successfully!")
    # else:
    #     print(f"Failed to submit form. Status code: {response.status_code}")
    #     print(f"Response: {response.text}")
