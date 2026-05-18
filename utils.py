from typing import Any
from datetime import datetime

import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jinja2


import requests
import constants
import config

def write_logs(key: str, params: dict, result: Any):
    with open(constants.LOG_CSV_FILE_NAME, mode="a", encoding="utf-8") as file:
        log = f"{datetime.now()};{key};{params};{result}\n"
        file.write(log)


def get_weather_info(city: str) -> dict:
    params = {
        "q": city,
        "appid": config.API_KEY,
        "units": "metric",
    }
    response = requests.get(constants.OPEN_WEATHER_API_URL, params=params)
    response_json = response.json()
    # print(response.url, response_json)
    temperature = response_json["main"]["temp"]
    temperature_like = response_json["main"]["feels_like"]
    weather_main = response_json["weather"][0]["main"]
    weather_description = response_json["weather"][0]["description"]
    wind_speed = response_json["wind"]["speed"]
    result =  {
        "temperature": temperature,
        "temperature_like": temperature_like,
        "weather_main": weather_main,
        "weather_description": weather_description,
        "wind_speed": wind_speed,
    }
    write_logs('get_weather_info', {"city": city}, result)
    return result


def send_email(
    recipients: list[str],
    mail_body: str,
    mail_subject: str,
    attachment: str = None,
):
    TOKEN = config.TOKEN_UKR_NET
    USER = config.USER_UKR_NET
    SMTP_SERVER = config.SMTP_SERVER

    msg = MIMEMultipart('alternative')
    msg['Subject'] = mail_subject
    msg['From'] = f'<Email was sent from {USER}>'
    msg['To'] = ', '.join(recipients)
    msg['Reply-To'] = USER
    msg['Return-Path'] = USER
    msg['X-Mailer'] = 'decorator'

    # text_to_send = MIMEText(mail_body, 'plain')
    text_to_send = MIMEText(mail_body, 'html')
    msg.attach(text_to_send)

    if attachment:
        is_file_exists = os.path.exists(attachment)
        if is_file_exists:
            basename = os.path.basename(attachment)
            filesize = os.path.getsize(attachment)
            file = MIMEBase('application', f'octet-stream; name={basename}')
            file.set_payload(open(attachment, 'br').read())
            file.add_header('Content-Description', attachment)
            file.add_header(
                'Content-Description',
                f'attachment; filename={attachment}, size={filesize}',
            )
            encoders.encode_base64(file)
            msg.attach(file)

    mail = smtplib.SMTP_SSL(SMTP_SERVER)
    mail.login(USER, TOKEN)
    mail.sendmail(USER, recipients, msg.as_string())
    mail.quit()


def create_weather_report(data: dict) -> str:
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "templates/weather.html"
    template = template_env.get_template(template_file)
    output = template.render(data)
    return output