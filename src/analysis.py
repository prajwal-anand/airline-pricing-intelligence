# =========================================================
# Airline Pricing Intelligence & Market Analytics Framework
# Exploratory Data Analysis Module
# =========================================================
#
# This module performs structured analytical exploration:
# 1. Pricing by Stops
# 2. Correlation Analysis
# 3. Route-Level Price Variance
# 4. Airline Pricing Strategy Analysis
#
# Output:
# - Console insights
# - Correlation heatmap saved to outputs/
# =========================================================

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# =========================================================
# Main EDA Runner
# =========================================================

def run_analysis(df: pd.DataFrame) -> None:
    """
    Execute structured exploratory analysis and generate insights.

    """

    print("\n=== [EDA] Running Analytical Insights ===")

    # Work on copy to avoid mutating original dataframe
    df_analysis = df.copy()

    # -----------------------------------------------------
    # 1. Price by Number of Stops
    # -----------------------------------------------------

    print("\n=== Price by Number of Stops ===")

    stops_analysis = (
        df_analysis.groupby('Total_Stops_Clean')['Price']
        .agg(['mean', 'median', 'count'])
        .sort_index()
        .round(2)
    )

    print(stops_analysis)

    # -----------------------------------------------------
    # 2. Correlation Analysis
    # -----------------------------------------------------

    print("\n=== Correlation Matrix ===")

    correlation = df_analysis[
        ['Price', 'Total_Duration_minutes', 'Total_Stops_Clean']
    ].corr()

    print(correlation.round(2))

    plot_heatmap(correlation)

    print("\n=== Correlation heatmap saved to outputs/correlation_map.png ===")

    # Executive Insight:
    # Total Stops shows strongest relationship with price,
    # but stops and duration are also strongly correlated,
    # suggesting route structure effects.

    # -----------------------------------------------------
    # 3. Route-Level Price Variance
    # -----------------------------------------------------

    print("\n=== Price Variance by Route (Top 10 by Std Dev) ===")

    route_stats = (
        df_analysis.groupby('Route')['Price']
        .agg(['mean', 'std', 'count'])
        .round(2)
        .sort_values('std', ascending=False)
        .head(10)
    )

    print(route_stats)

    # -----------------------------------------------------
    # 4. Airline Pricing Strategy (Within Same Route)
    # -----------------------------------------------------

    print("\n=== Airline Price Variation on Sample Route ===")

    route_example = df_analysis[df_analysis['Route'] == 'BLR → BOM → DEL']

    price_by_airline = (
        route_example.groupby('Airline')['Price']
        .agg(['mean', 'count'])
        .sort_values('mean', ascending=False)
        .round(2)
    )

    print(price_by_airline)

    # -----------------------------------------------------
    # 5. Airline Pricing Relative to Route Average
    # -----------------------------------------------------

    print("\n=== Airline Pricing Relative to Route Average ===")

    df_analysis['Price_vs_Route_Avg'] = (
        df_analysis['Price'] - df_analysis['Route_Avg_Price']
    )

    relative_pricing = (
        df_analysis.groupby('Airline')['Price_vs_Route_Avg']
        .agg(['mean', 'std', 'count'])
        .sort_values('mean', ascending=False)
        .round(2)
    )

    print(relative_pricing)

    # Executive Insight:
    # Premium airlines consistently price above route averages,
    # while low-cost carriers price below, confirming brand pricing power.

    # -----------------------------------------------------
    # 6. Percentage of Flights Priced Above Route Average
    # -----------------------------------------------------

    print("\n=== % Flights Priced Above Route Average ===")

    df_analysis['Above_Route_Avg'] = df_analysis['Price_vs_Route_Avg'] > 0

    above_avg_percentage = (
        df_analysis.groupby('Airline')['Above_Route_Avg']
        .mean()
        .sort_values(ascending=False) * 100
    ).round(2)

    print(above_avg_percentage)

    print("\n=== EDA Complete ===")


# =========================================================
# Visualization Utilities
# =========================================================

def plot_heatmap(correlation: pd.DataFrame) -> None:
    """
    Generate and save correlation heatmap.
    """

    correlation_clean = correlation.copy()

    correlation_clean.columns = [
        'Price',
        'Total Duration (Minutes)',
        'Total Stops'
    ]

    correlation_clean.index = [
        'Price',
        'Total Duration (Minutes)',
        'Total Stops'
    ]

    plt.figure(figsize=(8, 6))

    sns.heatmap(
        correlation_clean,
        annot=True,
        cmap='magma',
        fmt='.2f'
    )

    plt.title("Correlation Matrix: Price vs Duration vs Stops")
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    plt.savefig("outputs/correlation_map.png")
    plt.close()