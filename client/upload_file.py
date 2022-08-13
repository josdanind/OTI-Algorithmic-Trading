import requests

HOST = "localhost"
PORT = 80
URL = f"http://{HOST}:{PORT}/assets/upload"

file = {"file": open("test.txt", "rb")}
resp = requests.post(url=URL, files=file)

print(resp.json())
