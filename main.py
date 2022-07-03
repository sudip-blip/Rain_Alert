import smtplib
import requests
from decouple import config

my_email = config("my_email")
password = config("password")
api_key = config("api_key")
My_long = config("My_long")
My_lat = config("My_lat")
weather_endpoint = "https://api.openweathermap.org/data/2.5/onecall"

weather_params = {
    "lat": My_lat,
    "lon": My_long,
    "appid": api_key,
    "exclude": "current,minutely,daily",
}

response = requests.get(weather_endpoint, params=weather_params)
response.raise_for_status()
will_rain = False
for i in range(13):
    weather_data = response.json()["hourly"][i]["weather"][0]["id"]
    if weather_data < 700:
        will_rain = True


if will_rain:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject:It rains.\n\n It will rain today,dont forget to take your umbrella with you.",
        )
