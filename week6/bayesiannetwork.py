import pandas as pd

# Data
data = pd.DataFrame({
    'Rain': ['No', 'No', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'No'],
    'TrafficJam': ['Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'No', 'No'],
    'ArriveLate': ['Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'Yes', 'No']
})

# Step 1: Probability of Rain
p_rain = data['Rain'].value_counts(normalize=True)

# Step 2: P(TrafficJam | Rain)
p_traffic_given_rain = pd.crosstab(
    data['TrafficJam'],
    data['Rain'],
    normalize='columns'
)

# Step 3: P(ArriveLate | TrafficJam)
p_late_given_traffic = pd.crosstab(
    data['ArriveLate'],
    data['TrafficJam'],
    normalize='columns'
)

print("P(Rain):\n", p_rain)
print("\nP(TrafficJam | Rain):\n", p_traffic_given_rain)
print("\nP(ArriveLate | TrafficJam):\n", p_late_given_traffic)

# Inference: P(ArriveLate | Rain = Yes)

# Using law of total probability:
# P(Late | Rain=Yes) = sum over TrafficJam

p_yes = (
    p_traffic_given_rain['Yes']['Yes'] * p_late_given_traffic['Yes']['Yes'] +
    p_traffic_given_rain['No']['Yes'] * p_late_given_traffic['Yes']['No']
)

p_no = 1 - p_yes

print("\nP(ArriveLate | Rain=Yes):")
print("Yes:", round(p_yes, 3))
print("No :", round(p_no, 3))
