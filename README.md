# Proyecto MLOps de Streaming: Sistema de Recomendación y Análisis de Datos

Bienvenidos a este proyecto MLOps, donde construiremos una API para extraer datos útiles desde un conjunto de datos de películas, y usaremos Machine Learning para construir un sistema de recomendaciones. En este proyecto, nos centraremos en las operaciones de MLOps y aprenderemos a implementar y mantener un modelo de ML en un entorno de producción.

## Descripción del proyecto

Este proyecto es un sistema de recomendación de películas para una startup de agregación de plataformas de streaming. El proyecto implica un trabajo de Data Engineering inicial para limpiar y transformar los datos y, a continuación, el desarrollo de una API para facilitar consultas de datos y el uso de un modelo de Machine Learning.

## Procedimiento

- Preprocesamiento de datos: Limpiaremos y transformaremos los datos según las especificaciones dadas.

- Desarrollo de API: Desarrollaremos una API utilizando el marco FastAPI para exponer los datos para su uso.

- Despliegue: Desplegaremos nuestra API utilizando Render, Railway o un servicio similar para que pueda ser consumida desde la web.

- Análisis exploratorio de datos (EDA): Realizaremos un EDA en los datos limpios para identificar relaciones entre las variables y encontrar patrones interesantes.

- Sistema de recomendación: Utilizaremos nuestro EDA y los datos para entrenar un modelo de Machine Learning que pueda recomendar películas basándose en la similitud de las películas.

## ETL

El script de ETL limpia y procesa los datos de películas obtenidos de archivos CSV. Realiza las siguientes acciones:

- Limpia los datos faltantes y los valores nulos.

- Convierte ciertos campos a tipos de datos adecuados.

- Calcula un nuevo campo llamado "retorno", que es la relación entre los ingresos y el presupuesto de una película.

- Normaliza y extrae información relevante de campos que contienen listas de diccionarios (como 'genres', 'belongs_to_collection', 'production_companies', 'production_countries', 'spoken_languages').

Finalmente, se exporta un archivo CSV con los datos limpios y procesados.

## API

La API se implementa con FastAPI y proporciona varios endpoints para acceder a los datos de películas. Aquí están los endpoints disponibles:

- /peliculas_idioma/{idioma}: Devuelve la cantidad de películas con un idioma original dado.

- /peliculas_duracion/{title}: Devuelve la duración y el año de lanzamiento de una película con un título específico.

- /peliculas_franquicia/{franq}: Devuelve el número de películas y la ganancia total para una franquicia de películas dada.

- /peliculas_pais/{pais}: Devuelve el número de películas producidas en un país específico.

- /productoras_exitosas/{productora}: Devuelve el ingreso total y el número de películas para una productora específica.

- /director/{nombre_director}: Devuelve información detallada sobre las películas dirigidas por un director en particular.



### Requisitos

- Python 3.7+
- FastAPI
- Render, Railway o similar para el despliegue
- Librerías de ciencia de datos y ML como pandas, numpy, scikit-learn

### Fuente de datos

movies_dataset.csv: Contiene datos sobre las películas.
credits.csv: Contiene créditos de películas, incluyendo actores y equipo.

### Contacto

Si tienes alguna pregunta o problema con el proyecto, no dudes en contactarme.

Linkedin: https://www.linkedin.com/in/matiasdasilva92/
