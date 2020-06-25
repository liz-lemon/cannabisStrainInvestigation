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