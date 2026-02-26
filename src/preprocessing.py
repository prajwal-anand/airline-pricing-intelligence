"""
Preprocessing Module
--------------------
Handles:
- Date feature engineering
- Time feature extraction
- Duration cleaning
- Stops cleaning
- Pricing benchmark features
- Time bucket creation

"""

import pandas as pd

# ============================================================
# Main Preprocessing Function
# ============================================================

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and engineers features for airline pricing analysis.
    
    Parameters:
        df (pd.DataFrame): Raw flight pricing dataset
        
    Returns:
        pd.DataFrame: Cleaned and feature-engineered dataset
    """

    df = df.copy()

    # ========================================================
    # 1. Date Features
    # ========================================================
    df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True)
    df['Day_of_Journey'] = df['Date_of_Journey'].dt.day
    df['Month_of_Journey'] = df['Date_of_Journey'].dt.month

    # ========================================================
    # 2. Departure Time Features
    # ========================================================
    df['Dep_Time'] = pd.to_datetime(df['Dep_Time'], format="%H:%M")
    df['Dep_Hour'] = df['Dep_Time'].dt.hour
    df['Dep_Minutes'] = df['Dep_Time'].dt.minute

    # ========================================================
    # 3. Arrival Time Features
    # ========================================================
    df['Arrival_Time'] = df['Arrival_Time'].str.split(' ').str[0]
    df['Arrival_Time'] = pd.to_datetime(df['Arrival_Time'], format="%H:%M")
    df['Arrival_Hour'] = df['Arrival_Time'].dt.hour
    df['Arrival_Minutes'] = df['Arrival_Time'].dt.minute

    # ========================================================
    # 4. Duration Features
    # ========================================================
    duration = df['Duration'].str.extract(r'^(?:(\d+)h)?\s*(?:(\d+)m)?$')
    df['Duration_Hour'] = pd.to_numeric(duration[0]).fillna(0).astype(int)
    df['Duration_Minute'] = pd.to_numeric(duration[1]).fillna(0).astype(int)
    df['Total_Duration_minutes'] = (
        df['Duration_Hour'] * 60 + df['Duration_Minute']
    )

    # ========================================================
    # 5. Stops Cleaning
    # ========================================================
    df['Total_Stops'] = df['Total_Stops'].replace('non-stop', '0 stops')
    df['Total_Stops_Clean'] = (
        df['Total_Stops']
        .str.extract(r'(\d+)')
        .astype(float)
    )

    df = df.dropna(subset=['Total_Stops_Clean', 'Route'])
    df['Total_Stops_Clean'] = df['Total_Stops_Clean'].astype(int)

    # ========================================================
    # 6. Pricing Benchmark Features
    # ========================================================
    df['Airline_Avg_Price'] = df.groupby('Airline')['Price'].transform('mean')
    df['Route_Avg_Price'] = df.groupby('Route')['Price'].transform('mean')
    df['Route_Price_Std'] = df.groupby('Route')['Price'].transform('std')

    # ========================================================
    # 7. Departure Time Buckets
    # ========================================================
    bins = [0, 6, 12, 18, 24]
    labels = ['Early Morning', 'Morning', 'Afternoon', 'Evening']
    df['Dep_Time_Bucket'] = pd.cut(
        df['Dep_Hour'],
        bins=bins,
        labels=labels,
        right=False
    )

    return df