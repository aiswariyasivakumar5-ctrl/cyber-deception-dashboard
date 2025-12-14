import random

class CyberEnvironment:
    def __init__(self, num_real=3, num_honeypots=1):
        self.num_real = num_real
        self.num_honeypots = num_honeypots
        self.reset()

    def reset(self):
        self.servers = []

        for i in range(self.num_real):
            self.servers.append({
                "id": f"real_{i}",
                "type": "real",
                "compromised": False
            })

        for i in range(self.num_honeypots):
            self.servers.append({
                "id": f"honeypot_{i}",
                "type": "honeypot",
                "compromised": False
            })

        random.shuffle(self.servers)
        return self.servers

    def attack(self, server_id):
        for s in self.servers:
            if s["id"] == server_id:
                s["compromised"] = True
                if s["type"] == "honeypot":
                    return +10, "ATTACKER TRAPPED"
                else:
                    return -10, "REAL SERVER COMPROMISED"
