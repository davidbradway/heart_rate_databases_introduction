import requests

ip: str = "http://152.3.77.242:5000"
endpoint : str = "/api/heart_rate"

r = requests.post(ip+endpoint, json={"user_email": "suyash@suyashkumar.com",
                                     "user_age": 50, # in years
                                     "heart_rate": 100})
res = r.json()
print(res)
print("The response was {0}.".format(res['result']))
