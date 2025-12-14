import random

class Defender:
    def __init__(self):
        self.q_table = {}
        self.alpha = 0.1   # learning rate
        self.gamma = 0.9   # discount factor
        self.epsilon = 0.2 # exploration rate

    def get_state(self, environment):
        real = sum(1 for s in environment.servers if s["type"] == "real")
        honeypot = sum(1 for s in environment.servers if s["type"] == "honeypot")
        return (real, honeypot)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice([0, 1])

        self.q_table.setdefault(state, {0: 0, 1: 0})
        return max(self.q_table[state], key=self.q_table[state].get)

    def deploy_honeypot(self, environment):
        environment.servers.append({
            "id": f"honeypot_dyn_{len(environment.servers)}",
            "type": "honeypot",
            "compromised": False
        })

    def update_q(self, state, action, reward, next_state):
        self.q_table.setdefault(state, {0: 0, 1: 0})
        self.q_table.setdefault(next_state, {0: 0, 1: 0})

        old = self.q_table[state][action]
        future = max(self.q_table[next_state].values())

        self.q_table[state][action] = old + self.alpha * (reward + self.gamma * future - old)
