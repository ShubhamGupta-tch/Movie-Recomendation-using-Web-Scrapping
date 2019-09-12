from django.shortcuts import render, get_object_or_404
import imdb
from collections import Counter
from users.views import image, history, spider, similar
import tmdbsimple as tmdb
import importlib
tmdb.API_KEY = 'eb9f535abc9a24f973e9fdcb9a17c0bb'

i = imdb.IMDb()

def recommend(list_to_recommend_from):
	print(list_to_recommend_from)
	recommended_movie = []
	if len(list_to_recommend_from) > 0:
		q = Counter(list_to_recommend_from)
		print(q)
		for movie, count in q.most_common(1):
			recommended_movie.append(movie)
			print(movie)
	return recommended_movie

def collaborative_filtering():
	from users.views import user_history
	all_users = []
	all_users_search = []
	for x in user_history:
		for m in x:
			user = m
			all_users.append(user)
			for _ in x:
				user_search = x[m]
				all_users_search.append(user_search)

	all_users.join(all_users_search)
	for users in all_users:
		for x in range(100):
			for y in range(100):
				if user[x] == user[y]:
					user[x].join(user[y])
				else:
					pass
			print(x)
	return user


def user_recommendation(username):
	from users.views import user_history
	fuh = [] #Final User History
	try:
		for x in user_history:
			movie_name = x[username]
			fuh.append(movie_name)
		print('--------------------------')
		print('FINAL USER HISTORY:')
		print(fuh)
		print('--------------------------')
	except:
		pass

	recommended_movies_info = ''
	if len(fuh) >= 1:
		try:
			recommended_movie = recommend(fuh)
			recommended_movie = recommended_movie[0]
			new_url = "https://www.movie-map.com/" + recommended_movie + ".html"
			recommended_movies_list = spider(new_url)
			recommended_movies_info = similar(5, recommended_movies_list)

		except:
			pass
	print('-------------RECOMENDED MOVIE INFORMATION-------------')
	print(recommended_movies_info)

	return recommended_movies_info



def top_movies(number_of_results):
	top = i.get_top250_movies()
	top_list = []
	q = 26
	for x in range(q, (number_of_results+q)):
		movie_dict = {}
		a = top[x]
		img = image(a['title'])
		final_dict = {'name':a, 'link':img}
		movie_dict.update(final_dict)
		top_list.append(movie_dict)
	return top_list

def cool_movies(number_of_results):
	top = i.get_top250_movies()
	top_list = []
	q = 77
	for x in range(q, (number_of_results+q)):
		movie_dict = {}
		a = top[x]
		img = image(a['title'])
		final_dict = {'name':a, 'link':img}
		movie_dict.update(final_dict)
		top_list.append(movie_dict)
	return top_list

def home(request):
	m = top_movies(6)
	cool = cool_movies(6)
	user_recommended_movies = ''
	if request.user.is_authenticated == True:
		username = request.user.username
		user_recommended_movies = user_recommendation(username)
		print('USER RECOMMENDED MOVIES:')
		print(user_recommended_movies)
		print('------------------------')


	else:
		pass

	popular_movies_info = ''
	try:
		popular_movie = recommend(history)
		popular_movie = popular_movie[0]
		new_url = "https://www.movie-map.com/" + popular_movie + ".html"
		popular_movies_list = spider(new_url)
		popular_movies_info = similar(5, popular_movies_list)

	except:
		pass

	context = {
		'top_movies': m,
		'cool': cool,
		'popular': popular_movies_info,
		'recommend': user_recommended_movies,
	}
	return render(request, 'home.html', context)

def more(request):
	m = top_movies(20)
	context = {
		'more_movies':m
	}
	return render(request, 'more.html', context)