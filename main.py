import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import csv
import os

jugador_actual = None
datos_juego = {}
root_ventana = None

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

def cargar_datos():
    global datos_juego
    datos_juego = {
        'enemigos': cargar_csv('data/enemigos.csv'),
        'habilidades': cargar_csv('data/habilidades.csv'),
        'equipo': cargar_csv('data/equipo.csv')
    }
    print("Datos del juego cargados correctamente")

def configurar_ventana():
    global root_ventana
    root_ventana.position_center()
    root_ventana.protocol("WM_DELETE_WINDOW", salir_juego)

def salir_juego():
    global jugador_actual, root_ventana
    if jugador_actual:
        print(f"Guardando progreso de {jugador_actual['nombre']}...")
    root_ventana.quit()

def inicializar_juego():
    global root_ventana
    root_ventana = ttk.Window(
        title="JuegoRPG",
        themename="cyborg",
        size=(2048, 1024),
        resizable=(True, True),
        iconphoto=None
    )
    
    cargar_datos()
    configurar_ventana()
    
    from modules.interfaz import inicializar_interfaz
    inicializar_interfaz(root_ventana)

def iniciar():
    print("Iniciando RPG por Turnos...")
    root_ventana.mainloop()

if __name__ == "__main__":
    try:
        inicializar_juego()
        iniciar()
    except Exception as e:
        print(f"Error crítico: {e}")
        input("Presiona Enter para salir...")
