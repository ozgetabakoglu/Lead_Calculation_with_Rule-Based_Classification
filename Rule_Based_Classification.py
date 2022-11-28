
###########################################
# Lead Calculation with Rule-Based Classification
###########################################

###########################################
# Business Problem
###########################################
# A game company wants to create new level-based customer definitions (personas) by
# using some features of its customers, and to create segments according to these new customer definitions and to estimate
# how much the new customers can earn on average according to these segments.

# For example: It is desired to determine how much a 25-year-old male user from Turkey who is an IOS user can earn on average.


###########################################
# Dataset Story
###########################################
# Persona.csv dataset contains the prices of the products sold by an international game company and
# some demographic information of the users who buy these products. The data set consists of records created in
# each sales transaction. This means that the table is not deduplicated.
# In other words, a user with certain demographic characteristics may have made more than one purchase.

# Price: Customer's spending amount
# Source: The type of device the customer is connecting to
# Sex: Gender of the client
# Country: Country of the customer
# Age: Customer's age

################# Pre-Application #####################

#    PRICE   SOURCE   SEX COUNTRY  AGE
# 0     39  android  male     bra   17
# 1     39  android  male     bra   17
# 2     49  android  male     bra   17
# 3     29  android  male     tur   17
# 4     49  android  male     tur   17

################# Post Application #####################

#       customers_level_based        PRICE SEGMENT
# 0   BRA_ANDROID_FEMALE_0_18  1139.800000       A
# 1  BRA_ANDROID_FEMALE_19_23  1070.600000       A
# 2  BRA_ANDROID_FEMALE_24_30   508.142857       A
# 3  BRA_ANDROID_FEMALE_31_40   233.166667       C
# 4  BRA_ANDROID_FEMALE_41_66   236.666667       C


###########################################
# PROJECT TASKS
###########################################

###########################################
# TASK 1: Answer the following questions.
###########################################

# Question 1: Read the persona.csv file and show the general information about the dataset.
import pandas as pd
pd.set_option("display.max_rows", None)
df = pd.read_csv('Modül_1_Veri_Bilimi_için_Python_Programlama/Part_2_Veri_Bilimi_için_Python_Programlama/Kural_Tabanli_Siniflandirma/persona.csv')
df.head()
df.shape
df.info()

# Question 2: How many unique SOURCE are there? What are their frequencies?
df["SOURCE"].nunique()
df["SOURCE"].value_counts()

# Question 3: How many unique PRICEs are there?
df["PRICE"].nunique()

# Question 4: How many sales were made from which PRICE?
df["PRICE"].value_counts()

# Question 5: How many sales were made from which country?
df["COUNTRY"].value_counts()
df.groupby("COUNTRY")["PRICE"].count()

df.pivot_table(values="PRICE",index="COUNTRY",aggfunc="count")


# Question 6: How much was earned in total from sales by country?
df.groupby("COUNTRY")["PRICE"].sum()
df.groupby("COUNTRY").agg({"PRICE": "sum"})

df.pivot_table(values="PRICE",index="COUNTRY",aggfunc="sum")

# Question 7: What are the sales numbers by SOURCE types?
df["SOURCE"].value_counts()

# Question 8: What are the PRICE averages by country?
df.groupby(by=['COUNTRY']).agg({"PRICE": "mean"})

# Question 9: What are the PRICE averages by SOURCEs?
df.groupby(by=['SOURCE']).agg({"PRICE": "mean"})

# Question 10: What are the PRICE averages in the COUNTRY-SOURCE breakdown?
df.groupby(by=["COUNTRY", 'SOURCE']).agg({"PRICE": "mean"})



#############################################
# TASK 2: What are the average earnings in breakdown of COUNTRY, SOURCE, SEX, AGE?
#############################################
df.groupby(["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).head()


#############################################
# TASK 3: Sort the output by PRICE.
###########################################
# Apply the sort_values method to PRICE in descending order to see the output in the previous question better.
# Save the output as agg_df.
agg_df = df.groupby(by=["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
agg_df.head()


#############################################
# TASK 4: Convert the names in the index to variable names.
###########################################
# All variables except PRICE in the output of the third question are index names.
# Convert these names to variable names.
# Hint: reset_index()
# agg_df.reset_index(inplace=True)
agg_df = agg_df.reset_index()
agg_df.head()


#############################################
# TASK 5: Convert AGE variable to categorical variable and add it to agg_df.
###########################################
# Convert the numeric variable age to a categorical variable.
# Construct the intervals as you think will be persuasive.
# For example: '0_18', '19_23', '24_30', '31_40', '41_70'

# Let's specify where the AGE variable will be divided:
bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]

# Let's express what the nomenclature will be for the dividing points:
mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]

# divide age:
agg_df["age_cat"] = pd.cut(agg_df["AGE"], bins, labels=mylabels)
agg_df.head()


###########################################
# TASK 6: Identify new level based customers and add them as variables to the dataset.
###########################################
# Define a variable named customers_level_based and add this variable to the dataset.
# Attention!
# After creating customers_level_based values with list comp, these values need to be deduplicated.
# For example, more than one of the following expressions: USA_ANDROID_MALE_0_18
# It is necessary to take them to groupby and get the price average.


# METHOD 2
agg_df['customers_level_based'] = agg_df[['COUNTRY', 'SOURCE', 'SEX', 'age_cat']].agg(lambda x: '_'.join(x).upper(), axis=1)

# METHOD 1
# variable names:
agg_df.columns

# how do we access the observation values?
for row in agg_df.values:
    print(row)

# We want to put the VALUES of the variables COUNTRY, SOURCE, SEX and age_cat side by side and concatenate them with an underscore.
# We can do this with list comprehension.
# Let's perform the operation in such a way that we select the observation values in the loop above:
[row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]

# Let's add to the dataset:
agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5 ].upper() for row in agg_df.values]
agg_df.head()

# Let's remove the unnecessary variables:
agg_df = agg_df[["customers_level_based", "PRICE"]]
agg_df.head()

for i in agg_df["customers_level_based"].values:
    print(i.split("_"))


# We are one step closer to our goal.
# There is a small problem here. There will be many identical segments.
# can be many numbers from segment USA_ANDROID_MALE_0_18, for example.
agg_df["customers_level_based"].value_counts()

# For this reason, after groupby according to the segments, we should get the price averages and deduplicate the segments.
agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})

# is in the customers_level_based index. Let's turn that into a variable.
agg_df = agg_df.reset_index()
agg_df.head()

# let's check. we expect each persona to be 1:
agg_df["customers_level_based"].value_counts()
agg_df.head()


###########################################
# TASK 7: Segment new customers (USA_ANDROID_MALE_0_18).
###########################################
# Segment by PRICE,
# add segments to agg_df with the naming "SEGMENT",
# describe the segments,
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"PRICE": "mean"})



###########################################
# TASK 8: Classify the new customers and estimate how much income they can bring.
###########################################
# Which segment does a 33-year-old Turkish woman using ANDROID belong to and how much income is expected to earn on average?
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

# In which segment and on average how much income would a 35 year old French woman using iOS expect to earn?
new_user = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]
