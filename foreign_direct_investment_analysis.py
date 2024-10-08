# -*- coding: utf-8 -*-
"""Foreign Direct Investment Analysis.ipynb

**Importing Libraries/ Dependencies**
"""

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

"""**Loading Data**"""

FDI = pd.read_csv('/content/FDI data.csv')

"""**Data Exploration and Cleaning**"""

FDI.shape

FDI.head()

FDI.style.set_caption('Amount in US$ Millions').format(precision=2)

FDI.columns

"""**Column Details:**

**There are two types of columns:**



1.   **The first column is the 'Sector' column in which there are 63**
     **different sectors that received FDI from 2001-01 to 2016-17**.
2.   **The other columns are 'Year-wise' columns in which we can see how much**
       **different sectors received invesment from 2001-01 to 2016-17**


"""

Year = ['2000-01', '2001-02', '2002-03', '2003-04', '2004-05',
       '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11',
       '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17']
Sectors = ['Sector']

# extracting detailed information
FDI.info()

# checking for null values
pd.isnull(FDI).sum()

# checking for duplicate values
FDI.duplicated().value_counts()

#Creating Average Exchange Rate list  :- Reference(Rbi website)
Rates = [45.68,47.69,48.39,45.95,44.93,44.27,45.24,40.26,45.99,
         47.44,45.56,47.92,54.40,60.50,61.14,65.46,67.07]

"""**Converting American '$' to Indian '₹' :**"""

#Creating a function to Convert FDI's value from USD to INR
def multiply_columns(df, col_list,num):
    for col in col_list:
        df[col] = df[col] * Rates[col_list.index(col)]/10
    return df

FDI_InUSD=FDI.copy()
FDI_02 = multiply_columns(FDI, Year, Rates)

#FDI INFLOWS (Amount in ₹ Crores)
FDI_02.style.set_caption("FDI INFLOWS (Amount in ₹ Crores)").format(precision=2)

"""**Unpivoting/Melting/Reshaping Dataframes from wide to long format**"""

# Unpivoting melt Dataframe
melt = pd.melt(FDI_InUSD, id_vars = Sectors, value_vars = Year, var_name='Year',
    value_name='FDI(US$ Million)',ignore_index=True)
melt=round(melt,2)
melt

#Unpivoting melt01 Dataframe
melt01 = pd.melt(FDI_02, id_vars = Sectors, value_vars = Year, var_name='Year',
    value_name='FDI(₹ Crores)',ignore_index=True)
melt01=round(melt01,2)
melt01

# Merging the FDI(US$ Million) column of melt Dataframe into melto1 Dataframe
Merged=melt01.merge(melt,how='left')
Merged

#Sorting the Sectors and Year columns
Sorted = Merged.sort_values(['Sector','Year'], ignore_index=True)
Sorted

#Repalcing some Long values of Sector Column to Short form
Sorted = Sorted[['Sector','FDI(₹ Crores)', 'FDI(US$ Million)'
                 ,]].replace(["CONSTRUCTION DEVELOPMENT: Townships, housing, built-up infrastructure and construction-development projects"
                              ,"SERVICES SECTOR (Fin.,Banking,Insurance,Non Fin/Business,Outsourcing,R&D,Courier,Tech. Testing and Analysis, Other)"
                              ,'TEA AND COFFEE (PROCESSING & WAREHOUSING COFFEE & RUBBER)']
                             ,["CONSTRUCTION DEVELOPMENT","SERVICES SECTOR",'TEA AND COFFEE'])

"""**Sector-wise Total FDI 2000-17**"""

#Grouping by Sector column to find Total FDI Inflow per Sector from FY2000-01 to FY2016-17
Sectorwise_fdi = Sorted.groupby('Sector').sum()
Sectorwise_fdi.sort_values(by='FDI(US$ Million)',ascending=False)

Merged.to_csv('clean_FDI.csv',index=False)

"""**Conclusion**"""

#Creating a new column with year 2000-17 in Sectorwise_fdi Dataframe
Sectorwise_fdi['Year'] = '2000-17'

Sectorwise_fdi = Sectorwise_fdi[['Year','FDI(₹ Crores)', 'FDI(US$ Million)']]
Sectorwise_fdi['% of Total Inflows'] = (Sectorwise_fdi['FDI(₹ Crores)']/ Sectorwise_fdi['FDI(₹ Crores)'].sum())*100

Sort_val1 = Sectorwise_fdi.sort_values('FDI(₹ Crores)',ascending=False)
Sort_val= Sort_val1.style.set_caption("SECTOR-WISE FDI INFLOWS").format(precision=3)
Sort_val

"""**The Sectoral composition of FDI over the period of April 2000 to June 2017, we** **can find that the largest recipient of such investment is service sector (Financial and non-financial services)**. **The share of this sector in FDI flows is 17 % of the inflow total foreign direct investment.**

**The foreign investors are interested in mainly financial services due its profit generating advantage. This sector gives scope for the foreign investor to takes back the profits to the home country. As service sector the services are consumed in the host country and there by generating outflow of funds from the host country.**

**The second recipient is Computer software and hardware which shares 7% of total FDI. Telecommunication,, Construction Development , Automobile industry,Trade, Drugs and pharmaceuticals, Chemical ( Other than Fertilizers),Power, Construction,Hotel and tourism contribute around 7%,6%, 5%, 4.7%, 4%, 4%, 3%, 3% .**

**Their is very low interset towards sectors like Coir, Defence Industries, Mathematical,surveying and drawing Instruments, Coal Production and there are around 28 to 30 sectors where share is less than or equal to 1%.**
"""