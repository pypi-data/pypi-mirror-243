# Artificial Intelligence Management

> This is a toolbox to help AI & ML teams to have a better management of their metrics and processes.

Our desire is to enable the company with data related to AI solution, in a easy way to read and use. Some new goals are going to be included later

[Confluence Documentation Link]()

[Tangram Link](https://tangram.adeo.com/products/1d6f6abb-63ba-4663-bd1e-18007bffde36/overview)

## Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Installation/Usage](#Installation/Usage)
- [Contact](#Contact)

## Project Structure

Describe the structure of the `project` folder, including the organization of modules, directories, and any important files.

```
ai_management/
├── __init__.py
├── model_evaluation.py
├── constants.py
├── examples/
│ ├── usage_examples.ipynb
```

Explain the purpose of each module or significant files.

## ModelEvaluation

Historize the technical model evaluation results at a Google Big Query table at a Google Cloud Platform project.

## Installation
```python
pip install ai-management
```

## Usage

### Binary classification
```python
y_true = [1, 0, 0, 1, 1]
y_pred = [1, 0, 0, 0, 1]

y_test_a_lst = y_true
y_pred_a_lst = y_pred

y_test_a_arr = np.array(y_true)
y_pred_a_arr = np.array(y_pred)
```

### Multi class classification
```python
y_true = [0, 1, 2, 1, 2]
y_pred = [[0.9, 0.1, 0.0], [0.3, 0.2, 0.5], [0.2, 0.3, 0.5], [0.1, 0.8, 0.1], [0.1, 0.2, 0.7]]

y_test_b_lst = y_true
y_pred_b_lst = y_pred

y_test_b_arr = np.array(y_true)
y_pred_b_arr = np.array(y_pred)
```

### Multi label classification
```python
y_test = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
y_pred = [[0, 1, 2], [3, 4, 5], [6, 7, 9]]

y_test_c_lst = y_test
y_pred_c_lst = y_pred

y_test_c_arr = np.array(y_true)
y_pred_c_arr = np.array(y_pred)
```



### Solution Evaluation
```python
import ai_management as aim 
me = aim.ModelEvaluation(
    project_id='project',
    destination='project.dataset.table'
)
me.historize_model_evaluation(
    soltn_nm = 'Solution X', 
    lst_mdls = [
        {
            'mdl_nm' : 'Model A',
            'algrthm_typ' : 'binary_classification',
            'data' : [y_test_a_lst, y_pred_a_lst]}, 
        {
            'mdl_nm' : 'Model B',
            'algrthm_typ' : 'multi_class_classification',
            'data' : [y_test_b_lst, y_pred_b_lst]},
        {
            'mdl_nm' : 'Model C',
            'algrthm_typ' : 'multi_label_classification',
            'data' : [y_test_c_lst, y_pred_c_lst]},
    ]
)
```


## Contact

* Leroy Merlin Brazil AI scientists and developers: chapter_inteligencia_artificia@leroymerlin.com.br

