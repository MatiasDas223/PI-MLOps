import pandas as pd
import numpy as np
import ast

movies = pd.read_csv('movies_dataset.csv')


movies['release_date'].isnull().sum()
movies['budget'].fillna(0,inplace= True)
movies['revenue'].fillna(0,inplace= True)
movies.dropna(subset=['release_date'], inplace=True)

movies['release_date'] = pd.to_datetime(movies['release_date'], errors='coerce')
movies.dropna(subset= ['release_date'], inplace= True)
movies.rename(columns= {'id': 'id_movie'}, inplace= True)

movies['release_year'] = movies['release_date'].dt.year

# Transformamos budget en un float
movies['budget'] = movies['budget'].astype(float)

# Calculamos return
movies['return'] = movies['revenue']/movies['budget']

# A los valores nulos (0/0) y infinitos (num/0) los reemplazamos por 0
movies.fillna(0, inplace= True)
movies['return'] = movies['return'].replace(['inf', 'Infinity', 'Inf'], 0)

movies.drop(columns= ['video','imdb_id','adult','original_title','poster_path', 'homepage'], axis= 1, inplace=True)

# convierte las cadenas a listas de diccionarios
movies['genres'] = movies['genres'].apply(ast.literal_eval)

movies['genero_ids'] = movies['genres'].apply(lambda x: [i['id'] for i in x] if isinstance(x, list) else [])
movies['genero_names'] = movies['genres'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

# y podemos eliminar la columna 'genero' original
movies.drop(columns='genres', inplace= True)

# Función para convertir cadenas a diccionarios, manejar cadenas mal formadas y manejar valores que no son cadenas
def string_to_dict(dict_string):
    try:
        # Intenta convertir la cadena a un diccionario
        return ast.literal_eval(dict_string)
    except ValueError:
        # Si la cadena no se puede convertir a un diccionario, devuelve NaN
        return np.nan
    except SyntaxError:
        # Si la cadena no se puede convertir debido a un error de sintaxis (por ejemplo, si no es una cadena), devuelve NaN
        return np.nan

# Convierte las cadenas en 'belongs_to_collection' a diccionarios
movies['belongs_to_collection'] = movies['belongs_to_collection'].apply(string_to_dict)

# Desanida el diccionario en 'belongs_to_collection' en columnas separadas
movies = pd.concat([movies, movies['belongs_to_collection'].apply(pd.Series)], axis=1)

# Y puedes eliminar la columna 'belongs_to_collection' original si ya no la necesitas
movies = movies.drop(columns='belongs_to_collection')
movies = movies.drop(columns=[0], errors='ignore')

movies = movies.rename(columns={
    'id': 'id_collection',
    'name': 'name_collection',
    'poster_path': 'collection_poster_path',
    'backdrop_path': 'collection_backdrop_path'
})

# convierte las cadenas a listas de diccionarios
movies['production_companies'] = movies['production_companies'].apply(ast.literal_eval)

#Como el nombre de las claves son las mismas podemos usar las funciones ya definidas

movies['production_companies_ids'] = movies['production_companies'].apply(lambda x: [i['id'] for i in x] if isinstance(x, list) else [])
movies['production_companies_names'] = movies['production_companies'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

movies.drop(columns= ['production_companies'], inplace= True)

# Convierte las cadenas en 'production_countries' a diccionarios
movies['production_countries'] = movies['production_countries'].apply(string_to_dict)

movies['production_countries_names'] = movies['production_countries'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
movies['production_countries_iso'] = movies['production_countries'].apply(lambda x: [i['iso_3166_1'] for i in x] if isinstance(x, list) else [])

movies.drop(columns= ['production_countries'], inplace= True)

# Convierte las cadenas en 'production_countries' a diccionarios
movies['spoken_languages'] = movies['spoken_languages'].apply(string_to_dict)

movies['spoken_languages_names'] = movies['spoken_languages'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
movies['spoken_languages_iso'] = movies['spoken_languages'].apply(lambda x: [i['iso_639_1'] for i in x] if isinstance(x, list) else [])

movies.drop(columns= ['spoken_languages'], inplace= True)

credits = pd.read_csv('credits.csv')

# Convierte la columna "crew" en una lista de diccionarios
credits['crew'] = credits['crew'].apply(ast.literal_eval)
credits['cast'] = credits['cast'].apply(ast.literal_eval)

def obtener_director(crew_list):
    director_names = []  # Inicializar una lista vacía para almacenar los nombres de los directores
    for crew_member in crew_list:
        if crew_member.get('job') == 'Director':
            director_names.append(crew_member.get('name'))

    if director_names:  # Verificar si la lista no está vacía (se encontraron directores)
        return director_names
    else:
        return np.nan

# Aplicar la función a la columna "crew" para obtener el nombre del director
credits['director'] = credits['crew'].apply(obtener_director)

# Renombro apra que se llamen igual en ambos df
credits.rename(columns = {'id' : 'id_movie'}, inplace= True)

def obtener_actores(crew_list):
    for crew_member in crew_list:
        if crew_member.get('cast_id') == 1:
            return crew_member.get('name')
    return np.nan

# Aplicar la función a la columna "crew" para obtener el nombre del director
credits['director'] = credits['crew'].apply(obtener_director)

credits['principal_actor'] = credits['cast'].apply(obtener_actores)

# Renombro apra que se llamen igual en ambos df
credits.rename(columns = {'id' : 'id_movie'}, inplace= True)

directors = credits[['id_movie','director', 'principal_actor']]
directors.to_csv('directors.csv')

directors = pd.read_csv('directors.csv')

movies['id_movie'] = movies['id_movie'].astype('int64')

# Unimos a la pelicula con su director
movies = movies.merge(directors, on ='id_movie', how='left') 

movies.to_csv('movies.csv')