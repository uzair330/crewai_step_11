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


class EvaluatorOptimizerFlow(Flow):
    model = model_name

    @start()
    def generate_response(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Write a draft summary about the benefits of AI in education."}]
        )
        draft = response["choices"][0]["message"]["content"].strip()
        print("Initial Draft Summary:")
        print(draft)
        return draft

    @listen(generate_response)
    def evaluate_and_optimize(self, draft):
        # In a real-world scenario, you might get human feedback.
        # Here, we simulate optimization by asking the model for improvements.
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Critically evaluate and improve this summary: {draft}"}]
        )
        improved = response["choices"][0]["message"]["content"].strip()
        print("Improved Summary:")
        print(improved)
        return improved


def kickoff():
    evaluatorOptimizer = EvaluatorOptimizerFlow()
    evaluatorOptimizer.kickoff()


def plot():
    evaluatorOptimizer = EvaluatorOptimizerFlow()
    evaluatorOptimizer.plot()


if __name__ == "__main__":
    kickoff()
