import requests

url = "https://apidojo-booking-v1.p.rapidapi.com/currency/get-exchange-rates"

querystring = {"base_currency":"USD","languagecode":"en-us"}

headers = {
	"X-RapidAPI-Key": "e888c42f67msh10e9b05c155346cp112e4djsncdfda2df318c",
	"X-RapidAPI-Host": "apidojo-booking-v1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)