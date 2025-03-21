from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_order_tracking_chatbot.tools.custom_tool import OrderTrackingTool
import os

os.environ["MEM0_API_KEY"]="m0-MZtXk0fHkrVMBljIeyzRXQvfIwmqzS5mw6nmbsxm"
@CrewBase
class CrewaiOrderTrackingChatbotCrew():
    """CrewaiOrderTrackingChatbot crew"""

    @agent
    def order_tracking_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['order_tracking_specialist'],
            tools=[OrderTrackingTool()],
        )


    @task
    def extract_tracking_id_task(self) -> Task:
        return Task(
            config=self.tasks_config['extract_tracking_id_task'],
            tools=[OrderTrackingTool()],
        )

    @task
    def update_memory_task(self) -> Task:
        return Task(
            config=self.tasks_config['update_memory_task'],
            tools=[OrderTrackingTool()],
        )

    @task
    def call_tracking_api_task(self) -> Task:
        return Task(
            config=self.tasks_config['call_tracking_api_task'],
            tools=[OrderTrackingTool()],
        )

    @task
    def generate_response_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_response_task'],
            tools=[OrderTrackingTool()],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiOrderTrackingChatbot crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,
            memory_config={
            "provider": "mem0",
            "config": {"user_id": "crew_user_1"},
            "file_path": "memory.json"
        }
    )
