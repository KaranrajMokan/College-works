#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 18:01:55 2021

@author: karanrajmokan
"""

import pandas as pd
from numpy import random
import matplotlib.pyplot as plotting
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', None)
df = pd.read_csv("auto-mpg.data",header=None, delim_whitespace=True)
df = df.rename(columns={0: 'mpg', 1: 'cylinders', 2: 'displacement', 3: 'horsepower',
                        4: 'weight', 5: 'acceleration', 6: 'modelyear', 7: 'origin',
                        8: 'carname'})


print("\nNumber of unique cars in the dataset = ",len(df['carname'].unique()))
print("Total number of attributes in the dataset = ",len(df.columns))



cars=df['carname']
mpg=df['mpg']
distinct_car_companies=[]
for i in cars:
    i=i.split(" ")
    if i[0] not in distinct_car_companies:
        distinct_car_companies.append(i[0])
        
print("\nNumber of distinct car companies =",len(distinct_car_companies))
print("The car with the best mpg is",df.loc[df['mpg'] == mpg.max(), 'carname'].iloc[0],
      "and its mpg is",mpg.max())

eight_cylinders_cars=df.loc[df['cylinders'] == 8, 'carname']
eight_cylinders_car_companies=[]
for i in eight_cylinders_cars:
    i=i.split(" ")
    eight_cylinders_car_companies.append(i[0])

counter = 0
frequent_car_company = eight_cylinders_car_companies[0]   
for i in eight_cylinders_car_companies: 
    curr_frequency = eight_cylinders_car_companies.count(i) 
    if(curr_frequency> counter): 
       counter = curr_frequency 
       frequent_car_company = i

print("The car company which produced most 8-cylinder cars is",
      frequent_car_company)
three_cylinders=df.loc[df['cylinders'] == 3, 'carname'].tolist()
print("The names of cars with three cylinders are",', '.join(three_cylinders))
print()



df['horsepower'] = df['horsepower'].apply(lambda x: float(x.replace('?','NaN')))
print(df.describe(percentiles=[0.5])[1:])
print()



print("The histograms of the attributes are given below:")
df.hist(bins=5,grid=False,layout=[2,4],figsize=[9,10])
plotting.show()
print()



print("The scatterplot of weight vs mpg is given below:")
df.plot.scatter(x='weight', y='mpg', c='#5A9')
plotting.show()
print("\nThe correlation coefficient between weight and mpg is",
      df['weight'].corr(df['mpg']))
print()




print("\nBEFORE ADDING RANDOM NOISE")
print("The scatterplot of model year vs cylinders is given below:")
df.plot.scatter(x='modelyear', y='cylinders', c='DarkBlue',alpha=0.6)
plotting.show()
print()

cylinders=list(df['cylinders'])
modelyear=list(df['modelyear'])

for i in range(len(cylinders)):
    cylinders[i]+=random.randint(0,1000)*2+10
    modelyear[i]+=random.randint(0,1000)*3+15
    
    
print("\nAFTER ADDING RANDOM NOISE")
print("The scatterplot of model year vs cylinders is given below:")
plotting.scatter(modelyear,cylinders, c='DarkBlue',alpha=0.6)
plotting.show()
print() 




print("The scatterplot of horsepower vs acceleration is given below:")
df.plot.scatter(x='horsepower', y='acceleration', c='black',alpha=0.6)
plotting.show()
print()

print("The scatterplot of displacement vs weight is given below:")
df.plot.scatter(x='displacement', y='weight', c='DarkGreen',alpha=0.6)
plotting.show()
print()




dictValues = {}
for i in df['modelyear']:
    if i not in dictValues.keys():
        newCars = df.loc[df['modelyear'] == i, 'carname']
        i+=1900
        dictValues[i]=newCars.shape[0]

x=list(dictValues.keys())
y=list(dictValues.values())

print("The time series plot between years and number of cars produced is shown below:")
plotting.plot(x, y, color='#4b0082', linewidth=4, marker='h', markerfacecolor='lightgreen',
              markeredgewidth=2, markersize=12)
plotting.xlabel('Year')  
plotting.ylabel('No. of cars produced')  
plotting.title('Year vs No. of cars produced!') 
plotting.show() 
print()



print("The correlation heatmap is shown below:")
correlation = df.corr()
heatmap = sns.heatmap(correlation, cbar=True, annot=True, cmap="YlGnBu", linewidths=.5)
heatmap.set_title("Correlation heatmap\n")
print()


