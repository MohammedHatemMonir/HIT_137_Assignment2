import pandas as pd
import os

"""
Group Name: Sydney 11
Course Code: HIT137

Group Members:
Mohamed Hatem Moneir Mansour Elshekh - 393891
Roshan Pandey - 395865
Kamana  - 392322
Sejal Pradhan - 396928

This program analyzes temperature data collected from multiple weather stations in Australia.
The data is stored in multiple CSV files under a "temperatures" folder, with each file 
representing data from one year. The program processes ALL .csv files in the temperatures 
folder and ignores missing temperature values (NaN) in calculations.

Main Functions Implemented:

1. Seasonal Average: Calculate the average temperature for each season across ALL 
   stations and ALL years. Save the results to "average_temp.txt".
   - Uses Australian seasons: Summer (Dec-Feb), Autumn (Mar-May), Winter (Jun-Aug), Spring (Sep-Nov)
   - Output format example: "Summer: 28.5°C"

2. Temperature Range: Find the station(s) with the largest temperature range (difference 
   between the highest and lowest temperature ever recorded at that station). 
   Save the results to "largest_temp_range_station.txt".
   - Output format example: "Station ABC: Range 45.2°C (Max: 48.3°C, Min: 3.1°C)"
   - If multiple stations tie, lists all of them

3. Temperature Stability: Find which station(s) have the most stable temperatures 
   (smallest standard deviation) and which have the most variable temperatures 
   (largest standard deviation). Save the results to "temperature_stability_stations.txt".
   - Output format example: 
     - "Most Stable: Station XYZ: StdDev 2.3°C"
     - "Most Variable: Station DEF: StdDev 12.8°C"
   - If multiple stations tie, lists all of them



References

ChatGPT-5. (2025). AI assistant for code layout and documentation grammar. OpenAI. https://openai.com/chatgpt
 - Used for: comment tone and structure (no algorithmic code copied).

The Organic Chemistry Tutor. (2021, March 5). How To Calculate The Standard Deviation [Video]. https://www.youtube.com/watch?v=sMOZf4GN3oc
- Used for: understanding std. deviation concept applied in calculate_standard_deviation().

W3Schools. (2024). Python - List Files in a Directory. https://www.w3schools.com/python/python_file_handling.asp
- Used for: basic directory listing patterns (get_csv_files).

W3Schools. (2024). Python file write. https://www.w3schools.com/python/python_file_write.asp
- Used for: with-open patterns and text file writing (write_* functions).

W3Schools. (2025). Pandas Read CSV. https://www.w3schools.com/python/pandas/pandas_csv.asp
- Used for: reading CSVs with pandas (process_csv_file).

Python Software Foundation. (2024). The __main__ module. https://docs.python.org/3/library/__main__.html
- Used for: main entry-point guard.

Learn By Example. (2025). Python open() function. https://www.learnbyexample.org/python-open-function/
- Used for: open(..., encoding="utf-8") usage in file I/O.

Python Software Foundation. (2025). Errors and Exceptions. https://docs.python.org/3/tutorial/errors.html
- Used for: checked error types and how to catch them in except blocks.
"""

def get_csv_files(folder="temperatures"):
    """
    Get all CSV files from the specified folder.
    Returns a list of file paths.
    """
    files = []
    try:
        for filename in os.listdir(folder):  # Go through each file in the temperatures folder
            if filename.endswith('.csv'):  # Only process files that end with .csv extension
                files.append(os.path.join(folder, filename))  # Use os.path.join for portability
    except FileNotFoundError:
        print(f"Folder not found: {folder}")
    except Exception as e:
        print("Failed to list CSV files:", e)
    return files

def extract_year_from_filename(file):
    """
    Extract year from CSV filename.
    Returns the year as an integer, or None if extraction fails.
    """
    try:
        filename = os.path.basename(file)  # Get filename only
        filename_no_ext = os.path.splitext(filename)[0]  # Remove extension
        year_part = filename_no_ext.split('_')[-1]  # Expect year after last underscore
        year = int(year_part)
        return year
    except (ValueError, IndexError):
        print("Error getting year from filename:", file)
        return None
    except Exception as e:
        print("Unexpected error extracting year:", e)
        return None

def process_csv_file(file, year):
    """
    Process a single CSV file and convert from wide to long format.
    Returns a list of temperature records for this file.
    """
    # Use f = open() structure to read the CSV file instead of direct pandas methods
    try:
        with open(file, 'r', encoding='utf-8') as f:  # Open the file safely
            csv_data = pd.read_csv(f)  # Use pandas to read the CSV data
    except FileNotFoundError:
        print("CSV file not found:", file)
        return []
    except Exception as e:
        print("There was an error reading the CSV file:", e)
        return []
    
    # Convert from wide to long format - transform month columns into individual records
    months = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December']
    
    file_data = [] # Store records for this file
    month_number = 1 # Start with month 1 (January)
    for month in months: # Process each month column in the CSV
        try:
            if month in csv_data.columns:  # Check if this month exists as a column in the CSV
                for i in range(len(csv_data)):  # Go through each row (station) in the CSV
                    try:
                        station_name = csv_data.iloc[i]['STATION_NAME']  # Get the station name
                        temperature = csv_data.iloc[i][month]  # Get the temperature for this month

                        # Create date string with proper formatting (YYYY-MM-DD)
                        if month_number < 10:  # If month is 1-9, add leading zero
                            month_str = "0" + str(month_number)
                        else:
                            month_str = str(month_number)
                        date_string = str(year) + "-" + month_str + "-01"  # First day of month

                        # Create a record dictionary to store this temperature reading
                        record = {}
                        record['Station'] = station_name
                        record['Date'] = date_string
                        record['Temperature'] = temperature
                        file_data.append(record)
                    except Exception as e:
                        print("Error processing row", i, "in month", month, "-", e)
                        continue  # Skip this row if there's an error and move to next row
        except Exception as e:
            print("Error processing month:", month, "-", e)
            continue  # Skip this month if there's an error and move to next month
        
        month_number = month_number + 1 # Move to next month number
    
    return file_data

def load_all_data(folder="temperatures"):
    """
    Load and process all CSV temperature data files from the specified folder.
    
    This function reads all .csv files in the temperatures folder, extracts the year from
    each filename, and converts the data from wide format (months as columns) to long format
    (one record per station-month combination).
    
    Returns a list of dictionaries, where each dictionary represents one temperature record
    with keys: 'Station', 'Date', 'Temperature'
    """
    # Get all CSV files from the folder
    files = get_csv_files(folder)
    
    all_data = [] # This will store all temperature records from all files
    
    for file in files: # Process each CSV file one by one
        # Extract year from filename
        year = extract_year_from_filename(file)
        if year is None: # Skip file if we couldn't extract year
            continue
        
        # Process this CSV file and get its records
        file_records = process_csv_file(file, year)
        all_data.extend(file_records) # Add all records from this file to our main data list
    
    return all_data # Return the complete list of temperature records

def group_temperatures_by_season(data):
    """
    Group temperature data by Australian seasons.
    Returns a dictionary with season names as keys and temperature lists as values.
    """
    # Create separate lists to collect temperatures for each season
    seasonal_temps = {
        'Summer': [], # Will store all summer temperature readings
        'Autumn': [], # Will store all autumn temperature readings
        'Winter': [], # Will store all winter temperature readings
        'Spring': []  # Will store all spring temperature readings
    }
    
    for record in data: # Go through each temperature record in our data
        # Get month from date string by splitting the "YYYY-MM-DD" format
        date_parts = record['Date'].split('-') # Split date string by dash character
        month = int(date_parts[1]) # Get the month part (middle section) and convert to integer
        temp = record['Temperature'] # Get the temperature value from this record

        # Check if temperature is valid robustly (skip NaN/None/invalid)
        if pd.notna(temp):
            try:
                temp = float(temp) # Convert temperature to a float number for calculations
            except (TypeError, ValueError):
                continue
            
            # Group temperatures by Australian seasons based on month number
            if month == 12 or month == 1 or month == 2: # December, January, February = Summer
                seasonal_temps['Summer'].append(temp) # Add this temperature to summer list
            elif month == 3 or month == 4 or month == 5: # March, April, May = Autumn
                seasonal_temps['Autumn'].append(temp) # Add this temperature to autumn list
            elif month == 6 or month == 7 or month == 8: # June, July, August = Winter
                seasonal_temps['Winter'].append(temp) # Add this temperature to winter list
            elif month == 9 or month == 10 or month == 11: # September, October, November = Spring
                seasonal_temps['Spring'].append(temp) # Add this temperature to spring list
    
    return seasonal_temps

def calculate_seasonal_averages(seasonal_temps):
    """
    Calculate average temperatures for each season.
    Returns a dictionary with season names and their average temperatures.
    """
    averages = {}
    
    for season, temps in seasonal_temps.items():
        if len(temps) > 0: # Only calculate if we have temperatures for this season
            averages[season] = sum(temps) / len(temps) # Sum all temps and divide by count
        else:
            averages[season] = 0 # Set to 0 if no temperatures available
    
    return averages

def write_seasonal_results(averages):
    """
    Write seasonal average results to file.
    """
    try:
        with open("average_temp.txt", "w", encoding="utf-8") as f:  # Safe file writing
            f.write("Summer: " + str(round(averages['Summer'], 2)) + "°C\n")
            f.write("Autumn: " + str(round(averages['Autumn'], 2)) + "°C\n")
            f.write("Winter: " + str(round(averages['Winter'], 2)) + "°C\n")
            f.write("Spring: " + str(round(averages['Spring'], 2)) + "°C\n")
    except Exception as e:
        print("There was an error writing the seasonal averages file:", e)

def seasonal_average(data):
    """
    Calculate the average temperature for each Australian season across all stations and years.
    
    Australian seasons are defined as:
    - Summer: December, January, February (months 12, 1, 2)
    - Autumn: March, April, May (months 3, 4, 5)
    - Winter: June, July, August (months 6, 7, 8)
    - Spring: September, October, November (months 9, 10, 11)
    
    The results are saved to "average_temp.txt" with format "Season: XX.XX°C"
    """
    # Group temperatures by season
    seasonal_temps = group_temperatures_by_season(data)
    
    # Calculate averages for each season
    averages = calculate_seasonal_averages(seasonal_temps)
    
    # Write results to file
    write_seasonal_results(averages)

def group_temperatures_by_station(data):
    """
    Group temperature data by station name.
    Returns a dictionary with station names as keys and temperature lists as values.
    """
    stations = {} # Dictionary where key = station name, value = list of temperatures
    
    for record in data: # Go through each temperature record in our data
        station = record['Station'] # Get the station name from this record
        temp = record['Temperature'] # Get the temperature value from this record

        # Check if temperature is valid robustly (skip NaN/None/invalid)
        if pd.notna(temp):
            try:
                temp = float(temp) # Convert temperature to a float number for calculations
            except (TypeError, ValueError):
                continue
            
            # Add station to dictionary if we haven't seen it before
            if station not in stations:
                stations[station] = [] # Create empty list for this station's temperatures
            
            stations[station].append(temp) # Add this temperature to the station's list
    
    return stations

def calculate_station_ranges(stations):
    """
    Calculate min, max, and range for each station.
    Returns a dictionary with station statistics.
    """
    station_ranges = {} # Dictionary to store range statistics for each station
    for station in stations: # Go through each station we've collected data for
        temps = stations[station] # Get the list of all temperatures for this station
        if len(temps) > 0: # Only calculate if we have temperature data for this station
            min_temp = min(temps) # Find the lowest temperature ever recorded at this station
            max_temp = max(temps) # Find the highest temperature ever recorded at this station
            range_temp = max_temp - min_temp # Calculate the range (difference between max and min)
            station_ranges[station] = { # Store all the statistics for this station
                'min': min_temp, # Store minimum temperature
                'max': max_temp, # Store maximum temperature
                'range': range_temp # Store temperature range
            }
    return station_ranges

def find_maximum_range_stations(station_ranges):
    """Find station(s) with the largest temperature range and return a list of (station, stats)."""
    if not station_ranges:
        return []
    biggest = max(info['range'] for info in station_ranges.values())
    return [(name, info) for name, info in station_ranges.items() if info['range'] == biggest]

def write_range_results(tied_stations):
    """Write temperature range results to file, including all tied stations."""
    try:
        with open("largest_temp_range_station.txt", "w", encoding="utf-8") as f:
            if not tied_stations:
                f.write("No station data available.\n")
                return
            for station, stats in tied_stations:
                f.write(
                    f"Station {station}: Range {round(stats['range'], 2)}°C "
                    f"(Max: {round(stats['max'], 2)}°C, Min: {round(stats['min'], 2)}°C)\n"
                )
    except Exception as e:
        print("There was an error writing the temperature range file:", e)

def temperature_range(data):
    """
    Find the station(s) with the largest temperature range across all years.
    
    Temperature range is calculated as the difference between the highest and lowest
    temperature ever recorded at each station. The station with the maximum range
    is identified and saved to "largest_temp_range_station.txt".
    
    Output format: "Station ABC: Range 45.2°C (Max: 48.3°C, Min: 3.1°C)"
    """
    # Group temperatures by station
    stations = group_temperatures_by_station(data)
    
    # Calculate min, max, and range for each station
    station_ranges = calculate_station_ranges(stations)
    
    # Find station(s) with the biggest temperature range (handle ties)
    tied_stations = find_maximum_range_stations(station_ranges)
    
    # Write results to file
    write_range_results(tied_stations)

def calculate_standard_deviation(temps):
    """
    Calculate standard deviation for a list of temperatures manually.
    Returns the standard deviation value.
    """
    if len(temps) <= 1: # Need at least 2 temperature readings to calculate standard deviation
        return 0
    
    # Step 1: Calculate the mean (average) temperature
    total = 0 # Initialize total sum to 0
    for temp in temps: # Add up all temperatures
        total = total + temp # Add this temperature to the running total
    mean = total / len(temps) # Calculate mean by dividing total by number of readings
    
    # Step 2: Calculate variance (average of squared differences from mean)
    variance_sum = 0 # Initialize sum of squared differences to 0
    for temp in temps: # Go through each temperature reading again
        difference = temp - mean # Calculate how far this temperature is from the mean
        variance_sum = variance_sum + (difference * difference) # Add squared difference to sum
    # Use sample variance (n - 1)
    variance = variance_sum / (len(temps) - 1)
    
    # Step 3: Calculate standard deviation (square root of variance)
    import math # Import math module to use square root function
    std_dev = math.sqrt(variance) # Calculate standard deviation as square root of variance
    return std_dev

def calculate_station_std_devs(stations):
    """
    Calculate standard deviation for each station.
    Returns a dictionary with station names and their standard deviations.
    """
    station_std_devs = {} # Dictionary to store standard deviation for each station
    for station in stations: # Go through each station we've collected data for
        temps = stations[station] # Get the list of all temperatures for this station
        std_dev = calculate_standard_deviation(temps) # Calculate standard deviation for this station
        if std_dev > 0: # Only include stations with valid standard deviation
            station_std_devs[station] = std_dev # Store standard deviation for this station
    return station_std_devs

def find_stability_extremes(station_std_devs):
    """
    Find the most stable and most variable stations.
    Returns (stable_stations, variable_stations, min_std, max_std).
    """
    if len(station_std_devs) == 0:  # No stations to analyze
        return [], [], 0, 0

    min_std = min(station_std_devs.values())  # Find the smallest standard deviation value
    max_std = max(station_std_devs.values())  # Find the largest standard deviation value

    most_stable_stations = [s for s, sd in station_std_devs.items() if sd == min_std]
    most_variable_stations = [s for s, sd in station_std_devs.items() if sd == max_std]

    return most_stable_stations, most_variable_stations, min_std, max_std

def write_stability_results(most_stable_stations, most_variable_stations, min_std, max_std):
    """Write temperature stability results to file, supporting ties."""
    try:
        with open("temperature_stability_stations.txt", "w", encoding="utf-8") as f:
            if not most_stable_stations and not most_variable_stations:
                f.write("No station data available.\n")
                return
            stable_text = ", ".join(f"Station {s}" for s in most_stable_stations) if most_stable_stations else "N/A"
            variable_text = ", ".join(f"Station {s}" for s in most_variable_stations) if most_variable_stations else "N/A"
            f.write(f"Most Stable: {stable_text}: StdDev {round(min_std, 2)}°C\n")
            f.write(f"Most Variable: {variable_text}: StdDev {round(max_std, 2)}°C\n")
    except Exception as e:
        print("There was an error writing the temperature stability file:", e)

def temperature_stability(data):
    """
    Find the stations with the most stable (lowest standard deviation) and most variable 
    (highest standard deviation) temperatures across all years.
    
    Standard deviation measures how much temperatures vary from the average at each station.
    Lower standard deviation = more stable temperatures
    Higher standard deviation = more variable temperatures
    
    Results are saved to "temperature_stability_stations.txt" with format:
    "Most Stable: Station XYZ: StdDev 2.3°C"
    "Most Variable: Station DEF: StdDev 12.8°C"
    """
    # Group temperatures by station (reusing function from temperature_range)
    stations = group_temperatures_by_station(data)
    
    # Calculate standard deviation for each station
    station_std_devs = calculate_station_std_devs(stations)
    
    # Find most stable and most variable stations
    most_stable_stations, most_variable_stations, min_std, max_std = find_stability_extremes(station_std_devs)
    
    # Write results to file
    if most_stable_stations or most_variable_stations:  # Only write if we found stations
        write_stability_results(most_stable_stations, most_variable_stations, min_std, max_std)

def main():
    """Entry point for Question 2 temperature analyses."""
    try:
        # Step 1: Load all temperature data from CSV files in the temperatures folder
        data = load_all_data("temperatures")  # Returns list of dictionaries instead of DataFrame

        # Step 2: Calculate and save seasonal averages across all stations and years
        seasonal_average(data)  # Creates "average_temp.txt" with seasonal temperature averages

        # Step 3: Find and save the station with the largest temperature range
        temperature_range(data)  # Creates "largest_temp_range_station.txt" with station having biggest temp range

        # Step 4: Find and save the most stable and most variable temperature stations
        temperature_stability(data)  # Creates "temperature_stability_stations.txt" with stability analysis

        # Print success message when all analysis is complete
        print(" Temperature analysis complete! Results saved to files.")
    except Exception as e:
        # Print error message if any part of the analysis fails
        print("error loading...", e)


if __name__ == "__main__":
    main()