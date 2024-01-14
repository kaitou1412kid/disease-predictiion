import os
import pandas as pd
import pickle
from pathlib import Path
import numpy as np
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
# from django.conf import settings
# settings.configure()
# BASE_DIR = settings.BASE_DIR
# from disease_prediction.settings import BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent
dataset_folder = os.path.join(BASE_DIR,'dataset')
disease_dataset_path = os.path.join(dataset_folder, 'data_dict.pkl')
final_svm_model = SVC()
final_nb_model = GaussianNB()
final_rf_model = RandomForestClassifier(random_state=18)
data_dict = pickle.load(open(disease_dataset_path,'rb'))
def predict_disease(symptoms):
    symptoms = symptoms.split(',')
    #creating input data for models
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in symptoms:
        index = data_dict["symptom_index"][symptom]
        input_data[index] = 1
    
    # reshaping the input data and converting it
	# into suitable format for model predictions
	
    input_data = np.array(input_data).reshape(1,-1)
	
	# generating individual outputs
    rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
    nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
    svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[0]]
	
	# making final prediction by taking mode of all predictions
    final_prediction = mode([rf_prediction, nb_prediction, svm_prediction])
    predictions = {
		"rf_model_prediction": rf_prediction,
		"naive_bayes_prediction": nb_prediction,
		"svm_model_prediction": svm_prediction,
		"final_prediction":final_prediction
	}
    return predictions

prediction = predict_disease("Skin Rash,Nodal Skin Eruptions,Continuous Sneezing")
print(prediction)
    