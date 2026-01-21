#1.Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#2.Generate or Load Data
np.random.seed(0)

temps=np.random.normal(75,10,30)
temps[5]=120
temps[15]=20
df=pd.DataFrame({'Day':pd.date_range(start='2025-06-01',periods=30,freq='D'),
                 'City':['New York']*30,
                 'Temperature':temps})


#3.Initial Data Explorationprint(df,'\n')
print(df.head(),'\n')
print(df.info(),'\n')
print(df.describe(),'\n')
print(df.isnull().sum(),'\n')


#4.Detect Outliers Using Z-score
mean=df['Temperature'].mean()
std=df['Temperature'].std()
df['Z-Score']=(df['Temperature']-mean)/std
df['Outlier']=df['Z-Score'].abs()>2
print(f'mean{mean},sdt:{std}','\n',df,'\n')

#5.Adjust Outliers (Capping)
upper=mean+2*std
lower=mean-2*std
df['Adjusted_Temp']=df['Temperature'].where(df['Outlier']==False,
                                            np.where(df['Z-Score']>2,upper,lower))
print(f'lower:{lower},upper{upper}','\n',df,'\n')

#6. Additional Pandas Features
#a.Filtering & Sorting
# Only outliers
outliers_df=df[df['Outlier']].sort_values('Temperature',ascending=False)
print(outliers_df)

#b.Apply a Function (e.g., classify day)
def classify_temp(t):
    if t<60:
        return 'Cold'
    elif 60<=t<80:
        return'Moderate'
    else:
        return 'Hot'
df['Temp_Category']=df['Adjusted_Temp'].apply(classify_temp)
print(df)

#c.GroupBy (if multiple cities/dates) 
#df.groupby('City')['Adjusted_Temp'].mean()
#print(df)


#d.Export to CSV
df.to_csv('cleaned_temperature_data.csv',index=False)
print(df)


#7.Visualization
plt.figure(figsize=(12,6))
plt.plot(df['Day'],df['Temperature'],label='Original',marker='o')
plt.plot(df['Day'],df['Adjusted_Temp'],label='Adjusted',marker='x')
plt.xlabel('Date')
plt.ylabel('Temperature (°F))')
plt.title('Temperature Over Time(Original vs Adjusted)')
plt.legend()
plt.grid(True)
plt.show()


#Histogram

df[['Temperature','Adjusted_Temp']].plot(kind='hist',bins=20,alpha=0.6,figsize=(8,5))
plt.title('Histogram of Temperatures')
plt.show()

