import csv

class Personaje:
    def __init__(self, nombre, clase="guerrero"):
        self.nombre = nombre
        self.clase = clase
        self.nivel = 1
        self.experiencia = 0
        self.experiencia_necesaria = 100
        
        self.stats_base = self.obtener_stats_base(clase)
        
        self.vida_actual = self.stats_base['vida_maxima']
        self.vida_maxima = self.stats_base['vida_maxima']
        self.mana_actual = self.stats_base['mana_maximo']
        self.mana_maximo = self.stats_base['mana_maximo']
        self.ataque = self.stats_base['ataque']
        self.defensa = self.stats_base['defensa']
        self.velocidad = self.stats_base['velocidad']
        
        self.equipo = {}
        self.habilidades = self.obtener_habilidades_iniciales(clase)
        
        self.inventario = {
            "Poción de Mana Pequeña": {"cantidad": 3, "tipo": "consumible", "mana": 20},
            "Poción de Mana Grande": {"cantidad": 1, "tipo": "consumible", "mana": 50}
        }
    
    def obtener_stats_base(self, clase):
        """Obtener stats iniciales según la clase"""
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
    
    def obtener_habilidades_iniciales(self, clase):
        """Obtener habilidades iniciales según clase"""
        habilidades = {
            "guerrero": ["Golpe Poderoso", "Defender"],
            "mago": ["Bola de Fuego", "Curar"],
            "arquero": ["Disparo Preciso", "Esquivar"]
        }
        return habilidades.get(clase, ["Ataque Básico"])
    
    def atacar(self, objetivo):
        """Ataque básico del personaje"""
        daño = max(1, self.ataque - (objetivo.defensa // 2))
        objetivo.recibir_daño(daño)
        return daño
    
    def recibir_daño(self, daño):
        """Recibir daño"""
        self.vida_actual = max(0, self.vida_actual - daño)
        return self.vida_actual > 0
    
    def curar(self, cantidad):
        """Curar al personaje"""
        self.vida_actual = min(self.vida_maxima, self.vida_actual + cantidad)
    
    def esta_vivo(self):
        """Verificar si el personaje está vivo"""
        return self.vida_actual > 0
    
    def ganar_experiencia(self, exp):
        """Ganar experiencia y subir de nivel si es necesario"""
        self.experiencia += exp
        if self.experiencia >= self.experiencia_necesaria:
            self.subir_nivel()
    
    def subir_nivel(self):
        """Subir de nivel"""
        self.nivel += 1
        self.experiencia = 0
        self.experiencia_necesaria = int(self.experiencia_necesaria * 1.5)
        
        self.vida_maxima += 10
        self.ataque += 2
        self.defensa += 1
        self.velocidad += 1
        
        self.vida_actual = self.vida_maxima
        self.mana_actual = self.mana_maximo
        
        return f"¡{self.nombre} ha subido al nivel {self.nivel}!"