import pandas as pd
import os
  
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
file_path = os.path.join(root_dir, "data", "Input data", "data_prep.tab")

df = pd.read_csv(file_path, sep="\t")
df.sort_values(by=["CLIENT_ID", "SEGM_DATE"], inplace=True)


num_columns = [col for col in df.columns if col not in ["CLIENT_ID", "SEGM_DATE"]]


original_columns = df.columns.tolist()
new_columns = []

for col in original_columns:
    new_columns.append(col)
    if col in num_columns:
        df[f"{col}_1"] = df.groupby("CLIENT_ID")[col].shift(1)  # Предыдущий месяц
        df[f"{col}_2"] = df.groupby("CLIENT_ID")[col].shift(2)  # Предпредыдущий месяц
        new_columns.extend([f"{col}_1", f"{col}_2"])

df = df[new_columns]

output_file = "data/data_prep_transforme.csv"  
df.to_csv(output_file, index=False)

print(f"File saved successfully: {output_file}")