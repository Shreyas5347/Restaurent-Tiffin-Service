import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_secret_key")
    WHATSAPP_PHONE_NUMBER = os.getenv("WHATSAPP_PHONE_NUMBER", "918828683828")
    UPI_ID = os.getenv("UPI_ID", "8828683828@axl")
    # Comma-separated list of allowed frontend origins (e.g. Cloudflare Pages URL)
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
