#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:26:44 2021

@author: karanrajmokan
"""
import pandas as pandas
import warnings
warnings.filterwarnings("ignore")
from apyori import apriori

def Repeat(x): 
    _size = len(x) 
    repeated = [] 
    for i in range(_size): 
        k = i + 1
        for j in range(k, _size): 
            if x[i] == x[j] and x[i] not in repeated: 
                repeated.append(x[i])
                
    mydict = {i:x.count(i) for i in repeated}
    return mydict

'''

#####################################################################################################

INFORMATION:

For the total 541910 records, 45222 unique Invoices are found
For the total 541910 records, 4224 unique Items are found

For the first 100000 records, 4657 unique Invoices are found
For the first 100000 records, 3050 unique Items are found

For the first 10000 records, 512 unique Invoices are found (512 unique invoices for 10080 records)
For the first 10000 records, 1982 unique Items are found (1985 unique items for 10080 records) 

####################################################################################################

'''

pandas.set_option('display.max_columns', None)
pandas.set_option('max_colwidth', None)
dataFrame = pandas.read_excel('Online Retail.xlsx')

simplifiedDataFrame = dataFrame.head(10080)
simplifiedDataFrame['Description'] = simplifiedDataFrame['Description'].str.strip()
simplifiedDataFrame['Description'] = simplifiedDataFrame['Description'].str.strip('.')

uniqueInvoices = simplifiedDataFrame.InvoiceNo.unique()
uniqueItems = simplifiedDataFrame.Description.unique()       

listOfTransactionData=[]
grouped = simplifiedDataFrame.groupby(simplifiedDataFrame.InvoiceNo)
for i in uniqueInvoices:
    listOfTransactionData.append(grouped.get_group(i)['Description'])

for i in listOfTransactionData:
    i.drop_duplicates(inplace = True)

itemSet=[]
for i in listOfTransactionData:
    temp=[]
    for j in i:
        if type(j) == str:
            temp.append(j)
    itemSet.append(temp)

'''

############################################################################

#PSUEDOCODE (CHECKING CODE)

items=["HAND WARMER UNION JACK", "HAND WARMER SCOTTY DOG DESIGN",
       "HAND WARMER OWL DESIGN", "WHITE HANGING HEART T-LIGHT HOLDER", "PAPER CHAIN KIT 50'S CHRISTMAS"]


noOfTransactionsContainingItemA=0
noOfTransactionsContainingItemB=0
noOfTransactionsContainingItemC=0
noOfTransactionsContainingItemD=0
noOfTransactionsContainingItemE=0
noOfTransactionsContainingAandB=0


for i in listOfTransactionData:
    
    ans = Repeat(i['Description'].tolist())
    for j in items:
        for key,value in ans.items():
            if j == key:
                print(i.InvoiceNo.unique(),key,value)
                
    descriptionData = i['Description'].tolist()
    
    if items[0] in descriptionData:
        noOfTransactionsContainingItemA+=1
    if items[1] in descriptionData:
        noOfTransactionsContainingItemB+=1
    if items[2] in descriptionData:
        noOfTransactionsContainingItemC+=1
    if items[3] in descriptionData:
        noOfTransactionsContainingItemD+=1
    if items[4] in descriptionData:
        noOfTransactionsContainingItemE+=1    
    if items[0] in descriptionData and items[1] in descriptionData:
        noOfTransactionsContainingAandB+=1

frequentItems=simplifiedDataFrame['Description'].value_counts()[:5].sort_values(ascending=False).to_dict()
totalTransactions=len(uniqueInvoices)

print(len(uniqueInvoices))
print(len(uniqueItems))
print(frequentItems)

print()
print("Number of transactions containing item HAND WARMER UNION JACK = " + str(noOfTransactionsContainingItemA))
print("Number of transactions containing item HAND WARMER SCOTTY DOG DESIGN = " + str(noOfTransactionsContainingItemB))
print("Number of transactions containing item HAND WARMER OWL DESIGN = " + str(noOfTransactionsContainingItemC))
print("Number of transactions containing item WHITE HANGING HEART T-LIGHT HOLDER = " + str(noOfTransactionsContainingItemD))
print("Number of transactions containing item PAPER CHAIN KIT 50'S CHRISTMAS = " + str(noOfTransactionsContainingItemE))

supportOfA=round(noOfTransactionsContainingItemA/totalTransactions,3)
supportOfB=round(noOfTransactionsContainingItemB/totalTransactions,3)
supportOfC=round(noOfTransactionsContainingItemC/totalTransactions,3)
supportOfD=round(noOfTransactionsContainingItemD/totalTransactions,3)
supportOfE=round(noOfTransactionsContainingItemE/totalTransactions,3)

print()
print("The support of item HAND WARMER UNION JACK = " + str(supportOfA))
print("The support of item HAND WARMER SCOTTY DOG DESIGN = " + str(supportOfB))
print("The support of item HAND WARMER OWL DESIGN = " + str(supportOfC))
print("The support of item WHITE HANGING HEART T-LIGHT HOLDER = " + str(supportOfD))
print("The support of item PAPER CHAIN KIT 50'S CHRISTMAS = " + str(supportOfE))

confidenceOfA_B=round(noOfTransactionsContainingAandB/noOfTransactionsContainingItemA,3)
liftOfA_B=round(confidenceOfA_B/supportOfB,3)

print()
print("The confidence of HAND WARMER UNION JACK and HAND WARMER SCOTTY DOG DESIGN = " + str(confidenceOfA_B))
print("The lift of HAND WARMER UNION JACK and HAND WARMER SCOTTY DOG DESIGN = " + str(liftOfA_B))


###################################################################################

RESPECTIVE OUTPUTS:

512
1983
{'HAND WARMER UNION JACK': 59, 
 'HAND WARMER SCOTTY DOG DESIGN': 58, 
 'WHITE HANGING HEART T-LIGHT HOLDER': 57, 
 'HAND WARMER OWL DESIGN': 57, 
 "PAPER CHAIN KIT 50'S CHRISTMAS": 52}

Number of transactions containing item HAND WARMER UNION JACK = 54
Number of transactions containing item HAND WARMER SCOTTY DOG DESIGN = 48
Number of transactions containing item HAND WARMER OWL DESIGN = 53
Number of transactions containing item WHITE HANGING HEART T-LIGHT HOLDER = 55
Number of transactions containing item PAPER CHAIN KIT 50'S CHRISTMAS = 47

The support of item HAND WARMER UNION JACK = 0.105
The support of item HAND WARMER SCOTTY DOG DESIGN = 0.094
The support of item HAND WARMER OWL DESIGN = 0.104
The support of item WHITE HANGING HEART T-LIGHT HOLDER = 0.107
The support of item PAPER CHAIN KIT 50'S CHRISTMAS = 0.092

The confidence of HAND WARMER UNION JACK and HAND WARMER SCOTTY DOG DESIGN = 0.407
The lift of HAND WARMER UNION JACK and HAND WARMER SCOTTY DOG DESIGN = 4.33

#####################################################################################
'''    


association_rules = apriori(itemSet, min_support=0.065, min_confidence=0.5, min_lift=1, min_length=2)

count=0
association_results=[]
for item in association_rules:
    pair = item[0] 
    items = [x for x in pair]
    if len(items)>1:
        count+=1
        association_results.append(item)
                
        print("Rule: " + items[0] + " -> " + items[1])
        print("Support: " + str(item[1]))
        print("Confidence: " + str(item[2][0][2]))
        print("Lift: " + str(item[2][0][3]))
        print("=====================================")


#print(association_results)

'''

#####################################################################################

OBSERVATION:

FOR ITERATION-1 (min_support=0.001, min_confidence=0.1, min_lift=1, min_length=2),
the result size is 467138

Rule: ZINC WILLIE WINKIE  CANDLE STICK -> ZINC METAL HEART DECORATION
Support: 0.001953125
Confidence: 0.125
Lift: 4.923076923076923
=====================================


--------------------------------------------------------------------------------------
FOR ITERATION-2 (min_support=0.01, min_confidence=0.15, min_lift=1, min_length=2),
the result size is 108729

Rule: 10 COLOUR SPACEBOY PEN -> HAND WARMER BIRD DESIGN
Support: 0.01171875
Confidence: 0.46153846153846156
Lift: 5.495527728085868
=====================================


--------------------------------------------------------------------------------------
FOR ITERATION-3 (min_support=0.02, min_confidence=0.2, min_lift=1, min_length=2),
the result size is 32883

Rule: WOOD 2 DRAWER CABINET WHITE FINISH -> WHITE METAL LANTERN
Support: 0.021484375
Confidence: 0.4583333333333333
Lift: 21.333333333333332
=====================================


---------------------------------------------------------------------------------------
FOR ITERATION-4 (min_support=0.05, min_confidence=0.5, min_lift=1, min_length=2),
the result size is 6

Rule: HAND WARMER BIRD DESIGN -> HAND WARMER OWL DESIGN
Support: 0.052734375
Confidence: 0.627906976744186
Lift: 6.065818341377797
=====================================
Rule: HAND WARMER RED RETROSPOT -> HAND WARMER OWL DESIGN
Support: 0.0546875
Confidence: 0.5283018867924528
Lift: 6.440251572327044
=====================================
Rule: HAND WARMER SCOTTY DOG DESIGN -> HAND WARMER OWL DESIGN
Support: 0.068359375
Confidence: 0.660377358490566
Lift: 7.044025157232704
=====================================
Rule: KNITTED UNION FLAG HOT WATER BOTTLE -> RED WOOLLY HOTTIE WHITE HEART
Support: 0.05859375
Confidence: 0.7317073170731707
Lift: 8.9198606271777
=====================================
Rule: WHITE HANGING HEART T-LIGHT HOLDER -> KNITTED UNION FLAG HOT WATER BOTTLE
Support: 0.05078125
Confidence: 0.6341463414634146
Lift: 5.903325942350333
=====================================
Rule: PAPER CHAIN KIT VINTAGE CHRISTMAS -> PAPER CHAIN KIT 50'S CHRISTMAS
Support: 0.0546875
Confidence: 0.5957446808510638
Lift: 6.932301740812378
=====================================


----------------------------------------------------------------------------------------
FOR ITERATION-5 (min_support=0.065, min_confidence=0.5, min_lift=1, min_length=2),
the result size is 1
Rule: HAND WARMER SCOTTY DOG DESIGN -> HAND WARMER OWL DESIGN
Support: 0.068359375
Confidence: 0.660377358490566
Lift: 7.044025157232704
=====================================


---------------------------------------------------------------------------------------
'''


