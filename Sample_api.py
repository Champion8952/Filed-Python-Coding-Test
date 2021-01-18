import requests

url = "localhost:5000/payments"

payload='CreditCardNumber=4111111111111111&CardHolder=Roopansh&ExpirationDate=18%2F11%2F2021&Amount=510'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
