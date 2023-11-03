import requests


BASE = "http://127.0.0.1:5000/"
response = requests.get(BASE + "video/1")
print(response.json())
data = [
    {"likes": 242, "name": "Joe", "views": 10000},
    {"likes": 1000, "name": "How to make REST API", "views": 80000},
    {"likes": 35, "name": "Tim", "views": 2000},
]

for i in range(len(data)):
    response = requests.post(BASE + "video", json=data[i])
    print(response.json())

#response = requests.delete(BASE + "video/0")
#input()
response = requests.get(BASE + "video/0")
print(response.json())
