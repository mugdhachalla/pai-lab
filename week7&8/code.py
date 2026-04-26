import numpy as np

class GridWorldMDP:
    def __init__(self, size, goal, trap):
        self.size = size
        self.goal = goal
        self.trap = trap
        self.state_space = [(i, j) for i in range(size) for j in range(size)]
        self.action_space = ["UP", "DOWN", "LEFT", "RIGHT"]
        self.rewards = self.build_rewards()
        self.transitions = self.build_transitions()

    def build_transitions(self):
        transitions = {}
        for state in self.state_space:
            transitions[state] = {}
            for action in self.action_space:
                transitions[state][action] = self.calculate_transition(state, action)
        return transitions

    def calculate_transition(self, state, action):
        i, j = state
        if action == "UP":
            return max(i - 1, 0), j
        elif action == "DOWN":
            return min(i + 1, self.size - 1), j
        elif action == "LEFT":
            return i, max(j - 1, 0)
        elif action == "RIGHT":
            return i, min(j + 1, self.size - 1)
        return state

    def valid_states(self, state):
        i, j = state
        if (i, j) == self.goal or (i, j) == self.trap:
            return [(i, j)]
        return [(i, j)]

    def build_rewards(self):
        rewards = {}
        for state in self.state_space:
            rewards[state] = -1.0
        rewards[self.goal] = 10.0
        rewards[self.trap] = -10.0
        return rewards

def value_iteration(mdp, gamma=0.9, epsilon=0.01):
    state_values = {state: 0 for state in mdp.state_space}
    while True:
        delta = 0
        for state in mdp.state_space:
            v = state_values[state]
            if state == mdp.goal or state == mdp.trap:
                continue
            v_new = max(
                mdp.rewards[mdp.transitions[state][action]] +
                gamma * state_values[mdp.transitions[state][action]]
                for action in mdp.action_space
            )
            state_values[state] = v_new
            delta = max(delta, abs(v - v_new))
        if delta < epsilon:
            break
    return state_values

def policy_iteration(mdp, gamma=0.9):
    policy = {state: np.random.choice(mdp.action_space)
              for state in mdp.state_space
              if state != mdp.goal and state != mdp.trap}

    state_values = {state: 0 for state in mdp.state_space}

    while True:
        # Policy Evaluation
        while True:
            delta = 0
            for state in mdp.state_space:
                v = state_values[state]
                if state == mdp.goal or state == mdp.trap:
                    continue
                action = policy[state]
                v_new = mdp.rewards[mdp.transitions[state][action]] + \
                        gamma * state_values[mdp.transitions[state][action]]
                state_values[state] = v_new
                delta = max(delta, abs(v - v_new))
            if delta < 0.01:
                break

        # Policy Improvement
        policy_stable = True
        for state in mdp.state_space:
            if state == mdp.goal or state == mdp.trap:
                continue
            old_action = policy[state]

            best_action = max(
                mdp.action_space,
                key=lambda action:
                mdp.rewards[mdp.transitions[state][action]] +
                gamma * state_values[mdp.transitions[state][action]]
            )

            policy[state] = best_action
            if old_action != best_action:
                policy_stable = False

        if policy_stable:
            break

    return policy, state_values


# Example
size = 3
goal = (2, 2)
trap = (1, 1)

mdp = GridWorldMDP(size, goal, trap)

# Value Iteration
value_iteration_result = value_iteration(mdp)
print("Value Iteration Results:")
for state, value in value_iteration_result.items():
    print(f"{state}: {value}")

# Policy Iteration
policy, state_values = policy_iteration(mdp)
print("\nPolicy Iteration Results:")
for state in policy:
    print(f"{state}: {policy[state]}")
