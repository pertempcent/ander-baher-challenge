import requests

def fetch_data():
    api_url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

if __name__ == "__main__":
    data = fetch_data()
    if data:
        for user in data:
            print(user["name"])
    else:
        print("Failed to fetch data from the API.")
