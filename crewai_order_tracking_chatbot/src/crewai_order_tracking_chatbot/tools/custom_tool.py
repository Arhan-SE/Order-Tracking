import requests
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

API_KEY = "26820b9f-a7e7-46cd-a772-7520e1d82041"
API_URL = "https://app.pinascargo.com/ai_api/tracking"

class OrderTrackingInput(BaseModel):
    """Schema for tracking order input."""
    booking_number: str = Field(..., description="Booking number for the order.")

class OrderTrackingTool(BaseTool):
    name: str = "Order Tracking Tool"
    description: str = "Fetches real-time order tracking details using a booking number."
    args_schema: Type[BaseModel] = OrderTrackingInput

    def _run(self, booking_number: str) -> str:
        response = requests.post(API_URL, json={"booking_number": booking_number}, headers={"apikey": API_KEY})
        return response.json().get("data")
