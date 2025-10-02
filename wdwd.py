import requests

print(requests.post('http://192.168.1.183:8000/events/', json={
  "name": "string",
  "date": "2019-08-24T14:15:22Z",
  "location": "string",
  "description": "string",
  "age_restriction": 0,
  "duration": 0
}).text)