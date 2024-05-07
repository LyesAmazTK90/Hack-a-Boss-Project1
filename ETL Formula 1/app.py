import configparser
from libreria.airtable import AirtableConnector
from libreria.ui import UI
# Importe de funciones de libreria/graficos.py
from libreria.ui import UI
from libreria.graficos import   diez_mejores_pilotos, \
                                comparativa_todos_pilotos, \
                                puntaje_piloto, \
                                puntaje_escuderia, \
                                distribucion_puntaje_piloto, \
                                distribucion_puntaje_escuderia, \
                                distribucion_puntaje_piloto_y_escuderia, \
                                puntaje_piloto_por_circuito, \
                                puntaje_escuderia_por_circuito, \
                                mapa, \
                                graficar_viento, \
                                graficas_temperatura, \
                                columna_lluvia, \
                                tiempos_rapidos_por_piloto_Grand_Prix_año

def main():
    # Read in configuration
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Extract config for AirtableConnector initialisation
    TOKEN = config.get('airtable', 'TOKEN')
    BASE_ID = config.get('airtable', 'BASE_ID')

    connector = AirtableConnector(TOKEN, BASE_ID)

    # Preparar prerequisitos
    carreras = connector.to_df('carreras')
    weather = connector.to_df('weather')
    carreras_detalles = connector.to_df('carreras_detalles')

    funciones = [
        (diez_mejores_pilotos, [carreras]), 
        (comparativa_todos_pilotos, [carreras]), 
        (puntaje_piloto, [carreras_detalles]),
        (puntaje_escuderia, [carreras_detalles]),
        (distribucion_puntaje_piloto, [carreras_detalles]),
        (distribucion_puntaje_escuderia, [carreras_detalles]),
        (distribucion_puntaje_piloto_y_escuderia, [carreras_detalles]),
        (puntaje_piloto_por_circuito, [carreras_detalles]),
        (puntaje_escuderia_por_circuito, [carreras_detalles]),
        (mapa, [weather]),
        (graficar_viento, [weather]),
        (graficas_temperatura, [weather]),
        (columna_lluvia, [weather]),
        # (tiempos_rapidos_por_piloto_Grand_Prix_año, [grouped_carreras]) #TODO: Arreglar funcion
]

    ui = UI(funciones)
    ui.start()

    
if __name__ == "__main__":
    main()