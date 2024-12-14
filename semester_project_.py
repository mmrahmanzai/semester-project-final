# -*- coding: utf-8 -*-
"""Semester Project .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ir_Awf9qAeilrOg8pxrajHdICsNW_V82
"""

#API Key 313ee463bb714ba58a9e6b78f6782b21

!pip install schedule==1.1.0

import schedule
import time
import datetime
import requests
import json
import pandas as pd
import os


def fetch_bls_data():

    today = datetime.datetime.today()

    # Check if today is the 14th day of the month
    if today.day == 14:

      # Series IDs go here along with my custom timeframe thats dynamic
      series_ids = ['CES0000000001','LNS14000000','CUUR0000SA0','WPUFD4'] #Nonfarm Payroll, Unemployment, CPI-U, PPI

      # Calculate the start and end year; preperation for gather rolling 12 months of data
      start_year = today.year - 1
      start_month = today.month - 1
      if start_month == 1:
        start_month = 12
        start_year = today.year - 1

      end_year = today.year
      end_month = today.month

      # Data being requested
      data = json.dumps({"seriesid": series_ids, "startyear": str(start_year), "endyear": str(end_year)})
      headers = {'Content-type': 'application/json'}

      # Make the API request
      response = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)

      # Check if the request was successful
      if response.status_code == 200:
          # Parse the JSON response
          data = json.loads(response.text)

          # Extract data into a list of dictionaries
          all_data = []
          print(data)
          month_string = ""
          #compare item ['period'] with the intended start_month
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

          # Create a Pandas DataFrame
          df = pd.DataFrame(all_data)

          # Load existing data from CSV, if it exists
          file_path = 'bls_data.csv'

          df.to_csv(file_path, index=False)

          print(f"Data fetched and stored to {file_path} successfully!")

      else:
          print(f"Error fetching data: {response.status_code}")
    else:
      print("Not the 8th day of the month. Skipping data fetch.")

fetch_bls_data()

schedule.every().day.at("02:00").do(fetch_bls_data)

# Keep the script running to execute the scheduled task
while True:
    schedule.run_pending()
    time.sleep(1)