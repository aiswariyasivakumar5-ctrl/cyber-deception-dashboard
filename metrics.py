import json
import matplotlib.pyplot as plt

class Metrics:
    def __init__(self):
        self.data = []

    def log(self, episode, outcome, reward):
        self.data.append({
            "episode": episode,
            "outcome": outcome,
            "reward": reward
        })

        with open("metrics.json", "w") as f:
            json.dump(self.data, f)
