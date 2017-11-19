import pymongo
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from functools import reduce

def toMongoDB(news):
	uri = "mongodb://tpbd:Pc48J1UiXZBn3xaumgBkxGrBHw00k9PCr0daNqRHnXoqXnv0nciTjxv85yWQo1X5rerrsbS0b3uDN0lMOy9nAA==@tpbd.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
	client = pymongo.MongoClient(uri)
	banco = client['news']
	
	import datetime
	db = banco.news
	teste = db.news
	teste.insert(news)



def getSources():
    source_url = 'https://newsapi.org/v2/sources?apiKey=f2f2020e4730450184febe2cc8fa7681&language=pt&county=br'
    response = requests.get(source_url).json()
    sources = []
    for source in response['sources']:
        sources.append(source['id'])
    return sources

def mapping():
    d = {}
    response = requests.get('https://newsapi.org/v2/sources?apiKey=f2f2020e4730450184febe2cc8fa7681&language=pt&county=br'
)
    response = response.json()
    for s in response['sources']:
        d[s['id']] = s['category']
    return d

def category(source, m):
    try:
        return m[source]
    except:
        return 'NC'

def cleanData(path):
    data = pd.read_csv(path)
    data = data.drop_duplicates('url')
    data.to_csv(path, index=False)

def getDailyNews():
    sources = getSources()
    key = 'f2f2020e4730450184febe2cc8fa7681'
    url = 'https://newsapi.org/v2/top-headlines?sources={0}&apiKey={1}'
    responses = []
    for i, source in tqdm(enumerate(sources)):
        try:
            u = url.format(source, key)
            response = requests.get(u)
            r = response.json()
            for article in r['articles']:
                article['source'] = source
            responses.append(r)
            toMongoDB(r)
        except:
            u = url.format(source, key)
            response = requests.get(u)
            r = response.json()
            for article in r['articles']:
                article['source'] = source
            responses.append(r)
            toMongoDB(r)
            
    print(responses)      
    news = pd.DataFrame(reduce(lambda x,y: x+y ,map(lambda r: r['articles'], responses)))
    #news = news.dropna()
    #news = news.drop_duplicates()
    d = mapping()
    news['category'] = news['source'].map(lambda s: category(s, d))
    news['scraping_date'] = datetime.now()
    

    try:
        aux = pd.read_csv('news.csv')
    except:
        aux = pd.DataFrame(columns=list(news.columns))
        aux.to_csv('news.csv', encoding="ISO-8859-1", index=False)

    with open('news.csv', 'a', encoding='utf-8') as f:
        news.to_csv(f, header=False, encoding="ISO-8859-1", index=False)

    cleanData('news.csv')
    print('Done')

    
if __name__ == '__main__':
    getDailyNews()


#
 #      	uri = "mongodb://tpbd:Pc48J1UiXZBn3xaumgBkxGrBHw00k9PCr0daNqRHnXoqXnv0nciTjxv85yWQo1X5rerrsbS0b3uDN0lMOy9nAA==@tpbd.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
#		client = pymongo.MongoClient(uri)
#		banco = client['news']
#		
#		import datetime
#		db = banco.news
#		teste = db.news
#		teste.insert(news)
