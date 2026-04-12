import numpy as np
def make_prediction(model, input_df):

    probability = model.predict_proba(input_df)[0][0]
    prediction = int(probability > 0.5)

    if probability >=0.7:
        risk = "High Risk"
    elif probability >=0.4 :
        risk = "Medium Risk"
    else:
        risk = "Low Risk"

    return prediction, float(probability), risk
