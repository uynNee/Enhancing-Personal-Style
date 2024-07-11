import pickle
import numpy as np


def predict_body_shape(gender, chest, waist, high, hip):
    with open('bodyshape_model.pkl', 'rb') as file:
        pickle_model = pickle.load(file)
    gender_value = 0 if gender == 'Men' else 1
    new_data = np.array([[gender_value, chest, waist, high, hip]])
    waist_hip_ratio = waist / hip
    # Correctly format waist_hip_ratio as a 2D array before appending
    new_data = np.append(new_data, np.array([[waist_hip_ratio]]), axis=1)
    predicted_shape = pickle_model.predict(new_data)[0]
    print(predicted_shape)
    predicted_shape = predicted_shape.strip('[]').strip("''")
    return predicted_shape
