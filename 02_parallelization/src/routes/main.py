#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start,router

from routes.crews.poem_crew.poem_crew import PoemCrew
from litellm import completion
from dotenv import load_dotenv
import os
load_dotenv()
model_name = os.getenv("MODEL")

class RoutedFlow(Flow):
    model = model_name

    @start()
    def generate_topic(self):
        response = completion(
            model=self.model,
            # For tech route
            # messages=[{"role": "user", "content": "The Role of AI in technology Development by 2025 in a paragraph."}]
            # -----------------------------------------
            # For lifestyle route
            messages=[{"role": "user", "content": "Top 10 Travel Destinations for 2025 in 5 line in form of list."}]
            
            
        )
        topic = response["choices"][0]["message"]["content"].strip()
        # For demonstration, add a fake flag to the state.
        self.state["is_tech"] = "tech" in topic.lower()
        print(f"Topic: {topic}")
        return topic

    @router(generate_topic)
    def route_topic(self):
        # Route based on the is_tech flag.
        if self.state.get("is_tech"):
            return "tech_route"
        else:
            return "lifestyle_route"

    @listen("tech_route")
    def generate_tech_outline(self, topic):
        outline=f"Tech route is called......"
        print(outline)
        return outline
        

    @listen("lifestyle_route")
    def generate_lifestyle_outline(self, topic):
        outline=f"Lifestyle route is called......"
        print(outline)
        return outline

def kickoff():
    routed_flow = RoutedFlow()
    routed_flow.kickoff()


def plot():
    routed_flow = RoutedFlow()
    routed_flow.plot()


if __name__ == "__main__":
    kickoff()
