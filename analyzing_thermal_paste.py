import pandas as pd
import matplotlib.pyplot as plt

def analyzing_thermal_paste(df):
    try:
        df['cost_benefit'] = (df['price'] / df['gram']) / df['thermal_conductivity']
        df = df.sort_values(by='cost_benefit')
        df = df[['cost_benefit'] + [col for col in df.columns if col != 'cost_benefit']]
        df.to_csv('thermal_pastes_complete_data.csv', index=False)
    except Exception as err:
        print(Exception)
        print(err)
