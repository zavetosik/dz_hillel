from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

TOKEN_UKR_NET = os.getenv("TOKEN_UKR_NET")
USER_UKR_NET = os.getenv("USER_UKR_NET")
SMTP_SERVER = os.getenv("SMTP_SERVER")
