import time
from collections.abc import Callable

class UI:
    def __init__(self, funciones_y_argumentos: tuple[Callable, list]):
        self.funciones = [funcion[0] for funcion in funciones_y_argumentos]
        self.argumentos = [funcion[1] for funcion in funciones_y_argumentos]


    def start(self):
        continuar = True
        # Texto inicial
        self.F1_intro_graphic1()
        self.F1_intro_graphic2()
        self.F1_intro_texto()

        # Loop de ejecucion
        while continuar:

            # Interaccion
            opcion = self.F1_seleccion()

            # Ejecucion
            if opcion:
                self.F1_procesar_solicitud(opcion)
            else:
                break
            
            continuar = self.F1_continuar()

        self.F1_intro_interactivo()
        print("\n\033[31m                   Muchas gracias por utilizar Formula 1...¡Hasta pronto!\033[0m")
        self.F1_intro_graphic2()


    def F1_seleccion(self):
        while True:
            self.F1_intro_interactivo()
            self.F1_intro_opciones()
            self.F1_intro_interactivo()
            opcion = input("Introduzca el numero de su opcion: ")
            if opcion == 'exit':
                return 
            try:
                opcion = int(opcion)
            except ValueError:
                print("Por favor intenta otra vez. Asegurese que sea solo un numero.")
                continue
            
            if 0 < opcion <= len(self.funciones):
                return opcion
            else:
                print(f"Por favor intenta otra vez. El numero debe ser entre el 1 y {len(self.funciones)}.")
                continue


    def F1_intro_graphic1(self):

        cocheF1 = """                                            d88b
                            _______________|8888|_______________
                            |_____________ ,~~~~~~. _____________|
          _________         |_____________: mmmmmm :_____________|         _________
         / _______ \   ,----|~~~~~~~~~~~,'\ _...._ /`.~~~~~~~~~~~|----,   / _______ \ 
        | /       \ |  |    |       |____|,d~    ~b.|____|       |    |  | /       \ |
        ||         |-------------------\-d.-~~~~~~-.b-/-------------------|         ||
        ||         | |8888 ....... _,===~/......... \~===._         8888| |         ||
        ||         |=========_,===~~======._.=~~=._.======~~===._=========|         ||
        ||         | |888===~~ ....../ /,, .`~~~~'. .,\ \       ~~===888| |         ||
        ||        |===================,P'.::::::::.. `?,===================|        ||
        ||        |_________________,P'_::----------.._`?,_________________|        ||
        `|        |-------------------~~~~~~~~~~~~~~~~~~-------------------|        |'
         \_______/                                                         \_______/    """


        for i in range(len(cocheF1)):
            # Utiliza la secuencia de escape ANSI para cambiar el color del texto a medida que se imprime
            print(f"\033[32m{cocheF1[i]}\033[0m", end='', flush=True)  # Color verde
            time.sleep(0.001)  # Pausa de 0.001 segundos entre cada caracter
        print()  # Salto de línea al final


    def F1_intro_graphic2(self):    
        
        logoF1="""                          __                           _         __  
                         / _|                         | |       /  | 
                        | |_ ___  _ __ _ __ ___  _   _| | __ _  `| | 
                        |  _/ _ \| '__| '_ ` _ \| | | | |/ _` |  | | 
                        | || (_) | |  | | | | | | |_| | | (_| |  | |_
                        |_| \___/|_|  |_| |_| |_|\__,_|_|\__,_| \___/ """
        
        for i in range(len(logoF1)):
            # Utiliza la secuencia de escape ANSI para cambiar el color del texto a medida que se imprime
            print(f"\033[32m{logoF1[i]}\033[0m", end='', flush=True)  # Color verde
            time.sleep(0.001)  # Pausa de 0.01 segundos entre cada caracter
        print()  # Salto de línea al final


    def F1_intro_texto(self):
        print("\n\033[31m                               ¡ADRENALINA EN ESTADO PURO!\033[0m")
        print("\nBienvenido a tu pitlane favorito con toda la información de actualidad del apasionante mundo de la Fórmula 1.\n")
        

    def F1_intro_interactivo(self):

        barreraF1 = """\n-------------FORMULA1------------FORMULA1------------FORMULA1------------FORMULA1------------FORMULA1------------
---FORMULA1------------FORMULA1------------FORMULA1------------FORMULA1------------FORMULA1------------FORMULA1--\n"""
        for i in range(len(barreraF1)):
            # Utiliza la secuencia de escape ANSI para cambiar el color del texto a medida que se imprime
            print(f"\033[32m{barreraF1[i]}\033[0m", end='', flush=True)  # Color verde
            time.sleep(0.001)  # Pausa de 0.01 segundos entre cada caracter
        print()  # Salto de línea al final


    def F1_intro_opciones(self):

        print(f"Introduce un numero entre 1 y {len(self.funciones)} seleccionando la opcion del siguiente listado:\n" + "\033[3m" + "\033[0m")
        for i, funcion in enumerate(self.funciones):
            print(f"{i+1} - {funcion.__name__}")
            print(f"Descripcion: {funcion.__doc__}\n")

        print(f"\nEscribe 'exit' para salir de la aplicacion.\n")


    def F1_continuar(self):

        while True:
            continuar = input("¿Deseas realizar otra consulta? (si/no): ").lower()
            if continuar == "no":
                return False
            elif continuar == "si":
                return True
            else:
                print("\nRespuesta inválida. Por favor, responde 'si' o 'no'.")     


    def F1_procesar_solicitud(self, user_opt_input):
        # Usuario selecciona empezando del numero 1, lista de funciones empieza en 0
        funcion = self.funciones[user_opt_input - 1]
        args = self.argumentos[user_opt_input - 1]

        print(f"\nEjecutando la función {user_opt_input}: {funcion.__name__}\n")

        funcion(*args)