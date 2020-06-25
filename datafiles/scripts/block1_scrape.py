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