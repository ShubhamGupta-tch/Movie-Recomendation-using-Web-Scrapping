from django.shortcuts import render
from tmdbv3api import TMDb
from tmdbv3api import Movie
tmdb = TMDb()
tmdb.api_key = 'eb9f535abc9a24f973e9fdcb9a17c0bb'
def movie(name):
    movie = Movie()
    search = movie.search(name)
    for res in search:
        x = res.id
        print(x)
        break

    recommendations = movie.recommendations(movie_id=x)
    oh = []
    num = 0
    for some in recommendations:
    	if num >= 6:
    		break

    	a = (some.title)
    	b = (some.poster_path)
    	c = (some.vote_average)
    	d = (some.release_date)
    	e = (some.vote_count)
    	final_dict = {'name':a, 'link':b, 'vote':c, 'date':d, 'count':e}
    	oh.append(final_dict)
    	num = num + 1
    return oh


def combine(request, movie1, movie2):
	similar1 = movie(movie1)
	similar2 = movie(movie2)
	similar1 += similar2
	context = {
		'mov1':similar1,
		'mov2':similar2,
	}
	return render(request, 'combine.html', context)

def home(request):
	return render(request, 'comhome.html')