import random

class SistemaCombate:
    def __init__(self):
        self.log = []
    
    def iniciar_combate(self, jugador, enemigo):
        """Iniciar un combate entre jugador y enemigo"""
        self.log.clear()
        self.agregar_log(f"¡Combate contra {enemigo.nombre}!")
        
        turno = 1
        while jugador.esta_vivo() and enemigo.esta_vivo():
            self.agregar_log(f"\n--- Turno {turno} ---")
            
            if jugador.velocidad >= enemigo.velocidad:
                self.turno_jugador(jugador, enemigo)
                if enemigo.esta_vivo():
                    self.turno_enemigo(enemigo, jugador)
            else:
                self.turno_enemigo(enemigo, jugador)
                if jugador.esta_vivo():
                    self.turno_jugador(jugador, enemigo)
            
            turno += 1
        
        return self.finalizar_combate(jugador, enemigo)
    
    def turno_jugador(self, jugador, enemigo):
        """Turno del jugador (esto se expandirá con la interfaz)"""
        # Por ahora, ataque básico automático
        daño = jugador.atacar(enemigo)
        self.agregar_log(f"{jugador.nombre} ataca a {enemigo.nombre} por {daño} de daño")
        
        if not enemigo.esta_vivo():
            self.agregar_log(f"¡{enemigo.nombre} ha sido derrotado!")
    
    def turno_enemigo(self, enemigo, jugador):
        """Turno del enemigo"""
        accion = enemigo.elegir_accion(jugador)
        
        if accion == "atacar":
            daño = enemigo.atacar(jugador)
            self.agregar_log(f"{enemigo.nombre} ataca a {jugador.nombre} por {daño} de daño")
        elif accion == "habilidad_especial":
            daño = enemigo.ataque * 1.5
            jugador.recibir_daño(int(daño))
            self.agregar_log(f"{enemigo.nombre} usa habilidad especial por {int(daño)} de daño")
        
        if not jugador.esta_vivo():
            self.agregar_log(f"¡{jugador.nombre} ha sido derrotado!")
    
    def finalizar_combate(self, jugador, enemigo):
        """Finalizar el combate y determinar resultados"""
        if jugador.esta_vivo():
            exp_ganada = enemigo.experiencia_otorgada
            jugador.ganar_experiencia(exp_ganada)
            self.agregar_log(f"\n¡Victoria! Ganas {exp_ganada} de experiencia")
            return True
        else:
            self.agregar_log(f"\n¡Derrota! {jugador.nombre} ha caído en combate")
            return False
    
    def agregar_log(self, mensaje):
        """Agregar mensaje al log del combate"""
        self.log.append(mensaje)
        print(mensaje)