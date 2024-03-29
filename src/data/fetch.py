import pandas as pd
import zipfile
from src.data.IDH import IndexIDH
from urllib.request import urlretrieve
import os
from yaspin import yaspin

def get_data(range_years: list, data_file):
    """
    Downloads the data and extracts the data into a csv file. 
    All data is stored in the data/raw/ folder.

    Parameters
    ----------
    range_years: <list>
        The range of years to download
    data_file: <str>
        The name of the file to download

    Returns
    -------
    None
    """
    for year in range(int(range_years[0]), int(range_years[1])+1):
        if os.path.exists(f'data/raw/data_{data_file[4:7]}_{year}_raw.csv') or os.path.exists(f'data/processed/edu_index.csv'):
            continue
        else:
            url = f'https://www2.census.gov/programs-surveys/acs/data/pums/{year}/5-Year/{data_file}'
            file_name = f'data/raw/raw_ppr_{year}.zip'
        try:
            urlretrieve(url, file_name)
        except:
            print(f'Error: File for {year} not found')
            continue

        # unzip the file
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall('data/raw/')

        # remove the zip file and pdf
        for file in os.listdir('data/raw/'):
            if file.endswith('.pdf'):
                os.remove(f'data/raw/{file}')
            elif file.endswith('.zip'):
                os.remove(f'data/raw/{file}')
            elif file.endswith('.csv') and not file.startswith('data'):
                os.rename(f'data/raw/{file}', f'data/raw/data_{data_file[4:7]}_{year}_raw.csv')
            else:
                continue

       
def download(range_years):
    """
    Function to simplyfy and give feedback to the user. It runs the get_data function for both the PPR and HPR data.

    Parameters
    ----------
    range_years: <list>
        The range of years to download

    Returns
    -------
    None
    """
    spin = yaspin(text='Downloading PPR data...', color='blue', spinner='dots')
    spin.start()
    get_data(range_years, data_file='csv_ppr.zip')
    spin.stop() 
    spin = yaspin(text='Downloading HPR data...', color='yellow', spinner='dots')
    spin.start()
    get_data(range_years, data_file='csv_hpr.zip')
    spin.stop()
    spin = yaspin(text='Calculating IDH data...', color='green', spinner='dots')
    spin.start()
    IDH = IndexIDH()
    IDH.edu_index('data/raw/')
    IDH.income_index()
    IDH.health_index()
    IDH.idh_index()
    spin.stop()
    
    # for file in os.listdir('data/raw/'):
    #     if file.endswith('raw.csv'):
    #         os.remove(f'data/raw/{file}')
    #     else:
    #         continue

if __name__ == '__main__':
    get_data(['2012','2021'])