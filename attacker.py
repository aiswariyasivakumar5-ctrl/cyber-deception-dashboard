import random

class Attacker:
    def __init__(self):
        self.q_table = {}
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.2

    def choose_target(self, servers):
        server_ids = [s["id"] for s in servers]

        for sid in server_ids:
            self.q_table.setdefault(sid, 0)

        if random.random() < self.epsilon:
            return random.choice(server_ids)

        return max(self.q_table, key=self.q_table.get)

    def update_q(self, server_id, reward):
        old = self.q_table[server_id]
        self.q_table[server_id] = old + self.alpha * (reward - old)
