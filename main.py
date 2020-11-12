"""
# Octagon data science challenge 2020
## Data Transformation portion
#### A study was conducted between 2016-2019 containing users of the drug sorafenib, a TKI generally used in treating hepatocellular carcinoma. The raw data contained 2379 rows of information that were grouped data. For example, the first row indicated that there were two members from Alberta, regardless if the patient used another anti-cancer therapy concurrently, regardless of sex, between the ages 18-19.
#### Given that the goal of this challenge was to conduct survival analysis, this data was not suitable for such an analysis and had to be transformed into a usable format. The function IndividualLevelData1 converts data into induvidual level information, giving information about each participants province, age, concurrent treatment status, sex, and outcome of the trail.
"""

import pandas as pd
import math
import csv

import sys
print(sys.version)

octoDF = pd.read_csv('octogonData_change1.csv')
octoDF.shape
#octoDF.columns
octoDF.head()


# APPENDING COUNTS:
## Data aligned as [Prov, Con-ACT, Sex, Age, event, censored, time]

def IndividualLevelData1(numOfParticipants, groupOfInterest, knownOutcome):
    alldata = {}
    counts = 1
    # knownOutcome = 0
    allColumns = groupOfInterest.columns
    for cols in allColumns:
        PersonWiseData = []
        if cols not in ['Prov', 'Con_ACT', 'Sex', 'Age', 'Measure']:
            if isinstance(groupOfInterest[cols].iloc[1], float) and not np.isnan(
                    groupOfInterest[cols].iloc[1]):  # !=True: #: type(groupOfInterest[cols].iloc[2]) == float:
                for events in range(int(groupOfInterest[cols].iloc[1])):
                    PersonWiseData.append(groupOfInterest['Prov'].iloc[1])
                    PersonWiseData.append(groupOfInterest['Con_ACT'].iloc[1])
                    PersonWiseData.append(groupOfInterest['Sex'].iloc[1])
                    PersonWiseData.append(groupOfInterest['Age'].iloc[1])
                    PersonWiseData.append(1)
                    PersonWiseData.append(0)
                    PersonWiseData.append(cols[1:])
                    alldata[counts] = PersonWiseData
                    counts += 1
                    # numOfParticipants -= 1
                    knownOutcome += 1
                    PersonWiseData = []
            if isinstance(groupOfInterest[cols].iloc[2], float) and not np.isnan(
                    groupOfInterest[cols].iloc[2]):  # != True: #type(groupOfInterest[cols].iloc[2]) == float64:
                for events in range(int(groupOfInterest[cols].iloc[2])):
                    PersonWiseData.append(groupOfInterest['Prov'].iloc[1])
                    PersonWiseData.append(groupOfInterest['Con_ACT'].iloc[1])
                    PersonWiseData.append(groupOfInterest['Sex'].iloc[1])
                    PersonWiseData.append(groupOfInterest['Age'].iloc[1])
                    PersonWiseData.append(0)
                    PersonWiseData.append(1)
                    PersonWiseData.append(cols[1:])
                    alldata[counts] = PersonWiseData
                    # numOfParticipants -= 1
                    counts += 1
                    knownOutcome += 1
                    PersonWiseData = []

    # Check to ensure that all participants in the study had an outcome as either censored or event
    if numOfParticipants != knownOutcome:
        PersonWiseData.append(groupOfInterest['Prov'].iloc[1])
        PersonWiseData.append(groupOfInterest['Con_ACT'].iloc[1])
        PersonWiseData.append(groupOfInterest['Sex'].iloc[1])
        PersonWiseData.append(groupOfInterest['Age'].iloc[1])
        PersonWiseData.append(0)
        PersonWiseData.append(1)
        PersonWiseData.append('39')
        alldata[counts] = PersonWiseData
        PersonWiseData = []

    return (alldata)


# Getting rows that contain unique data
entireDF = []
count = 0
for i, row in octoDF.iterrows():
    if row['Prov'] == 'ALL' or row['Con_ACT'] == 'ALL' or row['Sex'] == 'ALL' or row['Age'] == 'ALL' or row[
        'Measure'] == 'events' or row['Measure'] == 'censored':
        pass
    else:
        # print("INDEX: ",i,"TX: ", octoDF[i:i+3]['M0'].iloc[0])
        count += 1
        entireDF.append(IndividualLevelData1(int(octoDF[i:i + 3]['M0'].iloc[0]), octoDF[i:i + 3], 0))

# Check to ensure all members are captured
everyone = []
for e in entireDF:
    for v in e.values():
        everyone.append(v)
print(len(everyone))

with open('transformed.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Province','Con_ACT', 'Sex', 'Age', 'event', 'censored','timeTo'])
    for e in entireDF:
        for k,v in e.items():
            writer.writerow(v)