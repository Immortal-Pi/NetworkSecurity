import os 
import yaml 
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging 
import os, sys 
import numpy as np 
import dill 
import pickle
from sklearn.model_selection import GridSearchCV 
from sklearn.metrics import r2_score

def read_yaml_file(file_path: str)-> dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e 
    
def write_yaml_file(file_path: str, content: object, replace: bool = False)-> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def save_numpy_array_data(file_path: str, array: np.array):
    """ 
    Save numpy array data to file 
    file_path: str location of file to save 
    array: np.array data to save 
    """
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e 
    
def load_numpy_array_data(file_path: str)->np.array:
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e 


def save_object(file_path: str, obj: object)-> None:
    try:
        logging.info('Enter the save_object method of MainUtils class')
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
        logging.info('Exited the save_object method of MainUtils class')
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
    
    
def load_object(file_path: str)-> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f'the file: {file_path} is not exists')
        with open(file_path,'rb') as file_obj:
            print(file_obj)
            return pickle.load(file_obj) 
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e 
    
def evaluate_models(xtrain,ytrain,xtest,ytest,models,params):
    try:
        report={}
        for i in range(len(list(models))):
            model=list(models.values())[i]
            para=params[list(models.keys())[i]]

            gs=GridSearchCV(model,para,cv=3)
            gs.fit(xtrain,ytrain)

            model.set_params(**gs.best_params_)
            model.fit(xtrain,ytrain)
            ytrain_pred=model.predict(xtrain)
            ytest_pred=model.predict(xtest)
            train_model_score=r2_score(ytrain,ytrain_pred)
            test_model_score=r2_score(ytest,ytest_pred)
            report[list(models.keys())[i]]=test_model_score 
        return report 


    except Exception as e:
        raise NetworkSecurityException(e,sys)