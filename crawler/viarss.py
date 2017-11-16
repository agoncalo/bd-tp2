import feedparser

d = feedparser.parse('http://feeds.folha.uol.com.br/emcimadahora/rss091.xml')

'title' in d.feed
d.feed.get('title', 'No title')

d.entries[0].description

i = 0
while i < len(d.entries):
    print(d.entries[0].description)