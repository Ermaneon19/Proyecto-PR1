import random
import csv
import os

def obtener_stats_desde_csv(nombre):
    csv_path = 'data/enemigos.csv'
    if os.path.exists(csv_path):
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['nombre'] == nombre:
                        return {
                            'vida_maxima': int(row['vida_maxima']),
                            'ataque': int(row['ataque']),
                            'defensa': int(row['defensa']),
                            'velocidad': int(row['velocidad']),
                            'experiencia_otorgada': int(row['experiencia_otorgada'])
                        }
        except Exception as e:
            print(f"Error cargando enemigo desde CSV: {e}")
    
    return {
        'vida_maxima': 50,
        'ataque': 12,
        'defensa': 5,
        'velocidad': 8,
        'experiencia_otorgada': 25
    }

def crear_enemigo(nombre, zona="bosque", datos_enemigo=None, multiplicador_dificultad=1.0):
    if datos_enemigo:
        stats = {
            'vida_maxima': int(datos_enemigo.get('vida_maxima', 50)),
            'ataque': int(datos_enemigo.get('ataque', 10)),
            'defensa': int(datos_enemigo.get('defensa', 5)),
            'velocidad': int(datos_enemigo.get('velocidad', 8)),
            'experiencia_otorgada': int(datos_enemigo.get('experiencia_otorgada', 20))
        }
    else:
        stats = obtener_stats_desde_csv(nombre)
    
    stats['vida_maxima'] = int(stats['vida_maxima'] * multiplicador_dificultad)
    stats['ataque'] = int(stats['ataque'] * multiplicador_dificultad)
    stats['defensa'] = int(stats['defensa'] * multiplicador_dificultad)
    stats['velocidad'] = int(stats['velocidad'] * multiplicador_dificultad)
    stats['experiencia_otorgada'] = int(stats['experiencia_otorgada'] * multiplicador_dificultad)
    
    enemigo = {
        "nombre": nombre,
        "zona": zona,
        "vida_actual": stats['vida_maxima'],
        "vida_maxima": stats['vida_maxima'],
        "ataque": stats['ataque'],
        "defensa": stats['defensa'],
        "velocidad": stats['velocidad'],
        "experiencia_otorgada": stats['experiencia_otorgada']
    }
    return enemigo

def atacar_enemigo(enemigo, objetivo):
    from modules.personaje import recibir_daño_personaje
    daño = max(1, enemigo["ataque"] - (objetivo["defensa"] // 3))
    recibir_daño_personaje(objetivo, daño)
    return daño

def recibir_daño_enemigo(enemigo, daño):
    enemigo["vida_actual"] = max(0, enemigo["vida_actual"] - daño)
    return enemigo["vida_actual"] > 0

def esta_vivo_enemigo(enemigo):
    return enemigo["vida_actual"] > 0

def elegir_accion_enemigo(enemigo, jugador):
    if enemigo["vida_actual"] < enemigo["vida_maxima"] * 0.3 and random.random() < 0.2:
        return "habilidad_especial"
    return "atacar"

def usar_habilidad_aleatoria_enemigo(enemigo, objetivo):
    from modules.personaje import recibir_daño_personaje
    habilidades = [
        {
            "nombre": "Ataque Feroz",
            "daño_multiplier": 1.2,
            "descripcion": "Un ataque más poderoso"
        },
        {
            "nombre": "Golpe Rápido",
            "daño_multiplier": 0.9,
            "descripcion": "Un ataque rápido"
        },
        {
            "nombre": "Ataque Normal",
            "daño_multiplier": 1.0,
            "descripcion": "Un ataque estándar"
        },
        {
            "nombre": "Golpe Crítico",
            "daño_multiplier": 1.5,
            "descripcion": "¡Un golpe crítico!"
        }
    ]
    
    habilidad = random.choice(habilidades)
    
    daño_base = enemigo["ataque"] * habilidad["daño_multiplier"]
    daño = max(1, int(daño_base) - (objetivo["defensa"] // 3))
    
    recibir_daño_personaje(objetivo, daño)
    
    return {
        "nombre": habilidad["nombre"],
        "daño": daño,
        "descripcion": habilidad["descripcion"]
    }
