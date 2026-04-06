import numpy as np

# States: Interested, Neutral, Disengaged
states = ["Interested", "Neutral", "Disengaged"]

# Observations: 0=low, 1=medium, 2=high activity
obs = [2, 2, 1, 0, 0]

# Initial probabilities
pi = np.array([0.5, 0.3, 0.2])

# Transition matrix (A)
A = np.array([
    [0.7, 0.2, 0.1],  # Interested
    [0.3, 0.4, 0.3],  # Neutral
    [0.2, 0.3, 0.5]   # Disengaged
])

# Emission matrix (B)
B = np.array([
    [0.1, 0.3, 0.6],  # Interested emits high activity more
    [0.3, 0.4, 0.3],
    [0.6, 0.3, 0.1]   # Disengaged emits low activity more
])

# Forward algorithm
T = len(obs)
N = len(states)
alpha = np.zeros((T, N))

# Step 1: Initialization
alpha[0] = pi * B[:, obs[0]]

# Step 2: Recursion
for t in range(1, T):
    for j in range(N):
        alpha[t, j] = np.sum(alpha[t-1] * A[:, j]) * B[j, obs[t]]

# Step 3: Termination
probability = np.sum(alpha[T-1])

print("Forward Probabilities:\n", alpha)
print("Total Sequence Probability:", probability)
