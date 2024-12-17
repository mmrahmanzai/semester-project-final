
import schedule
import time
import datetime
import requests
import json
import pandas as pd
import os


def fetch_bls_data():

    today = datetime.datetime.today() # Establishing a today's date for the start date and end date

    if not os.path.exists('data'):
        os.makedirs('data')
    file_path = 'data/bls_data.csv'
    
    # Prepping an if statement to run function on a certain day of the month
    if today.day == 17:
    
      # Establishing what series IDs will be fetched (only doing 4 to ensure a clean visual)
      series_ids = ['CES0000000001','LNS14000000','CUUR0000SA0','WPUFD4'] #Nonfarm Payroll, Unemployment, CPI-U, PPI

      # Calculating the start and end year; preperation for gather rolling 12 months of data
      start_year = today.year - 1
      start_month = today.month - 1
      if start_month == 1:
        start_month = 12
        start_year = today.year - 1

      end_year = today.year
      end_month = today.month

      # Data being requested from BLS
      data = json.dumps({"seriesid": series_ids, "startyear": str(start_year), "endyear": str(end_year)})
      headers = {'Content-type': 'application/json'}

      # Making the API request
      response = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)

      # Checking if the request was successful
      if response.status_code == 200:
          # Parsing the JSON response
          data = json.loads(response.text)

          # Extracting data into a list of dictionaries
          all_data = []
          print(data)
          month_string = ""
          # Compare item "period" with the intended start_month
          if start_month < 10:
            month_string = "M0" + str(start_month)
          else:
            month_string = "M" + str(start_month)
          for series in data['Results']['series']:
              series_id = series['seriesID']
              for item in series['data']:
                if item['year'] == str(start_year) and item['period'] < month_string:
                  continue
                else:
                  row = {
                      'seriesID': series_id,
                      'year': item['year'],
                      'period': item['period'],
                      'value': item['value']
                  }
                  all_data.append(row)

          # Creating a Pandas DataFrame
          df = pd.DataFrame(all_data)

          # Loading existing data from CSV
          file_path = 'bls_data.csv'

          df.to_csv(file_path, index=False)

          print(f"Data fetched and stored to {file_path} successfully!") # Providing a message if successful

      else:
          print(f"Error fetching data: {response.status_code}") # Error message when data not pulled
    else:
      print("Not the 15th day of the month. Skipping data fetch.") # If not the specific day of the month, will inform

fetch_bls_data()

# Scheduling script to run daily to ensure day the script should run is not missed
schedule.every().day.at("02:00").do(fetch_bls_data)

# Keep the script running to execute the scheduled task
while True:
    schedule.run_pending()
    time.sleep(1)
