import pickle
import time
from copy import deepcopy
from datetime import timedelta

import numpy as np
import pandas as pd

from sam_ml.config import setup_logger

logger = setup_logger(__name__)

class Model:
    """ Model parent class """

    def __init__(self, model_object = None, model_name: str = "model", model_type: str = "Model"):
        """
        @params:
            model_object: model with 'fit', 'predict', 'set_params', and 'get_params' method (see sklearn API)
            model_name: name of the model
            model_type: kind of estimator (e.g. 'RFC' for RandomForestClassifier)
        """
        self.model = model_object
        self.model_name = model_name
        self.model_type = model_type
        self.train_score: float = None
        self.train_time: str = None
        self.feature_names: list = []

    def __repr__(self) -> str:
        return f"Model(model_object={self.model.__str__()}, model_name='{self.model_name}', model_type='{self.model_type}')"

    def train(self, x_train: pd.DataFrame, y_train: pd.Series, console_out: bool = True, **kwargs) -> tuple[float, str]:
        """
        @return:
            tuple of train score and train time
        """
        logger.debug(f"training {self.model_name} - started")

        start_time = time.time()
        self.fit(x_train, y_train)
        end_time = time.time()
        self.train_score = self.evaluate_score(x_train, y_train, **kwargs)
        self.train_time = str(timedelta(seconds=int(end_time-start_time)))

        if console_out:
            print(f"Train score: {self.train_score} - Train time: {self.train_time}")
            
        logger.debug(f"training {self.model_name} - finished")

        return self.train_score, self.train_time
    
    def train_warm_start(self, x_train: pd.DataFrame, y_train: pd.Series, console_out: bool = True, **kwargs) -> tuple[float, str]:
        """
        @return:
            tuple of train score and train time
        """
        logger.debug(f"training {self.model_name} - started")

        start_time = time.time()
        self.fit_warm_start(x_train, y_train)
        end_time = time.time()
        self.train_score = self.evaluate_score(x_train, y_train, **kwargs)
        self.train_time = str(timedelta(seconds=int(end_time-start_time)))

        if console_out:
            print(f"Train score: {self.train_score} - Train time: {self.train_time}")
            
        logger.debug(f"training {self.model_name} - finished")

        return self.train_score, self.train_time

    def fit(self, x_train: pd.DataFrame, y_train: pd.Series, **kwargs):
        self.feature_names = list(x_train.columns)
        self.model.fit(x_train, y_train, **kwargs)
        return self
    
    def fit_warm_start(self, x_train: pd.DataFrame, y_train: pd.Series, **kwargs):
        self.feature_names = list(x_train.columns)
        self.model.fit(x_train, y_train, **kwargs)
        return self

    def predict(self, x_test: pd.DataFrame) -> list:
        """
        @return:
            list with predictions
        """
        return list(self.model.predict(x_test))
    
    def predict_proba(self, x_test: pd.DataFrame) -> np.ndarray:
        """
        @return:
            np.ndarray with prediction probabilities
        """
        try:
            return self.model.predict_proba(x_test)
        except:
            raise NotImplementedError(f"predict_proba for {self.model_name} is not implemented")

    def get_params(self, deep: bool = True):
        return self.model.get_params(deep)

    def set_params(self, **params):
        self.model.set_params(**params)
        return self

    def evaluate_score(self, x_test: pd.DataFrame, y_test: pd.Series, **kwargs) -> float:
        score = self.model.score(x_test, y_test)
        return score
    
    def get_deepcopy(self):
        """function to create a deepcopy of object"""
        return deepcopy(self)

    def save_model(self, path: str, only_estimator: bool = False):
        """ 
        function to pickle and save the Class object 
        
        @params:
            path: path to save the model with suffix '.pkl'
            only_estimator: if True, only the estimator of the class object will be saved
        """
        logger.debug(f"saving {self.model_name} - started")
        with open(path, "wb") as f:
            if only_estimator:
                pickle.dump(self.model, f)
            else:
                pickle.dump(self, f)
        logger.debug(f"saving {self.model_name} - finished")

    @staticmethod
    def load_model(path: str):
        """ function to load a pickled model class object """
        logger.debug("loading model - started")
        with open(path, "rb") as f:
            model = pickle.load(f)
        logger.debug("loading model - finished")
        return model
