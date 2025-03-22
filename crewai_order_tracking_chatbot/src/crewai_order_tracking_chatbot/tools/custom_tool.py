import requests
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
from mem0 import Memory
from dotenv import load_dotenv
load_dotenv()
CLIENT_API_KEY = os.getenv("CLIENT_API_KEY")#"26820b9f-a7e7-46cd-a772-7520e1d82041"
CLIENT_API_URL = os.getenv("CLIENT_API_URL")#"https://app.pinascargo.com/ai_api/tracking"

class OrderTrackingInput(BaseModel):
    """Schema for tracking order input."""
    booking_number: str = Field(..., description="Booking number for the order.")

class OrderTrackingTool(BaseTool):
    name: str = "Order Tracking Tool"
    description: str = "Fetches real-time order tracking details using a booking number."
    args_schema: Type[BaseModel] = OrderTrackingInput

    def _run(self, booking_number: str) -> str:
        response = requests.post(CLIENT_API_URL, json={"booking_number": booking_number}, headers={"apikey": CLIENT_API_KEY})
        return response.json().get("data")


load_dotenv()

# Mem0 Configuration
config = {
    "vector_store": {
        "provider": "supabase",
        "config": {
            "connection_string": os.getenv("DATABASE_URL"),
            "collection_name": "memories"
        }
    }
}

# Initialize Mem0
memory = Memory.from_config(config)

# Memory Retrieval Schema
class MemorySearchInput(BaseModel):
    query: str = Field(..., description="Query to search relevant memories.")

# Memory Retrieval Tool
class MemoryRetrievalTool(BaseTool):
    name: str = "Memory Retrieval Tool"
    description: str = "Fetches past relevant memories based on the query."
    args_schema: Type[BaseModel] = MemorySearchInput

    def _run(self, query: str) -> str:
        relevant_memories = memory.search(query=query, user_id="default_user", limit=3)
        if not relevant_memories["results"]:
            return "No relevant memories found."
        return "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])

