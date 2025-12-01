# Importar librerías necesarias
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Meter
from ttkbootstrap.widgets.tableview import Tableview
from tkinter import Canvas
from tkinter.scrolledtext import ScrolledText
import random
import math

# Diccionario global para almacenar widgets y datos
estado = {
    "root": None, "container": None, "frame_actual": None, "nivel_dificultad": 1,
    "entry_nombre": None, "clase_seleccionada": None, "notebook": None,
    "meter_vida": None, "meter_ataque": None, "meter_defensa": None,
    "meter_vida_jugador": None, "meter_mana_jugador": None,
    "meter_vida_combate": None, "meter_mana_combate": None, "meter_vida_enemigo": None,
    "combo_enemigos": None, "texto_log": None, "tabla_habilidades": None,
    "enemigo_actual": None, "frame_menu_habilidades": None, "frame_menu_objetos": None,
    "label_sprite_jugador": None, "label_sprite_enemigo": None, "label_efecto": None,
    "frame_arena": None, "animacion_activa": False, "canvas_efectos": None
}

# Sprites de personajes y enemigos (emojis)
SPRITES = {
    "jugador": {"guerrero": "🧔⚔️", "mago": "🧙‍♂️", "arquero": "🏹🧝"},
    "enemigo": {"lobo": "🐺", "orco": "👹", "araña gigante": "🕷️", "esqueleto": "💀", 
                "goblin": "👺", "dragon": "🐉", "demonio": "👿", "default": "👾"},
    "efecto": {"golpe": "💥", "critico": "⚡💥", "fuego": "🔥", "hielo": "❄️", 
               "curacion": "💚✨", "defensa": "🛡️✨", "miss": "💨"}
}

# Colores para efectos visuales
COLORES_EFECTO = {
    "corte": "#FF4444",      # Rojo para cortes de espada
    "corte_brillo": "#FFAAAA",
    "flecha": "#8B4513",     # Marrón para flechas
    "flecha_punta": "#C0C0C0",
    "fuego": "#FF6600",      # Naranja para fuego
    "fuego_centro": "#FFFF00",
    "hielo": "#00BFFF",      # Azul claro para hielo
    "hielo_centro": "#FFFFFF",
    "magia": "#9932CC",      # Púrpura para magia
    "magia_brillo": "#DDA0DD",
    "curacion": "#00FF00",   # Verde para curación
    "defensa": "#4169E1"     # Azul para defensa
}

# Funciones auxiliares básicas
def obtener_jugador():
    import main
    return main.jugador_actual

def obtener_datos():
    import main
    if not main.datos_juego or not main.datos_juego.get('enemigos'):
        main.cargar_datos()
    return main.datos_juego

def limpiar_pantalla():
    if estado["frame_actual"]:
        estado["frame_actual"].destroy()

def mostrar_mensaje(mensaje):
    ttk.dialogs.Messagebox.show_info(title="Información", message=mensaje, parent=estado["root"])

# FUNCIÓN PARA MOSTRAR AVISOS TEMPORALES EN COMBATE
def mostrar_aviso_temporal(mensaje, duracion=3500, color="#FFFFFF", tamaño_fuente=14):
    """Muestra un aviso temporal en el canvas de combate que desaparece automáticamente"""
    if not verificar_canvas():
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        # Eliminar avisos anteriores
        canvas.delete("aviso")
        
        # Obtener el centro del canvas (ahora es 300)
        centro_x = POS_CENTRO
        
        # Crear texto del aviso centrado y más arriba en el canvas
        # Usar anchor='n' para que el texto se ancle desde arriba y se expanda hacia abajo
        canvas.create_text(centro_x, 5, text=mensaje, font=("Helvetica", tamaño_fuente, "bold"),
                         fill=color, tags="aviso", anchor='n', width=550)
        
        # Hacer que desaparezca después de la duración especificada
        def eliminar_aviso():
            if verificar_canvas():
                try:
                    canvas.delete("aviso")
                except:
                    pass
        
        estado["root"].after(duracion, eliminar_aviso)
    except:
        pass

def crear_frame_principal():
    limpiar_pantalla()
    estado["frame_actual"] = ttk.Frame(estado["container"])
    estado["frame_actual"].pack(fill=BOTH, expand=True)
    return estado["frame_actual"]

def crear_meter(parent, texto, estilo, tamaño=150):
    return Meter(parent, metersize=tamaño, padding=10, amountused=0, metertype="semi",
                 subtext=texto, interactive=False, bootstyle=estilo)

# FUNCIÓN PARA CREAR BOTONES CON EFECTOS HOVER
def crear_boton_con_hover(parent, texto, comando, estilo, width=20, **kwargs):
    """Crea un botón con efectos hover mejorados"""
    btn = ttk.Button(parent, text=texto, command=comando, bootstyle=estilo, width=width, **kwargs)
    
    # Guardar estilo original
    estilo_sin_outline = estilo.replace("-outline", "")
    
    def on_enter(e):
        """Efecto al entrar el mouse"""
        try:
            # Cambiar a estilo sólido
            btn.configure(bootstyle=estilo_sin_outline)
            # Cambiar cursor
            btn.configure(cursor="hand2")
        except:
            pass
    
    def on_leave(e):
        """Efecto al salir el mouse"""
        try:
            # Volver a estilo original
            btn.configure(bootstyle=estilo)
            # Restaurar cursor
            btn.configure(cursor="")
        except:
            pass
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn

# FUNCIÓN PARA CREAR FONDO ANIMADO CON PARTÍCULAS
def crear_fondo_animado(root):
    """Crea un canvas con partículas animadas de fondo"""
    canvas_fondo = Canvas(root, highlightthickness=0, bg='#000000')
    canvas_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    canvas_fondo.lower()
    
    # Lista de partículas
    particulas = []
    num_particulas = 50
    
    # Crear partículas iniciales
    for _ in range(num_particulas):
        particula = {
            'x': random.randint(0, root.winfo_screenwidth()),
            'y': random.randint(0, root.winfo_screenheight()),
            'velocidad': random.uniform(0.5, 2.0),
            'tamaño': random.randint(1, 3),
            'opacidad': random.uniform(0.3, 0.8),
            'color': random.choice(['#FFFFFF', '#4A90E2', '#7B68EE', '#FFD700', '#FF6B6B'])
        }
        particulas.append(particula)
    
    def animar_particulas():
        """Anima las partículas en el canvas"""
        if not canvas_fondo.winfo_exists():
            return
        
        try:
            canvas_fondo.delete("particula")
            
            ancho = root.winfo_width()
            alto = root.winfo_height()
            
            if ancho <= 1 or alto <= 1:
                root.after(50, animar_particulas)
                return
            
            # Actualizar y dibujar partículas
            for particula in particulas:
                # Mover partícula hacia abajo
                particula['y'] += particula['velocidad']
                
                # Si sale de la pantalla, reiniciar arriba
                if particula['y'] > alto:
                    particula['y'] = 0
                    particula['x'] = random.randint(0, ancho)
                
                # Ajustar posición si la ventana cambió de tamaño
                if particula['x'] > ancho:
                    particula['x'] = random.randint(0, ancho)
                
                # Dibujar partícula
                color = particula['color']
                tamaño = particula['tamaño']
                x = particula['x']
                y = particula['y']
                
                # Crear partícula como círculo
                canvas_fondo.create_oval(
                    x - tamaño, y - tamaño,
                    x + tamaño, y + tamaño,
                    fill=color, outline=color, tags="particula"
                )
            
            # Continuar animación
            root.after(30, animar_particulas)
        except:
            pass
    
    # Iniciar animación después de un pequeño delay
    root.after(100, animar_particulas)
    
    return canvas_fondo

# PANTALLA DE INICIO
def mostrar_pantalla_inicio():
    frame = crear_frame_principal()
    
    ttk.Label(frame, text="⚔️ Los Tres Pilares Olvidados ⚔️", font=("Helvetica", 24, "bold"), 
              bootstyle="primary").pack(pady=40)
    
    frame_btns = ttk.Frame(frame)
    frame_btns.pack(pady=20)
    
    botones = [
        ("🎮 NUEVO JUEGO", "success-outline", mostrar_creacion_personaje),
        ("📁 CARGAR JUEGO", "info-outline", mostrar_cargar_partida),
        ("🚪 SALIR", "danger-outline", lambda: estado["root"].destroy())
    ]
    for texto, estilo, cmd in botones:
        crear_boton_con_hover(frame_btns, texto, cmd, estilo, width=20).pack(pady=10)
    
    ttk.Label(frame, text="Desarrollado con Python y ttkbootstrap", font=("Helvetica", 10),
              bootstyle="secondary").pack(side=BOTTOM, pady=20)

# CREACIÓN DE PERSONAJE
def actualizar_stats_preview(*args):
    stats = {"guerrero": (120, 18, 20), "mago": (80, 20, 5), "arquero": (90, 30, 2)}
    vida, ataque, defensa = stats.get(estado["clase_seleccionada"].get(), stats["guerrero"])
    estado["meter_vida"].configure(amountused=vida)
    estado["meter_ataque"].configure(amountused=ataque)
    estado["meter_defensa"].configure(amountused=defensa)

def mostrar_creacion_personaje():
    frame = crear_frame_principal()
    
    ttk.Label(frame, text="CREACIÓN DE PERSONAJE", font=("Helvetica", 20, "bold"),
              bootstyle="primary").pack(pady=20)
    
    frame_principal = ttk.Frame(frame)
    frame_principal.pack(fill=BOTH, expand=True, padx=20)
    
    # Formulario
    frame_form = ttk.Labelframe(frame_principal, text="Datos del Héroe", bootstyle="info")
    frame_form.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
    
    ttk.Label(frame_form, text="Nombre:", bootstyle="primary").pack(anchor=W, pady=(10, 5))
    estado["entry_nombre"] = ttk.Entry(frame_form, width=30)
    estado["entry_nombre"].pack(fill=X, pady=(0, 15))
    estado["entry_nombre"].insert(0, "")
    
    ttk.Label(frame_form, text="Clase:", bootstyle="primary").pack(anchor=W, pady=(10, 5))
    estado["clase_seleccionada"] = ttk.StringVar(value="guerrero")
    frame_clases = ttk.Frame(frame_form)
    frame_clases.pack(fill=X, pady=(0, 15))
    
    for texto, valor in [("⚔️ Guerrero", "guerrero"), ("🔮 Mago", "mago"), ("🏹 Arquero", "arquero")]:
        ttk.Radiobutton(frame_clases, text=texto, value=valor, variable=estado["clase_seleccionada"],
                        bootstyle="info-toolbutton").pack(side=LEFT, padx=(0, 10))

    # Estadísticas
    frame_stats = ttk.Labelframe(frame_principal, text="Estadísticas", bootstyle="success")
    frame_stats.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))
    
    # meters vida, ataque y defensa
    estado["meter_vida"] = crear_meter(frame_stats, "VIDA", "danger")
    estado["meter_vida"].pack(pady=10)
    estado["meter_ataque"] = crear_meter(frame_stats, "ATAQUE", "warning")
    estado["meter_ataque"].pack(pady=10)
    estado["meter_defensa"] = crear_meter(frame_stats, "DEFENSA", "info")
    estado["meter_defensa"].pack(pady=10)
    
    estado["clase_seleccionada"].trace_add('write', actualizar_stats_preview)
    actualizar_stats_preview()
    
    # Botones
    frame_btns = ttk.Frame(frame)
    frame_btns.pack(fill=X, pady=20)
    crear_boton_con_hover(frame_btns, "🎯 CREAR PERSONAJE", crear_personaje,
               "success", width=20).pack(side=RIGHT, padx=(10, 0))
    crear_boton_con_hover(frame_btns, "↩️ VOLVER", mostrar_pantalla_inicio,
               "secondary", width=15).pack(side=RIGHT)

def crear_personaje():
    nombre = estado["entry_nombre"].get().strip()
    if not nombre:
        mostrar_mensaje("¡Debes ingresar un nombre para tu héroe!")
        return
    
    from modules.personaje import crear_personaje as crear_pj
    import main
    main.jugador_actual = crear_pj(nombre, estado["clase_seleccionada"].get())
    mostrar_animacion_bienvenida()

# ANIMACIÓN DE BIENVENIDA
def mostrar_animacion_bienvenida():
    frame = crear_frame_principal()
    jugador = obtener_jugador()
    
    frame_anim = ttk.Frame(frame)
    frame_anim.place(relx=0.5, rely=0.5, anchor="center")
    
    iconos = {"guerrero": "⚔️", "mago": "🔮", "arquero": "🏹"}
    label_icono = ttk.Label(frame_anim, text=iconos.get(jugador["clase"], "🎭"),
                            font=("Helvetica", 60), bootstyle="warning")
    label_icono.pack(pady=20)
    
    label_bienvenida = ttk.Label(frame_anim, text="", font=("Helvetica", 28, "bold"), bootstyle="success")
    label_bienvenida.pack(pady=10)
    label_nombre = ttk.Label(frame_anim, text="", font=("Helvetica", 36, "bold"), bootstyle="primary")
    label_nombre.pack(pady=10)
    label_mensaje = ttk.Label(frame_anim, text="", font=("Helvetica", 14), bootstyle="secondary")
    label_mensaje.pack(pady=20)
    
    animar_texto(label_bienvenida, "¡Bienvenido a tu partida!", 0, lambda:
        animar_texto(label_nombre, jugador["nombre"].upper(), 0, lambda:
            animar_texto(label_mensaje, "Prepárate para la aventura...", 0, lambda:
                animar_pulso(label_icono, 0, 9, mostrar_pantalla_principal))))

def animar_texto(label, texto, i, callback=None):
    if i <= len(texto):
        label.configure(text=texto[:i])
        estado["root"].after(50, lambda: animar_texto(label, texto, i + 1, callback))
    elif callback:
        estado["root"].after(300, callback)

def animar_pulso(label, paso, max_pasos, callback):
    tamaños = [60, 70, 60]
    if paso < max_pasos:
        label.configure(font=("Helvetica", tamaños[paso % 3]))
        estado["root"].after(150, lambda: animar_pulso(label, paso + 1, max_pasos, callback))
    elif callback:
        estado["root"].after(500, callback)

# PANTALLA PRINCIPAL
def mostrar_pantalla_principal():
    frame = crear_frame_principal()
    jugador = obtener_jugador()
    
    ttk.Label(frame, text=f"AVENTURAS DE {jugador['nombre'].upper()}", font=("Helvetica", 16, "bold"),
              bootstyle="primary").pack(pady=10)
    
    estado["notebook"] = ttk.Notebook(frame, bootstyle="primary")
    estado["notebook"].pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    pestanas = [
        ("🎭 ESTADO", crear_pestana_estado)
    ]
    for texto, funcion in pestanas:
        f = ttk.Frame(estado["notebook"])
        funcion(f)
        estado["notebook"].add(f, text=texto)

def crear_pestana_estado(parent):
    jugador = obtener_jugador()
    frame_principal = ttk.Frame(parent)
    frame_principal.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Izquierda - Stats
    frame_izq = ttk.Frame(frame_principal)
    frame_izq.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
    
    frame_stats = ttk.Labelframe(frame_izq, text="Estadísticas Principales", bootstyle="info")
    frame_stats.pack(fill=BOTH, expand=True, pady=(0, 10))
    
    # Calcular porcentajes reales
    pct_vida = (jugador["vida_actual"] / jugador["vida_maxima"]) * 100
    pct_mana = (jugador["mana_actual"] / jugador["mana_maximo"]) * 100
    
    estado["meter_vida_jugador"] = Meter(frame_stats, metersize=180, padding=15, amountused=pct_vida,
        metertype="semi", subtext="VIDA", interactive=False, bootstyle="danger",
        textright=f"{jugador['vida_actual']}/{jugador['vida_maxima']}", stripethickness=10)
    estado["meter_vida_jugador"].pack(pady=10)
    
    estado["meter_mana_jugador"] = Meter(frame_stats, metersize=180, padding=15, amountused=pct_mana,
        metertype="semi", subtext="MANA", interactive=False, bootstyle="primary",
        textright=f"{jugador['mana_actual']}/{jugador['mana_maximo']}", stripethickness=10)
    estado["meter_mana_jugador"].pack(pady=10)
    
    frame_exp = ttk.Frame(frame_stats)
    frame_exp.pack(fill=X, pady=10)
    ttk.Label(frame_exp, text="EXPERIENCIA:", bootstyle="primary").pack(side=LEFT)
    ttk.Label(frame_exp, text=f"{jugador['experiencia']}/{jugador['experiencia_necesaria']}",
             bootstyle="success").pack(side=RIGHT)
    
    # Atributos
    frame_attr = ttk.Labelframe(frame_izq, text="Atributos", bootstyle="success")
    frame_attr.pack(fill=BOTH, expand=True)
    
    atributos = [("Nivel", jugador["nivel"], "warning"), ("Ataque", jugador["ataque"], "danger"),
                 ("Defensa", jugador["defensa"], "info"), ("Velocidad", jugador["velocidad"], "success"),
                 ("Clase", jugador["clase"].title(), "primary")]
    for nombre, valor, estilo in atributos:
        f = ttk.Frame(frame_attr)
        f.pack(fill=X, pady=8, padx=10)
        ttk.Label(f, text=nombre, bootstyle="primary", width=12).pack(side=LEFT)
        ttk.Label(f, text=str(valor), bootstyle=estilo, font=("Helvetica", 10, "bold")).pack(side=RIGHT)
    
    ttk.Button(frame_attr, text="🔄 ACTUALIZAR", command=actualizar_estado_personaje,
               bootstyle="outline-primary").pack(side=BOTTOM, pady=10)
    
    # Derecha - Menú
    frame_menu = ttk.Labelframe(frame_principal, text="Menú de Acciones", bootstyle="warning")
    frame_menu.pack(side=RIGHT, fill=BOTH, expand=True, padx=(5, 0))
    
    botones_menu = [("⚔️ IR A LA BATALLA", "danger", ir_a_batalla),
                    ("💾 GUARDAR PARTIDA", "success", guardar_partida_interfaz),
                    ("🏠 MENÚ PRINCIPAL", "info", mostrar_pantalla_inicio),
                    ("🚪 SALIR DEL JUEGO", "secondary", lambda: estado["root"].destroy())]
    for texto, estilo, cmd in botones_menu:
        ttk.Button(frame_menu, text=texto, command=cmd, bootstyle=estilo, width=25).pack(pady=15, padx=10)

def crear_pestana_habilidades(parent):
    jugador = obtener_jugador()
    frame_principal = ttk.Frame(parent)
    frame_principal.pack(fill=BOTH, expand=True, padx=10, pady=10)

    columnas = [{"text": "Habilidad", "stretch": True}, {"text": "Daño", "stretch": False},
                {"text": "Costo Mana", "stretch": False}, {"text": "Descripción", "stretch": True}]
    datos = [("Golpe Poderoso", "25", "10", "Golpe cargado con fuerza adicional"),
        ("Defender", "0", "5", "Aumenta la defensa por un turno"),
             ("Bola de Fuego", "35", "20", "Proyectil de fuego que quema al enemigo")]
    
    estado["tabla_habilidades"] = Tableview(frame_principal, coldata=columnas, rowdata=datos,
                                             paginated=True, searchable=True, bootstyle="primary", height=200)
    estado["tabla_habilidades"].pack(fill=BOTH, expand=True)
    
    ttk.Label(frame_principal, text=f"Habilidades desbloqueadas: {len(jugador['habilidades'])}",
              bootstyle="success").pack(anchor=W, pady=(10, 0))

def crear_pestana_inventario(parent):
    frame_principal = ttk.Frame(parent)
    frame_principal.pack(fill=BOTH, expand=True, padx=10, pady=10)
    ttk.Label(frame_principal, text="SISTEMA DE INVENTARIO", font=("Helvetica", 16, "bold"),
              bootstyle="warning").pack(expand=True)
    ttk.Label(frame_principal, text="Esta función estará disponible en la próxima actualización",
              font=("Helvetica", 12), bootstyle="secondary").pack(expand=True)

# FUNCIONES DE ACTUALIZACIÓN
def actualizar_estado_personaje():
    jugador = obtener_jugador()
    if not jugador:
        return
    pct_vida = (jugador["vida_actual"] / jugador["vida_maxima"]) * 100
    pct_mana = (jugador["mana_actual"] / jugador["mana_maximo"]) * 100
    estado["meter_vida_jugador"].configure(amountused=pct_vida,
        textright=f"{jugador['vida_actual']}/{jugador['vida_maxima']}")
    estado["meter_mana_jugador"].configure(amountused=pct_mana,
        textright=f"{jugador['mana_actual']}/{jugador['mana_maximo']}")

def actualizar_combate_ui():
    if not estado.get("enemigo_actual"):
        return
    
    # Verificar que los widgets existan en el diccionario
    if not estado.get("meter_vida_combate") or not estado.get("meter_mana_combate") or not estado.get("meter_vida_enemigo"):
        return
    
    # Función helper para verificar si un widget existe y está activo
    def widget_existe(widget):
        if not widget:
            return False
        try:
            # Verificar que el widget existe (no usar winfo_viewable() porque puede fallar)
            return widget.winfo_exists()
        except:
            return False
    
    # Obtener referencias a los widgets
    meter_vida = estado.get("meter_vida_combate")
    meter_mana = estado.get("meter_mana_combate")
    meter_enemigo = estado.get("meter_vida_enemigo")
    
    # Si no existen los widgets, salir
    if not meter_vida or not meter_mana or not meter_enemigo:
        return
    
    jugador = obtener_jugador()
    enemigo = estado["enemigo_actual"]
    
    # Actualizar cada widget individualmente con verificación y manejo de errores
    # Importar TclError para capturarlo específicamente
    from tkinter import TclError
    
    # Verificar y actualizar meter_vida
    try:
        if widget_existe(meter_vida):
            meter_vida.configure(
                amountused=(jugador["vida_actual"] / jugador["vida_maxima"]) * 100,
                textright=f"{jugador['vida_actual']}/{jugador['vida_maxima']}")
    except (TclError, AttributeError, RuntimeError):
        # Widget fue destruido o está siendo destruido, ignorar error
        pass
    except Exception:
        # Cualquier otro error también ignorar para evitar crashes
        pass
    
    # Verificar y actualizar meter_mana
    try:
        if widget_existe(meter_mana):
            meter_mana.configure(
                amountused=(jugador["mana_actual"] / jugador["mana_maximo"]) * 100,
                textright=f"{jugador['mana_actual']}/{jugador['mana_maximo']}")
    except (TclError, AttributeError, RuntimeError):
        # Widget fue destruido o está siendo destruido, ignorar error
        pass
    except Exception:
        # Cualquier otro error también ignorar para evitar crashes
        pass
    
    # Verificar y actualizar meter_enemigo
    try:
        if widget_existe(meter_enemigo):
            meter_enemigo.configure(
                amountused=(enemigo["vida_actual"] / enemigo["vida_maxima"]) * 100,
                textright=f"{enemigo['vida_actual']}/{enemigo['vida_maxima']}")
    except (TclError, AttributeError, RuntimeError):
        # Widget fue destruido o está siendo destruido, ignorar error
        pass
    except Exception:
        # Cualquier otro error también ignorar para evitar crashes
        pass

# COMBATE
def ir_a_batalla():
    datos = obtener_datos()
    enemigos_data = datos.get('enemigos', [])
    if not enemigos_data:
        mostrar_mensaje("No hay enemigos disponibles.")
        return
    
    multiplicador = 1.0 + (estado["nivel_dificultad"] - 1) * 0.15
    enemigo_data = random.choice(enemigos_data)
    
    from modules.enemigo import crear_enemigo
    enemigo = crear_enemigo(enemigo_data['nombre'], enemigo_data.get('zona', 'bosque'),
                            enemigo_data, multiplicador_dificultad=multiplicador)
    mostrar_pantalla_combate(enemigo)

def mostrar_pantalla_combate(enemigo):
    frame = crear_frame_principal()
    estado["enemigo_actual"] = enemigo
    estado["animacion_activa"] = False
    jugador = obtener_jugador()
    
    # Título
    ttk.Label(frame, text="⚔️ COMBATE ⚔️", font=("Helvetica", 20, "bold"), bootstyle="danger").pack(pady=5)
    ttk.Label(frame, text=f"Nivel de Dificultad: {estado['nivel_dificultad']}", font=("Helvetica", 12, "bold"),
              bootstyle="warning").pack()
    
    # Frame principal de combate (dividido en 3 columnas)
    frame_combate = ttk.Frame(frame)
    frame_combate.pack(fill=BOTH, expand=True, padx=40, pady=10)
    
    # COLUMNA IZQUIERDA - Jugador
    frame_jugador = ttk.Labelframe(frame_combate, text="Tu Estado", bootstyle="info")
    frame_jugador.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
    
    # Sprite del jugador arriba
    sprite_pj = SPRITES["jugador"].get(jugador["clase"], "🧔")
    ttk.Label(frame_jugador, text=sprite_pj, font=("Segoe UI Emoji", 50)).pack(pady=10)
    ttk.Label(frame_jugador, text=jugador["nombre"], font=("Helvetica", 14, "bold"), 
              bootstyle="primary").pack()
    ttk.Label(frame_jugador, text=f"({jugador['clase'].title()})", font=("Helvetica", 10),
              bootstyle="secondary").pack()
    
    # Barras de vida y mana
    pct_vida = (jugador["vida_actual"] / jugador["vida_maxima"]) * 100
    estado["meter_vida_combate"] = Meter(frame_jugador, metersize=130, padding=8, amountused=pct_vida,
        metertype="semi", subtext="VIDA", interactive=False, bootstyle="danger",
        textright=f"{jugador['vida_actual']}/{jugador['vida_maxima']}", stripethickness=8)
    estado["meter_vida_combate"].pack(pady=5)
    
    pct_mana = (jugador["mana_actual"] / jugador["mana_maximo"]) * 100
    estado["meter_mana_combate"] = Meter(frame_jugador, metersize=130, padding=8, amountused=pct_mana,
        metertype="semi", subtext="MANA", interactive=False, bootstyle="primary",
        textright=f"{jugador['mana_actual']}/{jugador['mana_maximo']}", stripethickness=8)
    estado["meter_mana_combate"].pack(pady=5)
    
    # COLUMNA CENTRAL - Arena de combate (Canvas para animaciones)
    frame_arena = ttk.Frame(frame_combate)
    frame_arena.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
    
    # Canvas más ancho para dar más espacio
    estado["canvas_efectos"] = Canvas(frame_arena, width=600, height=250, 
                                       bg='#1a1a2e', highlightthickness=3, highlightbackground='#FFD700')
    estado["canvas_efectos"].pack(expand=True)
    
    # Dibujar en el canvas
    # Símbolo VS en el centro
    estado["canvas_efectos"].create_text(300, 60, text="⚔️ VS ⚔️", font=("Helvetica", 24, "bold"),
                                          fill="#FFD700", tags="vs")
    
    # Sprite jugador (izquierda del canvas, más separado del centro)
    estado["canvas_efectos"].create_text(120, 150, text=sprite_pj, font=("Segoe UI Emoji", 45), 
                                          fill="white", tags="sprite_jugador")
    
    # Sprite enemigo (derecha del canvas, más separado del centro)
    sprite_en = SPRITES["enemigo"].get(enemigo["nombre"].lower(), SPRITES["enemigo"]["default"])
    estado["canvas_efectos"].create_text(480, 150, text=sprite_en, font=("Segoe UI Emoji", 45),
                                          fill="white", tags="sprite_enemigo")
    
    # Línea divisoria decorativa en el centro
    estado["canvas_efectos"].create_line(300, 90, 300, 220, fill="#4a4a6a", width=2, dash=(5, 3))
    
    # COLUMNA DERECHA - Enemigo
    frame_enemigo = ttk.Labelframe(frame_combate, text="Enemigo", bootstyle="warning")
    frame_enemigo.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))
    
    # Sprite del enemigo arriba
    ttk.Label(frame_enemigo, text=sprite_en, font=("Segoe UI Emoji", 50)).pack(pady=10)
    ttk.Label(frame_enemigo, text=enemigo["nombre"], font=("Helvetica", 14, "bold"),
              bootstyle="warning").pack()
    ttk.Label(frame_enemigo, text=f"(Zona: {enemigo['zona'].title()})", font=("Helvetica", 10),
              bootstyle="secondary").pack()
    
    # Barra de vida del enemigo
    pct_vida_en = (enemigo["vida_actual"] / enemigo["vida_maxima"]) * 100
    estado["meter_vida_enemigo"] = Meter(frame_enemigo, metersize=130, padding=8, amountused=pct_vida_en,
        metertype="semi", subtext="VIDA", interactive=False, bootstyle="danger",
        textright=f"{enemigo['vida_actual']}/{enemigo['vida_maxima']}", stripethickness=8)
    estado["meter_vida_enemigo"].pack(pady=5)
    
    # Stats del enemigo
    frame_info_en = ttk.Frame(frame_enemigo)
    frame_info_en.pack(pady=10)
    ttk.Label(frame_info_en, text=f"⚔️ Ataque: {enemigo['ataque']}", bootstyle="danger", 
              font=("Helvetica", 12, "bold")).pack()
    ttk.Label(frame_info_en, text=f"🛡️ Defensa: {enemigo['defensa']}", bootstyle="info",
              font=("Helvetica", 12, "bold")).pack()
    
    # Acciones
    frame_acc = ttk.Labelframe(frame, text="Acciones", bootstyle="success")
    frame_acc.pack(fill=X, padx=20, pady=10)
    frame_btns = ttk.Frame(frame_acc)
    frame_btns.pack(pady=10)
    
    botones = [("⚔️ ATACAR", "danger", mostrar_menu_habilidades),
               ("🛡️ DEFENDER", "info", defender),
               ("🧪 USAR OBJETO", "primary", mostrar_menu_objetos),
               ("↩️ VOLVER", "secondary", mostrar_pantalla_principal)]
    for texto, estilo, cmd in botones:
        crear_boton_con_hover(frame_btns, texto, cmd, estilo, width=20).pack(side=LEFT, padx=5)

# FUNCIONES DE ANIMACIÓN DE COMBATE CON CANVAS
# Posiciones para el canvas de 600px de ancho
POS_JUGADOR = 120  # Posición X del jugador (más separado del centro)
POS_ENEMIGO = 480  # Posición X del enemigo (más separado del centro)
POS_CENTRO = 300   # Centro del canvas

# Función helper para verificar que el canvas existe
def verificar_canvas():
    """Verifica que el canvas de efectos existe y está activo"""
    if not estado.get("canvas_efectos"):
        return False
    try:
        return estado["canvas_efectos"].winfo_exists()
    except:
        return False

def animar_ataque_jugador(callback=None):
    if not verificar_canvas():
        if callback:
            callback()
        return
    estado["animacion_activa"] = True
    jugador = obtener_jugador()
    clase = jugador["clase"]
    
    # Elegir tipo de animación según la clase
    if clase == "guerrero":
        animar_corte_espada(POS_JUGADOR, POS_ENEMIGO, callback)
    elif clase == "arquero":
        animar_flecha(POS_JUGADOR, POS_ENEMIGO, callback)
    else:
        animar_ataque_basico(POS_JUGADOR, POS_ENEMIGO, callback)

def animar_ataque_enemigo(callback=None):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    estado["animacion_activa"] = True
    enemigo = estado["enemigo_actual"]
    nombre_enemigo = enemigo["nombre"].lower()
    
    # Seleccionar animación según el tipo de enemigo
    if "lobo" in nombre_enemigo:
        animar_ataque_lobo(callback)
    elif "orco" in nombre_enemigo:
        animar_ataque_orco(callback)
    elif "araña" in nombre_enemigo or "araña gigante" in nombre_enemigo:
        animar_ataque_araña(callback)
    elif "esqueleto" in nombre_enemigo:
        animar_ataque_esqueleto(callback)
    elif "goblin" in nombre_enemigo:
        animar_ataque_goblin(callback)
    elif "dragon" in nombre_enemigo:
        animar_ataque_dragon(callback)
    elif "demonio" in nombre_enemigo:
        animar_ataque_demonio(callback)
    else:
        # Animación genérica mejorada con colores visibles
        animar_ataque_basico(POS_ENEMIGO, POS_JUGADOR, callback, es_enemigo=True)

def animar_habilidad_especial(tipo_efecto, callback=None):
    if not verificar_canvas():
        if callback:
            callback()
        return
    estado["animacion_activa"] = True
    jugador = obtener_jugador()
    
    if tipo_efecto == "fuego" or "Fuego" in str(tipo_efecto):
        animar_bola_fuego(POS_JUGADOR, POS_ENEMIGO, callback)
    elif tipo_efecto == "hielo":
        animar_rayo_hielo(POS_JUGADOR, POS_ENEMIGO, callback)
    elif tipo_efecto == "curacion":
        animar_curacion(POS_JUGADOR, callback)
    elif tipo_efecto == "defensa":
        animar_escudo(POS_JUGADOR, callback)
    elif jugador["clase"] == "arquero":
        animar_flecha_multiple(POS_JUGADOR, POS_ENEMIGO, callback)
    else:
        animar_golpe_poderoso(POS_JUGADOR, POS_ENEMIGO, callback)

# ANIMACIÓN: Corte de espada (Guerrero)
def animar_corte_espada(x_inicio, x_fin, callback):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    # Mover sprite del jugador
    mover_sprite_canvas("sprite_jugador", 30, 0)
    
    def dibujar_corte(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        
        if paso < 8:
            # Dibujar líneas de corte diagonal
            progreso = paso / 8
            x = x_inicio + (x_fin - x_inicio) * progreso * 0.7
            
            # Corte principal (diagonal)
            canvas.create_line(x - 20, 110, x + 40, 190, fill=COLORES_EFECTO["corte"], 
                             width=6 - paso//2, tags="efecto")
            canvas.create_line(x - 15, 115, x + 35, 185, fill=COLORES_EFECTO["corte_brillo"], 
                             width=3, tags="efecto")
            
            # Segundo corte (X)
            if paso > 3:
                canvas.create_line(x + 40, 110, x - 20, 190, fill=COLORES_EFECTO["corte"], 
                                 width=5 - paso//3, tags="efecto")
            
            # Chispas mejoradas con más partículas
            for i in range(8):
                spark_x = x + random.randint(-20, 40)
                spark_y = 150 + random.randint(-30, 30)
                tamaño_spark = random.randint(8, 16)
                # Variar colores de las chispas
                colores_spark = ["#FFD700", "#FFA500", "#FFFFFF", "#FF6B6B"]
                color_spark = random.choice(colores_spark)
                canvas.create_text(spark_x, spark_y, text="✨", font=("Segoe UI Emoji", tamaño_spark), 
                                 fill=color_spark, tags="efecto")
            
            # Partículas adicionales de impacto
            for i in range(5):
                part_x = x + random.randint(-25, 45)
                part_y = 150 + random.randint(-20, 20)
                canvas.create_oval(part_x - 2, part_y - 2, part_x + 2, part_y + 2,
                                 fill="#FFD700", outline="#FFA500", tags="efecto")
            
            if verificar_canvas():
                estado["root"].after(50, lambda: dibujar_corte(paso + 1))
        else:
            try:
                canvas.delete("efecto")
                sacudir_sprite_canvas("sprite_enemigo", 0, lambda: terminar_animacion(callback))
            except:
                terminar_animacion(callback)
    
    if verificar_canvas():
        estado["root"].after(100, lambda: dibujar_corte(0))

# ANIMACIÓN: Flecha (Arquero)
def animar_flecha(x_inicio, x_fin, callback):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    def dibujar_flecha(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        if paso < 12:
            progreso = paso / 12
            x = x_inicio + (x_fin - x_inicio) * progreso
            
            # Cuerpo de la flecha
            canvas.create_line(x - 30, 150, x, 150, fill=COLORES_EFECTO["flecha"], 
                             width=4, tags="efecto")
            # Punta de flecha
            canvas.create_polygon(x, 150, x + 12, 146, x + 12, 154, 
                                fill=COLORES_EFECTO["flecha_punta"], tags="efecto")
            # Plumas
            canvas.create_line(x - 30, 150, x - 38, 142, fill="#8B0000", width=2, tags="efecto")
            canvas.create_line(x - 30, 150, x - 38, 158, fill="#8B0000", width=2, tags="efecto")
            
            # Estela
            if paso > 2:
                canvas.create_line(x - 50, 150, x - 30, 150, fill="#FFFF00", 
                                 width=2, stipple="gray50", tags="efecto")
            
            if verificar_canvas():
                estado["root"].after(35, lambda: dibujar_flecha(paso + 1))
        else:
            # Impacto
            try:
                canvas.create_text(x_fin, 150, text="💥", font=("Segoe UI Emoji", 30), tags="efecto")
                if verificar_canvas():
                    estado["root"].after(200, lambda: canvas.delete("efecto") if verificar_canvas() else None)
                sacudir_sprite_canvas("sprite_enemigo", 0, lambda: terminar_animacion(callback))
            except:
                terminar_animacion(callback)
    
    dibujar_flecha(0)

# ANIMACIÓN: Bola de fuego (Mago)
def animar_bola_fuego(x_inicio, x_fin, callback):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    def dibujar_fuego(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        if paso < 12:
            progreso = paso / 12
            x = x_inicio + (x_fin - x_inicio) * progreso
            tamaño = 15 + paso * 2
            
            # Bola de fuego (círculos concéntricos)
            canvas.create_oval(x - tamaño, 150 - tamaño//2, x + tamaño, 150 + tamaño//2,
                             fill=COLORES_EFECTO["fuego"], outline=COLORES_EFECTO["fuego_centro"],
                             width=3, tags="efecto")
            canvas.create_oval(x - tamaño//2, 150 - tamaño//4, x + tamaño//2, 150 + tamaño//4,
                             fill=COLORES_EFECTO["fuego_centro"], tags="efecto")
            
            # Llamas mejoradas con más partículas
            for i in range(8):
                flama_x = x + random.randint(-tamaño, tamaño)
                flama_y = 150 + random.randint(-20, 20)
                tamaño_flama = random.randint(10, 18)
                canvas.create_text(flama_x, flama_y, text="🔥", 
                                 font=("Segoe UI Emoji", tamaño_flama), tags="efecto")
            
            # Partículas de fuego adicionales
            for i in range(6):
                part_x = x + random.randint(-tamaño - 10, tamaño + 10)
                part_y = 150 + random.randint(-25, 25)
                # Partículas de diferentes tamaños y colores
                colores_fuego = ["#FF6600", "#FF9900", "#FFFF00", "#FF3300"]
                color_fuego = random.choice(colores_fuego)
                tamaño_part = random.randint(3, 6)
                canvas.create_oval(part_x - tamaño_part, part_y - tamaño_part,
                                 part_x + tamaño_part, part_y + tamaño_part,
                                 fill=color_fuego, outline="#FF6600", tags="efecto")
            
            if verificar_canvas():
                estado["root"].after(45, lambda: dibujar_fuego(paso + 1))
        else:
            # Explosión final
            try:
                for i in range(6):
                    angulo = i * 60
                    exp_x = x_fin + int(30 * math.cos(math.radians(angulo)))
                    exp_y = 150 + int(30 * math.sin(math.radians(angulo)))
                    canvas.create_text(exp_x, exp_y, text="💥", 
                                     font=("Segoe UI Emoji", 16), tags="efecto")
                canvas.create_text(x_fin, 150, text="🔥", font=("Segoe UI Emoji", 35), tags="efecto")
                if verificar_canvas():
                    estado["root"].after(300, lambda: canvas.delete("efecto") if verificar_canvas() else None)
                sacudir_sprite_canvas("sprite_enemigo", 0, lambda: terminar_animacion(callback))
            except:
                terminar_animacion(callback)
    
    dibujar_fuego(0)

# ANIMACIÓN: Rayo de hielo
def animar_rayo_hielo(x_inicio, x_fin, callback):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    def dibujar_hielo(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        if paso < 10:
            progreso = paso / 10
            x = x_inicio + (x_fin - x_inicio) * progreso
            
            # Rayo zigzag
            puntos = []
            for i in range(8):
                px = x_inicio + (x - x_inicio) * (i / 8)
                py = 150 + random.randint(-12, 12)
                puntos.extend([px, py])
            
            if len(puntos) >= 4:
                canvas.create_line(puntos, fill=COLORES_EFECTO["hielo"], width=4, tags="efecto")
                canvas.create_line(puntos, fill=COLORES_EFECTO["hielo_centro"], width=2, tags="efecto")
            
            # Cristales de hielo mejorados con más partículas
            for i in range(8):
                cx = x + random.randint(-25, 25)
                cy = 150 + random.randint(-20, 20)
                tamaño_hielo = random.randint(12, 20)
                canvas.create_text(cx, cy, text="❄️", font=("Segoe UI Emoji", tamaño_hielo), tags="efecto")
            
            # Partículas de hielo adicionales
            for i in range(5):
                part_x = x + random.randint(-30, 30)
                part_y = 150 + random.randint(-25, 25)
                canvas.create_oval(part_x - 3, part_y - 3, part_x + 3, part_y + 3,
                                 fill="#00BFFF", outline="#FFFFFF", width=1, tags="efecto")
            
            if verificar_canvas():
                estado["root"].after(50, lambda: dibujar_hielo(paso + 1))
        else:
            try:
                canvas.create_text(x_fin, 150, text="❄️", font=("Segoe UI Emoji", 40), tags="efecto")
                if verificar_canvas():
                    estado["root"].after(300, lambda: canvas.delete("efecto") if verificar_canvas() else None)
                sacudir_sprite_canvas("sprite_enemigo", 0, lambda: terminar_animacion(callback))
            except:
                terminar_animacion(callback)
    
    dibujar_hielo(0)

# ANIMACIÓN: Golpe poderoso
def animar_golpe_poderoso(x_inicio, x_fin, callback):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    def dibujar_golpe(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        if paso < 6:
            # Onda de choque
            radio = paso * 18
            canvas.create_oval(x_fin - radio, 150 - radio//2, x_fin + radio, 150 + radio//2,
                             outline=COLORES_EFECTO["magia"], width=4 - paso//2, tags="efecto")
            canvas.create_oval(x_fin - radio//2, 150 - radio//4, x_fin + radio//2, 150 + radio//4,
                             outline=COLORES_EFECTO["magia_brillo"], width=2, tags="efecto")
            
            # Impacto central
            canvas.create_text(x_fin, 150, text="💥", font=("Segoe UI Emoji", 30 + paso * 4), tags="efecto")
            
            if verificar_canvas():
                estado["root"].after(80, lambda: dibujar_golpe(paso + 1))
        else:
            try:
                canvas.delete("efecto")
                sacudir_sprite_canvas("sprite_enemigo", 0, lambda: terminar_animacion(callback))
            except:
                terminar_animacion(callback)
    
    dibujar_golpe(0)

# ANIMACIÓN: Múltiples flechas
def animar_flecha_multiple(x_inicio, x_fin, callback):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    def dibujar_flechas(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        if paso < 10:
            progreso = paso / 10
            x = x_inicio + (x_fin - x_inicio) * progreso
            
            # 3 flechas en paralelo
            for offset in [-20, 0, 20]:
                y = 150 + offset
                canvas.create_line(x - 25, y, x + 8, y, fill=COLORES_EFECTO["flecha"], 
                                 width=3, tags="efecto")
                canvas.create_polygon(x + 8, y, x + 16, y - 3, x + 16, y + 3,
                                    fill=COLORES_EFECTO["flecha_punta"], tags="efecto")
            
            if verificar_canvas():
                estado["root"].after(40, lambda: dibujar_flechas(paso + 1))
        else:
            try:
                for offset in [-20, 0, 20]:
                    canvas.create_text(x_fin, 150 + offset, text="💥", 
                                     font=("Segoe UI Emoji", 20), tags="efecto")
                if verificar_canvas():
                    estado["root"].after(250, lambda: canvas.delete("efecto") if verificar_canvas() else None)
                sacudir_sprite_canvas("sprite_enemigo", 0, lambda: terminar_animacion(callback))
            except:
                terminar_animacion(callback)
    
    dibujar_flechas(0)

# ANIMACIONES ESPECÍFICAS DE ENEMIGOS

# ANIMACIÓN: Ataque de Lobo
def animar_ataque_lobo(callback=None):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    def dibujar_ataque_lobo(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        
        if paso < 10:
            # Lobo corriendo hacia el jugador
            progreso = paso / 10
            x = POS_ENEMIGO - (POS_ENEMIGO - POS_JUGADOR) * progreso * 0.7
            
            # Dibujar rastros de movimiento
            for i in range(3):
                trail_x = x + random.randint(-15, 15)
                trail_y = 150 + random.randint(-10, 10)
                canvas.create_text(trail_x, trail_y, text="💨", font=("Segoe UI Emoji", 12), 
                                 fill="#CCCCCC", tags="efecto")
            
            # Garras del lobo
            canvas.create_text(x, 150, text="🐺", font=("Segoe UI Emoji", 40), tags="efecto")
            canvas.create_text(x - 20, 140, text="✂️", font=("Segoe UI Emoji", 20), 
                             fill="#FF4444", tags="efecto")
            canvas.create_text(x + 20, 160, text="✂️", font=("Segoe UI Emoji", 20), 
                             fill="#FF4444", tags="efecto")
            
            if verificar_canvas():
                estado["root"].after(50, lambda: dibujar_ataque_lobo(paso + 1))
        else:
            # Impacto
            try:
                canvas.create_text(POS_JUGADOR, 150, text="💥", font=("Segoe UI Emoji", 45), 
                                 fill="#FF4444", tags="efecto")
                # Partículas de sangre
                for i in range(6):
                    part_x = POS_JUGADOR + random.randint(-25, 25)
                    part_y = 150 + random.randint(-20, 20)
                    canvas.create_text(part_x, part_y, text="🩸", font=("Segoe UI Emoji", 12), tags="efecto")
                
                if verificar_canvas():
                    estado["root"].after(200, lambda: canvas.delete("efecto") if verificar_canvas() else None)
                sacudir_sprite_canvas("sprite_jugador", 0, lambda: terminar_animacion(callback))
            except:
                terminar_animacion(callback)
    
    dibujar_ataque_lobo(0)

# ANIMACIÓN: Ataque de Orco
def animar_ataque_orco(callback=None):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    def dibujar_ataque_orco(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        
        if paso < 8:
            # Orco moviéndose y golpeando con maza
            progreso = paso / 8
            x = POS_ENEMIGO - (POS_ENEMIGO - POS_JUGADOR) * progreso * 0.6
            
            # Maza girando
            angulo = paso * 45
            maza_x = x + int(30 * math.cos(math.radians(angulo)))
            maza_y = 150 + int(20 * math.sin(math.radians(angulo)))
            
            canvas.create_text(x, 150, text="👹", font=("Segoe UI Emoji", 40), tags="efecto")
            canvas.create_text(maza_x, maza_y, text="🔨", font=("Segoe UI Emoji", 25), tags="efecto")
            
            # Chispas del impacto
            if paso > 4:
                for i in range(3):
                    spark_x = x + random.randint(-20, 20)
                    spark_y = 150 + random.randint(-15, 15)
                    canvas.create_text(spark_x, spark_y, text="✨", font=("Segoe UI Emoji", 10), 
                                     fill="#FFD700", tags="efecto")
            
            if verificar_canvas():
                estado["root"].after(60, lambda: dibujar_ataque_orco(paso + 1))
        else:
            # Impacto fuerte
            try:
                canvas.create_text(POS_JUGADOR, 150, text="💥", font=("Segoe UI Emoji", 50), 
                                 fill="#FF6600", tags="efecto")
                # Onda de choque
                for i in range(3):
                    radio = 20 + i * 15
                    canvas.create_oval(POS_JUGADOR - radio, 150 - radio//2, 
                                     POS_JUGADOR + radio, 150 + radio//2,
                                     outline="#FF6600", width=2, tags="efecto")
                
                if verificar_canvas():
                    estado["root"].after(250, lambda: canvas.delete("efecto") if verificar_canvas() else None)
                sacudir_sprite_canvas("sprite_jugador", 0, lambda: terminar_animacion(callback))
            except:
                terminar_animacion(callback)
    
    dibujar_ataque_orco(0)

# ANIMACIÓN: Ataque de Araña
def animar_ataque_araña(callback=None):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    def dibujar_ataque_araña(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        
        if paso < 12:
            # Telaraña lanzada hacia el jugador
            progreso = paso / 12
            x = POS_ENEMIGO - (POS_ENEMIGO - POS_JUGADOR) * progreso
            
            # Dibujar telaraña
            canvas.create_text(x, 150, text="🕷️", font=("Segoe UI Emoji", 35), tags="efecto")
            
            # Líneas de telaraña
            for i in range(4):
                angulo = i * 90
                line_x = x + int(25 * math.cos(math.radians(angulo)))
                line_y = 150 + int(25 * math.sin(math.radians(angulo)))
                canvas.create_line(x, 150, line_x, line_y, fill="#8B4513", width=2, tags="efecto")
            
            # Partículas de veneno
            if paso > 6:
                for i in range(3):
                    poison_x = x + random.randint(-20, 20)
                    poison_y = 150 + random.randint(-15, 15)
                    canvas.create_text(poison_x, poison_y, text="💚", font=("Segoe UI Emoji", 10), tags="efecto")
            
            if verificar_canvas():
                estado["root"].after(45, lambda: dibujar_ataque_araña(paso + 1))
        else:
            # Impacto con telaraña
            try:
                canvas.create_text(POS_JUGADOR, 150, text="🕸️", font=("Segoe UI Emoji", 40), tags="efecto")
                # Telaraña envolvente
                for i in range(6):
                    angulo = i * 60
                    web_x = POS_JUGADOR + int(30 * math.cos(math.radians(angulo)))
                    web_y = 150 + int(30 * math.sin(math.radians(angulo)))
                    canvas.create_line(POS_JUGADOR, 150, web_x, web_y, fill="#8B4513", width=2, tags="efecto")
                
                if verificar_canvas():
                    estado["root"].after(300, lambda: canvas.delete("efecto") if verificar_canvas() else None)
                sacudir_sprite_canvas("sprite_jugador", 0, lambda: terminar_animacion(callback))
            except:
                terminar_animacion(callback)
    
    dibujar_ataque_araña(0)

# ANIMACIÓN: Ataque de Esqueleto
def animar_ataque_esqueleto(callback=None):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    def dibujar_ataque_esqueleto(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        
        if paso < 10:
            # Esqueleto lanzando hueso o atacando con espada
            progreso = paso / 10
            x = POS_ENEMIGO - (POS_ENEMIGO - POS_JUGADOR) * progreso * 0.7
            
            canvas.create_text(x, 150, text="💀", font=("Segoe UI Emoji", 40), tags="efecto")
            
            # Hueso o espada volando
            if paso > 3:
                weapon_x = x - 40
                canvas.create_text(weapon_x, 150, text="🦴", font=("Segoe UI Emoji", 20), tags="efecto")
            
            # Aura oscura
            canvas.create_oval(x - 30, 120, x + 30, 180,
                             outline="#4B0082", width=2, tags="efecto")
            
            if verificar_canvas():
                estado["root"].after(50, lambda: dibujar_ataque_esqueleto(paso + 1))
        else:
            # Impacto oscuro
            try:
                canvas.create_text(POS_JUGADOR, 150, text="💀", font=("Segoe UI Emoji", 45), 
                                 fill="#4B0082", tags="efecto")
                # Aura oscura
                for i in range(3):
                    radio = 15 + i * 10
                    canvas.create_oval(POS_JUGADOR - radio, 150 - radio//2, 
                                     POS_JUGADOR + radio, 150 + radio//2,
                                     outline="#4B0082", width=2, tags="efecto")
                
                if verificar_canvas():
                    estado["root"].after(250, lambda: canvas.delete("efecto") if verificar_canvas() else None)
                sacudir_sprite_canvas("sprite_jugador", 0, lambda: terminar_animacion(callback))
            except:
                terminar_animacion(callback)
    
    dibujar_ataque_esqueleto(0)

# ANIMACIÓN: Ataque de Goblin
def animar_ataque_goblin(callback=None):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    def dibujar_ataque_goblin(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        
        if paso < 8:
            # Goblin saltando y atacando
            progreso = paso / 8
            x = POS_ENEMIGO - (POS_ENEMIGO - POS_JUGADOR) * progreso * 0.6
            y_offset = abs(math.sin(progreso * math.pi)) * 20  # Salto
            
            canvas.create_text(x, 150 - y_offset, text="👺", font=("Segoe UI Emoji", 35), tags="efecto")
            
            # Daga
            if paso > 2:
                daga_x = x - 30
                canvas.create_text(daga_x, 150 - y_offset, text="🗡️", font=("Segoe UI Emoji", 18), tags="efecto")
            
            if verificar_canvas():
                estado["root"].after(55, lambda: dibujar_ataque_goblin(paso + 1))
        else:
            # Impacto rápido
            try:
                canvas.create_text(POS_JUGADOR, 150, text="💥", font=("Segoe UI Emoji", 35), 
                                 fill="#FF4444", tags="efecto")
                if verificar_canvas():
                    estado["root"].after(200, lambda: canvas.delete("efecto") if verificar_canvas() else None)
                sacudir_sprite_canvas("sprite_jugador", 0, lambda: terminar_animacion(callback))
            except:
                terminar_animacion(callback)
    
    dibujar_ataque_goblin(0)

# ANIMACIÓN: Ataque de Dragón
def animar_ataque_dragon(callback=None):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    def dibujar_ataque_dragon(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        
        if paso < 15:
            # Dragón escupiendo fuego
            progreso = paso / 15
            x = POS_ENEMIGO - (POS_ENEMIGO - POS_JUGADOR) * progreso * 0.5
            
            # Cabeza del dragón
            canvas.create_text(POS_ENEMIGO, 150, text="🐉", font=("Segoe UI Emoji", 50), tags="efecto")
            
            # Llamas de fuego
            tamaño_fuego = paso * 3
            for i in range(5):
                flama_x = x + random.randint(-tamaño_fuego, tamaño_fuego)
                flama_y = 150 + random.randint(-15, 15)
                tamaño_flama = random.randint(15, 25)
                canvas.create_text(flama_x, flama_y, text="🔥", font=("Segoe UI Emoji", tamaño_flama), tags="efecto")
            
            # Partículas de fuego
            for i in range(8):
                part_x = x + random.randint(-tamaño_fuego - 10, tamaño_fuego + 10)
                part_y = 150 + random.randint(-20, 20)
                color_fuego = random.choice(["#FF3300", "#FF6600", "#FF9900", "#FFFF00"])
                tamaño_part = random.randint(4, 8)
                canvas.create_oval(part_x - tamaño_part, part_y - tamaño_part,
                                 part_x + tamaño_part, part_y + tamaño_part,
                                 fill=color_fuego, outline=color_fuego, tags="efecto")
            
            if verificar_canvas():
                estado["root"].after(40, lambda: dibujar_ataque_dragon(paso + 1))
        else:
            # Explosión de fuego
            try:
                canvas.create_text(POS_JUGADOR, 150, text="💥", font=("Segoe UI Emoji", 50), 
                                 fill="#FF3300", tags="efecto")
                # Explosión circular
                for i in range(8):
                    angulo = i * 45
                    exp_x = POS_JUGADOR + int(40 * math.cos(math.radians(angulo)))
                    exp_y = 150 + int(40 * math.sin(math.radians(angulo)))
                    canvas.create_text(exp_x, exp_y, text="🔥", font=("Segoe UI Emoji", 20), tags="efecto")
                
                if verificar_canvas():
                    estado["root"].after(350, lambda: canvas.delete("efecto") if verificar_canvas() else None)
                sacudir_sprite_canvas("sprite_jugador", 0, lambda: terminar_animacion(callback))
            except:
                terminar_animacion(callback)
    
    dibujar_ataque_dragon(0)

# ANIMACIÓN: Ataque de Demonio
def animar_ataque_demonio(callback=None):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    def dibujar_ataque_demonio(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        
        if paso < 12:
            # Demonio lanzando energía oscura
            progreso = paso / 12
            x = POS_ENEMIGO - (POS_ENEMIGO - POS_JUGADOR) * progreso
            
            # Demonio
            canvas.create_text(POS_ENEMIGO, 150, text="👿", font=("Segoe UI Emoji", 50), tags="efecto")
            
            # Bola de energía oscura
            tamaño_energia = 15 + paso * 2
            canvas.create_oval(x - tamaño_energia, 150 - tamaño_energia//2,
                             x + tamaño_energia, 150 + tamaño_energia//2,
                             fill="#8B0000", outline="#FF0000", width=2, tags="efecto")
            canvas.create_oval(x - tamaño_energia//2, 150 - tamaño_energia//4,
                             x + tamaño_energia//2, 150 + tamaño_energia//4,
                             fill="#FF0000", tags="efecto")
            
            # Partículas oscuras
            for i in range(5):
                part_x = x + random.randint(-tamaño_energia, tamaño_energia)
                part_y = 150 + random.randint(-15, 15)
                canvas.create_text(part_x, part_y, text="💜", font=("Segoe UI Emoji", 12), tags="efecto")
            
            if verificar_canvas():
                estado["root"].after(45, lambda: dibujar_ataque_demonio(paso + 1))
        else:
            # Explosión oscura
            try:
                canvas.create_text(POS_JUGADOR, 150, text="💥", font=("Segoe UI Emoji", 50), 
                                 fill="#8B0000", tags="efecto")
                # Rayos oscuros
                for i in range(6):
                    angulo = i * 60
                    ray_x = POS_JUGADOR + int(35 * math.cos(math.radians(angulo)))
                    ray_y = 150 + int(35 * math.sin(math.radians(angulo)))
                    canvas.create_line(POS_JUGADOR, 150, ray_x, ray_y, fill="#8B0000", width=3, tags="efecto")
                
                if verificar_canvas():
                    estado["root"].after(300, lambda: canvas.delete("efecto") if verificar_canvas() else None)
                sacudir_sprite_canvas("sprite_jugador", 0, lambda: terminar_animacion(callback))
            except:
                terminar_animacion(callback)
    
    dibujar_ataque_demonio(0)

# ANIMACIÓN: Curación
def animar_curacion(x_pos, callback):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    def dibujar_curacion(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        if paso < 12:
            # Partículas subiendo mejoradas
            for i in range(12):
                px = x_pos + random.randint(-30, 30)
                py = 180 - paso * 6 + random.randint(-10, 10)
                tamaño_part = random.randint(10, 18)
                # Variar colores de las partículas de curación
                colores_curacion = ["#00FF00", "#90EE90", "#98FB98", "#00FF7F"]
                color_part = random.choice(colores_curacion)
                canvas.create_text(px, py, text="✨", font=("Segoe UI Emoji", tamaño_part), 
                                 fill=color_part, tags="efecto")
            
            # Partículas adicionales de curación
            for i in range(8):
                part_x = x_pos + random.randint(-35, 35)
                part_y = 180 - paso * 5 + random.randint(-12, 12)
                canvas.create_oval(part_x - 2, part_y - 2, part_x + 2, part_y + 2,
                                 fill="#00FF00", outline="#90EE90", tags="efecto")
            
            # Aura de curación
            canvas.create_oval(x_pos - 40, 110, x_pos + 40, 190,
                             outline=COLORES_EFECTO["curacion"], width=2, tags="efecto")
            canvas.create_text(x_pos, 150, text="💚", font=("Segoe UI Emoji", 25), tags="efecto")
            
            if verificar_canvas():
                estado["root"].after(60, lambda: dibujar_curacion(paso + 1))
        else:
            try:
                canvas.delete("efecto")
                terminar_animacion(callback)
            except:
                terminar_animacion(callback)
    
    dibujar_curacion(0)

# ANIMACIÓN: Escudo de defensa
def animar_escudo(x_pos, callback):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    def dibujar_escudo(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        if paso < 10:
            # Escudo creciendo
            tamaño = paso * 6
            canvas.create_arc(x_pos - tamaño, 150 - tamaño, x_pos + tamaño, 150 + tamaño,
                            start=45, extent=90, fill=COLORES_EFECTO["defensa"],
                            outline="#FFFFFF", width=3, tags="efecto")
            canvas.create_text(x_pos, 150, text="🛡️", font=("Segoe UI Emoji", 20 + paso * 2), tags="efecto")
            
            if verificar_canvas():
                estado["root"].after(60, lambda: dibujar_escudo(paso + 1))
        else:
            try:
                canvas.delete("efecto")
                terminar_animacion(callback)
            except:
                terminar_animacion(callback)
    
    dibujar_escudo(0)

# ANIMACIÓN: Ataque básico
def animar_ataque_basico(x_inicio, x_fin, callback, es_enemigo=False):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    canvas = estado["canvas_efectos"]
    
    try:
        canvas.delete("efecto")
    except:
        if callback:
            callback()
        return
    
    sprite_tag = "sprite_enemigo" if es_enemigo else "sprite_jugador"
    target_tag = "sprite_jugador" if es_enemigo else "sprite_enemigo"
    direccion = -1 if es_enemigo else 1
    
    def mover_y_golpear(paso):
        if not verificar_canvas():
            if callback:
                callback()
            return
        
        try:
            canvas.delete("efecto")
        except:
            if callback:
                callback()
            return
        if paso < 5:
            mover_sprite_canvas(sprite_tag, direccion * paso * 15, 0)
            if verificar_canvas():
                estado["root"].after(50, lambda: mover_y_golpear(paso + 1))
        elif paso < 8:
            try:
                # Efecto de impacto más visible con colores brillantes para enemigos
                if es_enemigo:
                    # Colores brillantes para el ataque del enemigo (rojo/naranja)
                    canvas.create_text(POS_CENTRO, 150, text="💥", font=("Segoe UI Emoji", 45), 
                                     fill="#FF4444", tags="efecto")
                    # Partículas de impacto rojas/naranjas brillantes
                    for i in range(6):
                        part_x = POS_CENTRO + random.randint(-35, 35)
                        part_y = 150 + random.randint(-25, 25)
                        color_part = random.choice(["#FF4444", "#FF6600", "#FF8800", "#FFAA00", "#FF0000"])
                        tamaño_part = random.randint(4, 7)
                        canvas.create_oval(part_x - tamaño_part, part_y - tamaño_part, 
                                         part_x + tamaño_part, part_y + tamaño_part,
                                         fill=color_part, outline=color_part, tags="efecto")
                    # Chispas adicionales
                    for i in range(4):
                        spark_x = POS_CENTRO + random.randint(-30, 30)
                        spark_y = 150 + random.randint(-20, 20)
                        canvas.create_text(spark_x, spark_y, text="✨", font=("Segoe UI Emoji", 12), 
                                         fill="#FFD700", tags="efecto")
                else:
                    canvas.create_text(POS_CENTRO, 150, text="💥", font=("Segoe UI Emoji", 35), tags="efecto")
                if verificar_canvas():
                    estado["root"].after(80, lambda: mover_y_golpear(paso + 1))
            except:
                if callback:
                    callback()
        elif paso < 13:
            mover_sprite_canvas(sprite_tag, direccion * (13 - paso) * 15, 0)
            if verificar_canvas():
                estado["root"].after(50, lambda: mover_y_golpear(paso + 1))
        else:
            try:
                canvas.delete("efecto")
                mover_sprite_canvas(sprite_tag, 0, 0)
                # Si es ataque del enemigo, hacer que el sprite del jugador se sacuda y parpadee
                if es_enemigo:
                    # Sacudir el sprite del jugador con parpadeo blanco brillante
                    def sacudir_con_parpadeo(paso_sacudida):
                        if not verificar_canvas():
                            terminar_animacion(callback)
                            return
                        
                        if paso_sacudida < 10:
                            # Aumentar el offset para hacer la sacudida más visible
                            offset = 12 if paso_sacudida % 2 == 0 else -12
                            # Alternar entre blanco brillante y blanco normal mientras se sacude
                            color_blanco = "#FFFFFF" if paso_sacudida % 2 == 0 else "#E0E0E0"
                            mover_sprite_canvas("sprite_jugador", offset, 0, color_blanco)
                            if verificar_canvas():
                                estado["root"].after(50, lambda: sacudir_con_parpadeo(paso_sacudida + 1))
                        else:
                            mover_sprite_canvas("sprite_jugador", 0, 0, "white")
                            terminar_animacion(callback)
                    
                    sacudir_con_parpadeo(0)
                else:
                    # Si es ataque del jugador, solo sacudir al enemigo
                    sacudir_sprite_canvas(target_tag, 0, lambda: terminar_animacion(callback))
            except:
                terminar_animacion(callback)
    
    mover_y_golpear(0)

# Funciones auxiliares para Canvas
def mover_sprite_canvas(tag, dx, dy, color="white"):
    """Mueve el sprite en el canvas, con opción de cambiar el color"""
    if not verificar_canvas():
        return
    
    try:
        canvas = estado["canvas_efectos"]
        canvas.delete(tag)
        jugador = obtener_jugador()
        enemigo = estado["enemigo_actual"]
        
        if tag == "sprite_jugador":
            sprite = SPRITES["jugador"].get(jugador["clase"], "🧔")
            canvas.create_text(POS_JUGADOR + dx, 150 + dy, text=sprite, font=("Segoe UI Emoji", 45), 
                             fill=color, tags=tag)
        elif tag == "sprite_enemigo":
            sprite = SPRITES["enemigo"].get(enemigo["nombre"].lower(), SPRITES["enemigo"]["default"])
            canvas.create_text(POS_ENEMIGO + dx, 150 + dy, text=sprite, font=("Segoe UI Emoji", 45),
                             fill=color, tags=tag)
    except:
        pass

def sacudir_sprite_canvas(tag, paso, callback):
    if not verificar_canvas():
        if callback:
            callback()
        return
    
    if paso < 6:
        offset = 6 if paso % 2 == 0 else -6
        mover_sprite_canvas(tag, offset, 0)
        if verificar_canvas():
            estado["root"].after(50, lambda: sacudir_sprite_canvas(tag, paso + 1, callback))
    else:
        mover_sprite_canvas(tag, 0, 0)
        if callback:
            callback()

def terminar_animacion(callback):
    estado["animacion_activa"] = False
    if verificar_canvas():
        try:
            estado["canvas_efectos"].delete("efecto")
        except:
            pass
    if callback:
        callback()

def mostrar_menu_habilidades():
    datos = obtener_datos()
    jugador = obtener_jugador()
    habilidades = [h for h in datos.get('habilidades', []) if h.get('clase', '').lower() == jugador["clase"].lower()]
    
    if not habilidades:
        mostrar_mensaje("No tienes habilidades disponibles")
        return
    
    # Cerrar el menú de objetos si está abierto
    if estado["frame_menu_objetos"]:
        estado["frame_menu_objetos"].destroy()
        estado["frame_menu_objetos"] = None
    
    # Cerrar el menú de habilidades si ya está abierto
    if estado["frame_menu_habilidades"]:
        estado["frame_menu_habilidades"].destroy()
    
    estado["frame_menu_habilidades"] = ttk.Labelframe(estado["frame_actual"], text="Selecciona una Habilidad", bootstyle="primary")
    estado["frame_menu_habilidades"].pack(fill=X, padx=20, pady=10)
    frame_habs = ttk.Frame(estado["frame_menu_habilidades"])
    frame_habs.pack(pady=10)
    
    for i, hab in enumerate(habilidades):
        nombre, daño, costo = hab.get('nombre', ''), hab.get('daño_base', '0'), hab.get('coste_mana', '0')
        tiene_mana = jugador["mana_actual"] >= int(costo)
        
        f = ttk.Frame(frame_habs)
        f.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="ew")
        ttk.Button(f, text=f"{nombre}\nDaño: {daño} | Mana: {costo}", command=lambda h=hab: usar_habilidad(h),
                   bootstyle="primary" if tiene_mana else "secondary", width=20,
                   state="normal" if tiene_mana else "disabled").pack()
        ttk.Label(f, text=hab.get('descripcion', ''), font=("Helvetica", 8), bootstyle="secondary",
                  wraplength=150).pack(pady=(2, 0))

def usar_habilidad(habilidad):
    if estado["animacion_activa"]:
        return
    
    nombre, daño, costo = habilidad.get('nombre', ''), int(habilidad.get('daño_base', 0)), int(habilidad.get('coste_mana', 0))
    jugador, enemigo = obtener_jugador(), estado["enemigo_actual"]
    
    if jugador["mana_actual"] < costo:
        mostrar_aviso_temporal("❌ ¡No tienes suficiente mana!", 
                             duracion=3000, color="#FF6B6B", tamaño_fuente=14)
        return
    
    jugador["mana_actual"] -= costo
    
    # Cerrar el menú de habilidades
    if estado["frame_menu_habilidades"]:
        estado["frame_menu_habilidades"].destroy()
        estado["frame_menu_habilidades"] = None
    
    # Cerrar el menú de objetos si está abierto
    if estado["frame_menu_objetos"]:
        estado["frame_menu_objetos"].destroy()
        estado["frame_menu_objetos"] = None
    
    if daño > 0:
        # Determinar tipo de efecto según el nombre de la habilidad
        if "Fuego" in nombre or "Bola" in nombre:
            tipo_efecto = "fuego"
        elif "Hielo" in nombre or "Frost" in nombre:
            tipo_efecto = "hielo"
        else:
            tipo_efecto = "golpe"
        
        # Animar y luego aplicar daño
        def aplicar_daño():
            from modules.enemigo import recibir_daño_enemigo
            daño_real = max(1, daño + (jugador["ataque"] // 2) - (enemigo["defensa"] // 3))
            recibir_daño_enemigo(enemigo, daño_real)
            actualizar_combate_ui()
            mostrar_aviso_temporal(f"⚔️ {nombre} causa {daño_real} de daño!", 
                                 duracion=3500, color="#4ECDC4", tamaño_fuente=14)
            verificar_fin_combate()
        
        if "Fuego" in nombre or "Bola" in nombre or "Disparo" in nombre:
            animar_habilidad_especial(tipo_efecto, aplicar_daño)
        else:
            animar_ataque_jugador(aplicar_daño)
    else:
        # Habilidades de soporte
        from modules.personaje import curar_personaje
        
        def aplicar_efecto():
            if "Curar" in nombre:
                curar_personaje(jugador, 30)
                mostrar_mensaje("¡Te curas 30 de vida!")
            elif "Defender" in nombre:
                jugador["defensa"] += 5
                mostrar_mensaje("¡Tu defensa aumenta!")
            elif "Esquivar" in nombre:
                jugador["velocidad"] += 3
                mostrar_mensaje("¡Tu velocidad aumenta!")
            actualizar_combate_ui()
            verificar_fin_combate()
        
        animar_habilidad_especial("curacion" if "Curar" in nombre else "defensa", aplicar_efecto)
    
def verificar_fin_combate():
    jugador, enemigo = obtener_jugador(), estado["enemigo_actual"]
    from modules.enemigo import esta_vivo_enemigo
    
    if not esta_vivo_enemigo(enemigo):
        from modules.personaje import ganar_experiencia
        exp = enemigo["experiencia_otorgada"]
        ganar_experiencia(jugador, exp)
        jugador["vida_actual"] = jugador["vida_maxima"]
        estado["nivel_dificultad"] += 1
        estado["root"].after(500, lambda: mostrar_victoria(exp))
    else:
        estado["root"].after(800, turno_enemigo)

def mostrar_victoria(exp):
    mostrar_mensaje(f"🎉 ¡VICTORIA! 🎉\n\nGanas {exp} exp.\nVida restaurada.\nDificultad: Nivel {estado['nivel_dificultad']}")
    mostrar_pantalla_principal()
    
def defender():
    if estado["animacion_activa"]:
        return
    
    jugador = obtener_jugador()
    jugador["defensa"] += 3
    
    def aplicar_defensa():
        mostrar_aviso_temporal("🛡️ Defensa aumentada temporalmente!", 
                             duracion=3500, color="#4169E1", tamaño_fuente=14)
        actualizar_combate_ui()
        estado["root"].after(800, turno_enemigo)
    
    animar_habilidad_especial("defensa", aplicar_defensa)

def turno_enemigo():
    enemigo, jugador = estado["enemigo_actual"], obtener_jugador()
    from modules.enemigo import esta_vivo_enemigo, usar_habilidad_aleatoria_enemigo
    from modules.personaje import esta_vivo_personaje
    
    if not enemigo or not esta_vivo_enemigo(enemigo):
        return
    if not esta_vivo_personaje(jugador):
        mostrar_derrota()
        return
    
    # Animar ataque del enemigo
    def aplicar_ataque_enemigo():
        resultado = usar_habilidad_aleatoria_enemigo(enemigo, jugador)
        actualizar_combate_ui()
        # Mostrar aviso temporal en lugar de ventana modal
        mostrar_aviso_temporal(f"👹 {enemigo['nombre']} causa {resultado['daño']} de daño!", 
                             duracion=3500, color="#FF6B6B", tamaño_fuente=14)
        
        if not esta_vivo_personaje(jugador):
            estado["root"].after(500, mostrar_derrota)
    
    animar_ataque_enemigo(aplicar_ataque_enemigo)

def mostrar_derrota():
    jugador = obtener_jugador()
    jugador["vida_actual"] = jugador["vida_maxima"]
    actualizar_combate_ui()
    mostrar_mensaje("💀 ¡Has sido derrotado!\n\nTu personaje ha sido curado automáticamente.")

def mostrar_menu_objetos():
    jugador = obtener_jugador()
    objetos = {n: d for n, d in jugador["inventario"].items() if d.get('tipo') == 'consumible' and d.get('cantidad', 0) > 0}
    
    if not objetos:
        mostrar_aviso_temporal("❌ No tienes objetos consumibles", 
                             duracion=3000, color="#FF6B6B", tamaño_fuente=14)
        return
    
    # Cerrar el menú de habilidades si está abierto
    if estado["frame_menu_habilidades"]:
        estado["frame_menu_habilidades"].destroy()
        estado["frame_menu_habilidades"] = None
    
    # Cerrar el menú de objetos si ya está abierto
    if estado["frame_menu_objetos"]:
        estado["frame_menu_objetos"].destroy()
    
    estado["frame_menu_objetos"] = ttk.Labelframe(estado["frame_actual"], text="Selecciona un Objeto", bootstyle="primary")
    estado["frame_menu_objetos"].pack(fill=X, padx=20, pady=10)
    frame_objs = ttk.Frame(estado["frame_menu_objetos"])
    frame_objs.pack(pady=10)
    
    for i, (nombre, datos) in enumerate(objetos.items()):
        f = ttk.Frame(frame_objs)
        f.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="ew")
        ttk.Button(f, text=f"{nombre}\nMana: +{datos.get('mana', 0)} | Cantidad: {datos.get('cantidad', 0)}",
                   command=lambda n=nombre: usar_objeto(n), bootstyle="primary", width=20).pack()

def usar_objeto(nombre_objeto):
    jugador = obtener_jugador()
    if nombre_objeto not in jugador["inventario"]:
        mostrar_mensaje("¡Objeto no encontrado!")
        return
    
    objeto = jugador["inventario"][nombre_objeto]
    if objeto.get('cantidad', 0) <= 0:
        mostrar_mensaje("¡No tienes más de este objeto!")
        return
    
    objeto['cantidad'] -= 1
    if objeto.get('tipo') == 'consumible' and objeto.get('mana', 0) > 0:
        mana_antes = jugador["mana_actual"]
        jugador["mana_actual"] = min(jugador["mana_maximo"], jugador["mana_actual"] + objeto.get('mana', 0))
        mostrar_mensaje(f"¡Usas {nombre_objeto} y recuperas {jugador['mana_actual'] - mana_antes} de mana!")
    
    if objeto['cantidad'] <= 0:
        del jugador["inventario"][nombre_objeto]
    
    actualizar_combate_ui()
    # Cerrar el menú de objetos
    if estado["frame_menu_objetos"]:
        estado["frame_menu_objetos"].destroy()
        estado["frame_menu_objetos"] = None
    
    # Cerrar el menú de habilidades si está abierto
    if estado["frame_menu_habilidades"]:
        estado["frame_menu_habilidades"].destroy()
        estado["frame_menu_habilidades"] = None

# FUNCIONES DE GUARDAR Y CARGAR PARTIDA
def guardar_partida_interfaz():
    import main
    import re
    
    # Crear ventana para ingresar nombre de partida
    ventana_guardar = ttk.Toplevel(estado["root"])
    ventana_guardar.title("Guardar Partida")
    ventana_guardar.geometry("500x300")
    ventana_guardar.position_center()
    
    ttk.Label(ventana_guardar, text="Nombre de la partida:", 
              font=("Helvetica", 12, "bold"), bootstyle="primary").pack(pady=20)
    
    entry_nombre = ttk.Entry(ventana_guardar, width=30, font=("Helvetica", 11))
    entry_nombre.pack(pady=10, padx=20)
    entry_nombre.focus()
    
    # Sugerir nombre basado en el personaje y fecha
    from datetime import datetime
    jugador = obtener_jugador()
    if jugador:
        sugerencia = f"{jugador['nombre']}_Nivel{jugador['nivel']}"
        entry_nombre.insert(0, sugerencia)
        entry_nombre.select_range(0, "end")
    
    ttk.Label(ventana_guardar, text="(El archivo se guardará con extensión .csv)", 
              font=("Helvetica", 9), bootstyle="secondary").pack(pady=5)
    
    frame_btns = ttk.Frame(ventana_guardar)
    frame_btns.pack(pady=20)
    
    def guardar_con_nombre():
        nombre = entry_nombre.get().strip()
        
        if not nombre:
            mostrar_mensaje("Por favor ingresa un nombre para la partida")
            return
        
        # Limpiar el nombre: eliminar caracteres no válidos para nombres de archivo
        nombre_limpio = re.sub(r'[<>:"/\\|?*]', '_', nombre)
        nombre_limpio = nombre_limpio.replace(' ', '_')
        
        # Agregar extensión .csv si no la tiene
        if not nombre_limpio.endswith('.csv'):
            nombre_archivo = nombre_limpio + '.csv'
        else:
            nombre_archivo = nombre_limpio
        
        ventana_guardar.destroy()
        
        exito, mensaje = main.guardar_partida(nombre_archivo)
        if exito:
            mostrar_mensaje(f"✅ {mensaje}")
        else:
            mostrar_mensaje(f"❌ {mensaje}")
    
    crear_boton_con_hover(frame_btns, "Guardar", guardar_con_nombre,
               "success", width=15).pack(side=LEFT, padx=5)
    crear_boton_con_hover(frame_btns, "Cancelar", ventana_guardar.destroy,
               "secondary", width=15).pack(side=LEFT, padx=5)
    
    # Permitir guardar con Enter
    entry_nombre.bind('<Return>', lambda e: guardar_con_nombre())

def mostrar_cargar_partida():
    import main
    partidas = main.obtener_partidas_guardadas()
    
    if not partidas:
        mostrar_mensaje("No hay partidas guardadas")
        return
    
    # Crear ventana de selección de partida
    ventana_cargar = ttk.Toplevel(estado["root"])
    ventana_cargar.title("Cargar Partida")
    ventana_cargar.geometry("500x400")
    ventana_cargar.position_center()
    
    ttk.Label(ventana_cargar, text="Selecciona una partida para cargar:", 
              font=("Helvetica", 12, "bold"), bootstyle="primary").pack(pady=20)
    
    frame_lista = ttk.Frame(ventana_cargar)
    frame_lista.pack(fill=BOTH, expand=True, padx=20, pady=10)
    
    # Lista de partidas con información
    lista_partidas = ttk.Treeview(frame_lista, columns=("info",), show="tree", height=10)
    lista_partidas.heading("#0", text="Archivo")
    lista_partidas.heading("info", text="Información")
    lista_partidas.column("#0", width=200)
    lista_partidas.column("info", width=250)
    lista_partidas.pack(fill=BOTH, expand=True)
    
    for partida in partidas:
        lista_partidas.insert("", "end", text=partida['archivo'], values=(partida['info'],))
    
    # Botones
    frame_btns = ttk.Frame(ventana_cargar)
    frame_btns.pack(pady=10)
    
    def cargar_seleccionada():
        seleccion = lista_partidas.selection()
        if not seleccion:
            mostrar_mensaje("Por favor selecciona una partida")
            return
        
        item = lista_partidas.item(seleccion[0])
        archivo = item['text']
        
        exito, mensaje = main.cargar_partida(archivo)
        ventana_cargar.destroy()
        
        if exito:
            mostrar_mensaje(f"✅ {mensaje}")
            mostrar_pantalla_principal()
        else:
            mostrar_mensaje(f"❌ {mensaje}")
    
    crear_boton_con_hover(frame_btns, "Cargar", cargar_seleccionada, 
               "success", width=15).pack(side=LEFT, padx=5)
    crear_boton_con_hover(frame_btns, "Cancelar", ventana_cargar.destroy, 
               "secondary", width=15).pack(side=LEFT, padx=5)

# INICIALIZACIÓN
def inicializar_interfaz(root):
    estado["root"] = root
    estado["container"] = ttk.Frame(root)
    estado["container"].pack(fill=BOTH, expand=True, padx=10, pady=10)
    mostrar_pantalla_inicio()
