#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start,router,or_

from routes.crews.poem_crew.poem_crew import PoemCrew
from litellm import completion
from dotenv import load_dotenv
import os
load_dotenv()
model_name = os.getenv("MODEL")


class AutonomousAgentFlow(Flow):
    model = model_name

    @start()
    def initial_prompt(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Generate a creative idea for an AI article."}]
        )
        idea = response["choices"][0]["message"]["content"].strip()
        self.state["idea"] = idea
        # Set a flag for further branching; for example, if the idea includes the word "technology"
        self.state["is_tech"] = "technology" in idea.lower()
        print("Initial Idea:")
        print(idea)
        return idea

    @router(initial_prompt)
    def choose_flow(self):
        # Route the flow based on the idea category.
        if self.state.get("is_tech"):
            return "tech_flow"
        else:
            return "general_flow"

    @listen("tech_flow")
    def tech_content(self, idea):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Develop a detailed outline for an AI article focused on technology: {idea}"}]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        return outline

    @listen("general_flow")
    def general_content(self, idea):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Develop a detailed outline for an AI article: {idea}"}]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        return outline

    @listen(or_(tech_content, general_content))
    def final_optimization(self, outline):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Improve and polish this article outline: {outline}"}]
        )
        final_outline = response["choices"][0]["message"]["content"].strip()
        print("Final Optimized Outline:")
        print(final_outline)
        return final_outline


def kickoff():
    autonomousAgentFlow = AutonomousAgentFlow()
    autonomousAgentFlow.kickoff()


def plot():
    autonomousAgentFlow = AutonomousAgentFlow()
    autonomousAgentFlow.plot()


if __name__ == "__main__":
    kickoff()
