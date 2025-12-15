import json

LOG_FILE = "access.log"
OUTPUT_FILE = "metrics.json"

metrics = {
    "events": []
}

with open(LOG_FILE, "r") as file:
    for line in file:
        if "honeypot" in line:
            outcome = "TRAPPED"
            reward = 5
        elif "403" in line:
            outcome = "BLOCKED"
            reward = 2
        else:
            outcome = "ESCAPED"
            reward = -1

        metrics["events"].append({
            "log": line.strip(),
            "outcome": outcome,
            "reward": reward
        })

with open(OUTPUT_FILE, "w") as f:
    json.dump(metrics, f, indent=4)

print("✅ metrics.json generated successfully")
