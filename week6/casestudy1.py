import pandas as pd

# Sample dataset
data = pd.DataFrame({
    'Income': ['High', 'Low', 'Medium', 'Low', 'High', 'Medium', 'Low', 'High'],
    'Credit': ['Good', 'Bad', 'Good', 'Bad', 'Good', 'Bad', 'Bad', 'Good'],
    'Employment': ['Salaried', 'Self', 'Salaried', 'Self', 'Salaried', 'Self', 'Salaried', 'Self'],
    'Default': ['No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'No']
})

# Step 1: Prior Probabilities
P_default = data['Default'].value_counts(normalize=True)

# Step 2: Conditional Probabilities
P_income_given_default = pd.crosstab(data['Income'], data['Default'], normalize='columns')
P_credit_given_default = pd.crosstab(data['Credit'], data['Default'], normalize='columns')
P_emp_given_default = pd.crosstab(data['Employment'], data['Default'], normalize='columns')

print("P(Default):\n", P_default)
print("\nP(Income | Default):\n", P_income_given_default)
print("\nP(Credit | Default):\n", P_credit_given_default)
print("\nP(Employment | Default):\n", P_emp_given_default)

# -------------------------------
# 🔍 Inference Function (Naive Bayes)
# -------------------------------

def predict_default(income, credit, employment):
    # Likelihood for Default = Yes
    p_yes = (
        P_default['Yes'] *
        P_income_given_default.loc[income, 'Yes'] *
        P_credit_given_default.loc[credit, 'Yes'] *
        P_emp_given_default.loc[employment, 'Yes']
    )
    
    # Likelihood for Default = No
    p_no = (
        P_default['No'] *
        P_income_given_default.loc[income, 'No'] *
        P_credit_given_default.loc[credit, 'No'] *
        P_emp_given_default.loc[employment, 'No']
    )
    
    # Normalize
    total = p_yes + p_no
    p_yes /= total
    p_no /= total
    
    return {"Default=Yes": round(p_yes, 3), "Default=No": round(p_no, 3)}

# -------------------------------
# 🧪 Test Cases
# -------------------------------

print("\nPrediction 1:")
print(predict_default('Low', 'Bad', 'Self'))

print("\nPrediction 2 (Incomplete data handled manually):")
# Example: missing employment → assume equal probability
def predict_partial(income, credit):
    p_yes = (
        P_default['Yes'] *
        P_income_given_default.loc[income, 'Yes'] *
        P_credit_given_default.loc[credit, 'Yes']
    )
    
    p_no = (
        P_default['No'] *
        P_income_given_default.loc[income, 'No'] *
        P_credit_given_default.loc[credit, 'No']
    )
    
    total = p_yes + p_no
    return {"Default=Yes": round(p_yes/total, 3), "Default=No": round(p_no/total, 3)}

print(predict_partial('Low', 'Bad'))
