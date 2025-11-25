
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import csv
import os

# Variables globales del juego
jugador_actual = None  # Almacena el diccionario del jugador actual
datos_juego = {}  # Almacena todos los datos del juego (enemigos, habilidades, equipo)
root_ventana = None  # Almacena la ventana principal

# Función para cargar un archivo CSV
def cargar_csv(archivo):
    
    if os.path.exists(archivo):
        try:
           
            with open(archivo, 'r', encoding='utf-8') as f:
                return list(csv.DictReader(f))
        except Exception as e:
            
            print(f"Error cargando {archivo}: {e}")
            return []
    else:
        
        print(f"Archivo no encontrado: {archivo}")
        return []

# Función para cargar todos los datos del juego
def cargar_datos():
    global datos_juego

    datos_juego = {
        'enemigos': cargar_csv('data/enemigos.csv'),
        'habilidades': cargar_csv('data/habilidades.csv'),
        'equipo': cargar_csv('data/equipo.csv')
    }
    print("Datos del juego cargados correctamente")

# Función para configurar la ventana principal
def configurar_ventana():
    global root_ventana
    
    root_ventana.position_center()
    
    root_ventana.protocol("WM_DELETE_WINDOW", salir_juego)

# Función para salir del juego
def salir_juego():
    global jugador_actual, root_ventana
    
    if jugador_actual:
        print(f"Guardando progreso de {jugador_actual['nombre']}...")
    
    root_ventana.quit()

# Función para inicializar el juego
def inicializar_juego():
    global root_ventana
    
    root_ventana = ttk.Window(
        title="JuegoRPG",
        themename="cyborg",
        size=(2048, 1024),
        resizable=(True, True),
        iconphoto=None
    )
    
    # Cargar datos del juego
    cargar_datos()
    # Configurar la ventana
    configurar_ventana()
    
    # Inicializar la interfaz gráfica
    from modules.interfaz import inicializar_interfaz
    inicializar_interfaz(root_ventana)

# Función para iniciar el juego
def iniciar():
    print("Iniciando RPG por Turnos...")
    
    root_ventana.mainloop()

# Punto de entrada del programa
if __name__ == "__main__":
    try:
        
        inicializar_juego()
        iniciar()
    except Exception as e:
        
        print(f"Error crítico: {e}")
        input("Presiona Enter para salir...")
