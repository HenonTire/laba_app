import requests

url = "https://laba-app-1.onrender.com/login/"

response = requests.post(
    url,
    json={
        "username": "henon",
        "password": "testing321"
    }
)

print(response.status_code)
print(response.json())
