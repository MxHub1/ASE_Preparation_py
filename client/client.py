import requests
import json

BASE_URL = 'http://127.0.0.1:8080'  # Update with the actual URL of your REST service

# Example GET request
def get_data():
    try:
        response = requests.get(f'{BASE_URL}/data')
        data = response.json()
        print('GET Response:', data)

    except Exception as e:
        print('Error:', str(e))

# Example POST request
def post_data(name, quantity):
    try:
        payload = {'name': name, 'quantity': quantity}
        headers = {'Content-Type': 'application/json'}

        response = requests.post(f'{BASE_URL}/data', data=json.dumps(payload), headers=headers)
        data = response.json()
        print('POST Response:', data)

    except Exception as e:
        print('Error:', str(e))

if __name__ == '__main__':
    # Test the GET request
    data = get_data()

    print(data)

    # Test the POST request
    # post_data('Item1', 10)