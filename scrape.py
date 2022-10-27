import requests
from bs4 import BeautifulSoup
import pprint

response = requests.get('https://news.ycombinator.com/')
beautiful_soup_object = BeautifulSoup(response.text,'html.parser')
news_link = beautiful_soup_object.select('.titleline > a')
subtext = beautiful_soup_object.select('.subtext')

def get_new_page(index):
	new_page_response = requests.get(f'https://news.ycombinator.com/news?p={index}')
	new_page_beautiful_soup_object = BeautifulSoup(new_page_response.text,'html.parser')
	new_page_news_link = new_page_beautiful_soup_object.select('.titleline > a')
	new_page_subtext = new_page_beautiful_soup_object.select('.subtext')
	return new_page_news_link, new_page_subtext

for page_index in range(1,11):
	new_response = get_new_page(page_index)
	news_link += new_response[0]
	subtext += new_response[1]


def sort_stories_by_votes(hn_title_list):
	return sorted(hn_title_list,key=lambda k:k['votes'],reverse = True)

def create_custom_hacker_news(news_link,subtext):
	hackernews_custom_title_list = []
	for index,item in enumerate(news_link):
		news_title = item.getText()
		news_article_link = item.get('href',None)
		vote = subtext[index].select('.score')
		if len(vote):
			points = int(vote[0].getText().replace(' points',''))
			if points > 99:
				hackernews_custom_title_list.append({'title':news_title,'link':news_article_link,'votes':points})
	return sort_stories_by_votes(hackernews_custom_title_list)
	

pprint.pprint(create_custom_hacker_news(news_link,subtext)) 

