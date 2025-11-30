import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class PopulationSimulator:
    def __init__(self, data):
        """
        Initialize the simulator with population data.
        
        Args:
            data (pd.DataFrame): DataFrame with 'Country', 'Population_2025', 'Birth_Rate', 'Death_Rate', 'Median_Age'.
        """
        self.data = data.copy()
        
    def simulate(self, start_year=2025, end_year=2125):
        """
        Simulates population growth from start_year to end_year using the Component Method.
        
        Logic:
        - Birth Rate is constant (as per user request).
        - Death Rate increases based on aging factor.
        - Aging Factor is derived from Median Age. Higher median age -> faster increase in death rate.
        
        Returns:
            pd.DataFrame: Long-format DataFrame with columns ['Country', 'Year', 'Population', 'Births', 'Deaths'].
        """
        years = range(start_year, end_year + 1)
        results = []
        
        for _, row in self.data.iterrows():
            country = row['Country']
            current_pop = row['Population_2025']
            birth_rate = row['Birth_Rate'] # per 1000
            current_death_rate = row['Death_Rate'] # per 1000
            median_age = row['Median_Age']
            
            # Aging Multiplier:
            # If median age is high (>40), death rate increases faster.
            # If median age is low (<20), death rate stays stable or increases very slowly (as population ages).
            # This is a heuristic model to satisfy the user's request.
            
            # Base aging factor: 0.5% increase in death rate per year for young countries, 
            # up to 1.5% increase per year for very old countries.
            aging_factor = 0.005 + (max(0, median_age - 20) / 1000.0)
            
            # Cap the aging factor to avoid runaway death rates
            aging_factor = min(aging_factor, 0.02) 

            for year in years:
                # Calculate vital statistics
                births = current_pop * (birth_rate / 1000.0)
                deaths = current_pop * (current_death_rate / 1000.0)
                
                # Store results
                results.append({
                    'Country': country,
                    'Year': year,
                    'Population': int(current_pop),
                    'Births': int(births),
                    'Deaths': int(deaths),
                    'Death_Rate_Actual': current_death_rate
                })
                
                # Update population for next year
                net_change = births - deaths
                current_pop += net_change
                
                # Update death rate for next year (Aging effect)
                # Death rate increases by the aging factor
                current_death_rate = current_death_rate * (1 + aging_factor)
                
                # Cap death rate at a realistic maximum (e.g., 30 per 1000, which is very high)
                current_death_rate = min(current_death_rate, 30.0)
                
        return pd.DataFrame(results)

    def predict_trend(self, country_name, simulation_df):
        """
        Fits a regression model to the simulated data for a specific country.
        """
        country_data = simulation_df[simulation_df['Country'] == country_name]
        if country_data.empty:
            return None
            
        X = country_data[['Year']].values
        y = country_data['Population'].values
        
        model = LinearRegression()
        model.fit(X, y)
        predictions = model.predict(X)
        
        return {
            'model': model,
            'predictions': predictions,
            'r2_score': model.score(X, y),
            'coefficient': model.coef_[0],
            'intercept': model.intercept_
        }

if __name__ == "__main__":
    # Test the simulator
    from data_loader import load_population_data
    
    try:
        df = load_population_data()
        sim = PopulationSimulator(df)
        results = sim.simulate(2025, 2030)
        print("Simulation results sample:")
        print(results[results['Country'] == 'Japan'].head())
    except Exception as e:
        print(f"Error in simulation: {e}")
