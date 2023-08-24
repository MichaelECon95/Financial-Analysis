# Importing necessary libraries
import pandas as pd

# Loading the dataset
file_path = '/.../Financials.csv'
data = pd.read_csv(file_path)

# Displaying the first few rows of the dataset
data.head()

'''
Column Names: The column names seem to have leading and trailing spaces, which can cause problems when trying to access them.

Dollar Sign ('$') and Commas (','): Various columns contain dollar signs and commas within the numerical values, which will prevent them from being treated as numerical data types.

Dashes ('-'): Some columns appear to contain dashes, which may need to be converted or handled.
'''

#Clean Column Names
# Removing leading and trailing spaces from the column names
data.columns = data.columns.str.strip()

# Displaying the cleaned column names
data.columns.tolist()

#Remove Special Characters and Convert to Numeric

'''
# List of columns that need cleaning
columns_to_clean = [
    'Units Sold', 'Manufacturing Price', 'Sale Price', 'Gross Sales', 'Discounts', 'Sales', 'COGS', 'Profit'
]

# Function to clean the columns by removing special characters and converting to numeric
def clean_columns(value):
    value = value.replace('$', '').replace(',', '').replace('-', '')
    return float(value) if value else None

# Applying the cleaning function to the specified columns
for column in columns_to_clean:
    data[column] = data[column].apply(clean_columns)

# Displaying the first few rows after cleaning
data.head()

Results in error

'''
#Modifing the cleaning function to handle empty strings appropriately and reapply the cleaning process.

'''
# Modifying the cleaning function to handle empty strings
def clean_columns(value):
    value = value.replace('$', '').replace(',', '').replace('-', '')
    return float(value) if value.strip() != '' else None

# Reapplying the cleaning function to the specified columns
for column in columns_to_clean:
    data[column] = data[column].apply(clean_columns)

# Displaying the first few rows after cleaning
data.head()

Results in error, occurred because some of the values are already float, and we are attempting to use the replace method on them.

'''

#Reloading the data and reapply the cleaning function to ensure everything is processed correctly.

'''
# Reloading the dataset
data = pd.read_csv(file_path)

# Removing leading and trailing spaces from the column names
data.columns = data.columns.str.strip()

# Applying the cleaning function to the specified columns
for column in columns_to_clean:
    data[column] = data[column].apply(clean_columns)

# Displaying the first few rows after cleaning
data.head()


Results in another error. Possibly more complex patterns in the data than initially anticipated. The presence of parentheses in the numerical values could be causing this issue.
'''

#adjusting the cleaning function to handle these cases as well

'''
# Modifying the cleaning function to handle parentheses
def clean_columns(value):
    value = value.replace('$', '').replace(',', '').replace('-', '').replace('(', '').replace(')', '')
    return float(value) if value.strip() != '' else None

# Reapplying the cleaning function to the specified columns
for column in columns_to_clean:
    data[column] = data[column].apply(clean_columns)

# Displaying the first few rows after cleaning
data.head()



Results in error.
 Instead of applying the cleaning function directly, we'll identify and convert the specific columns that contain the problematic characters

'''


#Instead of applying the cleaning function directly, attempting to identify and convert the specific columns that contain the problematic characters.


#Reload the dataset and clean the column names.
# Reloading the dataset
data = pd.read_csv(file_path)

# Removing leading and trailing spaces from the column names
data.columns = data.columns.str.strip()

# Displaying the first few rows after cleaning the column names
data.head()



#Identify the specific columns with the problematic characters.

# Sample values from each column to identify the columns that need cleaning
sample_values = {column: data[column].sample(1).values[0] for column in data.columns}
sample_values

'''
columns that need cleaning:

Units Sold
Manufacturing Price
Sale Price
Gross Sales
Discounts
Sales
COGS
Profit

'''

#Clean and convert the identified columns.

'''
# List of columns that need cleaning based on the sample values
columns_to_clean = [
    'Units Sold', 'Manufacturing Price', 'Sale Price', 'Gross Sales', 'Discounts', 'Sales', 'COGS', 'Profit'
]

# Cleaning the specified columns
for column in columns_to_clean:
    # Removing special characters
    data[column] = data[column].replace('[\$,(),-]', '', regex=True)
    # Replacing empty strings with NaN
    data[column] = data[column].replace('', float('nan'))
    # Converting to float
    data[column] = data[column].astype(float)

# Displaying the first few rows after cleaning
data.head()

Results in error still due to empty strings

'''

#Modifing the cleaning process to directly handle empty strings during the conversion. We will use the Pandas to_numeric function, which should handle errors more gracefully

# Cleaning the specified columns using the to_numeric function
for column in columns_to_clean:
    # Removing special characters
    data[column] = data[column].replace('[\$,(),-]', '', regex=True)
    # Converting to float using to_numeric, setting errors='coerce' to handle empty strings
    data[column] = pd.to_numeric(data[column], errors='coerce')

# Converting the 'Date' column to a datetime data type
data['Date'] = pd.to_datetime(data['Date'])

# Displaying the first few rows after cleaning
data.head()

'''
Data successfully cleaned, and the special characters have been removed from the relevant columns. The columns have also been converted to numerical data types.
'''


#Familiarizing the data
#plottiong the sales and profit with respect to the timeline.

# Importing necessary libraries for plotting
import matplotlib.pyplot as plt

# Grouping data by date and summing sales and profit
time_series_data = data.groupby('Date').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()

# Plotting Sales
plt.figure(figsize=(12, 6))
plt.plot(time_series_data['Date'], time_series_data['Sales'], label='Sales')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.title('Sales Over Time')
plt.legend()
plt.grid(True)
plt.show()

# Plotting Profit
plt.figure(figsize=(12, 6))
plt.plot(time_series_data['Date'], time_series_data['Profit'], label='Profit', color='orange')
plt.xlabel('Date')
plt.ylabel('Profit')
plt.title('Profit Over Time')
plt.legend()
plt.grid(True)
plt.show()

'''
The line plots provide insights into the trends in sales and profit over time:

Sales Over Time:

The sales plot shows variations over time, with certain periods demonstrating noticeable peaks.

These peaks could correspond to specific events, seasons, or promotions that led to increased sales.

Profit Over Time:

The profit plot also shows variations, with some similarities to the sales trends.

The correlation between sales and profit could be further analyzed to understand how different factors affect profitability.

These visualizations can serve as a starting point for a more in-depth analysis of the data. By examining the relationship between different features (such as market segments, countries, products, and discounts), additional insights can be gained to inform business strategies and decision-making.
'''






