# Aplicacion Interactiva - Visualizaciones de Formula 1 
## Autores: DSB09 Grupo 3

# Como Utilizar
Para utilizar este proyecto se requiere seguir estos pasos:
- Clonar el repositorio (`git clone`)
- Instalar dependencias del proyecto (`pip install -r requirements.txt`)
- Agregar tus detalles de configuracion y credenciales a `ejemplo_config.ini` y cambiale el nombre a `config.ini` que esta incluido en el `.gitignore` para no subir informacion confidencial
- Abrir `test_app.ipynb` o `app.py`
- En `test_app.ipynb`, corre todas las celdas, y a divertirse!
- En `app.py`, usa la aplicacion por la terminal usando el comando `python3 app.py` o `python3 -m app` y a divertirse!

## Credenciales
Para utilizar la aplicacion, debe tener acceso a Airtable y crear sus propias bases de datos usando `setup.ipynb`. Para que funcione `scrape_weather()` del modulo `scrape_f1.py` necesita tambien acceso a OpenWeather. La aplicacion requiere tener toda la informacion dentro del `ejemplo_config.ini` para hacer el "scraping" requerido (`token` del usuario y `base_id` de la base de datos para Airtable, y `api_key` para OpenWeather). 

**CUIDADO:** Si modifica el funcionamiento de `setup.ipynb`, puede que el resto de la aplicacion no funcione. Revise la seccion de [Como Modificar](#como-modificar) antes de hacer cualquier modificacion, ya que `graficos.py` interactua directamente con los datos como estan en las tablas de Airtable creadas en `setup.ipynb`.

# Librerias
Hay 4 modulos claves en el proyecto, todas bajo la carpeta `libreria`:
- `scrape_f1.py`
- `airtable.py`
- `graficos.py`
- `ui.py`

## scrape_f1.py
Contiene una serie de funciones que se utilizan para hacer "scraping" de informacion por la web relacionada al Formula 1, retornando DataFrames para procesamiento de datos.

## airtable.py
Contiene un objecto principal, `AirtableConnector`, que permite interactuar con Airtable atraves de el objeto como una interfaz. Simplifica la creacion de tablas, como subir datos y como leer datos directamente a un DataFrame.

## graficos.py
Contiene una serie de funciones con graficos. Los graficos todos utilizan los DataFrames formados al importar los datos de Airtable (`AirtableConnector.to_df()`) para estandarizar y pasarlo todo de formato consistent a la interfaz en `ui.py`. Pasos de limpieza de datos se contienen dentro de cada funcion y esto es algo que se podria mejorar en futuro agregando un `preprocessing.py` que `graficos.py` pueda importar e utilizar.

## ui.py
Contiene un objeto principal `UI` al que se le pasa una serie de funciones y sus argumentos. Esta es la manera de inicializar el proyecto y la interfaz del usuario (_'User Interface'_) usando `UI.start()` despues de inicializar con la lista de funciones. 

La lista de funciones debe ser una lista de tuples de 2 elementos, donde el primer elemento es el nombre de la funcion (`Callable object`) y el segundo es una lista con los argumentos que hay que pasarle. En la mayoria de los casos estos argumentos son DataFrames.

# Como Modificar
La aplicacion se puede modificar agregando nuevas funciones de graficos que usen `display()` o `.show()`. No requieren retornar nada, sino visualizar. Estas funciones se pueden meter en `graficos.py` e importarse al archivo principal `app.py` o `test_app.ipynb` y pasarselo a la lista de funciones que se usa al inicializar el objeto `UI` de `ui.py`, junto a una lista de cualquier argumento. 

Vea `app.py` o `test_app.ipynb` para ver ejemplos.

Se puede modificar la base de datos, pero requerira que el usuario reemplace el modulo `graficos.py` con su propio modulo, procesando datos del modo en que se formateen en la nueva base de datos del usuario. Para modificar la base de datos utilice `setup.ipynb` y cambie o agregue las funciones de "scraping" requeridas a `scrape_f1.py`. Tambien se puede crear otro modulo de extraccion de datos y usarlo en complemento con los otros modulos una vez sean los datos subidos a Airtable. 

El modulo `airtable.py` no tiene dependencia en los otros modulos ni en su formato asi que con seguir los ejemplos en `setup.ipynb` se deberia poder crear su propia base de datos utilizando el objecto `AirtableConnector` y sus metodos.

## License
For open source projects, say how it is licensed.

## Project status
Completed - minor patches to possibly be implemented in future
