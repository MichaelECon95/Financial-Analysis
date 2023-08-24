import pandas as pd
import matplotlib.pyplot as plt

# Path to the dataset
file_path = '/.../Financials.csv'

# Loading the dataset
data = pd.read_csv(file_path)

#Step 1: Clean Column Names

# Removing leading and trailing spaces from the column names
data.columns = data.columns.str.strip()

#Step 2: Remove Special Characters and Convert to Numeric
# List of columns that need cleaning
columns_to_clean = [
    'Units Sold', 'Manufacturing Price', 'Sale Price', 'Gross Sales', 'Discounts', 'Sales', 'COGS', 'Profit'
]
# Cleaning the specified columns
for column in columns_to_clean:
    # Removing special characters
    data[column] = data[column].replace('[\$,(),-]', '', regex=True)
    # Converting to float using to_numeric, setting errors='coerce' to handle empty strings
    data[column] = pd.to_numeric(data[column], errors='coerce')

# Converting the 'Date' column to a datetime data type
data['Date'] = pd.to_datetime(data['Date'])

# Displaying the first few rows after preprocessing
data.head()

# Step 3: Plotting Sales and Profit with Respect to Timeline

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

--------------------------------------------------------

#Diving into the dataset and identify three key topics of discussion that can provide insights for informed business strategies and assist in decision-making.
# We'll create visualizations for each topic and provide summaries and recommendations.

# Visualization 1: Sales and Profit Analysis by Market Segment

# Visualization:
# Bar chart to visualize the sales and profit across different market segments.
# This will help us understand which segments are performing well and where there might be opportunities for growth or improvement.

# Grouping data by Segment and summing sales and profit
segment_data = data.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()

# Plotting Sales and Profit by Segment
plt.figure(figsize=(12, 6))
bar_width = 0.35
index = range(len(segment_data['Segment']))

plt.bar(index, segment_data['Sales'], bar_width, label='Sales')
plt.bar([i + bar_width for i in index], segment_data['Profit'], bar_width, label='Profit')

plt.xlabel('Segment')
plt.ylabel('Amount')
plt.title('Sales and Profit by Market Segment')
plt.xticks([i + bar_width / 2 for i in index], segment_data['Segment'])
plt.legend()
plt.grid(True)
plt.show()

# Returning the data for summary
segment_data

'''
Summary:
The bar chart represents the sales and profit across different market segments. Here's what we observed:

Government: Highest sales and profit among all segments.
Enterprise: High sales but relatively low profit, indicating potential inefficiencies.
Small Business: Substantial sales with a moderate profit margin.
Midmarket and Channel Partners: Lower sales and profit.
The choice of a bar chart allows us to clearly compare both sales and profit across different market segments.

Recommendations:
Investigate Enterprise Segment: The high sales but low profit in the Enterprise segment may suggest inefficiencies that need to be addressed. Analyzing costs, pricing strategies, and discounting in this segment may reveal opportunities for improvement.
Explore Growth in Midmarket and Channel Partners: These segments have lower sales and profit. Understanding the market needs and tailoring products or services accordingly might unlock growth potential.
'''

----------------------------------------------------------------

# Visualization 2: Sales and Profit Analysis by Country/Region

# Visualization: 
# We'll create a a horizontal bar chart to visualize both sales and profit for each country/region.
# This will allow us to compare sales and profit across countries more easily and identify specific areas for focus.

# Plotting Sales and Profit by Country/Region using horizontal bar chart
country_data = data.groupby('Country').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
plt.figure(figsize=(12, 8))
index = range(len(country_data['Country']))

plt.barh(index, country_data['Sales'], 0.4, label='Sales', color='blue', edgecolor='black')
plt.barh([i + 0.4 for i in index], country_data['Profit'], 0.4, label='Profit', color='orange', edgecolor='black')

plt.ylabel('Country/Region')
plt.xlabel('Amount')
plt.title('Sales and Profit by Country/Region')
plt.yticks([i + 0.4 / 2 for i in index], country_data['Country'])
plt.legend()
plt.grid(True)
plt.gca().invert_yaxis() # Invert y-axis to have the largest values on top
plt.show()

'''
Summary :
The horizontal bar chart represents sales and profit across different countries or regions. 
The following observations can be made:

Top Countries: Countries like the USA, Canada, France, Germany, and Mexico are the top performers in both sales and profit.

Other Countries: There is a varied relationship between sales and profit across other countries, and individual performance can be clearly seen.

The choice of a horizontal bar chart allows us to view individual countries and directly compare both sales and profit, providing a more comprehensive understanding of market performance.

Recommendations:
Focus on High-Performing Markets: Invest in top-performing markets to sustain growth.
Analyze Underperforming Markets: Investigate countries where the relationship between sales and profit is not aligned, focusing on underlying reasons for discrepancies.
'''

---------------------------------------------------------------------

# Visualization 3: Analysis of Discounts and Their Impact on Sales and Profit
#Visualization: We'll create a combonation chart.
# We aim to represent the relationship between sales, profit, and discount percentages in an appealing and informative manner.
# A combination chart that includes both a line chart for total revenue and a stacked area chart for sales and profit could be a great choice.
# This visualization would allow us to see the trends and comparisons clearly and would present the data in an engaging way.

# Calculating the Total Revenue again as the sum of Sales and Profit

# Calculating the Discount Percentage
data['Discount Percentage'] = (data['Discounts'] / data['Gross Sales']) * 100

# Binning the discount percentage into categories
data.loc[:, 'Discount Category'] = pd.cut(data['Discount Percentage'], bins=[0, 5, 10, 15, 20, 25, 30, 100], labels=['0-5%', '5-10%', '10-15%', '15-20%', '20-25%', '25-30%', '30%+'])

# Grouping data by Discount Category and summing sales and profit
discount_bar_data = data.groupby('Discount Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()

# Filtering the data for discount percentage ranges up to 15-20%
discount_bar_data_filtered = discount_bar_data[discount_bar_data['Discount Category'].isin(['0-5%', '5-10%', '10-15%', '15-20%'])]

# Using .loc to calculate and assign the 'Total Revenue'
discount_bar_data_filtered.loc[:, 'Total Revenue'] = discount_bar_data_filtered['Sales'] + discount_bar_data_filtered['Profit']

# Plotting the data
plt.figure(figsize=(12, 6))
plt.fill_between(discount_bar_data_filtered['Discount Category'], 0, discount_bar_data_filtered['Sales'], label='Sales', color='blue', alpha=0.5)
plt.fill_between(discount_bar_data_filtered['Discount Category'], discount_bar_data_filtered['Sales'], discount_bar_data_filtered['Total Revenue'], label='Profit', color='orange', alpha=0.5)
plt.plot(discount_bar_data_filtered['Discount Category'], discount_bar_data_filtered['Total Revenue'], label='Total Revenue', color='green', marker='o')

plt.xlabel('Discount Percentage Range')
plt.ylabel('Amount')
plt.title('Sales, Profit, and Total Revenue vs Discount Percentage (0% to 15-20%, Combination Chart)')
plt.legend()
plt.grid(True)
plt.show()

#Visual shows relationship between sales, profit, and discount percentages (from 0% to 15-20%) 

'''
Sales (Blue Area): This area represents the sales for different discount percentage ranges, forming the base of the chart.

Profit (Orange Area): Stacked on top of the sales area, this represents profit for each discount range, allowing us to see how profit adds to the total revenue.

Total Revenue (Green Line): This line plot provides a continuous view of the overall performance, showing the sum of sales and profit for each discount percentage range.

Recommendations:
1. Optimize Discount Strategies:
Low Discount Range (0-5%): This range has shown the highest sales and profit. Offering minimal discounts might be an effective strategy for certain products or customer segments.
Moderate Discount Range (5-15%): There is a noticeable decrease in both sales and profit as the discount percentage increases.
Careful analysis is needed to determine the optimal discount levels that maximize profitability without sacrificing sales.

2. Monitor the Impact of Discounts on Profit:
The visualization highlights how sales and profit are affected differently by discounts.
Monitoring and analyzing the impact of different discount levels on profit margins can guide pricing and discounting strategies to ensure they align with overall business goals.

3. Customize Promotions Based on Insights:
Understanding the relationship between discounts, sales, and profit can help in customizing promotions for specific products, seasons, or customer segments.
Tailoring promotions based on these insights can lead to more effective marketing campaigns.

4. Consider Additional Factors:
While discounts play a significant role in sales and profit, other factors such as product type, customer behavior, seasonality, and market competition should also be considered.
A comprehensive analysis that includes these factors can lead to more nuanced and effective strategies.


Summary :
The analysis of discounts and their impact on sales and profit provides valuable insights that can guide pricing and promotional strategies.
The key is to find a balance between attracting customers through discounts and maintaining healthy profit margins. 

Continuous monitoring, testing different discount levels, and integrating insights from other aspects of the business are crucial for implementing effective and profitable discount strategies.

'''

--------------------------------------------------------------

'''
Overall Summary:

The additional analysis of discounts enhances our understanding of sales dynamics and customer behavior.

By studying the relationship between discounts, sales, and profit, businesses can create informed pricing and promotional strategies that drive sales without eroding profit margins.

Together with the insights gained from the previous topics (market segments, country/region performance, and product trends), this comprehensive analysis provides a robust foundation for decision-making, strategic planning, and continuous improvement in various aspects of the business.

These analyses collectively enable the identification of growth opportunities, optimization of marketing and sales efforts, and alignment of business strategies with market demands and customer preferences.

By leveraging data-driven insights, businesses can enhance their competitive edge and achieve sustainable growth and success.

'''

