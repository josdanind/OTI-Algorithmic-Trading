import requests
from common import URL, read_json, print_dict

jwt = read_json("./token.json")
HEADERS = {"Authorization": f"{jwt['token_type']} {jwt['access_token']}"}

url = URL + f"/traders"

response = requests.get(url, headers=HEADERS)
content = response.json()

if response.status_code == 200:
    print(content)
else:
    print_dict(content)
