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


class OrchestratorFlow(Flow):
    model = model_name
 
    @start()
    def initial_draft(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Draft a short blog post about AI automation."}]
        )
        draft = response["choices"][0]["message"]["content"].strip()
        self.state["draft"] = draft
        print("Initial Draft:")
        print(draft)
        return draft

    @listen(initial_draft)
    def refine_draft(self, draft):
        # Simulate dynamic task delegation: iterate refinement.
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Refine this draft for clarity and style: {draft}"}]
        )
        refined = response["choices"][0]["message"]["content"].strip()
        self.state["draft"] = refined
        print("Refined Draft:")
        print(refined)
        return refined

def kickoff():
    orchestrator_flow = OrchestratorFlow()
    orchestrator_flow.kickoff()


def plot():
    orchestrator_flow = OrchestratorFlow()
    orchestrator_flow.plot()


if __name__ == "__main__":
    kickoff()
