import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

data_california = pd.read_csv('california_charge_selected.csv')

data_california = data_california.drop(['transaction_date_pacific_time', 'currency'], axis=1)

'''Rename and convert to datetime'''
data_california = data_california.rename(columns={'start_date': 'start_date_time'})
data_california['start_date_time'] = pd.to_datetime(data_california['start_date_time'])
data_california['start_day'] = data_california['start_date_time'].dt.strftime('%A')
data_california['start_date'] = data_california['start_date_time'].dt.date
data_california['start_time'] = data_california['start_date_time'].dt.time

'''Extract start_hour, start_minute, and start_second. I will decide if to keep/drop these by exploring model's performance'''
data_california['start_hour'] = data_california['start_date_time'].dt.hour
data_california['start_minute'] = data_california['start_date_time'].dt.minute
data_california['start_second'] = data_california['start_date_time'].dt.second

'''Rename and convert end_date'''
data_california = data_california.rename(columns={'end_date': 'end_date_time'})
data_california['end_date_time'] = pd.to_datetime(data_california['end_date_time'])
data_california['end_day'] = data_california['end_date_time'].dt.strftime('%A') 
data_california['end_date'] = data_california['end_date_time'].dt.date
data_california['end_time'] = data_california['end_date_time'].dt.time

'''Extract end_hour, end_minute, and end_second. I will decide if to keep/drop these by exploring model's performance'''
data_california['end_hour'] = data_california['end_date_time'].dt.hour
data_california['end_minute'] = data_california['end_date_time'].dt.minute
data_california['end_second'] = data_california['end_date_time'].dt.second

'''Calculate cyclic features for start time.'''
data_california['start_hour_sin'] = np.sin(data_california['start_hour'] * (2. * np.pi / 24))
data_california['start_hour_cos'] = np.cos(data_california['start_hour'] * (2. * np.pi / 24))
data_california['start_minute_sin'] = np.sin(data_california['start_minute'] * (2. * np.pi / 60))
data_california['start_minute_cos'] = np.cos(data_california['start_minute'] * (2. * np.pi / 60))
data_california['start_second_sin'] = np.sin(data_california['start_second'] * (2. * np.pi / 60))
data_california['start_second_cos'] = np.cos(data_california['start_second'] * (2. * np.pi / 60))

# Calculate cyclic features for end time
data_california['end_hour_sin'] = np.sin(data_california['end_hour'] * (2. * np.pi / 24))
data_california['end_hour_cos'] = np.cos(data_california['end_hour'] * (2. * np.pi / 24))
data_california['end_minute_sin'] = np.sin(data_california['end_minute'] * (2. * np.pi / 60))
data_california['end_minute_cos'] = np.cos(data_california['end_minute'] * (2. * np.pi / 60))
data_california['end_second_sin'] = np.sin(data_california['end_second'] * (2. * np.pi / 60))
data_california['end_second_cos'] = np.cos(data_california['end_second'] * (2. * np.pi / 60))

data_california = data_california.drop(['start_date_time', 'end_date_time', 'start_date', 'start_time', 'end_date', 'end_time'], axis=1)
for col in data_california.columns:
    if data_california[col].dtype == 'object':
        data_california[col] = data_california[col].astype('string')

print(data_california)
cols_california = data_california.columns
print(cols_california)
print(data_california.dtypes)

X = data_california.drop('energy_kWh', axis=1)
y = data_california['energy_kWh'] 

print(X, y)

# # Handle categorical data
# categorical_cols = data_california.select_dtypes(include=['object']).columns
# data_california = pd.get_dummies(data_california, columns=categorical_cols, drop_first=True)

# # Assuming 'energy_kWh' is the target column
# X = data_california.drop('energy_kWh', axis=1)
# y = data_california['energy_kWh']

# # Split the dataset into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# print(X_train)

# # Initialize the Decision Tree Regressor
# tree_regressor = DecisionTreeRegressor(random_state=42)

# # Train the model
# tree_regressor.fit(X_train, y_train)

# # Predict and evaluate the model
# y_pred = tree_regressor.predict(X_test)
# rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# print(f'RMSE: {rmse}')