import utils
from pywebio.input import input, input_group
from pywebio.output import put_text, put_success
from pywebio import start_server
from pywebio.session import run_js


def main():
    data = input_group(
        "Запит на поточну погоду chi23@ukr.net test_hillel_api_mailing@ukr.net",
        [
            input("City", name="city", required=True),
            input("Email", name="email", required=True),
            input("Friend email", name="friend_email", required=False),
            input("Name", name="name", required=True),
        ]
    )
    current_weather = utils.get_weather_info(data["city"])
    email_body = utils.create_weather_report(current_weather)

    recipients = [data["email"]]
    if data["friend_email"]:
        recipients.append(data["friend_email"])

    utils.send_email(
        recipients,
        email_body,
        mail_subject=f'Weather in {data["city"]}',
        # attachment='log.csv'
    )

    put_success("Email was sent. The page reloads in 5 seconds...")

    run_js("""
        setTimeout(() => {
            window.location.reload();
        }, 5000);
    """)


start_server(
    main,
    host="0.0.0.0",
    port=8888,
    debug=True,
)
