import os 
import sys 
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import ModelTraninerConfig
from NetworkSecurity.utils.main_utils.utils import save_object,load_object
from NetworkSecurity.utils.main_utils.utils import load_numpy_array_data,evaluate_models
from NetworkSecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel
from NetworkSecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from NetworkSecurity.entity.config_entity import ModelTraninerConfig
import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
import dagshub

dagshub.init(repo_owner='Immortal-Pi', repo_name='NetworkSecurity', mlflow=True)

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTraninerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact 

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
    def track_mlflow(self,best_model,classificationmetric):
        with mlflow.start_run():
            f1_score=classificationmetric.f1_score
            precision_score=classificationmetric.precision_score
            recall_score=classificationmetric.recall_score 
            # mlflow.log_params()
            mlflow.log_metrics(
                {'f1_score':f1_score,
                    'precision':precision_score,
                    'recall':recall_score
                 }
            )
            mlflow.sklearn.log_model(best_model,'model')

    
    def train_model(self,xtrain,ytrain,xtest,ytest):
        models={
            'Random Forest':RandomForestClassifier(verbose=1),
            'Decision Tree':DecisionTreeClassifier(),
            'Gradient Boosting':GradientBoostingClassifier(verbose=1),
            'Logistic Regression':LogisticRegression(verbose=1),
            'AdaBoost':AdaBoostClassifier(),
        } 

        # hyper parameter tuning 
        params={
            'Decision Tree':{
                'criterion':['gini','entropy','log_loss'],
                'splitter':['best','random'],
                'max_features':['sqrt','log2'],
            },
            'Random Forest':{
                'max_features':['sqrt','log2'],
                'criterion':['gini','entropy','log_loss'],
                # 'n_estimators':[8,16,32,64,128,256],
                'n_estimators':[8,16,32,128,256]
            },
            'Gradient Boosting':{
                'loss':['log_loss','exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                'criterion':['squared_error','friedman_mse'],
                'max_features':['auto','sqrt','log2'],
                'n_estimators':[8,16,32,64,128,256]
            },
            'Logistic Regression':{},
            'AdaBoost':{
                'learning_rate':[.1,.01,0.001],
                # 'learning_rate':[.1,.01,0.5,0.001],
                'n_estimators':[8,16,32,64,128,256]
            }
        }
        model_report:dict=evaluate_models(xtrain,ytrain,xtest,ytest,models,params)

        # get the best model score from dict
        best_model_score=max(sorted(model_report.values()))
        best_model_name=list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model=models[best_model_name]
        y_train_pred=best_model.predict(xtrain)

        classification_train_metric=get_classification_score(y_true=ytrain,y_pred=y_train_pred)
    
        y_test_pred=best_model.predict(xtest)
        classification_test_metric=get_classification_score(y_true=ytest,y_pred=y_test_pred)
        
        # function to track the mlflow 
        self.track_mlflow(best_model,classificationmetric=classification_train_metric)


        # load the pickle file 
        preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        networkmodel=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=networkmodel)

        # push the final model into final_models folder
        save_object('final_models/model.pkl',best_model)

        ## Model Trainer Aritifact 
        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_artifact=classification_test_metric
                             )
        logging.info(f'Model trainer artifact: {model_trainer_artifact}')
        return model_trainer_artifact

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            # loading training array and testing array
            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)
            xtrain,ytrain,xtest,ytest=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1],
            )
            model_trainer_artifact=self.train_model(xtrain,ytrain,xtest,ytest)
            return model_trainer_artifact


        except Exception as e:
            raise NetworkSecurityException(e,sys)
