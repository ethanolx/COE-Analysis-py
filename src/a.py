import pandas as pd
import matplotlib.pyplot as plt

# Load Data
pqp = pd.read_csv('./data/coe-results-prevailing-quota-premium.csv')
coe = pd.read_csv('./data/coe-results.csv')
deregistered = pd.read_csv(
    './data/motor-vehicles-de-registered-under-vehicle-quota-system-vqs.csv')
registered = pd.read_csv(
    './data/new-registration-of-motor-vehicles-under-vehicle-quota-system-vqs.csv')
population = pd.read_csv('./data/motor-vehicle-population-under-vehicle-quota-system.csv')

c = pd.merge(left=coe, right=pqp, on=['month', 'vehicle_class'])
d = pd.merge(left=pd.merge(left=deregistered, right=registered, on=[
             'month', 'category'], suffixes=['_of_deregistered', '_of_registered']), right=population, on=['month', 'category'], how='inner')

every = pd.merge(left=c, right=d, left_on=[
                 'month', 'vehicle_class'], right_on=['month', 'category'])

every = every.drop(columns='category')

a = every['month'].str.split(pat='-', expand=True)
every['year'] = a[0].apply(int)
every['month'] = a[1].apply(int)

# COE by category
# every.groupby(by='vehicle_class').boxplot(column='premium') # type: ignore

# COE trend
# every.groupby(by='month').median().plot(kind='line', y='premium')

# Received by quota
# every.plot(kind='scatter', x='quota', y='bids_received')

# plt.plot(every['year'].unique(), every.groupby(by='year').mean()['number_de'])
# plt.plot(every['year'].unique(), every.groupby(by='year').mean()['number_re'])

# a = every.pivot_table(index='year', columns='vehicle_class', values='quota')
# a.plot()
every.to_csv(path_or_buf='./data/out/final.csv')
print(every.head())
print(every.columns.values)
plt.show()
