# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ORS_API_KEY = os.getenv("ORS_API_KEY")
