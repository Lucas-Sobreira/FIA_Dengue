import pandas as pd
# from tqdm import tqdm
# pd.set_option('max_colwidth', -1)

url = 'https://info.dengue.mat.br/api/alertcity'
path = '/usr/local/airflow/dags/projeto_dengue/'

df_municipios = pd.read_excel(path + 'municipios.xlsx', sheet_name='Sheet_01')

df_dengue = pd.DataFrame({})

def coleta_dados(df_dengue, df_municipios, url, year = 2023):
    # for disease in ['dengue', 'chikungunya', 'zika']:
    #     for cod_mun in df_municipios['Código']:

    for cod_mun in df_municipios.head(3)['Código']: 
            search_filter = (
                'geocode={}&disease={}&format=csv&'.format(cod_mun, 'dengue') + #disease
                'ew_start=1&ew_end=2&ey_start={}&ey_end={}'.format(year, year) #semana
            )
            
            df = pd.read_csv('%s?%s' % (url, search_filter))
            df['disease'] = 'dengue' #disease
            df['year'] = year
            df_dengue = pd.concat([df_dengue, df])
    
    return df_dengue
