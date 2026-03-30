# -----------------------------------------
# 🏥 AI-Based Medical Diagnosis using Bayesian Network (Naive Bayes)
# -----------------------------------------

import pandas as pd

# -------------------------------
# 📊 Step 1: Dataset
# -------------------------------
data = pd.DataFrame({
    'Fever': ['Yes','No','Yes','Yes','No','Yes','No','Yes'],
    'Cough': ['Yes','No','Yes','No','Yes','Yes','No','Yes'],
    'Fatigue': ['Yes','No','Yes','Yes','No','Yes','No','Yes'],
    'Test': ['Positive','Negative','Positive','Positive','Negative','Positive','Negative','Positive'],
    'Disease': ['Yes','No','Yes','Yes','No','Yes','No','Yes']
})

# -------------------------------
# 📈 Step 2: Probabilities
# -------------------------------

# Prior Probability
P_disease = data['Disease'].value_counts(normalize=True)

# Conditional Probabilities
P_fever = pd.crosstab(data['Fever'], data['Disease'], normalize='columns')
P_cough = pd.crosstab(data['Cough'], data['Disease'], normalize='columns')
P_fatigue = pd.crosstab(data['Fatigue'], data['Disease'], normalize='columns')
P_test = pd.crosstab(data['Test'], data['Disease'], normalize='columns')

# -------------------------------
# 🔍 Step 3: Prediction Function
# -------------------------------

def predict_disease(fever=None, cough=None, fatigue=None, test=None):
    
    # Start with prior probabilities
    p_yes = P_disease['Yes']
    p_no = P_disease['No']
    
    # Multiply only available evidence (handles missing data)
    if fever:
        p_yes *= P_fever.loc[fever, 'Yes']
        p_no *= P_fever.loc[fever, 'No']
        
    if cough:
        p_yes *= P_cough.loc[cough, 'Yes']
        p_no *= P_cough.loc[cough, 'No']
        
    if fatigue:
        p_yes *= P_fatigue.loc[fatigue, 'Yes']
        p_no *= P_fatigue.loc[fatigue, 'No']
        
    if test:
        p_yes *= P_test.loc[test, 'Yes']
        p_no *= P_test.loc[test, 'No']
    
    # Normalize
    total = p_yes + p_no
    p_yes /= total
    p_no /= total
    
    return {
        "Disease=Yes": round(p_yes, 3),
        "Disease=No": round(p_no, 3)
    }

# -------------------------------
# 🧪 Step 4: Test Cases
# -------------------------------

print("=== Full Evidence ===")
print(predict_disease('Yes','Yes','Yes','Positive'))

print("\n=== Missing Test Result ===")
print(predict_disease('Yes','Yes','Yes'))

print("\n=== Only Fever Known ===")
print(predict_disease(fever='Yes'))

# -------------------------------
# 📊 Step 5: Show Learned Probabilities
# -------------------------------

print("\n--- Learned Probabilities ---")
print("\nP(Disease):\n", P_disease)
print("\nP(Fever | Disease):\n", P_fever)
print("\nP(Cough | Disease):\n", P_cough)
print("\nP(Fatigue | Disease):\n", P_fatigue)
print("\nP(Test | Disease):\n", P_test)
