from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404
from .forms import CustomUserCreationForm
import requests
from bs4 import BeautifulSoup
import imdb
import urllib.request
import tmdbsimple as tmdb
from collections import Counter
tmdb.API_KEY = 'eb9f535abc9a24f973e9fdcb9a17c0bb'

i = imdb.IMDb()
history = []
user_history = []
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def spider(url):
	word_list = []
	try:
		source_code = requests.get(url)
		plain_text =  source_code.text
		soup = BeautifulSoup(plain_text, features="lxml")
		for link in soup.find('div', attrs = {'id':'gnodMap'}):
		    title = link.string
		    word_list.append(title)
	except:
		pass
	return word_list

def info(movie_name):
	a = i.search_movie(movie_name)
	b = a[0]
	i.update(b)
	s = b.summary()
	return s

def image(movie_query):
	import tmdbsimple as tmdb
	tmdb.API_KEY = 'eb9f535abc9a24f973e9fdcb9a17c0bb'
	image_url = ''
	search = tmdb.Search()
	response = search.movie(query=movie_query)
	for s in search.results:
		x = s['poster_path']
		image_url = x
		break
	return image_url

def similar(number_of_movies, movie_name_list):
	similar_movie_list = []
	s = 1
	for _ in movie_name_list:
		try:
			movie_name_list.remove('\n')
		except:
			break

	for x in range(s, (number_of_movies+s)):
		mov_dict = {}
		a = movie_name_list[x]
		try:
			img = image(a)
			if len(img) >= 1:
				final_dict = {'name':a, 'link':img}
				mov_dict.update(final_dict)
				similar_movie_list.append(mov_dict)
			else:
				continue
		except:
			pass
	return similar_movie_list

def youtube_link(search_query):
	yt_link = ''
	textToSearch = search_query
	query = urllib.parse.quote(textToSearch)
	url = "https://www.youtube.com/results?search_query=" + query
	response = urllib.request.urlopen(url)
	print(response)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
	    youtube = 'https://www.youtube.com' + vid['href']
	    yt_link = youtube
	    break

	return yt_link



def search(request, query):
	query = query

	if request.user.is_authenticated == True:
		user = request.user.username
		user_history.append({user:query})

	history.append(query)
	url = "https://www.movie-map.com/" + query + ".html"
	movie_list = spider(url)
	movie_info = info(query)
	movie_image = image(query)
	similar_movies = similar(12, movie_list)
	yt = youtube_link(query)
	print(similar_movies)
	print(history)
	#recommended_movie = recommend()
	#recommended_movie = recommended_movie[0]
	#new_url = "https://www.movie-map.com/" + recommended_movie + ".html"
	#recommended_movies_list = spider(new_url)
	#recommended_movies_info = similar(10, recommended_movies_list)

	context = {
		'word': query,
		'movie': movie_list,
		'detail': movie_info,
		'mov_image': movie_image,
		'similar': similar_movies,
		'youtube': yt
		#'recommend': recommended_movies_info
	}
	return render(request, 'search.html', context)
	
