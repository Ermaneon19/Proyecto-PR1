import random
import csv
import os

class Enemigo:
    def __init__(self, nombre, zona="bosque", datos_enemigo=None, multiplicador_dificultad=1.0):
        self.nombre = nombre
        self.zona = zona
        
        if datos_enemigo:
            self.stats = {
                'vida_maxima': int(datos_enemigo.get('vida_maxima', 50)),
                'ataque': int(datos_enemigo.get('ataque', 10)),
                'defensa': int(datos_enemigo.get('defensa', 5)),
                'velocidad': int(datos_enemigo.get('velocidad', 8)),
                'experiencia_otorgada': int(datos_enemigo.get('experiencia_otorgada', 20))
            }
        else:
            self.stats = self.obtener_stats_desde_csv(nombre)
        
        self.stats['vida_maxima'] = int(self.stats['vida_maxima'] * multiplicador_dificultad)
        self.stats['ataque'] = int(self.stats['ataque'] * multiplicador_dificultad)
        self.stats['defensa'] = int(self.stats['defensa'] * multiplicador_dificultad)
        self.stats['velocidad'] = int(self.stats['velocidad'] * multiplicador_dificultad)
        self.stats['experiencia_otorgada'] = int(self.stats['experiencia_otorgada'] * multiplicador_dificultad)
        
        self.vida_actual = self.stats['vida_maxima']
        self.vida_maxima = self.stats['vida_maxima']
        self.ataque = self.stats['ataque']
        self.defensa = self.stats['defensa']
        self.velocidad = self.stats['velocidad']
        self.experiencia_otorgada = self.stats['experiencia_otorgada']
    
    def obtener_stats_desde_csv(self, nombre):
        """Obtener stats desde CSV"""
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
    
    def atacar(self, objetivo):
        """Ataque del enemigo"""
        daño = max(1, self.ataque - (objetivo.defensa // 3))
        objetivo.recibir_daño(daño)
        return daño
    
    def recibir_daño(self, daño):
        """Recibir daño"""
        self.vida_actual = max(0, self.vida_actual - daño)
        return self.vida_actual > 0
    
    def esta_vivo(self):
        """Verificar si el enemigo está vivo"""
        return self.vida_actual > 0
    
    def elegir_accion(self, jugador):
        """IA simple para elegir acción"""
        if self.vida_actual < self.vida_maxima * 0.3 and random.random() < 0.2:
            return "habilidad_especial"
        return "atacar"
    
    def usar_habilidad_aleatoria(self, objetivo):
        """Usar una habilidad de daño aleatoria"""
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
        
        daño_base = self.ataque * habilidad["daño_multiplier"]
        daño = max(1, int(daño_base) - (objetivo.defensa // 3))
        
        objetivo.recibir_daño(daño)
        
        return {
            "nombre": habilidad["nombre"],
            "daño": daño,
            "descripcion": habilidad["descripcion"]
        }