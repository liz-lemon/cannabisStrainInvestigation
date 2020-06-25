"""
Code Block 3
Read in all csv files created in code block 2 into a dataframe.
"""
import pandas as pd
import glob

path = r'/Users/lizzy/Desktop/cannabis_proj/results/' # use your path
weed_files = glob.glob(path + "/*.csv")

# empty dataframe
weed_df = pd.DataFrame()

# read in each file and append the information to our dataframe
for filename in all_files:
    strain_row = pd.read_csv(filename, sep='\[]', engine='python').transpose()
    weed_df = weed_df.append(strain_row)

# reset the index to 0
weed_df.reset_index(inplace=True)

# sort by strain name
weed_df.sort_values(by='index', inplace=True)

# rename columns to drop null column
weed_df.columns=['strain', 'features', 'growing', 'drop']

# drop null column at the end of the dataframe. 
weed_df.drop('drop', axis=1, inplace=True)

# remove brackets from features and growing columns. 
weed_df['features'] = weed_df['features'].str.replace('\[', '').str.replace('\]', '').astype(str)
weed_df['growing'] = weed_df['growing'].str.replace('\[', '').str.replace('\]', '').astype(str)

# split each feature for every strain into its own column. 
features = pd.DataFrame(weed_df['features'].str.split(',').tolist())

# split each growing trait for every strain into its own column
growing_traits = pd.DataFrame(weed_df['growing'].str.split(',').tolist())

# merge features and growing traits with strain name.
weed_df = pd.merge(weed_df, features, how='left', left_index=True, right_index=True).drop('features', axis=1)

growing_traits.drop(4, axis=1, inplace=True)

growing_traits.columns=['difficulty', 'grow_type', 'growing_time', 'yield_month']

# merge growing traits to final df
weed_df = pd.merge(weed_df, growing_traits, how='left', left_index=True, right_index=True).drop('growing', axis=1)
# reset the index
weed_df.reset_index(drop=True,inplace=True)
# export to excel for cleaning
weed_df.to_excel('datasets/cannaconnection.xlsx')