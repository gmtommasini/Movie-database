import requests
import os

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_ACESS_TOKEN = os.getenv("TMDB_ACESS_TOKEN")

BASE_URL = "https://api.themoviedb.org/3"
SEARCH_URL = BASE_URL + "/search/movie"
DETAILS_URL = BASE_URL + "/movie/"#<movie_ID>
# IMAGE_BASE_URL = "https://image.tmdb.org/t/p/original"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

headers = {
  "accept": "application/json",
  "Authorization": f"Bearer {TMDB_ACESS_TOKEN}"
}  

def search_movie(title:str, year:int=None, lang:str='en') -> list:
    params = { 
        "query": title,
        "include_adult":False,
        # "language":lang, # Does not seem to make difference
    }
    if year:
      params["primary_release_year"] = str(year)
    print(params)
    response = requests.get(url=SEARCH_URL, params=params, headers=headers)
    print(response.json())
    movies = response.json()['results']
    print(movies)
    return movies


def get_details(id:str):  
    params ={"append_to_response": "credits"}
    url = DETAILS_URL + id 
    response = requests.get(url= url, headers=headers, params=params)
    # directors = [crew_member['name'] for crew_member in response.json()['crew'] if crew_member['job'] == 'Director']
    # print(response.json())
    return response.json()

def get_directors(id:str):  
    params ={"append_to_response": "credits"}
    url = DETAILS_URL + id + "/credits"
    print(url)
    response = requests.get(url= url, headers=headers, params=params)
    directors = [crew_member['name'] for crew_member in response.json()['crew'] if crew_member['job'] == 'Director']
    # print(response.json())
    return directors


if __name__ == '__main__':
  # search_movie("with interests", lang='en')
  # print("API_KEY: ", TMDB_API_KEY)
  # search_movie('The Matrix')
  # get_details("603")
  get_directors("603")

