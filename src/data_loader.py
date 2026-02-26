"""
Predictive Validation Module
-----------------------------
Builds and validates a Random Forest regression model to:
- Validate pricing drivers
- Extract feature importance
- Evaluate predictive accuracy
"""

from src.preprocessing import preprocess_data
import pandas as pd

def load_data(file_path):
    pd.set_option("display.max_columns", None)
    df = pd.read_excel(file_path)
    print(f"\nDataset successfully loaded from {file_path}\n")
    return df

def dataset_overview(df):
    print(f"\nShape = {df.shape}\n")
    print("Key Summary Stats")
    print(df.describe())
    print(f"\nList of Columns: \n{df.columns}")
    print("\n Overview Complete.")