import pandas as pd
import glob
import os

def load_all_data(folder="temperatures"):
    files = glob.glob(os.path.join(folder, "*.csv"))
    dataframes = [pd.read_csv(f) for f in files]
    return pd.concat(dataframes, ignore_index=True)

def seasonal_average(df):
    # Convert date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    
    seasons = {
        "Summer": [12, 1, 2],
        "Autumn": [3, 4, 5],
        "Winter": [6, 7, 8],
        "Spring": [9, 10, 11]
    }
    
    results = {}
    for season, months in seasons.items():
        avg_temp = df[df['Month'].isin(months)]['Temperature'].mean(skipna=True)
        results[season] = avg_temp
    
    with open("average_temp.txt", "w") as f:
        for season, avg in results.items():
            f.write(f"{season}: {avg:.2f}°C\n")

def temperature_range(df):
    station_stats = df.groupby("Station")['Temperature'].agg(['min','max'])
    station_stats['range'] = station_stats['max'] - station_stats['min']
    
    max_range = station_stats['range'].max()
    winners = station_stats[station_stats['range'] == max_range]
    
    with open("largest_temp_range_station.txt", "w") as f:
        for station, row in winners.iterrows():
            f.write(f"Station {station}: Range {row['range']:.2f}°C (Max: {row['max']:.2f}°C, Min: {row['min']:.2f}°C)\n")

def temperature_stability(df):
    station_stats = df.groupby("Station")['Temperature'].std()
    min_std = station_stats.min()
    max_std = station_stats.max()
    
    most_stable = station_stats[station_stats == min_std]
    most_variable = station_stats[station_stats == max_std]
    
    with open("temperature_stability_stations.txt", "w") as f:
        for station, std in most_stable.items():
            f.write(f"Most Stable: Station {station}: StdDev {std:.2f}°C\n")
        for station, std in most_variable.items():
            f.write(f"Most Variable: Station {station}: StdDev {std:.2f}°C\n")

if __name__ == "__main__":
    df = load_all_data()
    seasonal_average(df)
    temperature_range(df)
    temperature_stability(df)
    print(" Temperature analysis complete! Results saved to files.")
