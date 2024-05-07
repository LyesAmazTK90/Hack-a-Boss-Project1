import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from datetime import datetime


def all_races_info():
    constructor_df = pd.DataFrame(columns=['Pos', 'No', 'Driver', 'Car', 'Laps', 'Time/Retired', 'PTS', 'Fecha', 'Circuito'])

    for year in range(1950, 2024):
        # Llama a la función "urls_carreras" utilizando como parámetro el año que ingresó el usuario. Guarda el dataframe de respuesta
        lista_urls = urls_carreras(year)

        # inicializar una lista vacía para guardar los reusltados
        all_drivers_races = []

        total_carreras = len(lista_urls)
        # Bucle para recorrer las carreras del año analizado. Utiliza la función "info_carrera"
        for i, url in enumerate(lista_urls, 1):
            print(f"Scrapenado los resultados de las carreras del año {year}: {i} de {total_carreras} ({(i/total_carreras)*100:.2f}%)...")
            all_results = info_carrera(url)
            all_drivers_races.append(all_results)
            
        # Concatenar todos los resultados en un dataframe unico
        df_combinado = pd.concat(all_drivers_races)[['Pos', 'No', 'Driver', 'Car', 'Laps', 'Time/Retired', 'PTS', 'Fecha', 'Circuito']]
    
        constructor_df = pd.concat([df_combinado, constructor_df])
    
    return constructor_df
        
        
def scrape_all_races():
    races_df = pd.DataFrame(columns=['Grand Prix', 'Date', 'Winner', 'Car_race_win', 'Laps', 'Time_race_win',
        'Driver', 'Car_fastest_lap', 'Time_fastest_lap'])
    for year in range(1950, 2024):
        race_results = scrape_race_results(year)
        fastest_laps = scrape_fastest_laps(year)
        races = race_results.merge(fastest_laps, on='Grand Prix', how='outer', suffixes=('_race_win', '_fastest_lap')).dropna(axis=1)
        races_df = pd.concat([races_df, races])
    
    return races_df


def scrape_all_constructors():
    constructor_df = pd.DataFrame(columns=['Pos', 'Team', 'PTS', 'Year'])
    for year in range(1950, 2024):
        constructor_standings = scrape_constructor_standings(year)

        if constructor_standings is not None:
            constructor_standings['Year'] = year
            constructor_df = pd.concat([constructor_df, constructor_standings[['Pos', 'Team', 'PTS', 'Year']]])
    
    return constructor_df


def scrape_weather(api_key: str) -> pd.DataFrame:
    url = 'https://api.openf1.org/v1/meetings'
    response = requests.get(url)
    data = response.json()
    carreras_df = pd.DataFrame(data)

    # Convertir date_start a datetime (no se usa)
    carreras_df['date_start'].apply(datetime.strptime, args=('%Y-%m-%dT%H:%M:%S',))

    # Filtros
    sin_preseason = ~carreras_df['meeting_name'].str.contains('Pre-Season')
    sin_2024 = carreras_df['year'] != 2024

    # Eliminar pre-season y 2024
    carreras_df = carreras_df[sin_preseason & sin_2024]

    # resetear indices para unión 
    carreras_df.reset_index(drop=True, inplace=True)

    coordenadas= {
        'lat': [],
        'lon': [],
    }

    for location in carreras_df["location"]:
        weather_location = location.replace(" ","-").replace("Spa-","")

        url = f"http://api.openweathermap.org/geo/1.0/direct?q={weather_location}&limit=&appid={api_key}"
        response = requests.get(url)
        data = response.json()

        coordenadas['lat'].append(data[0]['lat'])
        coordenadas['lon'].append(data[0]['lon'])

    coordenadas_df = pd.DataFrame(coordenadas)

    carreras_df['lat'] = coordenadas_df['lat']
    carreras_df['lon'] = coordenadas_df['lon']

    url = 'https://api.openf1.org/v1/weather'
    response = requests.get(url)
    data = response.json()
    weather_df = pd.DataFrame(data)

    weather_df = weather_df.groupby(["meeting_key"]).agg({"air_temperature": ["mean"],
                                               "humidity":["mean"],
                                                "pressure":["mean"],
                                            	"rainfall":["mean"],
                                                "track_temperature": ["mean"],
                                                "wind_direction":["mean"],
                                                "wind_speed":["mean"]})

    columnas = list()

    for column in weather_df.columns.values:
        columnas.append(f"{column[0]}_{column[1]}")
        
    weather_df.columns = columnas

    weather_df = pd.merge(left = carreras_df, right = weather_df, on= "meeting_key")

    return weather_df


# Definición de la función encargada de confeccionar el dataframe con los puntajes de los pilotos para una carrera en particular de un año específico
# Recibe como argumento la url de la carrera (que está en el dataframe "df_carreras" obtenido con la función "resultados_carrera"
# Devuelve una tupla con la fecha de la carrera, el nombre del circuito y un dataframe con los resultados de la carrera

def info_carrera(url_carrera):

    # La URL de argumento lleva a los resultados de un gran Premio (esta web incluye una tabla con las siguientes columnas:
    # - Posicion (Pos) que es un correlativo que va desde 1
    # - Número del Piloto (NO)
    # - Piloto (Driver)
    # - Escudería (Car)
    # - Cantidad de vueltas (Laps)
    # - Tiempo o si abandonó (Time/Retired)
    # - Puntos obtenidos (PTS)
    
    if not url_carrera:
        print("URL No Valido")
        return
    
    response_carrera = requests.get(url_carrera)
    
   # BeautifulSoup de la respuesta que se solicitó en el paso previo:    
    soup_carrera = BeautifulSoup(response_carrera.text, "html.parser")
    
    # Extraer fecha de la carrera
    fecha = soup_carrera.find("span", class_="full-date")
    
    # Exrtaer nombre del circuito
    circuito = soup_carrera.find("span", class_="circuit-info")

    # Extraer la tabla de resultados del año siguiendo el mismo esquema de la anterior función
    table_carrera = soup_carrera.find("table", class_ = "resultsarchive-table")

    # Por si no se encuentra la tabla con resultados... incluye convertir la tabla a un string y se le agrega lo del StringIO para que no salte la advertencia del pd.read_html
    if table_carrera:
        df_carrera = pd.read_html(StringIO(str(table_carrera)))[0]
        df_carrera["Fecha"] = fecha.text if fecha else ""
        df_carrera["Circuito"] = circuito.text if circuito else ""
        return df_carrera
    else:
        print(f"No hay resultados de la carrera", url_carrera.split("/")[8].title(), "del año", url_carrera.split("/")[5])


# Código para obtener los ganadores de todas las carreras de un año y las urls de dichas carreas en una temporada (año)
def urls_carreras(year):
    
    base_url = f"https://www.formula1.com/en/results.html/{year}/races.html"
    
    response = requests.get(base_url)
    
    soup = BeautifulSoup(response.text, "html.parser")

    #Para exrtaer las URLs de cada carrera:
    urls = []
    for bs in soup.find_all("td", class_="dark bold"):
        url = bs.find("a", class_="dark bold ArchiveLink")
        if url:
            url = url["href"]
            urls.append(f"https://www.formula1.com{url}")


    return urls


# Function to scrape race results for a specific year
def scrape_race_results(year):
    # URL con los resultados del año (esta web incluye una tabla con las siguientes columnas:
    # - Gran Premio (Grand Prix)
    # - Fecha (Date)
    # - Ganador (Winner)
    # - Escudería (Car)
    # - Cantidad de vueltas del ganador (Laps)
    # - Tiempo del Ganador (Time)

    # Construct the URL for the given year
    url = f"https://www.formula1.com/en/results.html/{year}/races.html"
    
    # Make a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the table containing the race results
        table = soup.find("table", class_="resultsarchive-table")
        
        # If the table is found, extract the data into a dataframe. #Tener esto en cuenta para las tablas Markdown.
        if table:
            df = pd.read_html(StringIO(str(table)))[0]
            return df
        else:
            print(f"No race results found for {year}")

    else:
        print(f"Failed to retrieve data for {year}. Status code: {response.status_code}")


# Function to scrape constructor standings for a specific year
def scrape_constructor_standings(year):
    # Construct the URL for the given year
    url = f"https://www.formula1.com/en/results.html/{year}/team.html"
    
    # Make a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the table containing the constructor standings
        table = soup.find("table", class_="resultsarchive-table")
        
        # If the table is found, extract the data into a dataframe
        if table:
            print(f"Extracting constructor standings for {year}")
            df = pd.read_html(StringIO(str(table)))[0]
            return df
        else:
            print(f"No constructor standings found for {year}")            
    else:
        print(f"Failed to retrieve data for {year}. Status code: {response.status_code}")


# Function to scrape race results for a specific year with the driver for that GRAN PRIX:
def scrape_fastest_laps(year):
    # Construct the URL for the given year
    url = f"https://www.formula1.com/en/results.html/{year}/fastest-laps.html"
    # Make a GET request to the URL
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")
        # Find the table containing the race results
        table = soup.find("table", class_="resultsarchive-table")
        # If the table is found, extract the data into a dataframe
        if table:
            df = pd.read_html(StringIO(str(table)))[0]
            return df
        else:
            print(f"No race results found for {year}")
    else:
        print(f"Failed to retrieve data for {year}. Status code: {response.status_code}")
