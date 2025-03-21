
import requests
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

API_KEY = "26820b9f-a7e7-46cd-a772-7520e1d82041"
API_URL = "https://app.pinascargo.com/ai_api/tracking"


response = requests.post(API_URL, json={"booking_number": "936842"}, headers={"apikey": API_KEY})
print(response.json().get("data"))
