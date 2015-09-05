import requests, bs4, re, TwitterAPI

# Set up twitter
consumerKey = "yourConsumerKey"
consumerSecret = "yourConsumerSecret"
accessTokenKey = "yourAccessTokenKey"
accessTokenSecret = "yourAccessTokenSecret"

# connect to twitter
apiCall = TwitterAPI.TwitterAPI(consumerKey, consumerSecret, accessTokenKey, accessTokenSecret)

# make a request of the website
res = requests.get('http://hagen-atw.de/aktuelle-meldungen.html')
res.raise_for_status()

# parse the url
websiteSoup = bs4.BeautifulSoup(res.text, 'html.parser')

webTitle = websiteSoup.find_all("span", class_="magazinetitle")
webLinks = websiteSoup.find_all("a", class_="magazinmehr")
webArticleText = websiteSoup.find_all("span", class_="magazinetext")

# put all titles, links and articleText in array
titles = []
links = []
articelTexts = []

for singleTitle in webTitle:
	titles.append(singleTitle.text)

for singleLink in webLinks:
	baseUrl = 'http://www.hagen-atw.de'
	articleUrl = singleLink.get('href')
	completeUrl = baseUrl + articleUrl
	links.append(completeUrl)

for singleArticle in webArticleText:
	articelTexts.append(singleArticle.text)

def postToTwitter():
	tweetText = titles[0] + ' ' + links[0]
	tweet = apiCall.request('statuses/update', {'status': tweetText})
	print('SUCCES' if tweet.status_code == 200 else 'FAILURE')

lastArticle = open('/volume1/stuff/python/lastArticle.txt', encoding='utf-8')
lastHeadline = lastArticle.read()
# print(lastHeadline)

if titles[0] == lastHeadline:
	print('Headline are the same - nothing new')
	lastArticle.close()
	exit()
else:
	postToTwitter()
	lastArticle.close()
	
	newArticle = open('/volume1/stuff/python/lastArticle.txt', 'w', encoding='utf-8')
	newArticle.write(titles[0])
	newArticle.close()