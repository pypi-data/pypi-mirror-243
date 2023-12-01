from datetime import datetime

dict_model_typ = {
    'binary_classification' : 'supervised',
    'multi_class_classification' : 'supervised',
    'multi_label_classification' : 'supervised',
    'regression' : 'supervised',
    'time_series' : 'supervised',
    'clustering' : 'unsupervised',
    'assossiation' : 'unsupervised',
    'optimization' : 'unsupervised',
}

lst_ord_col_nm = [
    'SOLTN_NM', 'MDL_NM', 'ALGRTHM_TYP', 
    'MDL_TYP', 'KPI_NM', 'KPI_QTY', 
    'KPI_ARG', 'TRNNG_TS',
    'TEC_CRE_DT', 'TEC_UPT_DT', 'TEC_USER_UPT',
]
    
write_disposition = 'WRITE_APPEND'

schemaExport = [
    {"name":"SOLTN_NM", "type":"STRING", "description":"SOLUTION NAME"},
    {"name":"MDL_NM", "type":"STRING", "description":"MODEL NAME"},
    {"name":"ALGRTHM_TYP", "type":"STRING", "description":"ALGORITHM TYPE"},
    {"name":"MDL_TYP", "type":"STRING", "description":"SMODEL TYP"},
    {"name":"KPI_NM", "type":"STRING", "description":"KPI NAME"},
    {"name":"KPI_QTY", "type":"FLOAT64", "description":"KPI QUANTITY"},
    {"name":"KPI_ARG", "type":"STRING", "description":"KPI ARGUMENTS"},
    {"name":"TRNNG_TS", "type":"TIMESTAMP", "description":"TRAINING TIMESTAMP"},
    {"name":"TEC_CRE_DT", "type":"TIMESTAMP", "description":"DATE OF ROW CREATION"},
    {"name":"TEC_UPT_DT", "type":"TIMESTAMP", "description":"DATE OF ROW UPDATE"},
    {"name":"TEC_USER_UPT", "type":"STRING", "description":"USER OR PROCESS"}
]
