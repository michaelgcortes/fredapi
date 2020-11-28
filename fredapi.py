# How to work with APIs from Python and R

# Problem set up: 
# You need data, and there exists some API that you can get it from. 
# You want to do it in Python and/or R.
# How to do it? 

import requests
import pandas as pd
import matplotlib.pyplot as plt


# Function to wrap around the FRED API and provide Pythonic interface

def fredpy(series_id, start_date, units):

    # Requested key from FRED API website. You must make an account. 
    api_key = 'cbf1882aeb32943dc6a1ad50ceb1502a'

    # This is the generic URL scheme
    url_scheme = 'https://api.stlouisfed.org/fred/series/observations?series_id={SERIES_ID}' + \
                 '&api_key={API_KEY}&file_type=json&observation_start={START}' + \
                 '&units={UNITS}'

    # We plug in our values into the URL scheme using the 'format' method of string class
    url = url_scheme.format(SERIES_ID = series_id, START=start_date, API_KEY=api_key, UNITS=units)

    # Make the request using the 'requests' package using the GET method
    response = requests.get(url)

    # If successful, get the results
    if(response.status_code == 200):
        # Get the observation data from the json object
        json_data = response.json()['observations']
        # Convert the data to the data frame
        data = pd.DataFrame(json_data)
        # Drop irrelevant variables
        data.drop(columns=['realtime_start', 'realtime_end'], inplace=True)
        # Rename the 'value' column to the name of the series_id
        data.rename(columns={'value': series_id}, inplace=True)
        # Coerce the 'date' column to be of type 'datetime'
        data['date'] = pd.to_datetime(data['date'])
        # Coerce the series data to be of type float
        data[series_id] = data[series_id].astype(float)
        return data

    else:
        print('The request was unsuccessful')
        return None



# Test the function out by making a request
df = fredpy(series_id = 'GDP', start_date = '2010-01-01', units='pc1')


# Preview the results
print(df.head())


# Visualize the data
plt.plot(df['date'], df['GDP'])
plt.ylabel('GDP')
plt.xlabel('date')
plt.title('GDP data from FRED API')
plt.show()

