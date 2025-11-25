import random


log_combate = []


def limpiar_log():
    global log_combate
    log_combate = []


def agregar_log(mensaje):
    global log_combate
    
    log_combate.append(mensaje)
    
    print(mensaje)


def iniciar_combate(jugador, enemigo):
    
    limpiar_log()
   
    agregar_log(f"¡Combate contra {enemigo['nombre']}!")
    
    
    turno = 1
    
    while jugador["vida_actual"] > 0 and enemigo["vida_actual"] > 0:
        
        agregar_log(f"\n--- Turno {turno} ---")
        
       
        if jugador["velocidad"] >= enemigo["velocidad"]:
            
            turno_jugador(jugador, enemigo)
            
            if enemigo["vida_actual"] > 0:
                turno_enemigo(enemigo, jugador)
        else:
            
            turno_enemigo(enemigo, jugador)
            
            if jugador["vida_actual"] > 0:
                turno_jugador(jugador, enemigo)
        
        
        turno += 1
    
    
    return finalizar_combate(jugador, enemigo)


def turno_jugador(jugador, enemigo):
    from modules.personaje import atacar_personaje
    
    daño = atacar_personaje(jugador, enemigo)
    
    agregar_log(f"{jugador['nombre']} ataca a {enemigo['nombre']} por {daño} de daño")
    
    
    if enemigo["vida_actual"] <= 0:
        agregar_log(f"¡{enemigo['nombre']} ha sido derrotado!")


def turno_enemigo(enemigo, jugador):
    from modules.enemigo import elegir_accion_enemigo, atacar_enemigo
    
    accion = elegir_accion_enemigo(enemigo, jugador)
    
    
    if accion == "atacar":
        
        daño = atacar_enemigo(enemigo, jugador)
        agregar_log(f"{enemigo['nombre']} ataca a {jugador['nombre']} por {daño} de daño")
    elif accion == "habilidad_especial":
        
        from modules.personaje import recibir_daño_personaje
        daño = int(enemigo["ataque"] * 1.5)
        recibir_daño_personaje(jugador, daño)
        agregar_log(f"{enemigo['nombre']} usa habilidad especial por {daño} de daño")
    
    # Verificar si el jugador murió
    if jugador["vida_actual"] <= 0:
        agregar_log(f"¡{jugador['nombre']} ha sido derrotado!")


def finalizar_combate(jugador, enemigo):
    from modules.personaje import ganar_experiencia
   
    if jugador["vida_actual"] > 0:
        
        exp_ganada = enemigo["experiencia_otorgada"]
        
        ganar_experiencia(jugador, exp_ganada)

        agregar_log(f"\n¡Victoria! Ganas {exp_ganada} de experiencia")
        return True
    else:
        
        agregar_log(f"\n¡Derrota! {jugador['nombre']} ha caído en combate")
        return False


def obtener_log():
    global log_combate
    return log_combate
