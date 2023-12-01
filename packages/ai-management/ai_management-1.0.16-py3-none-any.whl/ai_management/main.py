import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from datetime import datetime
import time
import sys
import google.auth
from google.cloud import bigquery
from google.colab import auth
import ai_management.constants as c

class ModelEvaluation:
    """
    List of useble 
        - Methods:
            - historize_model_evaluation()
        - Attributes:
            - None
    """
    def __init__(self):
        pass

    def define_final_kpi_list(self, lst, lst_kpis):
        """
         Defines the final list of KPIs.

         Args:
             lst : list 
                List of KPIs to be added.
             lst_kpis : list
                List of existing KPIs.

         Returns:
             lst_kpis : list
                List of existing KPIs (updated).
         """
        if len(lst_kpis) > 0:
            for kpi in lst:
                lst_kpis.append(kpi)
        else:
            lst_kpis = lst.copy()
        return lst_kpis

    def binary_classification_evaluation(self, lst_kpis, y_test, y_pred):
        """
        Evaluate a binary classification model.

        Args:
            lst_kpis : list
                List of existing KPIs.
            y_test : ndarray
                True values.
            y_pred : ndarray
                Predicted values.

        Returns:
            lst_kpis : list
                List of existing KPIs (updated).
        """
        if str(type(y_test))=="<class 'numpy.ndarray'>":
            y_test = y_test.tolist()
        if str(type(y_pred))=="<class 'numpy.ndarray'>":
            y_pred = y_pred.tolist()
            
        fpr, tpr, _ = roc_curve(y_test, y_pred)
        lst = [
            ['accuracy', accuracy_score(y_test, y_pred)],
            ['precision', precision_score(y_test, y_pred)],
            ['recall', recall_score(y_test, y_pred)],
            ['f1', f1_score(y_test, y_pred)],
            ['auc', auc(fpr, tpr)],
            ['roc_auc', roc_auc_score(y_test, y_pred)],
        ]
        lst_kpis = self.define_final_kpi_list(lst, lst_kpis)
        return lst_kpis
    
    def multiclass_classification_evaluation(self, lst_kpis, y_test, y_pred):
        """
        Evaluate a multiclass classification model.

        Args:
            lst_kpis : list
                List of existing KPIs.
            y_test : ndarray
                True values.
            y_pred : ndarray
                Predicted values.

        Returns:
            lst_kpis : list
                List of existing KPIs (updated).
        """
        
        if str(type(y_test))=="<class 'numpy.ndarray'>":
            y_test = y_test.tolist()
        if str(type(y_pred))=="<class 'numpy.ndarray'>":
            y_pred = y_pred.tolist()
        
        y_pred_max_prob = [line.index(max(line)) for line in y_pred]
        # calculate no average dependant metrics
        lst = [['accuracy', accuracy_score(y_test, y_pred_max_prob)]]
        
#         # The reason is that OvR will binarize the problem. 
#         # For one of the combinations, you will therefore end up with only a single class in y_true 
#         # and the ROC AUC is not defined for this case. So here we can't use 'ovr'.
#         lst_multi_class = ['ovo']
#         for multi_class in lst_multi_class:
#             lst.append([f'roc_auc - {multi_class}', roc_auc_score(y_test, y_pred, multi_class=multi_class)])
        
        lst_kpis = self.define_final_kpi_list(lst, lst_kpis)
        
        # calculate average dependant metrics
        lst_avg = ['micro', 'macro', 'weighted']
        for average in lst_avg:            
            lst = [
                [f'precision - {average}', precision_score(y_test, y_pred_max_prob, average=average)],
                [f'recall - {average}', recall_score(y_test, y_pred_max_prob, average=average)],
                [f'f1 - {average}', f1_score(y_test, y_pred_max_prob, average=average)],
            ]
            
            lst_kpis = self.define_final_kpi_list(lst, lst_kpis)
        return lst_kpis
    
    def multilabel_classification_evaluation(self, lst_kpis, y_test, y_pred):
        """
        Evaluate a multilabel classification model.

        Args:
            lst_kpis : list
                List of existing KPIs.
            y_test : ndarray
                True values.
            y_pred : ndarray
                Predicted values.

        Returns:
            lst_kpis : list
                List of existing KPIs (updated).
        """
        
        if str(type(y_test))=="<class 'numpy.ndarray'>":
            y_test = y_test.tolist()
        if str(type(y_pred))=="<class 'numpy.ndarray'>":
            y_pred = y_pred.tolist()
        lst_flat = []
        for lst in [y_test, y_pred]:
            for sub_lst in lst:
                for ele in sub_lst:
                    lst_flat.append(ele)
        lst_flat = list(dict.fromkeys(lst_flat))
        multilabel_binarizer = MultiLabelBinarizer(classes=lst_flat)
        multilabel_binarizer.fit(lst_flat)
        y_test = multilabel_binarizer.transform(y_test)
        y_pred = multilabel_binarizer.transform(y_pred)
        
        # calculate no average dependant metrics
        lst_avg = ['micro', 'macro', 'weighted']
        
        for average in lst_avg:
            lst = [
                [f'precision - {average}', precision_score(y_test, y_pred, average=average)],
                [f'recall - {average}', recall_score(y_test, y_pred, average=average)],
                [f'f1 - {average}', f1_score(y_test, y_pred, average=average)],
            ]
            lst_kpis = self.define_final_kpi_list(lst, lst_kpis)
        return lst_kpis

    def regression_evaluation(self, lst_kpis, y_test, y_pred):
        """
        Evaluate a regression model.

        Args:
            lst_kpis : list
                List of existing KPIs.
            y_test : ndarray
                True values.
            y_pred : ndarray
                Predicted values.

        Returns:
            lst_kpis : list
                List of existing KPIs (updated).
        """
        small_qty = 1/10**6
        lst = [
            ['r2', r2_score(y_test, y_pred)],
            ['mse', mean_squared_error(y_test, y_pred)],
            ['rmse', np.sqrt(mean_squared_error(y_test, y_pred))],
            ['mae', mean_absolute_error(y_test, y_pred)],
            ['efficiency_score', 1 - (mean_absolute_error(y_test, y_pred) / mean_squared_error(y_test, y_pred))],
            ['mean_error_ratio', mean_absolute_error(y_test, y_pred) / np.mean(y_test + small_qty)],
            ['mape', mean_absolute_percentage_error(y_test + small_qty, y_pred + small_qty)],
        ]
        lst_kpis = self.define_final_kpi_list(lst, lst_kpis)
        return lst_kpis

    def time_series_evaluation(self, lst_kpis, y_test, y_pred):
        """
        Evaluate a time series model.

        Args:
            lst_kpis : list
                List of existing KPIs.
            y_test : ndarray
                True values.
            y_pred : ndarray
                Predicted values.

        Returns:
            lst_kpis : list
                List of existing KPIs (updated).
        """
        lst = self.regression_evaluation(lst_kpis, y_test, y_pred)
        lst_kpis = self.define_final_kpi_list(lst, lst_kpis)
        return lst_kpis

    def model_evaluation(self, lst_mdls, soltn_nm):
        """
        Evaluate a model.

        Args:
            lst_mdls (list): List of models to be evaluated.
            soltn_nm (str): Solution name.

        Returns:
            df : pd.DataFrame
                DataFrame with the evaluation results.
        """
        df = pd.DataFrame()
        for mdl in lst_mdls:
            lst_kpis = []
            mdl_nm = mdl['mdl_nm']
            algorithm_type = mdl['algrthm_typ']
            y_test, y_pred = mdl['data']

            model_type = c.dict_model_typ[algorithm_type]

            if model_type == 'supervised':
                if algorithm_type == 'binary_classification':
                    lst_kpis = self.binary_classification_evaluation(lst_kpis, y_test, y_pred)
                if algorithm_type == 'multi_class_classification':
                    lst_kpis = self.multiclass_classification_evaluation(lst_kpis, y_test, y_pred)
                if algorithm_type == 'multi_label_classification':
                    lst_kpis = self.multilabel_classification_evaluation(lst_kpis, y_test, y_pred)
                elif algorithm_type == 'regression':
                    lst_kpis = self.regression_evaluation(lst_kpis, y_test, y_pred)
                elif algorithm_type == 'time_series':
                    pass
            elif model_type == 'unsupervised':
                if algorithm_type == 'clustering':
                    pass
                elif algorithm_type == 'assossiation':
                    pass
                elif algorithm_type == 'optimization':
                    pass
            df_aux = pd.DataFrame(lst_kpis, columns=['KPI_NM', 'KPI_QTY'])
            df_aux['SOLTN_NM'] = soltn_nm
            df_aux['MDL_NM'] = mdl_nm
            df_aux['ALGRTHM_TYP'] = algorithm_type
            df_aux['MDL_TYP'] = model_type
            df_aux['KPI_ARG'] = None
            df_aux['TRNNG_TS'] = datetime.now()
            df_aux['TEC_CRE_DT'] = datetime.now()
            df_aux['TEC_UPT_DT'] = datetime.now()
            df_aux['TEC_USER_UPT'] = f'DAG_{soltn_nm}'
            df_aux = df_aux[c.lst_ord_col_nm]
            if len(df):
                df = pd.concat([df, df_aux])
            else:
                df = df_aux.copy()
        return df

    def historize_model_evaluation(
        self, soltn_nm, lst_mdls, project_id, destination, credentials=None):
        """
        Historize the technical model evaluation results.

        Args:
            soltn_nm : str
                Solution name.
            lst_mdls : list
                List of models to be evaluated.
                    Follows this pattern:
                        [
                            {
                                'mdl_nm' : 'Model A',
                                'algrthm_typ' : 'binary_classification',
                                'data' : [y_test, y_pred]
                            },
                        ]
                Where 
                    algrthm_typ : string
                        Select one of ['binary_classification', 'multi_class_classification', 'multi_label_classification', 'regression', 'time_series', 'clustering', 'assossiation', 'optimization']
                    y_test : ndarray
                        True values.
                    y_pred : ndarray
                        Predicted values.
            project_id : str
                GCP project id
            destination : str
                Table desctination at format 'gcp_project.dataset.table'
            credentials : google.oauth2.service_account.Credentials
                Credentials from Google Service Account

        Returns:
            None.
        """
        df = self.model_evaluation(lst_mdls, soltn_nm)
        print(f"{time.ctime()}, Start updating {destination} on mode '{c.write_disposition}' ")
        if credentials == None:
            if 'google.colab' in sys.modules:
                auth.authenticate_user()
                print(f"{time.ctime()}, Authentication done with user at Google Colab")
            else:
                print(f"{time.ctime()}, Authentication done with Environment Variables")
            client_bq = bigquery.Client(project=project_id)
        else:
            client_bq = bigquery.Client(project=project_id, credentials=credentials)
            print(f"{time.ctime()}, Authentication done with Credentials")
        client_bq.load_table_from_dataframe(
            dataframe=df,
            destination=destination, 
            job_config=bigquery.LoadJobConfig(
                schema=c.schemaExport,      
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND
            )
        ).result()
        print(f"{destination} updated")
