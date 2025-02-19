import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
data = pd.read_csv("/home/xlordplay/alfa_test_tasks/alfa_test/data/Input data/abt_em.tab",sep="\t")

categorical_feature = data.select_dtypes(include="object")
binary_arrear_indicator = {"N" : 0 , "Y" : 1}
gender_indicator = {"M" : 0 , "F" : 1, "U" : 2}
chq_acc_ind_indicator = {"N" : 0 ,"Y" : 1}
title_indicator = {"MR": 0 , "MRS" : 1 , "UNKNOWN" : 2, "MS": 3, "AC" : 4 , "MASTER" : 5, "REL" : 6,"MISS": 7 }

indicator_dict = {
    "arrear_ind": binary_arrear_indicator,
    "chq_acc_ind": chq_acc_ind_indicator,
    "gender": gender_indicator,
    "title": title_indicator,
}

# Замена значений в DataFrame
for col in categorical_feature:
    if col in data.columns:  # Проверяем, существует ли столбец
        data[col] = data[col].map(indicator_dict[col])
data.head()