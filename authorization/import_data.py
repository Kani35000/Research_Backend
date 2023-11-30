import pathlib
import pandas as pd
import numpy as np
import .text_preproc as tp


def csv_to_pandas(file_name, path='') -> pd.DataFrame:
    """
    :param path: file path
    :param file_name: file name complete with extension
    :return: dataframe of all existing columns
    """
    assert str(pathlib.Path(file_name).suffix) == '.csv', 'A csv file is expected'
    
    #csv file must contain a column called text
    data = pd.read_csv(path+file_name, dtype={'text':str})
    assert len(data.index) != 0, 'You have passed in an empty file'
    print(f'Received data of {data.shape[0]} rows and {data.shape[1]} columns')

    data.dropna(subset=['text'], inplace=True)
    data.drop_duplicates(inplace=True)
    print(f'After dropping duplicates and empty tweets, we are left with {data.shape[0]} rows and {data.shape[1]} columns')
    print('')
    return data


def text_case(data: pd.DataFrame) -> pd.DataFrame:
    """
    asserts that required column exists in data
    :param data: imported data
    :return: dataframe of 1 column
    """
    print('Pre-processing ...')
    df = data.copy() 
    df = df[['text']]
    df['text'] = df['text'].str.lower()

    return df


def process_input(file_name, path='') -> pd.DataFrame:
    """
    :param path: file path
    :param file_name: file name complete with extension
    :return: 
    """
    data = csv_to_pandas(path, file_name)
    df = data.copy()

    df['text'] = df['text'].map(tp.mention_url_notalpha)
    df = text_case(df)
    df['text'] = df['text'].apply(tp.tokenize_lemma_stopwords)
    x = df['text']
    return x, data
    