import pickle
import numpy as np
# /utils/prediction.py


def predict_body_shape(gender, chest, waist, high, hip):
    with open('bodyshape_model.pkl', 'rb') as file:
        pickle_model = pickle.load(file)
    gender_value = 0 if gender == 'Men' else 1
    # Convert chest, waist, high, and hip to float
    chest = float(chest)
    waist = float(waist)
    high = float(high)
    hip = float(hip)
    new_data = np.array([[gender_value, chest, waist, high, hip]])
    waist_hip_ratio = waist / hip
    new_data = np.append(new_data, np.array([[waist_hip_ratio]]), axis=1)
    predicted_shape = pickle_model.predict(new_data)[0]
    predicted_shape = predicted_shape.strip('[]').strip("''")
    return predicted_shape
