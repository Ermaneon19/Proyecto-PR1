import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Meter
from ttkbootstrap.widgets.tableview import Tableview
from PIL import Image, ImageTk
import os
import random

estado_interfaz = {
    "root": None,
    "container": None,
    "frame_actual": None,
    "nivel_dificultad": 1,
    "entry_nombre": None,
    "clase_seleccionada": None,
    "meter_vida": None,
    "meter_ataque": None,
    "meter_defensa": None,
    "notebook": None,
    "meter_vida_jugador": None,
    "meter_mana_jugador": None,
    "combo_enemigos": None,
    "texto_log": None,
    "tabla_habilidades": None,
    "enemigo_actual": None,
    "meter_vida_combate": None,
    "meter_mana_combate": None,
    "meter_vida_enemigo": None,
    "frame_menu_habilidades": None,
    "frame_menu_objetos": None
}

def obtener_jugador():
    import main
    return main.jugador_actual

def obtener_datos():
    import main
    return main.datos_juego

def obtener_root():
    import main
    return main.root_ventana

def limpiar_pantalla():
    if estado_interfaz["frame_actual"]:
        estado_interfaz["frame_actual"].destroy()

def mostrar_mensaje(mensaje):
    ttk.dialogs.Messagebox.show_info(
        title="Información",
        message=mensaje,
        parent=estado_interfaz["root"]
    )

def mostrar_pantalla_inicio():
    limpiar_pantalla()
    estado_interfaz["frame_actual"] = ttk.Frame(estado_interfaz["container"])
    estado_interfaz["frame_actual"].pack(fill=BOTH, expand=True)
    
    titulo = ttk.Label(
        estado_interfaz["frame_actual"],
        text="⚔️ MI RPG POR TURNOS ⚔️",
        font=("Helvetica", 24, "bold"),
        bootstyle="primary"
    )
    titulo.pack(pady=40)
    
    frame_botones = ttk.Frame(estado_interfaz["frame_actual"])
    frame_botones.pack(pady=20)
    
    btn_nuevo = ttk.Button(
        frame_botones,
        text="🎮 NUEVO JUEGO",
        command=mostrar_creacion_personaje,
        bootstyle="success-outline",
        width=20
    )
    btn_nuevo.pack(pady=10)
    
    btn_cargar = ttk.Button(
        frame_botones,
        text="📁 CARGAR JUEGO",
        command=lambda: mostrar_mensaje("Función en desarrollo"),
        bootstyle="info-outline",
        width=20
    )
    btn_cargar.pack(pady=10)
    
    btn_salir = ttk.Button(
        frame_botones,
        text="🚪 SALIR",
        command=lambda: obtener_root().quit(),
        bootstyle="danger-outline",
        width=20
    )
    btn_salir.pack(pady=10)
    
    info = ttk.Label(
        estado_interfaz["frame_actual"],
        text="Desarrollado con Python y ttkbootstrap",
        font=("Helvetica", 10),
        bootstyle="secondary"
    )
    info.pack(side=BOTTOM, pady=20)

def actualizar_stats_preview(*args):
    stats = {
        "guerrero": {"vida": 120, "ataque": 18, "defensa": 15},
        "mago": {"vida": 80, "ataque": 12, "defensa": 8},
        "arquero": {"vida": 90, "ataque": 16, "defensa": 10}
    }
    
    clase = estado_interfaz["clase_seleccionada"].get()
    stat = stats.get(clase, stats["guerrero"])
    
    estado_interfaz["meter_vida"].configure(amountused=stat["vida"])
    estado_interfaz["meter_ataque"].configure(amountused=stat["ataque"])
    estado_interfaz["meter_defensa"].configure(amountused=stat["defensa"])

def mostrar_creacion_personaje():
    limpiar_pantalla()
    estado_interfaz["frame_actual"] = ttk.Frame(estado_interfaz["container"])
    estado_interfaz["frame_actual"].pack(fill=BOTH, expand=True)
    
    titulo = ttk.Label(
        estado_interfaz["frame_actual"],
        text="CREACIÓN DE PERSONAJE",
        font=("Helvetica", 20, "bold"),
        bootstyle="primary"
    )
    titulo.pack(pady=20)
    
    frame_principal = ttk.Frame(estado_interfaz["frame_actual"])
    frame_principal.pack(fill=BOTH, expand=True, padx=20)
    
    frame_form = ttk.Labelframe(frame_principal, text="Datos del Héroe", bootstyle="info")
    frame_form.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
    
    ttk.Label(frame_form, text="Nombre:", bootstyle="primary").pack(anchor=W, pady=(10, 5))
    estado_interfaz["entry_nombre"] = ttk.Entry(frame_form, width=30)
    estado_interfaz["entry_nombre"].pack(fill=X, pady=(0, 15))
    estado_interfaz["entry_nombre"].insert(0, "Aragorn")
    
    ttk.Label(frame_form, text="Clase:", bootstyle="primary").pack(anchor=W, pady=(10, 5))
    
    estado_interfaz["clase_seleccionada"] = ttk.StringVar(value="guerrero")
    frame_clases = ttk.Frame(frame_form)
    frame_clases.pack(fill=X, pady=(0, 15))
    
    clases = [
        ("⚔️ Guerrero", "guerrero"),
        ("🔮 Mago", "mago"),
        ("🏹 Arquero", "arquero")
    ]
    
    for texto, valor in clases:
        ttk.Radiobutton(
            frame_clases,
            text=texto,
            value=valor,
            variable=estado_interfaz["clase_seleccionada"],
            bootstyle="info-toolbutton"
        ).pack(side=LEFT, padx=(0, 10))
    
    frame_stats = ttk.Labelframe(frame_principal, text="Estadísticas", bootstyle="success")
    frame_stats.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))
    
    estado_interfaz["meter_vida"] = Meter(
        frame_stats,
        metersize=150,
        padding=10,
        amountused=0,
        metertype="semi",
        subtext="VIDA",
        interactive=False,
        bootstyle="danger"
    )
    estado_interfaz["meter_vida"].pack(pady=10)
    
    estado_interfaz["meter_ataque"] = Meter(
        frame_stats,
        metersize=150,
        padding=10,
        amountused=0,
        metertype="semi",
        subtext="ATAQUE",
        interactive=False,
        bootstyle="warning"
    )
    estado_interfaz["meter_ataque"].pack(pady=10)
    
    estado_interfaz["meter_defensa"] = Meter(
        frame_stats,
        metersize=150,
        padding=10,
        amountused=0,
        metertype="semi",
        subtext="DEFENSA",
        interactive=False,
        bootstyle="info"
    )
    estado_interfaz["meter_defensa"].pack(pady=10)
    
    try:
        estado_interfaz["clase_seleccionada"].trace_add('write', actualizar_stats_preview)
    except AttributeError:
        estado_interfaz["clase_seleccionada"].trace('w', actualizar_stats_preview)
    actualizar_stats_preview()
    
    frame_botones = ttk.Frame(estado_interfaz["frame_actual"])
    frame_botones.pack(fill=X, pady=20)
    
    btn_crear = ttk.Button(
        frame_botones,
        text="🎯 CREAR PERSONAJE",
        command=crear_personaje,
        bootstyle="success",
        width=20
    )
    btn_crear.pack(side=RIGHT, padx=(10, 0))
    
    btn_volver = ttk.Button(
        frame_botones,
        text="↩️ VOLVER",
        command=mostrar_pantalla_inicio,
        bootstyle="secondary",
        width=15
    )
    btn_volver.pack(side=RIGHT)

def crear_personaje():
    nombre = estado_interfaz["entry_nombre"].get().strip()
    clase = estado_interfaz["clase_seleccionada"].get()
    
    if not nombre:
        mostrar_mensaje("¡Debes ingresar un nombre para tu héroe!")
        return
    
    from modules.personaje import crear_personaje as crear_personaje_func
    import main
    main.jugador_actual = crear_personaje_func(nombre, clase)
    
    mostrar_pantalla_principal()

def mostrar_pantalla_principal():
    limpiar_pantalla()
    estado_interfaz["frame_actual"] = ttk.Frame(estado_interfaz["container"])
    estado_interfaz["frame_actual"].pack(fill=BOTH, expand=True)
    
    jugador = obtener_jugador()
    
    titulo = ttk.Label(
        estado_interfaz["frame_actual"],
        text=f"AVENTURAS DE {jugador['nombre'].upper()}",
        font=("Helvetica", 16, "bold"),
        bootstyle="primary"
    )
    titulo.pack(pady=10)
    
    estado_interfaz["notebook"] = ttk.Notebook(estado_interfaz["frame_actual"], bootstyle="primary")
    estado_interfaz["notebook"].pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    frame_estado = ttk.Frame(estado_interfaz["notebook"])
    crear_pestana_estado(frame_estado)
    estado_interfaz["notebook"].add(frame_estado, text="🎭 ESTADO")
    
    frame_combate = ttk.Frame(estado_interfaz["notebook"])
    crear_pestana_combate(frame_combate)
    estado_interfaz["notebook"].add(frame_combate, text="⚔️ COMBATE")
    
    frame_habilidades = ttk.Frame(estado_interfaz["notebook"])
    crear_pestana_habilidades(frame_habilidades)
    estado_interfaz["notebook"].add(frame_habilidades, text="🔮 HABILIDADES")
    
    frame_inventario = ttk.Frame(estado_interfaz["notebook"])
    crear_pestana_inventario(frame_inventario)
    estado_interfaz["notebook"].add(frame_inventario, text="🎒 INVENTARIO")

def crear_pestana_estado(parent):
    jugador = obtener_jugador()
    
    frame_principal = ttk.Frame(parent)
    frame_principal.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    frame_izquierda = ttk.Frame(frame_principal)
    frame_izquierda.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
    
    frame_stats = ttk.Labelframe(frame_izquierda, text="Estadísticas Principales", bootstyle="info")
    frame_stats.pack(fill=BOTH, expand=True, pady=(0, 10))
    
    estado_interfaz["meter_vida_jugador"] = Meter(
        frame_stats,
        metersize=180,
        padding=15,
        amountused=100,
        metertype="semi",
        subtext="VIDA",
        interactive=False,
        bootstyle="danger",
        textright=f"/{jugador['vida_maxima']}",
        stripethickness=10
    )
    estado_interfaz["meter_vida_jugador"].pack(pady=10)
    
    estado_interfaz["meter_mana_jugador"] = Meter(
        frame_stats,
        metersize=180,
        padding=15,
        amountused=100,
        metertype="semi",
        subtext="MANA",
        interactive=False,
        bootstyle="primary",
        textright=f"/{jugador['mana_maximo']}",
        stripethickness=10
    )
    estado_interfaz["meter_mana_jugador"].pack(pady=10)
    
    frame_exp = ttk.Frame(frame_stats)
    frame_exp.pack(fill=X, pady=10)
    ttk.Label(frame_exp, text="EXPERIENCIA:", bootstyle="primary").pack(side=LEFT)
    ttk.Label(frame_exp, text=f"{jugador['experiencia']}/{jugador['experiencia_necesaria']}",
             bootstyle="success").pack(side=RIGHT)
    
    frame_secundarios = ttk.Labelframe(frame_izquierda, text="Atributos", bootstyle="success")
    frame_secundarios.pack(fill=BOTH, expand=True)
    
    stats_data = [
        ("Nivel", jugador["nivel"], "warning"),
        ("Ataque", jugador["ataque"], "danger"),
        ("Defensa", jugador["defensa"], "info"),
        ("Velocidad", jugador["velocidad"], "success"),
        ("Clase", jugador["clase"].title(), "primary")
    ]
    
    for stat, valor, style in stats_data:
        frame_stat = ttk.Frame(frame_secundarios)
        frame_stat.pack(fill=X, pady=8, padx=10)
        ttk.Label(frame_stat, text=stat, bootstyle="primary", width=12).pack(side=LEFT)
        ttk.Label(frame_stat, text=str(valor), bootstyle=style, font=("Helvetica", 10, "bold")).pack(side=RIGHT)
    
    ttk.Button(
        frame_secundarios,
        text="🔄 ACTUALIZAR",
        command=actualizar_estado_personaje,
        bootstyle="outline-primary"
    ).pack(side=BOTTOM, pady=10)
    
    frame_menu = ttk.Labelframe(frame_principal, text="Menú de Acciones", bootstyle="warning")
    frame_menu.pack(side=RIGHT, fill=BOTH, expand=True, padx=(5, 0))
    
    btn_batalla = ttk.Button(
        frame_menu,
        text="⚔️ IR A LA BATALLA",
        command=ir_a_batalla,
        bootstyle="danger",
        width=25
    )
    btn_batalla.pack(pady=15, padx=10)
    
    btn_inventario = ttk.Button(
        frame_menu,
        text="🎒 INVENTARIO",
        command=ir_a_inventario,
        bootstyle="info",
        width=25
    )
    btn_inventario.pack(pady=15, padx=10)
    
    btn_salir = ttk.Button(
        frame_menu,
        text="🚪 SALIR DEL JUEGO",
        command=salir_del_juego,
        bootstyle="secondary",
        width=25
    )
    btn_salir.pack(pady=15, padx=10)

def crear_pestana_combate(parent):
    frame_principal = ttk.Frame(parent)
    frame_principal.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    frame_enemigos = ttk.Labelframe(frame_principal, text="Seleccionar Enemigo", bootstyle="warning")
    frame_enemigos.pack(fill=X, pady=(0, 10))
    
    frame_seleccion = ttk.Frame(frame_enemigos)
    frame_seleccion.pack(fill=X, padx=10, pady=10)
    
    ttk.Label(frame_seleccion, text="Enemigo:", bootstyle="primary").pack(side=LEFT)
    
    estado_interfaz["combo_enemigos"] = ttk.Combobox(
        frame_seleccion,
        values=["Lobo", "Orco", "Araña Gigante", "Esqueleto", "Goblin"],
        state="readonly",
        width=15
    )
    estado_interfaz["combo_enemigos"].current(0)
    estado_interfaz["combo_enemigos"].pack(side=LEFT, padx=(10, 20))
    
    btn_iniciar_combate = ttk.Button(
        frame_seleccion,
        text="⚔️ INICIAR COMBATE",
        command=iniciar_combate,
        bootstyle="danger"
    )
    btn_iniciar_combate.pack(side=LEFT)
    
    frame_log = ttk.Labelframe(frame_principal, text="Log del Combate", bootstyle="secondary")
    frame_log.pack(fill=BOTH, expand=True, pady=(0, 10))
    
    estado_interfaz["texto_log"] = ttk.ScrolledText(
        frame_log,
        height=15,
        wrap=WORD,
        font=("Consolas", 10)
    )
    estado_interfaz["texto_log"].pack(fill=BOTH, expand=True, padx=10, pady=10)
    estado_interfaz["texto_log"].configure(state="disabled")
    
    frame_acciones = ttk.Labelframe(frame_principal, text="Acciones", bootstyle="info")
    frame_acciones.pack(fill=X)
    
    frame_botones = ttk.Frame(frame_acciones)
    frame_botones.pack(fill=X, padx=10, pady=10)
    
    acciones = [
        ("🗡️ ATAQUE BÁSICO", "primary"),
        ("🛡️ DEFENDER", "info"),
        ("🔥 HABILIDAD", "warning"),
        ("🏃 HUIR", "secondary")
    ]
    
    for texto, estilo in acciones:
        btn = ttk.Button(
            frame_botones,
            text=texto,
            bootstyle=estilo,
            width=15,
            command=lambda acc=texto: ejecutar_accion_combate(acc)
        )
        btn.pack(side=LEFT, padx=5)

def crear_pestana_habilidades(parent):
    jugador = obtener_jugador()
    
    frame_principal = ttk.Frame(parent)
    frame_principal.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    columnas = [
        {"text": "Habilidad", "stretch": True},
        {"text": "Daño", "stretch": False},
        {"text": "Costo Mana", "stretch": False},
        {"text": "Descripción", "stretch": True}
    ]
    
    datos = [
        ("Golpe Poderoso", "25", "10", "Golpe cargado con fuerza adicional"),
        ("Defender", "0", "5", "Aumenta la defensa por un turno"),
        ("Bola de Fuego", "35", "20", "Proyectil de fuego que quema al enemigo")
    ]
    
    estado_interfaz["tabla_habilidades"] = Tableview(
        frame_principal,
        coldata=columnas,
        rowdata=datos,
        paginated=True,
        searchable=True,
        bootstyle="primary",
        height=200
    )
    estado_interfaz["tabla_habilidades"].pack(fill=BOTH, expand=True)
    
    frame_info = ttk.Frame(frame_principal)
    frame_info.pack(fill=X, pady=(10, 0))
    
    ttk.Label(
        frame_info,
        text=f"Habilidades desbloqueadas: {len(jugador['habilidades'])}",
        bootstyle="success"
    ).pack(side=LEFT)

def crear_pestana_inventario(parent):
    frame_principal = ttk.Frame(parent)
    frame_principal.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    ttk.Label(
        frame_principal,
        text="🏆 SISTEMA DE INVENTARIO 🏆",
        font=("Helvetica", 16, "bold"),
        bootstyle="warning"
    ).pack(expand=True)
    
    ttk.Label(
        frame_principal,
        text="Esta función estará disponible en la próxima actualización",
        font=("Helvetica", 12),
        bootstyle="secondary"
    ).pack(expand=True)

def actualizar_estado_personaje():
    jugador = obtener_jugador()
    if jugador:
        porcentaje_vida = (jugador["vida_actual"] / jugador["vida_maxima"]) * 100
        porcentaje_mana = (jugador["mana_actual"] / jugador["mana_maximo"]) * 100
        
        estado_interfaz["meter_vida_jugador"].configure(
            amountused=porcentaje_vida,
            textright=f"{jugador['vida_actual']}/{jugador['vida_maxima']}"
        )
        estado_interfaz["meter_mana_jugador"].configure(
            amountused=porcentaje_mana,
            textright=f"{jugador['mana_actual']}/{jugador['mana_maximo']}"
        )

def ir_a_batalla():
    datos = obtener_datos()
    enemigos_data = datos.get('enemigos', [])
    if not enemigos_data:
        mostrar_mensaje("No hay enemigos disponibles")
        return
    
    multiplicador = 1.0 + (estado_interfaz["nivel_dificultad"] - 1) * 0.15
    
    enemigo_random = random.choice(enemigos_data)
    from modules.enemigo import crear_enemigo
    enemigo = crear_enemigo(
        enemigo_random['nombre'],
        enemigo_random.get('zona', 'bosque'),
        enemigo_random,
        multiplicador_dificultad=multiplicador
    )
    
    mostrar_pantalla_combate(enemigo)

def mostrar_pantalla_combate(enemigo):
    limpiar_pantalla()
    estado_interfaz["frame_actual"] = ttk.Frame(estado_interfaz["container"])
    estado_interfaz["frame_actual"].pack(fill=BOTH, expand=True)
    
    estado_interfaz["enemigo_actual"] = enemigo
    jugador = obtener_jugador()
    
    frame_titulo = ttk.Frame(estado_interfaz["frame_actual"])
    frame_titulo.pack(pady=10)
    
    titulo = ttk.Label(
        frame_titulo,
        text="⚔️ COMBATE ⚔️",
        font=("Helvetica", 20, "bold"),
        bootstyle="danger"
    )
    titulo.pack()
    
    dificultad_label = ttk.Label(
        frame_titulo,
        text=f"Nivel de Dificultad: {estado_interfaz['nivel_dificultad']}",
        font=("Helvetica", 12, "bold"),
        bootstyle="warning"
    )
    dificultad_label.pack(pady=(5, 0))
    
    frame_combatientes = ttk.Frame(estado_interfaz["frame_actual"])
    frame_combatientes.pack(fill=BOTH, expand=True, padx=20, pady=10)
    
    frame_personaje = ttk.Labelframe(frame_combatientes, text=jugador["nombre"], bootstyle="info")
    frame_personaje.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
    
    ttk.Label(
        frame_personaje,
        text=f"Clase: {jugador['clase'].title()}",
        font=("Helvetica", 12),
        bootstyle="primary"
    ).pack(pady=5)
    
    porcentaje_vida = (jugador["vida_actual"] / jugador["vida_maxima"]) * 100
    estado_interfaz["meter_vida_combate"] = Meter(
        frame_personaje,
        metersize=200,
        padding=15,
        amountused=porcentaje_vida,
        metertype="semi",
        subtext="VIDA",
        interactive=False,
        bootstyle="danger",
        textright=f"{jugador['vida_actual']}/{jugador['vida_maxima']}",
        stripethickness=10
    )
    estado_interfaz["meter_vida_combate"].pack(pady=10)
    
    porcentaje_mana = (jugador["mana_actual"] / jugador["mana_maximo"]) * 100
    estado_interfaz["meter_mana_combate"] = Meter(
        frame_personaje,
        metersize=200,
        padding=15,
        amountused=porcentaje_mana,
        metertype="semi",
        subtext="MANA",
        interactive=False,
        bootstyle="primary",
        textright=f"{jugador['mana_actual']}/{jugador['mana_maximo']}",
        stripethickness=10
    )
    estado_interfaz["meter_mana_combate"].pack(pady=10)
    
    frame_enemigo = ttk.Labelframe(frame_combatientes, text=enemigo["nombre"], bootstyle="warning")
    frame_enemigo.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))
    
    ttk.Label(
        frame_enemigo,
        text=f"Zona: {enemigo['zona'].title()}",
        font=("Helvetica", 12),
        bootstyle="warning"
    ).pack(pady=5)
    
    porcentaje_vida_enemigo = (enemigo["vida_actual"] / enemigo["vida_maxima"]) * 100
    estado_interfaz["meter_vida_enemigo"] = Meter(
        frame_enemigo,
        metersize=200,
        padding=15,
        amountused=porcentaje_vida_enemigo,
        metertype="semi",
        subtext="VIDA",
        interactive=False,
        bootstyle="danger",
        textright=f"{enemigo['vida_actual']}/{enemigo['vida_maxima']}",
        stripethickness=10
    )
    estado_interfaz["meter_vida_enemigo"].pack(pady=10)
    
    frame_stats_enemigo = ttk.Frame(frame_enemigo)
    frame_stats_enemigo.pack(pady=10)
    ttk.Label(frame_stats_enemigo, text=f"Ataque: {enemigo['ataque']}", bootstyle="danger").pack()
    ttk.Label(frame_stats_enemigo, text=f"Defensa: {enemigo['defensa']}", bootstyle="info").pack()
    
    frame_acciones = ttk.Labelframe(estado_interfaz["frame_actual"], text="Acciones", bootstyle="success")
    frame_acciones.pack(fill=X, padx=20, pady=10)
    
    frame_botones = ttk.Frame(frame_acciones)
    frame_botones.pack(pady=10)
    
    btn_atacar = ttk.Button(
        frame_botones,
        text="⚔️ ATACAR",
        command=mostrar_menu_habilidades,
        bootstyle="danger",
        width=20
    )
    btn_atacar.pack(side=LEFT, padx=5)
    
    btn_defender = ttk.Button(
        frame_botones,
        text="🛡️ DEFENDER",
        command=defender,
        bootstyle="info",
        width=20
    )
    btn_defender.pack(side=LEFT, padx=5)
    
    btn_objeto = ttk.Button(
        frame_botones,
        text="🧪 USAR OBJETO",
        command=mostrar_menu_objetos,
        bootstyle="primary",
        width=20
    )
    btn_objeto.pack(side=LEFT, padx=5)
    
    btn_volver = ttk.Button(
        frame_botones,
        text="↩️ VOLVER",
        command=mostrar_pantalla_principal,
        bootstyle="secondary",
        width=20
    )
    btn_volver.pack(side=LEFT, padx=5)
    
    estado_interfaz["frame_menu_habilidades"] = ttk.Labelframe(estado_interfaz["frame_actual"], text="Selecciona una Habilidad", bootstyle="primary")

def mostrar_menu_habilidades():
    datos = obtener_datos()
    habilidades_data = datos.get('habilidades', [])
    jugador = obtener_jugador()
    clase_jugador = jugador["clase"]
    
    habilidades_disponibles = [
        hab for hab in habilidades_data
        if hab.get('clase', '').lower() == clase_jugador.lower()
    ]
    
    if not habilidades_disponibles:
        mostrar_mensaje("No tienes habilidades disponibles")
        return
    
    if estado_interfaz["frame_menu_habilidades"]:
        estado_interfaz["frame_menu_habilidades"].destroy()
    
    estado_interfaz["frame_menu_habilidades"] = ttk.Labelframe(estado_interfaz["frame_actual"], text="Selecciona una Habilidad", bootstyle="primary")
    estado_interfaz["frame_menu_habilidades"].pack(fill=X, padx=20, pady=10)
    
    frame_habs = ttk.Frame(estado_interfaz["frame_menu_habilidades"])
    frame_habs.pack(pady=10)
    
    for i, habilidad in enumerate(habilidades_disponibles):
        nombre = habilidad.get('nombre', '')
        daño = habilidad.get('daño_base', '0')
        costo = habilidad.get('coste_mana', '0')
        descripcion = habilidad.get('descripcion', '')
        
        jugador = obtener_jugador()
        tiene_mana = jugador["mana_actual"] >= int(costo)
        
        frame_hab = ttk.Frame(frame_habs)
        frame_hab.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="ew")
        
        btn_hab = ttk.Button(
            frame_hab,
            text=f"{nombre}\nDaño: {daño} | Mana: {costo}",
            command=lambda h=habilidad: usar_habilidad(h),
            bootstyle="primary" if tiene_mana else "secondary",
            width=20,
            state="normal" if tiene_mana else "disabled"
        )
        btn_hab.pack()
        
        ttk.Label(
            frame_hab,
            text=descripcion,
            font=("Helvetica", 8),
            bootstyle="secondary",
            wraplength=150
        ).pack(pady=(2, 0))
    
    frame_habs.columnconfigure(0, weight=1)
    frame_habs.columnconfigure(1, weight=1)

def usar_habilidad(habilidad):
    nombre = habilidad.get('nombre', '')
    daño = int(habilidad.get('daño_base', 0))
    costo = int(habilidad.get('coste_mana', 0))
    
    jugador = obtener_jugador()
    enemigo = estado_interfaz["enemigo_actual"]
    
    if jugador["mana_actual"] < costo:
        mostrar_mensaje("¡No tienes suficiente mana!")
        return
    
    jugador["mana_actual"] -= costo
    
    if daño > 0:
        from modules.enemigo import recibir_daño_enemigo
        daño_real = max(1, daño + (jugador["ataque"] // 2) - (enemigo["defensa"] // 3))
        recibir_daño_enemigo(enemigo, daño_real)
        mostrar_mensaje(f"¡{nombre} causa {daño_real} de daño a {enemigo['nombre']}!")
    else:
        from modules.personaje import curar_personaje
        if "Curar" in nombre:
            curacion = 30
            curar_personaje(jugador, curacion)
            mostrar_mensaje(f"¡Te curas {curacion} de vida!")
        elif "Defender" in nombre:
            jugador["defensa"] += 5
            mostrar_mensaje(f"¡Tu defensa aumenta!")
        elif "Esquivar" in nombre:
            jugador["velocidad"] += 3
            mostrar_mensaje(f"¡Tu velocidad aumenta!")
    
    actualizar_combate_ui()
    
    if estado_interfaz["frame_menu_habilidades"]:
        estado_interfaz["frame_menu_habilidades"].destroy()
    
    from modules.enemigo import esta_vivo_enemigo
    if not esta_vivo_enemigo(enemigo):
        from modules.personaje import ganar_experiencia
        exp_ganada = enemigo["experiencia_otorgada"]
        ganar_experiencia(jugador, exp_ganada)
        
        jugador["vida_actual"] = jugador["vida_maxima"]
        
        estado_interfaz["nivel_dificultad"] += 1
        
        mostrar_mensaje(
            f"¡Victoria! Ganas {exp_ganada} de experiencia.\n"
            f"Tu vida se restaura completamente.\n"
            f"La dificultad aumenta (Nivel {estado_interfaz['nivel_dificultad']})"
        )
        mostrar_pantalla_principal()
        return
    
    turno_enemigo()

def defender():
    jugador = obtener_jugador()
    jugador["defensa"] += 3
    mostrar_mensaje("¡Te defiendes! Tu defensa aumenta temporalmente")
    
    actualizar_combate_ui()
    
    turno_enemigo()

def turno_enemigo():
    enemigo = estado_interfaz["enemigo_actual"]
    jugador = obtener_jugador()
    
    from modules.enemigo import esta_vivo_enemigo, usar_habilidad_aleatoria_enemigo
    from modules.personaje import esta_vivo_personaje
    
    if not enemigo or not esta_vivo_enemigo(enemigo):
        return
    
    if not esta_vivo_personaje(jugador):
        mostrar_mensaje("¡Has sido derrotado! Tu personaje ha sido curado automáticamente.")
        jugador["vida_actual"] = jugador["vida_maxima"]
        actualizar_combate_ui()
        return
    
    resultado = usar_habilidad_aleatoria_enemigo(enemigo, jugador)
    
    mensaje = f"¡{enemigo['nombre']} usa {resultado['nombre']} y causa {resultado['daño']} de daño!"
    mostrar_mensaje(mensaje)
    
    actualizar_combate_ui()
    
    if not esta_vivo_personaje(jugador):
        mostrar_mensaje("¡Has sido derrotado! Tu personaje ha sido curado automáticamente.")
        jugador["vida_actual"] = jugador["vida_maxima"]
        actualizar_combate_ui()

def mostrar_menu_objetos():
    jugador = obtener_jugador()
    inventario = jugador["inventario"]
    
    objetos_consumibles = {
        nombre: datos
        for nombre, datos in inventario.items()
        if datos.get('tipo') == 'consumible' and datos.get('cantidad', 0) > 0
    }
    
    if not objetos_consumibles:
        mostrar_mensaje("No tienes objetos consumibles en tu inventario")
        return
    
    if estado_interfaz["frame_menu_objetos"]:
        estado_interfaz["frame_menu_objetos"].destroy()
    
    estado_interfaz["frame_menu_objetos"] = ttk.Labelframe(estado_interfaz["frame_actual"], text="Selecciona un Objeto", bootstyle="primary")
    estado_interfaz["frame_menu_objetos"].pack(fill=X, padx=20, pady=10)
    
    frame_objs = ttk.Frame(estado_interfaz["frame_menu_objetos"])
    frame_objs.pack(pady=10)
    
    for i, (nombre, datos) in enumerate(objetos_consumibles.items()):
        cantidad = datos.get('cantidad', 0)
        mana = datos.get('mana', 0)
        
        frame_obj = ttk.Frame(frame_objs)
        frame_obj.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="ew")
        
        btn_obj = ttk.Button(
            frame_obj,
            text=f"{nombre}\nMana: +{mana} | Cantidad: {cantidad}",
            command=lambda n=nombre: usar_objeto(n),
            bootstyle="primary",
            width=20
        )
        btn_obj.pack()
    
    frame_objs.columnconfigure(0, weight=1)
    frame_objs.columnconfigure(1, weight=1)

def usar_objeto(nombre_objeto):
    jugador = obtener_jugador()
    inventario = jugador["inventario"]
    
    if nombre_objeto not in inventario:
        mostrar_mensaje("¡Objeto no encontrado!")
        return
    
    objeto = inventario[nombre_objeto]
    
    if objeto.get('cantidad', 0) <= 0:
        mostrar_mensaje("¡No tienes más de este objeto!")
        return
    
    objeto['cantidad'] -= 1
    
    if objeto.get('tipo') == 'consumible':
        mana_recuperado = objeto.get('mana', 0)
        if mana_recuperado > 0:
            mana_antes = jugador["mana_actual"]
            jugador["mana_actual"] = min(
                jugador["mana_maximo"],
                jugador["mana_actual"] + mana_recuperado
            )
            mana_real = jugador["mana_actual"] - mana_antes
            mostrar_mensaje(f"¡Usas {nombre_objeto} y recuperas {mana_real} de mana!")
    
    if objeto['cantidad'] <= 0:
        del inventario[nombre_objeto]
    
    actualizar_combate_ui()
    
    if estado_interfaz["frame_menu_objetos"]:
        estado_interfaz["frame_menu_objetos"].destroy()

def actualizar_combate_ui():
    if not estado_interfaz["enemigo_actual"]:
        return
    
    jugador = obtener_jugador()
    enemigo = estado_interfaz["enemigo_actual"]
    
    porcentaje_vida = (jugador["vida_actual"] / jugador["vida_maxima"]) * 100
    estado_interfaz["meter_vida_combate"].configure(
        amountused=porcentaje_vida,
        textright=f"{jugador['vida_actual']}/{jugador['vida_maxima']}"
    )
    
    porcentaje_mana = (jugador["mana_actual"] / jugador["mana_maximo"]) * 100
    estado_interfaz["meter_mana_combate"].configure(
        amountused=porcentaje_mana,
        textright=f"{jugador['mana_actual']}/{jugador['mana_maximo']}"
    )
    
    porcentaje_vida_enemigo = (enemigo["vida_actual"] / enemigo["vida_maxima"]) * 100
    estado_interfaz["meter_vida_enemigo"].configure(
        amountused=porcentaje_vida_enemigo,
        textright=f"{enemigo['vida_actual']}/{enemigo['vida_maxima']}"
    )

def ir_a_inventario():
    if estado_interfaz["notebook"]:
        estado_interfaz["notebook"].select(3)

def salir_del_juego():
    import main
    main.salir_juego()

def iniciar_combate():
    nombre_enemigo = estado_interfaz["combo_enemigos"].get()
    if not nombre_enemigo:
        mostrar_mensaje("¡Selecciona un enemigo!")
        return
    
    from modules.enemigo import crear_enemigo
    enemigo = crear_enemigo(nombre_enemigo)
    
    jugador = obtener_jugador()
    
    from modules.combate import iniciar_combate as iniciar_combate_func, obtener_log
    resultado = iniciar_combate_func(jugador, enemigo)
    
    estado_interfaz["texto_log"].configure(state="normal")
    estado_interfaz["texto_log"].delete(1.0, "end")
    
    log = obtener_log()
    for mensaje in log:
        estado_interfaz["texto_log"].insert("end", mensaje + "\n")
    
    estado_interfaz["texto_log"].configure(state="disabled")
    estado_interfaz["texto_log"].see("end")
    
    actualizar_estado_personaje()
    
    if resultado:
        mostrar_mensaje("¡Victoria! Revisa tu experiencia ganada.")
    else:
        mostrar_mensaje("¡Derrota! Tu personaje ha sido curado automáticamente.")
        jugador["vida_actual"] = jugador["vida_maxima"]
        actualizar_estado_personaje()

def ejecutar_accion_combate(accion):
    mostrar_mensaje(f"Acción: {accion} - En desarrollo")

def inicializar_interfaz(root):
    estado_interfaz["root"] = root
    estado_interfaz["container"] = ttk.Frame(root)
    estado_interfaz["container"].pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    mostrar_pantalla_inicio()
