#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from simpleflow.crews.poem_crew.poem_crew import PoemCrew
from litellm import completion
from dotenv import load_dotenv
import os
load_dotenv()
model_name = os.getenv("MODEL")

class TopicOutlineFlow(Flow):
    @start()
    def generate_topic(self):
        # Prompt the LLM to generate a blog topic.
        response = completion(
            model=model_name,
            messages=[{
                "role": "user",
                "content": "Generate a creative blog topic for 2025."
            }]
        )
        topic = response["choices"][0]["message"]["content"].strip()
        print(f"Generated Topic: {topic}")
        return topic

    @listen(generate_topic)
    def generate_outline(self, topic):
        # Now chain the output by using the topic in a follow-up prompt.
        response = completion(
            model=model_name,
            messages=[{
                "role": "user",
                "content": f"Based on the topic '{topic}', create a detailed outline for a blog post."
            }]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        print("Generated Outline:")
        print(outline)
        return outline


def kickoff():
    topic_flow = TopicOutlineFlow()
    topic_flow.kickoff()


def plot():
    topic_flow = TopicOutlineFlow()
    topic_flow.plot()


if __name__ == "__main__":
    kickoff()
