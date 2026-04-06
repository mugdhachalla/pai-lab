from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.inference import VariableElimination
import pandas as pd
data = pd.DataFrame(data={
    'Rain': ['No', 'No', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'No', 'Yes', 'No'],
    'Sprinkler': ['No', 'Yes', 'No', 'No', 'Yes', 'No', 'No', 'No', 'No', 'Yes'],
    'GrassWet': ['No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'Yes']
})
for col in data.columns:
    data[col] = data[col].astype('category')

model = DiscreteBayesianNetwork([('Rain', 'GrassWet'), ('Sprinkler', 'GrassWet')])
model.fit(data)
inference = VariableElimination(model)
query_result = inference.query(variables=['GrassWet'], evidence={'Rain': 'Yes'})

print("\n--- Inference Result: P(GrassWet | Rain='Yes') ---")
print(query_result)
