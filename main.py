
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import csv
import os
import json

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
        
        print(f"Archivo no e    contrado: {archivo}")
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
    
    # Configurar pantalla completa (maximizado)
    try:
        root_ventana.state('zoomed')  # Maximiza la ventana en Windows
    except:
        # Si no funciona 'zoomed', intentar pantalla completa real
        try:
            root_ventana.attributes('-fullscreen', True)
        except:
            # Si tampoco funciona, centrar la ventana
            root_ventana.position_center()
    
    root_ventana.protocol("WM_DELETE_WINDOW", salir_juego)

# Función para guardar la partida en un archivo CSV
def guardar_partida(archivo='partida_guardada.csv'):
    global jugador_actual
    
    if not jugador_actual:
        return False, "No hay partida para guardar"
    
    try:
        # Obtener el nivel de dificultad desde el módulo interfaz
        from modules import interfaz
        nivel_dificultad = interfaz.estado.get('nivel_dificultad', 1)
        
        # Crear directorio saves si no existe
        if not os.path.exists('saves'):
            os.makedirs('saves')
        
        ruta_archivo = os.path.join('saves', archivo)
        
        # Preparar los datos del personaje para guardar
        datos_guardar = {
            'nombre': jugador_actual.get('nombre', ''),
            'clase': jugador_actual.get('clase', ''),
            'nivel': str(jugador_actual.get('nivel', 1)),
            'experiencia': str(jugador_actual.get('experiencia', 0)),
            'experiencia_necesaria': str(jugador_actual.get('experiencia_necesaria', 100)),
            'vida_actual': str(jugador_actual.get('vida_actual', 0)),
            'vida_maxima': str(jugador_actual.get('vida_maxima', 0)),
            'mana_actual': str(jugador_actual.get('mana_actual', 0)),
            'mana_maximo': str(jugador_actual.get('mana_maximo', 0)),
            'ataque': str(jugador_actual.get('ataque', 0)),
            'defensa': str(jugador_actual.get('defensa', 0)),
            'velocidad': str(jugador_actual.get('velocidad', 0)),
            'nivel_dificultad': str(nivel_dificultad),
            'equipo': json.dumps(jugador_actual.get('equipo', {}), ensure_ascii=False),
            'habilidades': json.dumps(jugador_actual.get('habilidades', []), ensure_ascii=False),
            'inventario': json.dumps(jugador_actual.get('inventario', {}), ensure_ascii=False)
        }
        
        # Escribir en CSV
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=datos_guardar.keys())
            writer.writeheader()
            writer.writerow(datos_guardar)
        
        return True, f"Partida guardada exitosamente en {ruta_archivo}"
    
    except Exception as e:
        return False, f"Error al guardar partida: {str(e)}"

# Función para cargar la partida desde un archivo CSV
def cargar_partida(archivo='partida_guardada.csv'):
    global jugador_actual
    
    try:
        ruta_archivo = os.path.join('saves', archivo)
        
        if not os.path.exists(ruta_archivo):
            return False, f"Archivo de partida no encontrado: {ruta_archivo}"
        
        # Leer el CSV
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            datos = next(reader, None)
            
            if not datos:
                return False, "El archivo de partida está vacío"
            
            # Reconstruir el diccionario del personaje
            jugador_actual = {
                'nombre': datos.get('nombre', ''),
                'clase': datos.get('clase', 'guerrero'),
                'nivel': int(datos.get('nivel', 1)),
                'experiencia': int(datos.get('experiencia', 0)),
                'experiencia_necesaria': int(datos.get('experiencia_necesaria', 100)),
                'vida_actual': int(datos.get('vida_actual', 0)),
                'vida_maxima': int(datos.get('vida_maxima', 0)),
                'mana_actual': int(datos.get('mana_actual', 0)),
                'mana_maximo': int(datos.get('mana_maximo', 0)),
                'ataque': int(datos.get('ataque', 0)),
                'defensa': int(datos.get('defensa', 0)),
                'velocidad': int(datos.get('velocidad', 0)),
                'equipo': json.loads(datos.get('equipo', '{}')),
                'habilidades': json.loads(datos.get('habilidades', '[]')),
                'inventario': json.loads(datos.get('inventario', '{}'))
            }
            
            # Restaurar el nivel de dificultad
            from modules import interfaz
            nivel_dificultad = int(datos.get('nivel_dificultad', 1))
            interfaz.estado['nivel_dificultad'] = nivel_dificultad
        
        return True, f"Partida cargada exitosamente: {jugador_actual['nombre']}"
    
    except json.JSONDecodeError as e:
        return False, f"Error al decodificar datos de la partida: {str(e)}"
    except Exception as e:
        return False, f"Error al cargar partida: {str(e)}"

# Función para obtener lista de partidas guardadas con información
def obtener_partidas_guardadas():
    partidas = []
    directorio_saves = 'saves'
    
    if os.path.exists(directorio_saves):
        for archivo in os.listdir(directorio_saves):
            if archivo.endswith('.csv'):
                # Intentar leer información básica de la partida
                try:
                    ruta_archivo = os.path.join(directorio_saves, archivo)
                    with open(ruta_archivo, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        datos = next(reader, None)
                        if datos:
                            nombre_pj = datos.get('nombre', 'Desconocido')
                            nivel = datos.get('nivel', '?')
                            clase = datos.get('clase', '?')
                            info = f"{nombre_pj} - Nivel {nivel} ({clase.title()})"
                            partidas.append({'archivo': archivo, 'info': info})
                        else:
                            partidas.append({'archivo': archivo, 'info': archivo})
                except:
                    partidas.append({'archivo': archivo, 'info': archivo})
    
    return partidas

# Función para salir del juego
def salir_juego():
    global jugador_actual, root_ventana
    
    if jugador_actual:
        print(f"Saliendo del juego...")
    
    root_ventana.destroy()

# Función para inicializar el juego
def inicializar_juego():
    global root_ventana
    
    root_ventana = ttk.Window(
        title="Los Tres Pilares Olvidados",   
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
