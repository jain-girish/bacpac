from bs4 import BeautifulSoup
import requests, json, re
import pandas as pd

year = input("Enter year between 1929-2024: ")
print("Fetching Data...")
url = 'https://www.imdb.com/event/ev0000003/' + year + '/1/?ref_=ev_eh'
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
soup = BeautifulSoup(response.text, "html.parser")
if (response.status_code not in range(200,230)): print("Failed to access IMDB.")

script_tags = soup.find_all("script", attrs = {'type' : "text/javascript"})
for script_tag in script_tags:
    script_data = script_tag.text
    if "IMDbReactWidgets.NomineesWidget" in script_data: 
        start = script_data.find('''{"nomineesWidgetModel"''')
        end = script_data.find("}}]);") + 2
        script_data = json.loads(script_data[start:end])
        data = script_data['nomineesWidgetModel']['eventEditionSummary']['awards'][0]['categories']

Oscars = {year: []}
for award in data:
    movie = award['nominations'][0]['primaryNominees'][0]
    movie_url="https://www.imdb.com/title/" + movie['const'] #+ "/?ref_=ev_nom"
    response = requests.get(movie_url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(response.text, "html.parser")
    flag=0
    if (response.status_code not in range(200,230)): 
        # print("Failed for " + movie['name'])
        flag=1
    matches = re.findall("(\d\d\d\d)\) \⭐ ([0-9]*\.*[0-9]*)",str(soup))
    if(flag==0):
        Oscars[year].append({
            'name' : movie['name'],
            'coverArt': movie['imageUrl'],
            'IMDBRating': matches[0][1],
            'releaseYear': matches[0][0],
            'const': movie['const']
        })
print("Fetched")
print("##################################")
for i in range(len(Oscars[year])):
    movie = Oscars[year][i]
    print(i+1)
    print('Movie: ' + movie['name'])
    print('Rating: ' + movie['IMDBRating'])
    print('Release Year: ' + movie['releaseYear'])
    print('Cover Art Link: ' + movie['coverArt'])
    print("##################################")

ind = input("Enter no. for which you want reviews (else enter n): ")
while(ind.isnumeric()):
    review_url="https://www.imdb.com/title/" + Oscars[year][int(ind)-1]['const'] + "/reviews"
    response = requests.get(review_url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(response.text, "html.parser")
    reviews = re.findall('''<div class="text show-more__control">(.*)<\/div>''',str(soup))
    reviews_headings = re.findall('''<a class="title".*> (.*)\s\<\/a>''',str(soup))
    i=0
    c='y'
    while(i+1<len(reviews) and c.lower()=='y'):
        print(reviews_headings[i])
        print()
        reviews[i] = re.sub('<br/><br/>',' ',reviews[i])
        print(reviews[i])
        print()
        print(reviews_headings[i+1])
        print()
        reviews[i+1] = re.sub('<br/><br/>',' ',reviews[i+1])
        print(reviews[i+1])
        print()
        i+=2
        c = input("More reviews? (y/n) ")
    ind = input("Enter no. for which you want reviews (else enter n): ")
