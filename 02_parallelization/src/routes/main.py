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

class ParallelFlow(Flow):
    model = model_name

    @start()
    def generate_variant_1(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Generate a creative blog topic variant #1."}]
        )
        variant = response["choices"][0]["message"]["content"].strip()
        print(f"Variant 1: {variant}")
        return variant

    @start()
    def generate_variant_2(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Generate a creative blog topic variant #2."}]
        )
        variant = response["choices"][0]["message"]["content"].strip()
        print(f"Variant 2: {variant}")
        return variant

    @listen(or_(generate_variant_1, generate_variant_2))
    def aggregate_variants(self, variant):
        # For simplicity, print the first variant received.
        print("Aggregated Variant:")
        print(variant)
        return variant


def kickoff():
    parallel_flow = ParallelFlow()
    parallel_flow.kickoff()


def plot():
    parallel_flow = ParallelFlow()
    parallel_flow.plot()


if __name__ == "__main__":
    kickoff()
