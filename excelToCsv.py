import csv
import os
import pandas as pd




def read_excel(file_path):
    df = pd.read_excel(file_path)
    return df

def create_csv_files_from_excel(df, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    cities = df['il']
    for year in range(2001, 2024):
        if year in df.columns:
            yearly_data = pd.DataFrame({'city': cities, 'value': df[year]})
            file_path = os.path.join(output_directory, f"{year}_evlenme.csv")
            yearly_data.to_csv(file_path, index=False)

# Kullanım
df = read_excel("excel.xls")
output_directory = 'datas'  # Çıktı dosyalarının oluşturulacağı klasör
create_csv_files_from_excel(df, output_directory)