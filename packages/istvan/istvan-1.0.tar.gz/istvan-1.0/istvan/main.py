import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import requests
import pandas
from openpyxl.workbook import Workbook

import config


def pityu_loopyear(year):
    year = int(year)
    if year % 4 != 0:
        print("Not leap year.")
        return False
    else:
        if year % 100 != 0:
            print("Leap year.")
            return True
        else:
            if year % 400 != 0:
                print("Not leap year.")
                return False
            else:
                print("Leap year.")
                return True


class FlightSearch:

    def __init__(self):
        self.headers = {
            'accept': 'application/json',
            'apikey': config.apykey,
        }
        self.kiwi_endpoint = 'https://api.tequila.kiwi.com'
        self.search_endpoint = 'https://api.tequila.kiwi.com/v2/search'
        self.my_email = config.my_email
        self.password = config.my_email_password

    def add_iata_code(self, city_name):
        params = {
            "term": city_name,
            "location_types": "city"
        }

        response = requests.get(url=f"{self.kiwi_endpoint}/locations/query", params=params, headers=self.headers)
        result = response.json()
        return result["locations"][0]["code"]

    def search_all_flight(self, fly_from, fly_to, date_from, date_to, min_night, max_night, person):
        from_iata = self.add_iata_code(fly_from)
        to_iata = self.add_iata_code(fly_to)
        params = {
            'fly_from': from_iata,
            'fly_to': to_iata,
            'date_from': date_from,
            'date_to': date_to,
            'nights_in_dst_from': min_night,
            'nights_in_dst_to': max_night,
            'adults': person,
            "flight_type": "round",
            'partner_market': 'usd',
            'limit': '100',
        }

        response = requests.get(url=self.search_endpoint, params=params, headers=self.headers)
        all_flight_data = response.json()
        return all_flight_data

    def create_csv(self, flight_data):
        index = 0
        flight_dic = {
            "City_From": {0: None},
            "City_To": {0: None},
            "Price": {0: None},
            "Date_To": {0: None},
            "Date_Back": {0: None},
            "Night": {0: None},
            "Link": {0: None}
        }

        for option in flight_data["data"]:
            # onather option for cheapest file data
            from_city = option["cityFrom"]
            to_city = option["cityTo"]
            from_data = option["route"][0]["local_departure"].split(".")[0]
            back_data = option["route"][1]["local_departure"].split(".")[0]
            night = option["nightsInDest"]
            valuta = "EUR"
            price = option["price"]
            link = option['deep_link']

            # add new line to the first dic
            flight_dic["City_From"][index] = from_city
            flight_dic["City_To"][index] = to_city
            flight_dic["Price"][index] = f"{valuta}: {price}"
            flight_dic["Date_To"][index] = from_data
            flight_dic["Date_Back"][index] = back_data
            flight_dic["Night"][index] = night
            flight_dic["Link"][index] = link
            index += 1

        df = pandas.DataFrame(flight_dic)
        df.to_csv("flight.csv")
        df.to_excel("flight.xlsx", )


    def send_mail(self, send_to, subject, text, file, isTls=True):
        msg = MIMEMultipart()
        msg['From'] = "pista1125@gmail.com"
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(text))

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(file, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={file}')
        msg.attach(part)

        # context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
        # SSL connection only working on Python 3+
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        if isTls:
            smtp.starttls()
        smtp.login(self.my_email, self.password)
        smtp.sendmail("pista1125@gmail.com", send_to, msg.as_string())
        smtp.quit()

    def search_flight(self, fly_from, fly_to, date_from, date_to, min_night, max_night, person, email):
        data = self.search_all_flight(fly_from, fly_to, date_from, date_to, min_night, max_night, person )
        self.create_csv(data)
        self.send_mail(email, f"flight to: {fly_to}","Good luck", "flight.xlsx", True )