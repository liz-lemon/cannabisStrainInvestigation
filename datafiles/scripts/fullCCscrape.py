# refactor into functions/cleaner code
"""
Code Block One
obtain weblinks The code above will gather all the https for each strain and store it in a text file.
Next I want to open the text file, read the http and loop through each page extracting features for each strain.

Open the link and write a new csv file with the features for each strain.

I did this before but my approach was different and some strains varied in the number of values, messing up my columns.
"""
# open text file and append results for each a-z letter. 
weed_file = open("weed_file.txt", 'a+')

# loop through the alphabet
for c in ascii_lowercase:
    # get a response for each letter
    response = requests.get(f"https://www.cannaconnection.com/strains?show_char={c}")
    # start the soup 
    soup = BeautifulSoup(response.content, 'html5lib')
    # find the strain lists
    strains = soup.find_all(class_='strains-list')
    # find elements that match 'a href' criterion and assign them to a variable
    a = strains[0].find_all('a', text=True)
    # pull 
    for link in a[0:]:
        b = a[0].findAll(text=True)
        for item in b[0:]:
            if item == "\n":
                b.remove(item)
        output = link.get('href').encode('ascii', errors='ignore').decode()
        weed_file.write(output + "\n")
weed_file.close()

"""
Code Block Two
this will run through the text file created in code block one, line by line
from there it retrieve each strains' features such as parents, thc/cbd, effects and flavors
then it will retrieve its growing characteristics.
For each strain a new csv file will be opened with the features and growing characterisitcs written to the respective csv file in the results folder.
"""
# open the text file again.
weedfile = open('weed_file.txt', 'r')
# read each line in the file
lines = weedfile.readlines()
# loop through and send a web request to extract the features we need.
for line in lines[0:]:
    line = line.replace('\n', '')
    new_response = requests.get(line)

    soup = BeautifulSoup(new_response.content, 'html5lib')
    a = soup.find_all(class_='primary_block post-content')
    b = soup.find_all(class_='data-sheet')
    c = b[0].find_all(class_='feature-value')
    d = b[1].find_all('dd')
    #get strain title
    title = a[0].find('h1').text

    features = []
    for f in c:
        features.append(f.text.strip())

    growing = []
    for g in d:
        growing.append(g.text.strip())
    
    linearray = line.split("/")
    print("Scraping " + linearray[3].title())
    url = "https://www.cannaconnection.com/strains/" + linearray[4]
    print("URLSCRAPE " + url)
    strain = linearray[4]
    fileurl = "results/"+strain+".csv"
    array = [title, features, growing]
    file = open(fileurl, "a+")
    for elem in array[0:]:
        file.write(str(elem) + "\n")
    file.close()

weedfile.close()

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