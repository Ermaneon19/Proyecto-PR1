import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import csv
import os
from modules.personaje import Personaje
from modules.combate import SistemaCombate
from modules.interfaz import InterfazPrincipal

class JuegoRPG:
    def __init__(self):
        self.root = ttk.Window(
            title="JuegoRPG",
            themename="superhero",
            size=(2048, 1024),
            resizable=(True, True),
            iconphoto=None
        )
        
        self.cargar_datos()
        
        self.jugador = None
        self.sistema_combate = SistemaCombate()
        self.interfaz = InterfazPrincipal(self.root, self)
        
        self.configurar_ventana()
    
    def cargar_datos(self):
        """Cargar datos desde archivos CSV"""
        self.datos = {
            'enemigos': self.cargar_csv('data/enemigos.csv'),
            'habilidades': self.cargar_csv('data/habilidades.csv'),
            'equipo': self.cargar_csv('data/equipo.csv')
        }
        print("Datos del juego cargados correctamente")
    
    def cargar_csv(self, archivo):
        """Cargar un archivo CSV y convertirlo en lista de diccionarios"""
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
    
    def configurar_ventana(self):
        """Configurar la ventana principal"""
        self.root.position_center()
        self.root.protocol("WM_DELETE_WINDOW", self.salir)
    
    def salir(self):
        """Método para salir del juego"""
        if self.jugador:
            print(f"Guardando progreso de {self.jugador.nombre}...")
        self.root.quit()
    
    def iniciar(self):
        """Iniciar el juego"""
        print("Iniciando RPG por Turnos...")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        juego = JuegoRPG()
        juego.iniciar()
    except Exception as e:
        print(f"Error crítico: {e}")
        input("Presiona Enter para salir...")