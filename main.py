from env import CyberEnvironment
from attacker import Attacker
from defender import Defender
from metrics import Metrics

env = CyberEnvironment(num_real=3, num_honeypots=1)
attacker = Attacker()
defender = Defender()
metrics = Metrics()

EPISODES = 80

for episode in range(EPISODES):
    env.reset()

    state = defender.get_state(env)
    action = defender.choose_action(state)

    if action == 1:
        defender.deploy_honeypot(env)

    target = attacker.choose_target(env.servers)
    reward, outcome = env.attack(target)

    next_state = defender.get_state(env)
    defender.update_q(state, action, reward, next_state)
    attacker.update_q(target, reward)

    metrics.log(episode + 1, outcome, reward)

    print(f"Episode {episode+1} | Outcome: {outcome} | Reward: {reward}")

# Plot results
metrics.log(episode+1, outcome, reward)

