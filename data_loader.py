import pandas as pd
import os

def load_population_data(filepath="data/population_2025.csv"):
    """
    Loads population data from a CSV file.
    
    Args:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: DataFrame containing the population data.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    df = pd.read_csv(filepath)
    
    # Ensure correct data types
    df['Population_2025'] = pd.to_numeric(df['Population_2025'], errors='coerce')
    df['Birth_Rate'] = pd.to_numeric(df['Birth_Rate'], errors='coerce')
    df['Death_Rate'] = pd.to_numeric(df['Death_Rate'], errors='coerce')
    df['Median_Age'] = pd.to_numeric(df['Median_Age'], errors='coerce')
    
    # Drop rows with missing values
    df.dropna(inplace=True)
    
    return df

if __name__ == "__main__":
    # Test the loader
    try:
        df = load_population_data()
        print("Data loaded successfully:")
        print(df.head())
    except Exception as e:
        print(f"Error loading data: {e}")
