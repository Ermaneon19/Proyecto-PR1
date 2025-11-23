import csv

def obtener_stats_base(clase):
    stats = {
        "guerrero": {
            "vida_maxima": 120,
            "mana_maximo": 30,
            "ataque": 18,
            "defensa": 15,
            "velocidad": 8
        },
        "mago": {
            "vida_maxima": 80,
            "mana_maximo": 100,
            "ataque": 12,
            "defensa": 8,
            "velocidad": 10
        },
        "arquero": {
            "vida_maxima": 90,
            "mana_maximo": 50,
            "ataque": 16,
            "defensa": 10,
            "velocidad": 14
        }
    }
    return stats.get(clase, stats["guerrero"])

def obtener_habilidades_iniciales(clase):
    habilidades = {
        "guerrero": ["Golpe Poderoso", "Defender"],
        "mago": ["Bola de Fuego", "Curar"],
        "arquero": ["Disparo Preciso", "Esquivar"]
    }
    return habilidades.get(clase, ["Ataque Básico"])

def crear_personaje(nombre, clase="guerrero"):
    stats_base = obtener_stats_base(clase)
    
    personaje = {
        "nombre": nombre,
        "clase": clase,
        "nivel": 1,
        "experiencia": 0,
        "experiencia_necesaria": 100,
        "vida_actual": stats_base["vida_maxima"],
        "vida_maxima": stats_base["vida_maxima"],
        "mana_actual": stats_base["mana_maximo"],
        "mana_maximo": stats_base["mana_maximo"],
        "ataque": stats_base["ataque"],
        "defensa": stats_base["defensa"],
        "velocidad": stats_base["velocidad"],
        "equipo": {},
        "habilidades": obtener_habilidades_iniciales(clase),
        "inventario": {
            "Poción de Mana Pequeña": {"cantidad": 3, "tipo": "consumible", "mana": 20},
            "Poción de Mana Grande": {"cantidad": 1, "tipo": "consumible", "mana": 50}
        }
    }
    return personaje

def atacar_personaje(personaje, objetivo):
    from modules.enemigo import recibir_daño_enemigo
    daño = max(1, personaje["ataque"] - (objetivo["defensa"] // 2))
    recibir_daño_enemigo(objetivo, daño)
    return daño

def recibir_daño_personaje(personaje, daño):
    personaje["vida_actual"] = max(0, personaje["vida_actual"] - daño)
    return personaje["vida_actual"] > 0

def curar_personaje(personaje, cantidad):
    personaje["vida_actual"] = min(personaje["vida_maxima"], personaje["vida_actual"] + cantidad)

def esta_vivo_personaje(personaje):
    return personaje["vida_actual"] > 0

def ganar_experiencia(personaje, exp):
    personaje["experiencia"] += exp
    if personaje["experiencia"] >= personaje["experiencia_necesaria"]:
        subir_nivel(personaje)

def subir_nivel(personaje):
    personaje["nivel"] += 1
    personaje["experiencia"] = 0
    personaje["experiencia_necesaria"] = int(personaje["experiencia_necesaria"] * 1.5)
    
    personaje["vida_maxima"] += 10
    personaje["ataque"] += 2
    personaje["defensa"] += 1
    personaje["velocidad"] += 1
    
    personaje["vida_actual"] = personaje["vida_maxima"]
    personaje["mana_actual"] = personaje["mana_maximo"]
    
    return f"¡{personaje['nombre']} ha subido al nivel {personaje['nivel']}!"
