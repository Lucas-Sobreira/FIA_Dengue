import pandas as pd
import datetime

def coleta_dados(df_dengue, df_municipios, url, n_week, year = 2023):
    for disease in ['dengue', 'chikungunya', 'zika']:
        for cod_mun in df_municipios.head(3)['Código']: 
            search_filter = (
                'geocode={}&disease={}&format=csv&'.format(cod_mun, disease) + 
                # 'ew_start=1&ew_end={}&ey_start={}&ey_end={}'.format(str(n_week), year, year) 
                'ew_start=21&ew_end={}&ey_start={}&ey_end={}'.format(str(n_week), year, year) 
            )
            
            df = pd.read_csv('%s?%s' % (url, search_filter))
            df['disease'] = disease 
            df['year'] = year
            df_dengue = pd.concat([df_dengue, df])
            # df_dengue.to_csv("df_dengue.csv", index=False)

    # return ('\nSemana: {}\n\nDados:\n{}'.format(n_week, df_dengue))
    return df_dengue

path = '/usr/local/airflow/dags/projeto_dengue/'
df_municipios = pd.read_excel(path + 'municipios.xlsx', sheet_name='Sheet_01')

url = 'https://info.dengue.mat.br/api/alertcity'
df_dengue = pd.DataFrame({})

n_week = datetime.date.today().isocalendar()[1]
coleta_dados(df_dengue, df_municipios, url, n_week)