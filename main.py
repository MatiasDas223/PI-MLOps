import pandas as pd
from fastapi import FastAPI
import ast

movies = pd.read_parquet('movies.parquet')

app = FastAPI()

### Desarrollo de la API ###

### FUNCION PARA CONSULTAR LA CANTIDAD DE PELICULAS CON UN IDIOMA ORIGINAL DETERMINADO###

@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma:str):

    # Verificar que el idioma ingresado sea válido
    if not isinstance(idioma, str):
        return {'error': 'El idioma debe ser una cadena de texto.'}
    
    # Verificar que el idioma ingresado sea válido
    if idioma not in movies['original_language'].unique():
        return {'error': 'Idioma no encontrado.'}
    
    def recorrer_df(x):
        if idioma == x:
            return True
        else:
            return False
    
    cantidad = movies['original_language'].apply(recorrer_df)

    cantidad = cantidad.sum()
    
    return {'idioma':str(idioma), 'cantidad':int(cantidad)}


### FUNCION PARA CONSULTAR LA DURACION DE UNA PELICULA###


@app.get('/peliculas_duracion/{title}')
def peliculas_duracion(title: str ):

    # Filtrar el DataFrame por el título proporcionado
    resultado = movies[movies['title'] == title]

    if resultado.empty:
        return {'error': 'Título no encontrado.'}

    # Obtener el runtime y release_year asociados al título
    runtime = resultado['runtime'].iloc[0]

    release_year = resultado['release_year'].iloc[0]

    return {'titulo': str(title), 'runtime': int(runtime), 'release_year': int(release_year)}


### FUNCION PARA CONSULTAR LAS PELICULAS DE UNA FRANQUICIA DETERMINADA ###


@app.get('/peliculas_franquicia/{franq}')
def franquicia(franq: str ):

    # Filtrar el DataFrame por el título proporcionado
    resultado = movies[movies['name_collection'] == franq]

    if resultado.empty:
        return {'error': 'Franquicia no encontrada.'}

    # Obtener el numero de peliculas
    peliculas = resultado.shape[0]

    # Obtener la ganancia

    ganancia = resultado['revenue'].sum() - resultado['budget'].sum()

    return {'franquicia': franq, 'Nro. de peliculas': int(peliculas), 'Ganancia total': int(ganancia)}

### FUNCION PARA CONSULTAR LAS PELICULAS DE UN PAIS DETERMINADO ###

@app.get('/peliculas_pais/{pais}')
def peliculas_pais( pais: str ):

    # Verificar que el pais ingresado sea válido
    if not isinstance(pais, str):
        return {'error': 'El idioma debe ser una cadena de texto.'}
    
    def recorrer_df(x):
        # Utilizar una comparación en minúsculas para cada elemento en la lista
        return pais in x
    
    cantidad = movies['production_countries_names'].apply(recorrer_df)

    if cantidad.empty:
        return {'No se encontraron peliculas para ese pais'}

    cantidad = cantidad.sum()

    return {'Pais' : str(pais), 'Cantidad de peliculas producidas ': int(cantidad)}


### FUNCION PARA CONSULTAR LAS PELICULAS DE UNA PRODUCTORA ###

@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas( productora: str ):

    # Verificar que la oroductora ingresada sea válida
    if not isinstance(productora, str):
        return {'error': 'La productora debe ser una cadena de texto.'}
    
    def recorrer_df(x):
           # Utilizar una comparación en minúsculas para cada elemento en la lista
        return productora in  x
    
    cantidad = movies['production_companies_names'].apply(recorrer_df)

    if cantidad.empty:
        return {'No se encontraron peliculas para ese pais'}

    cantidad = movies[cantidad]

    numero = cantidad.shape[0]

    cantidad = cantidad['revenue'].sum()

    return {f'La productora {productora} obtuvo un revenue de USD {int(cantidad)} en un total de {int(numero)} peliculas'}


### FUNCION PARA CONSULTAR LAS PELICULAS DE UN DIRECTOR ###

@app.get('/director/{nombre_director}')
def get_director(nombre_director: str):
    # Convertir las cadenas en listas si el valor no es NaN
    movies['director'] = movies['director'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    # Filtrar el DataFrame buscando el nombre del director dentro de las listas
    resultado = movies[movies['director'].apply(lambda x: nombre_director in x if isinstance(x, list) else False)]

    if resultado.empty:
        return {'error': 'Ninguna película encontrada para ese director'}

    retorno_total = resultado['revenue'].sum() / resultado['budget'].sum()

    peliculas_info = []
    for index, row in resultado.iterrows():
        pelicula = f"- {row['title']}, {row['release_year']}, Retorno: {row['return']}, Costo: {row['budget']}, Ganancia: {row['revenue']}"
        peliculas_info.append(pelicula)

    info_director = f"Nombre del director: {nombre_director}\nRetorno total: {retorno_total}\nPelículas dirigidas:\n" + "\n".join(peliculas_info)
    return print(info_director)

@app.get('/recomendar_pelicula/{movie_title}')
def recomendacion(movie_title: str, n_recommendations=5):

    # Extraer las características de la película seleccionada
    selected_movie = movies[movies['title'] == movie_title].iloc[0]

    # Calcular similitud basada en colección
    similarity = (movies['name_collection'] == selected_movie['name_collection']) * 10 if pd.notnull(selected_movie['name_collection']) else 0

    # Calcular similitud basada en tópico
    similarity += (movies['topic'] == selected_movie['topic']) * 0.5

    # Calcular similitud basada en género
    similarity += movies['genero_names'].apply(lambda x: sum(g in x for g in selected_movie['genero_names'])) * 0.2

    # Calcular similitud basada en palabras clave
    similarity += movies['keywords_cleaned'].apply(lambda x: sum(k in x for k in selected_movie['keywords_cleaned'])) * 0.5

    # Excluir la película seleccionada
    similarity[selected_movie.name] = 0

    # Obtener las películas más similares
    top_n_indices = similarity.nlargest(n_recommendations).index
    top_n = movies.loc[top_n_indices]

    # Crear una cadena con los títulos de las películas
    titles = top_n['title'].tolist()
    titles = titles[0:4] 
    return f"Las películas similares a {movie_title} son: {', '.join(titles)}"

recomendacion('Toy Story', 5)