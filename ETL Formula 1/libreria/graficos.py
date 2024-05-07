import folium
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import datetime as datetime
from IPython.display import display

def diez_mejores_pilotos(carreras):
    """Función que muestra una gráfica der barras verticales de los 10 mejores pilotos de todos los tiempos por carreras ganadas. A su vez, diferencia por color a los pilotos en activo respecto a los pilotos inactivos. Finalmente, permite realizar una comparar entre los 10 pilotos seleccionados (mediante toggle)."""
    # Assuming df is your DataFrame with the provided columns
    # Step 1: Sort the DataFrame by the "Winner" column to identify the number of races won by each pilot
    pilots_wins = carreras['Winner'].value_counts().reset_index()
    pilots_wins.columns = ['Driver', 'Wins']
    pilots_wins = pilots_wins.sort_values(by='Wins', ascending=False)
    # Step 2: Create a list of active pilots for the year 2024
    active_pilots_2024 = ['Lewis Hamilton HAM', 'Max Verstappen VER', 'Valtteri Bottas BOT', 'Charles Leclerc LEC', 'Logan Sargeant SAR', 'Daniel Ricciardo RIC', 'Lando Norris NOR', 'Pierre Gasly GAS', 'Sergio Perez PER',
                          'Fernando Alonso ALO', 'Lance Stroll STR', 'Kevin Magnussen MAG', 'Yuki Tsunoda TSU', 'Alex Albon ALB', 'Zhou Guanyu ZHO', 'Niko Hulkenberg HUL', 'Esteban Ocon OCO', 'Carlos Sainz SAI', 'George Russell RUS', 'Oscar Piastri PIA']
    # Step 3: Create a colomn named "Active Pilots"
    carreras["active"] = carreras['Winner'].isin(active_pilots_2024)
    # Step 4: Sort the dataframe by "Winner" column to get the count of races won by each pilot
    pilots_races_won = carreras['Winner'].value_counts()
    # Step 5: Create a list of active pilots who are still racing in 2024
    active_pilots_2024 = ['Lewis Hamilton HAM', 'Max Verstappen VER', 'Valtteri Bottas BOT', 'Charles Leclerc LEC', 'Logan Sargeant SAR', 'Daniel Ricciardo RIC', 'Lando Norris NOR', 'Pierre Gasly GAS', 'Sergio Perez PER',
                          'Fernando Alonso ALO', 'Lance Stroll STR', 'Kevin Magnussen MAG', 'Yuki Tsunoda TSU', 'Alex Albon ALB', 'Zhou Guanyu ZHO', 'Niko Hulkenberg HUL', 'Esteban Ocon OCO', 'Carlos Sainz SAI', 'George Russell RUS', 'Oscar Piastri PIA']
    # Step 6: Create a list of top 10 pilots by races won
    top_10_pilots = pilots_races_won.head(10).index.tolist()
    # Step 7, create figure:
    fig = go.Figure()
    # Add traces for top 10 pilots
    for pilot in top_10_pilots:
        # Check if the pilot is active or inactive
        color = 'blue' if pilot in active_pilots_2024 else 'red'
        fig.add_trace(go.Bar(
            x=[pilot],
            y=[pilots_races_won[pilot]],
            name=pilot,
            marker=dict(color=color)
        ))
    # Add custom legend items with adjusted font size and position
    fig.add_annotation(
        x=0.5,
        y=1.1,  # Adjusted y value for alignment with the title
        xref="paper",
        yref="paper",
        text="Pilotos Activos",
        showarrow=False,
        font=dict(color='blue', size=16),  # Increased font size
    )
    fig.add_annotation(
        x=0.5,
        y=1.05,  # Adjusted y value for alignment with the title
        xref="paper",
        yref="paper",
        text="Pilotos Inactivos",
        showarrow=False,
        font=dict(color='red', size=15),  # Increased font size
    )
    # Update layout
    fig.update_layout(
        title='Top 10 Pilotos por carreras ganadas',
        xaxis=dict(title='Pilot'),
        yaxis=dict(title='Number of Races Won'),
        showlegend=True
    )
    fig.show()


def comparativa_todos_pilotos(carreras):
    """Grafica comparativa de barras verticales con las carreras ganadas por todos los pilotos desde 1950 hasta la actualidad, diferenciando por color los pilotos que siguen en activo."""
    active_pilots_2024 = ['Lewis Hamilton HAM', 'Max Verstappen VER', 'Valtteri Bottas BOT', 'Charles Leclerc LEC', 'Logan Sargeant SAR', 'Daniel Ricciardo RIC', 'Lando Norris NOR', 'Pierre Gasly GAS', 'Sergio Perez PER', 'Fernando Alonso ALO', 'Lance Stroll STR', 'Kevin Magnussen MAG', 'Yuki Tsunoda TSU', 'Alex Albon ALB', 'Zhou Guanyu ZHO', 'Niko Hulkenberg HUL', 'Esteban Ocon OCO', 'Carlos Sainz SAI', 'George Russell RUS', 'Oscar Piastri PIA']
    carreras["activo"] = carreras['Winner'].isin(active_pilots_2024)
    agrupado = carreras.groupby("Winner").agg(
        {"Time_race_win": ["count"], "activo": ["mean"]})
    agrupado.columns = [f"{column[0]}_{column[1]}" for column in agrupado.columns]
    fig = px.bar(agrupado, y='Time_race_win_count',
                 color='activo_mean',
                 height=400)
    fig.show()


def grafica_temperatura(df):
    df["air_temperature_mean"] = df["air_temperature_mean"].apply(
        lambda _: float(_))
    fig = px.scatter(data_frame=df,
                      x="date_start",
                      y="air_temperature_mean",
                      color="location",
                      hover_name="location",
                      width=None,
                      height=None,
                      opacity=0.5,
                      title="Cambios de temperatura por carrera, Temporada 2023")
    fig.show()


def columna_lluvia(df):
    lluvia = []
    for x in df["rainfall_mean"]:
        if x < 0.15:
            x = "no rain or little rain"
        elif x < 0.30:
            x = "rain"
        else:
            x = "a lot of rain"
        lluvia.append(x)
    df["lluvia"] = lluvia
    fig = px.pie(data_frame=df,
                  names="lluvia",
                  values="rainfall_mean",
                  title="Lluvia en la temporada 2023")
    fig.show()


def tiempos_rapidos_por_piloto_Grand_Prix_año(carreras):
    
    # Convert 'Date' column to datetime format
    grouped_carreras = carreras.groupby(["Grand Prix", "Date", "Driver", "Car_fastest_lap"])["Time_fastest_lap"].min().reset_index()
    grouped_carreras['Date'] = pd.to_datetime(grouped_carreras['Date'])
    print(grouped_carreras[grouped_carreras['Date'].dt.year == 2021])
    # Function to convert time strings to seconds
    def convert_to_seconds(time_str):
        parts = time_str.split(":")
        minutes = int(parts[0]) if len(parts) > 1 else 0
        seconds = float(parts[-1])
        return minutes * 60 + seconds

    # Function to format time as minutes.seconds for hover text
    def format_time_for_hover(time_seconds):
        minutes = int(time_seconds // 60)
        seconds = int(time_seconds % 60)
        milliseconds = int((time_seconds - int(time_seconds)) * 1000)
        return f"{minutes}.{seconds:02d}.{milliseconds:03d}"

    # Prompt the user to enter the desired year
    while True:
        try:
            year = int(input("Enter the year (1950-2023): "))
            if 1950 <= year <= 2023:
                break  # Exit the loop if the input is valid
            else:
                print("Please enter a year between 1950 and 2023.")
        except ValueError:
            print("Please enter a valid year.")

    # Filter the DataFrame for the specified year and reset the index
    filtered_df = grouped_carreras[grouped_carreras['Date'].dt.year == year].reset_index()

    # Convert time strings to seconds
    filtered_df["Time_fastest_lap_seconds"] = filtered_df["Time_fastest_lap"].apply(convert_to_seconds)

    # Create the plot
    fig = px.bar(
        filtered_df,
        x=filtered_df["Time_fastest_lap_seconds"],
        y=filtered_df["Grand Prix"],
        color=filtered_df["Driver"].sort_values(),
        hover_data={"Time_fastest_lap_seconds": filtered_df["Time_fastest_lap_seconds"].apply(format_time_for_hover)}
    )

    # Update axis labels
    fig.update_layout(
        xaxis_title="Time (minutes.seconds)",
        yaxis_title="Grand Prix"
    )

    # Show the plot
    fig.show()


def puntaje_piloto(carreras_detalles):
    """Función para generar una gráfica tipo "line" con la evolución del puntaje de un piloto a lo largo de una temporada (año) seleccionada por el usuario."""
    carreras_detalles['Fecha'] = pd.to_datetime(carreras_detalles['Fecha'])

    # Pedir al usuario que ingrese el año... el bucle es porque no sabemos cuantas veces podría ingresarlo mal
    while True:
        try:
            # estas fechas son las que tenemos datos de la web de formula1
            year = int(input("Ingrese un año entre 1950 y 2023: "))
        except ValueError:
            print("Ingrese un año válido")
            continue

        if 1950 <= year <= 2023:
            break
        else:
            print("Ingrese un año entre 1950 y 2023: ")

    year_filtrado = carreras_detalles[carreras_detalles['Fecha'].dt.year == year]

    # Ordenar el dataFrame por conductor y fecha
    year_filtrado = year_filtrado.sort_values(by=["Driver", "Fecha"])

    # Calcular los puntos acumulados por conductor
    year_filtrado["Puntos Acumulados Piloto"] = year_filtrado.groupby("Driver")["PTS"].cumsum()
    
    # CAMPEON Y ESCUDERIA GANADORA

    Campeon = year_filtrado.sort_values(by=['Puntos Acumulados Piloto'], ascending=False).iloc[0]['Driver']
    print('Campeon año', year, Campeon)

    # GRAFICO EVOLUCION PUNTAJE PILOTO

    # Filtrar el dataframe si fuese necessario y Crea el gráfico interactivo con Plotly Express

    fig = px.line(year_filtrado[year_filtrado["Puntos Acumulados Piloto"] >= 1],
                    x="Fecha", y="Puntos Acumulados Piloto", color="Driver",
                    title=f"Puntos Acumulados por Conductor a lo largo del año {year_filtrado[year_filtrado['Puntos Acumulados Piloto'] >= 1]['Fecha'].dt.year.iloc[0]}",
                    width=1500, height=800)

    # Mostrar el gráfico
    fig.show()


def puntaje_escuderia(carreras_detalles):
    """Función para generar una gráfica tipo "line" con la evolución del puntaje de una escudería a lo largo de una temporada (año) seleccionada por el usuario."""
    carreras_detalles['Fecha'] = pd.to_datetime(carreras_detalles['Fecha'])

    # Pedir al usuario que ingrese el año... el bucle es porque no sabemos cuantas veces podría ingresarlo mal
    while True:
        try:
            # estas fechas son las que tenemos datos de la web de formula1
            year = int(input("Ingrese un año entre 1950 y 2023: "))
        except ValueError:
            print("Ingrese un año válido")
            continue

        if 1950 <= year <= 2023:
            break
        else:
            print("Ingrese un año entre 1950 y 2023: ")

    year_filtrado = carreras_detalles[carreras_detalles['Fecha'].dt.year == year]

    # Ordenar el dataFrame por escuderia y fecha
    year_filtrado = year_filtrado.sort_values(by=["Car", "Fecha"])

    # Calcular los puntos acumulados por conductor
    year_filtrado["Puntos Acumulados Coche"] = year_filtrado.groupby("Car")["PTS"].cumsum()

    # CAMPEON Y ESCUDERIA GANADORA

    CocheCampeon = year_filtrado.sort_values(by=['Puntos Acumulados Coche'], ascending=False).iloc[0]['Car']
    print('Escuderia campeona año', year, CocheCampeon)

    # GRAFICO EVOLUCION PUNTAJE ESCUDERIA

    # Crear el gráfico interactivo con Plotly Express
    fig = px.line(year_filtrado, x="Fecha", y="Puntos Acumulados Coche", color="Car",
                  title=f"Puntos Acumulados por Escuderia a lo largo del año {year_filtrado['Fecha'].dt.year.iloc[0]}", width=1500, height=800)

    # Mostrar el gráfico
    fig.show()


def distribucion_puntaje_piloto(carreras_detalles):
    """Función para generar una gráfica tipo "pie" con la distribución final del puntaje de los pilotos en una temporada (año) seleccionada por el usuario."""
    carreras_detalles['Fecha'] = pd.to_datetime(carreras_detalles['Fecha'])

    # Pedir al usuario que ingrese el año... el bucle es porque no sabemos cuantas veces podría ingresarlo mal
    while True:
        try:
            # estas fechas son las que tenemos datos de la web de formula1
            year = int(input("Ingrese un año entre 1950 y 2023: "))
        except ValueError:
            print("Ingrese un año válido")
            continue

        if 1950 <= year <= 2023:
            break
        else:
            print("Ingrese un año entre 1950 y 2023: ")

    year_filtrado = carreras_detalles[carreras_detalles['Fecha'].dt.year == year]


    # Ordenar el dataFrame por conductor y fecha
    year_filtrado = year_filtrado.sort_values(by=["Driver", "Fecha"])

    # Calcular los puntos acumulados por conductor
    year_filtrado["Puntos Acumulados Piloto"] = year_filtrado.groupby("Driver")["PTS"].cumsum()

    # GRAFICO DISTRIBUCION PUNTAJE PILOTOS

    fig = px.pie(year_filtrado[year_filtrado["Puntos Acumulados Piloto"] >= 1], values='Puntos Acumulados Piloto',
                 names='Driver', title=f'Distribución de puntos al final de la temporada {year}', width=800, height=600)

    fig.show()


def distribucion_puntaje_escuderia(carreras_detalles):
    """Función para generar una gráfica tipo "pie" con la distribución final del puntaje de las escuderias en una temporada (año) seleccionada por el usuario."""
    carreras_detalles['Fecha'] = pd.to_datetime(carreras_detalles['Fecha'])

    # Pedir al usuario que ingrese el año... el bucle es porque no sabemos cuantas veces podría ingresarlo mal
    while True:
        try:
            # estas fechas son las que tenemos datos de la web de formula1
            year = int(input("Ingrese un año entre 1950 y 2023: "))
        except ValueError:
            print("Ingrese un año válido")
            continue

        if 1950 <= year <= 2023:
            break
        else:
            print("Ingrese un año entre 1950 y 2023: ")

    year_filtrado = carreras_detalles[carreras_detalles['Fecha'].dt.year == year]

    # Ordenar el dataFrame por escuderia y fecha
    year_filtrado = year_filtrado.sort_values(by=["Car", "Fecha"])

    # Calcular los puntos acumulados por conductor
    year_filtrado["Puntos Acumulados Coche"] = year_filtrado.groupby("Car")["PTS"].cumsum()

    # GRAFICO DISTRIBUCION PUNTAJE ESCUDERIAS

    fig = px.pie(year_filtrado, values='Puntos Acumulados Coche', names='Car',
                 title=f'Distribución de puntos al final de la temporada {year}', width=800, height=600)
    fig.show()


def distribucion_puntaje_piloto_y_escuderia(carreras_detalles):
    """Función para generar una gráfica tipo "sunburst" con la distribución final del puntaje de pilotos y escuderias en una temporada (año) seleccionada por el usuario."""
    carreras_detalles['Fecha'] = pd.to_datetime(carreras_detalles['Fecha'])

    # Pedir al usuario que ingrese el año... el bucle es porque no sabemos cuantas veces podría ingresarlo mal
    while True:
        try:
            # estas fechas son las que tenemos datos de la web de formula1
            year = int(input("Ingrese un año entre 1950 y 2023: "))
        except ValueError:
            print("Ingrese un año válido")
            continue

        if 1950 <= year <= 2023:
            break
        else:
            print("Ingrese un año entre 1950 y 2023: ")

    year_filtrado = carreras_detalles[carreras_detalles['Fecha'].dt.year == year]


    # Ordenar el dataFrame por conductor y fecha
    year_filtrado = year_filtrado.sort_values(by=["Driver", "Fecha"])

    # Calcular los puntos acumulados por conductor
    year_filtrado["Puntos Acumulados Piloto"] = year_filtrado.groupby("Driver")["PTS"].cumsum()
    
    # GRAFICO ESCUDERIAS Y PILOTOS

    fig = px.sunburst(year_filtrado, path=['Car', 'Driver'], values='Puntos Acumulados Piloto', width=600, height=600)
    fig.show()


def puntaje_piloto_por_circuito(carreras_detalles):
    """Función para generar una gráfica tipo "bar" con el puntaje de los pilotos categorizadas según el circuito donde lo obtuvieron para una temporada (año) seleccionada por el usuario."""
    carreras_detalles['Fecha'] = pd.to_datetime(carreras_detalles['Fecha'])

    # Pedir al usuario que ingrese el año... el bucle es porque no sabemos cuantas veces podría ingresarlo mal
    while True:
        try:
            # estas fechas son las que tenemos datos de la web de formula1
            year = int(input("Ingrese un año entre 1950 y 2023: "))
        except ValueError:
            print("Ingrese un año válido")
            continue

        if 1950 <= year <= 2023:
            break
        else:
            print("Ingrese un año entre 1950 y 2023: ")

    year_filtrado = carreras_detalles[carreras_detalles['Fecha'].dt.year == year]

    # PUNTAJES DE PILOTOS POR CIRCUITOS

    fig = px.bar(year_filtrado, y=year_filtrado['PTS'], x=year_filtrado['Driver'],
                 color=year_filtrado['Circuito'], height=700, width=1500)
    fig.update_layout(barmode='stack', xaxis={
                      'categoryorder': 'category ascending'})
    fig.show()


def puntaje_escuderia_por_circuito(carreras_detalles):
    """Función para generar una gráfica tipo "bar" con el puntaje de las escuderías categorizadas según el circuito donde lo obtuvieron para una temporada (año) seleccionada por el usuario."""
    carreras_detalles['Fecha'] = pd.to_datetime(carreras_detalles['Fecha'])

    # Pedir al usuario que ingrese el año... el bucle es porque no sabemos cuantas veces podría ingresarlo mal
    while True:
        try:
            # estas fechas son las que tenemos datos de la web de formula1
            year = int(input("Ingrese un año entre 1950 y 2023: "))
        except ValueError:
            print("Ingrese un año válido")
            continue

        if 1950 <= year <= 2023:
            break
        else:
            print("Ingrese un año entre 1950 y 2023: ")

    year_filtrado = carreras_detalles[carreras_detalles['Fecha'].dt.year == year]

    # PUNTAJES DE ESCUDERIAS POR CIRCUITOS

    fig = px.bar(year_filtrado, y=year_filtrado['PTS'], x=year_filtrado['Car'],
                 color=year_filtrado['Circuito'], height=500, width=1200)
    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})
    fig.show()


def mapa(df):
    """Función que muestra un mapa con marcadores por ciudad y etiquetas de los grandes premios de Fórmula 1."""
    mapa_ciudades_circuitos = folium.Map()
    premios = folium.map.FeatureGroup()

    for lat, lng, label in zip(df["lat"], df["lon"], df["meeting_name"]): 
    
        premios.add_child(folium.Marker(location = [lat, lng],
                                      popup    = label,))

    # Agrega incidentes al mapa
    mapa_ciudades_circuitos.add_child(premios)

    display(mapa_ciudades_circuitos)

    return mapa_ciudades_circuitos


def graficar_viento(df):
    """Función que muestra un gráfico de dispersión por gran premio en m/s."""
    df["wind_speed_mean"] = df["wind_speed_mean"].apply(lambda _: float(_))
    fig = px.scatter(data_frame  = df,
            x           = "date_start",
            y           = "wind_speed_mean",
            color       = "meeting_name",
            hover_name  = "meeting_name",
            width       = None,
            height      = None,
            opacity     = 0.5,
            title=   "wind_speed m/s 2023")
    
    fig.show()


def graficas_temperatura(df):
    """Función que obtiene la temperatura en gráfico de barras por gran premio. A su vez, muestra una comparativa en gráfica lineal con la temperatura de la pista."""
    df["air_temperature_mean"] = df["air_temperature_mean"].apply(lambda _: float(_))
    df["track_temperature_mean"] = df["track_temperature_mean"].apply(lambda _: float(_))

    plt.figure(figsize = (18, 5))

    plt.plot(df["air_temperature_mean"], color = "blue", label = "air_temperature" )

    plt.plot(df["track_temperature_mean"], color = "red", label = "track_temperature")
    plt.legend()
    plt.title('track_temperatur and air_temperature')

    plt.show()

    fig = px.histogram( data_frame= df ,
                    x = "date_start",
                    y = "air_temperature_mean",
                    color = "location",
                    nbins = 50 )
    
    fig.show()


def columna_lluvia(df):
    """Función que muestra un gráfico tipo pie del porcentaje de lluvia a lo largo de la temporada 2023."""
    df["rainfall_mean"] = df["rainfall_mean"].apply(lambda _: float(_))
    lluvia=[]
    for x in df["rainfall_mean"]:
        if x < 0.15:
            x = "no rain or little rain"
        elif x < 0.30:
            x = "rain"
        else:   
            x= "a lot of rain"
        lluvia.append(x)

    df["lluvia"] = lluvia
    fig = px.pie(data_frame = df,
                names      = "lluvia",
                values     = "rainfall_mean",
                title=   "Lluvia en la temporada 2023")
    
    fig.show()