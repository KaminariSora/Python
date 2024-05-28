import pandas as pd

df = pd.read_csv('cleanInformation/DataSet/D3_UsedCar.csv', encoding='latin1')
column_data = df['fuel_type'].value_counts()
# fuel_list = ', '.join(column_data)
# print(fuel_list)
# print(column_data)

unique_fuels = df[(df['fuel_type'] == 'Petrol') | (df['fuel_type'] == 'Diesel')]['fuel_type'].unique()
fuel_list = ', '.join(unique_fuels)
print(fuel_list)

# Count of each fuel type
fuel_counts = df['fuel_type'].value_counts()
print("\nCounts of each fuel type:")
print(fuel_counts)