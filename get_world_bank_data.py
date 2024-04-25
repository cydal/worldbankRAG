import os
import json
import wbgapi
import requests
import pandas as pd

def get_world_bank_data(indicator, country, start_year=2020, end_year=2023):
  """
  This function retrieves data for a specified indicator and country using the World Bank Open Data API (wbgapi).

  Args:
      indicator: Indicator code (e.g., "IT.NET.USER.ZS").
      country: Country code (e.g., "BR").
      start_year: Starting year for data (default: 2020).
      end_year: Ending year for data (default: 2023).

  Returns:
      A pandas DataFrame containing the data.
  """

  data = wbgapi.data.DataFrame(indicator, country, range(start_year, end_year + 1))
  return data


def get_world_bank_metadata(indicator, country, format="json"):
  """
  This function retrieves metadata for a specified indicator and country using the World Bank Open Data API (requests).

  Args:
      indicator: Indicator code (e.g., "IT.NET.USER.ZS").
      country: Country code (e.g., "BR").
      format: Output format (default: "json").

  Returns:
      A dictionary containing the metadata for the indicator and country.
  """

  base_url = "https://api.worldbank.org/v2/indicator/"
  url = f"{base_url}{indicator}?locations={country}&format={format}"

  response = requests.get(url)

  if response.status_code == 200:
    data = response.json()
    return data[1]
  else:
    print(f"Error retrieving metadata for {indicator}: {response.status_code}")
    return None


def get_world_bank_data_and_save(indicators, country, start_year=2020, end_year=2023, data_dir="data", metadata_dir="metadata"):
  """
  This function retrieves data and metadata for all specified indicators and country,
  saves dataframes as CSV and metadata as JSON files.

  Args:
      indicators: List of indicator codes (e.g., ["IT.NET.USER.ZS", "SI.POV.DDAY"]).
      country: Country code (e.g., "BR").
      start_year: Starting year for data (default: 2020).
      end_year: Ending year for data (default: 2023).
      data_dir: Directory to save dataframes (default: "data").
      metadata_dir: Directory to save metadata (default: "metadata").
  """

  os.makedirs(data_dir, exist_ok=True)
  os.makedirs(metadata_dir, exist_ok=True)

  for indicator in indicators:
    data = get_world_bank_data(indicator, country, start_year, end_year)
    metadata = get_world_bank_metadata(indicator, country)

    if data is not None:
      data_filename = f"{data_dir}/{indicator}.csv"
      data.to_csv(data_filename, index=False)
      print(f"Data for {indicator} saved to {data_filename}")

    if metadata:
      metadata_filename = f"{metadata_dir}/{indicator}.json"
      with open(metadata_filename, "w") as f:
        json.dump(metadata, f, indent=4)
      print(f"Metadata for {indicator} saved to {metadata_filename}")


def main():

    indicators = ["IT.NET.USER.ZS", "SI.POV.DDAY", "SL.UEM.TOTL.ZS"]
    country = "BRA"
    start_year = 2020
    end_year = 2023

    get_world_bank_data_and_save(indicators, country, start_year, end_year)

if __name__=="__main__": 
    main() 



