import pickle
from import_data import process_input
import numpy as np
import pandas as pd

print('Load Model ..')
model_path = 'classifier.pkl'
classifier = pickle.load(open(model_path, 'rb'))

def predict(filename, path='') -> pd.DataFrame:
    """
    Predicts whether a tweet or set of tweets is News or Not
    :return: a dataframe
    """
    input_params, main_dataframe = process_input(path, filename)
    print('Predicting...')
    predictions = classifier.predict(input_params)
    main_dataframe['predictions'] = predictions.tolist()
    print('Done')
    
    return main_dataframe


result = predict('tweet.csv')
result.to_csv('predictions.csv', index=False) 