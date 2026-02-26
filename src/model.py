"""
Predictive Validation Module
-----------------------------
Builds and validates a Random Forest regression model to:
- Validate pricing drivers
- Extract feature importance
- Evaluate predictive accuracy

"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# Feature Importance Visualization
# ============================================================

def plot_feature_importance(feature_importance_df):

    top_features = feature_importance_df.head(10)

    plt.figure(figsize=(8,6))
    plt.barh(top_features['Feature'], top_features['Importance'])
    plt.gca().invert_yaxis()
    plt.title("Top 10 Feature Importances")
    plt.tight_layout()
    plt.savefig("outputs/feature_importance.png")
    plt.close()

# ============================================================
# Model Data Preperation
# ============================================================

def prepare_model_data(df):
    features = [

        'Total_Stops_Clean',
        'Total_Duration_minutes',
        'Airline',
        'Source',
        'Destination',
        'Dep_Time_Bucket',
        'Day_of_Journey',
        'Month_of_Journey'
    ]
    X = df[features]
    y = df['Price']

    return X, y

# ============================================================
# Model Training & Validation
# ============================================================

def run_model(df):
    print("\n === Running Predictive Validation Model ===")

    # --------------------------------------------
    # 1. Prepare Data
    # --------------------------------------------
    X, y = prepare_model_data(df)
    
    # --------------------------------------------
    # 2. Preprocessing Pipeline
    # --------------------------------------------
    categorical_cols = ['Airline', 'Source', 'Destination', 'Dep_Time_Bucket']
    numerical_cols = ['Total_Stops_Clean', 'Total_Duration_minutes', 'Day_of_Journey', 'Month_of_Journey']

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ],
        remainder='passthrough'
    )

    # --------------------------------------------
    # 3. Model Definition
    # --------------------------------------------
    model = RandomForestRegressor(
        n_estimators= 100,
        random_state= 42
    )
    
    # --------------------------------------------
    # 4. Train/Test Split
    # --------------------------------------------
    pipeline = Pipeline(
        steps= [
            ('preprocessor', preprocessor),
            ('model', model)
        ]
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size= 0.2, random_state= 42
    )
    
    # --------------------------------------------
    # 5. Model Training
    # --------------------------------------------
    pipeline.fit(X_train, y_train)

    # --------------------------------------------
    # 6. Feature Importance Extraction
    # --------------------------------------------
    model = pipeline.named_steps['model']
    preprocessor = pipeline.named_steps['preprocessor']
    encoded_cat_features = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_cols)
    all_features = list(encoded_cat_features) + numerical_cols
    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature' : all_features,
        'Importance' : importances
    }).sort_values(by='Importance', ascending=False)
    
    print("\n=== Top 15 Feature Importances ===")
    print(feature_importance_df.head(15))
    plot_feature_importance(feature_importance_df)
    print("\n=== Feature Importance Chart saved to outputs/feature_importance.png ===\n")

    # --------------------------------------------
    # 7. Model Evaluation
    # --------------------------------------------
    y_pred = pipeline.predict(X_test)
    print(f"=== R2 Score: {round(r2_score(y_test,y_pred),3)} ===\n")
    print(f"=== MAE: {round(mean_absolute_error(y_test,y_pred), 2)} ===\n")

    return pipeline





