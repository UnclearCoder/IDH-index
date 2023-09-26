import pandas as pd
import numpy as np
import world_bank_data as wb
from urllib.request import urlretrieve
from termcolor import colored
from tqdm import tqdm
import zipfile
import os

class IndexIDH:

    def get_data(self, range_years=['2009', '2021']):
        # get data from ACS PUMS 5-year
        for year in range(int(range_years[0]), int(range_years[1])+1):
            url = f'https://www2.census.gov/programs-surveys/acs/data/pums/{year}/5-Year/csv_ppr.zip'
            file_name = f'Data/raw_{year}.zip'

        # progress bar
            print(colored(f'Downloading {year} data', 'yellow'))
            with tqdm(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
                urlretrieve(url, file_name, reporthook=lambda blocknum, blocksize, total: t.update(blocknum * blocksize - t.n))

        # unzip the file
            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall('Data')

    # remove the zip file and pdf
            for file in os.listdir('Data'):
                if file.endswith('.pdf'):
                    os.remove(f'Data/{file}')
                elif file.endswith('.zip'):
                    os.remove(f'Data/{file}')
                elif file.endswith('.csv') and not file.startswith('data'):
                    os.rename(f'Data/{file}', f'Data/data_{year}_raw.csv')
                else:
                    continue
        # merge all the data
        edu_index = []
        print(colored('Merging data and optimizing', 'green'))
        for year in range(2009, 2021):
            print(colored(f'Processing {year} data', 'yellow'))
            edu_index.append(IndexIDH().edu_index(year))
        # generate a dataframe for the education index
        edu_index = pd.DataFrame(edu_index, columns=['edu_index'])
        edu_index['year'] = range(2009, 2021)
        edu_index.to_csv('Data/edu_index.csv', index=False)
        # remove the raw data
        for file in os.listdir('Data'):
            if file.endswith('_raw.csv'):
                os.remove(f'Data/{file}')
            else:
                continue


    def health_index(self):
        # get Life expectancy at birth, total (years) for Puerto Rico
        pr_health = pd.DataFrame(wb.get_series('SP.DYN.LE00.IN', country='PR', simplify_index=True))
        pr_health.reset_index(inplace=True)
        pr_health.rename(columns={'SP.DYN.LE00.IN': 'health_index'}, inplace=True)
        pr_health['health'] = pr_health['health_index'].astype(float)
        pr_health['health_index'] = pr_health['health_index'].apply(lambda x: (x-20)/(85-20))
        pr_health['health_index'] = pr_health['health_index'].astype(float)
        return pr_health

    def income_index(self):
        return "Still under development"
    
    def edu_index(self, year):
        # check if edu index is already calculated
        if os.path.exists('Data/edu_index.csv'):
            data = pd.read_csv('Data/edu_index.csv')
            # return the index value for that year
            try:
                return data[data['year'] == year]['edu_index'].values[0]
            except (IndexError):
                return np.nan
        else:
            try: 
                data = f'Data/data_{year}_raw.csv'
                self.df = pd.read_csv(data, low_memory=False)
            except(FileNotFoundError):
                print('No data for that year, please run get_data()')
                return 'N/A'
            self.df = self.df[['AGEP', 'SCH', 'SCHL']]
            # calcualte the mean of years of schooling
            self.df2 = self.df[self.df['AGEP'] > 25].copy()
            self.df2['scholing'] =  self.df2['SCHL']
            self.df2.reset_index(inplace=True)
            self.df2['scholing'].replace({3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 
                                    12:10, 13:11, 14:12, 15:13, 15:13, 16:13, 17:13, 
                                    18:13.5, 19:14, 20:15, 21:17, 22:19, 23:19, 24:23}, inplace=True)
            self.df2['enroled'] = np.where(self.df2['scholing'] > 1, 1, 0)
            value1 = self.df2['scholing'].mean()

            # calculate the expected years of schooling
            self.df3 = self.df[self.df['AGEP'] < 25].copy()
            self.df3['enrolled'] = self.df3['SCH'].apply(lambda x: 1 if x > 1 else 0)
            self.df_age = self.df3.groupby(['AGEP'])[['AGEP','enrolled']].count()
            self.df_age['enrolled'] = self.df3.groupby(['AGEP'])['enrolled'].sum()
            self.df_age['enrollment_rate'] = self.df_age['enrolled'] / self.df_age['AGEP']
            self.df_age = self.df_age.rename (columns = {'AGEP': 'count'})
            self.df_age = self.df_age.reset_index()
            self.df_age.drop([0,1,2,3,4], inplace=True)
            value2 = self.df_age['enrollment_rate'].sum()

            # calculate index
            edu_index = (value1/15 + value2/18) / 2
            return edu_index  
    
    def idh_index(self):
        return self.data['IDH'].mean()


if __name__ == "__main__":
    # # generate csv file for 2009-2020 for the education index
    idh = IndexIDH()
    idh.get_data()
