import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
data = pd.read_csv('nationality.csv')

# Grouping by period, scheme description, and nationality (including 'All'), and summing the recipients
grouped_data = data.groupby(['period', 'scheme_description', 'nationality'])['recipients'].sum().reset_index()

# Extracting the total recipients for each scheme in each period directly from the 'All' rows
total_recipients = grouped_data[grouped_data['nationality'] == 'All'][['period', 'scheme_description', 'recipients']]

# Merging the grouped data with the total recipients to calculate the fraction
merged_data = pd.merge(grouped_data, total_recipients, on=['period', 'scheme_description'], suffixes=('', '_total'))

# Calculating the fraction and converting it to a percentage for all nationalities except 'All'
merged_data['percentage'] = merged_data.apply(lambda row: (row['recipients'] / row['recipients_total']) * 100 if row['nationality'] != 'All' else None, axis=1)

# Pivoting the table for a better view
pivot_table = merged_data.pivot_table(index=['period', 'scheme_description'], columns='nationality', values='percentage', fill_value=0)

# Sorting the data so that each scheme is grouped together, while keeping the period and scheme description as the index
sorted_pivot_table = pivot_table.sort_index(level=['scheme_description', 'period'])

# Saving the sorted pivot table to a new CSV file which we will use to generate the figures
sorted_pivot_table.to_csv('sorted_nationality_percentage_by_scheme_and_quarter.csv')


# Lets use the newly generated CSV 
data = pd.read_csv('sorted_nationality_percentage_by_scheme_and_quarter.csv')

# Filtering out the Irish nationals column
data_non_irish = data.drop(columns=['Irish nationals'])

# Set colours for each of the nationality groups so they can easily be distinguished
colors = ["#E69F00", "#56B4E9", "#009E73", "#CC79A7"]
sns.set_palette(sns.color_palette(colors))

# Create a variable which represents the non-Irish citizen population. The figure of 12% is from the CSO website.
non_irish_population_percentage = 12

# Getting a list of unique schemes
unique_schemes = data_non_irish['scheme_description'].unique()

# Creating the stacked bar charts
for scheme in unique_schemes:
    # Filtering data for the current scheme
    scheme_data = data_non_irish[data_non_irish['scheme_description'] == scheme]

    # Dropping the scheme_description column for plotting
    scheme_data_plot = scheme_data.drop(columns=['scheme_description'])

    # Setting index to period for plotting
    scheme_data_plot.set_index('period', inplace=True)

    # Plotting stacked bar chart
    scheme_data_plot.plot(kind='bar', stacked=True, color=colors, figsize=(12, 6))
    plt.title(f'Recipients of {scheme} by Broad Nationality Group (Excl. Irish Citizens)')

    # Adding a horizontal line for non-Irish citizen population
    plt.axhline(y=non_irish_population_percentage, color='purple', linestyle='--', 
                label='Non-Irish Citizen Population % (2022)')

    plt.xticks(rotation=45)
    plt.ylabel('Percentage (%)')
    plt.xlabel('Period (Year and Quarter)')
    plt.legend(title='Nationality / Population %', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
