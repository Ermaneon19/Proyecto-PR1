import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Meter
from ttkbootstrap.widgets.tableview import Tableview
from PIL import Image, ImageTk
import os

class InterfazPrincipal:
    def __init__(self, root, juego):
        self.root = root
        self.juego = juego
        self.frame_actual = None
        self.nivel_dificultad = 1
        
        self.container = ttk.Frame(root)
        self.container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        self.mostrar_pantalla_inicio()
    
    def limpiar_pantalla(self):
        """Limpiar la pantalla actual"""
        if self.frame_actual:
            self.frame_actual.destroy()
    
    def mostrar_pantalla_inicio(self):
        """Pantalla de inicio del juego"""
        self.limpiar_pantalla()
        self.frame_actual = ttk.Frame(self.container)
        self.frame_actual.pack(fill=BOTH, expand=True)
        
        titulo = ttk.Label(
            self.frame_actual,
            text="⚔️ MI RPG POR TURNOS ⚔️",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        )
        titulo.pack(pady=40)
        
        frame_botones = ttk.Frame(self.frame_actual)
        frame_botones.pack(pady=20)
        
        btn_nuevo = ttk.Button(
            frame_botones,
            text="🎮 NUEVO JUEGO",
            command=self.mostrar_creacion_personaje,
            bootstyle="success-outline",
            width=20
        )
        btn_nuevo.pack(pady=10)
        
        btn_cargar = ttk.Button(
            frame_botones,
            text="📁 CARGAR JUEGO",
            command=lambda: self.mostrar_mensaje("Función en desarrollo"),
            bootstyle="info-outline",
            width=20
        )
        btn_cargar.pack(pady=10)
        
        btn_salir = ttk.Button(
            frame_botones,
            text="🚪 SALIR",
            command=self.juego.root.quit,
            bootstyle="danger-outline",
            width=20
        )
        btn_salir.pack(pady=10)
        
        info = ttk.Label(
            self.frame_actual,
            text="Desarrollado con Python y ttkbootstrap",
            font=("Helvetica", 10),
            bootstyle="secondary"
        )
        info.pack(side=BOTTOM, pady=20)
    
    def mostrar_creacion_personaje(self):
        """Pantalla de creación de personaje"""
        self.limpiar_pantalla()
        self.frame_actual = ttk.Frame(self.container)
        self.frame_actual.pack(fill=BOTH, expand=True)
        
        titulo = ttk.Label(
            self.frame_actual,
            text="CREACIÓN DE PERSONAJE",
            font=("Helvetica", 20, "bold"),
            bootstyle="primary"
        )
        titulo.pack(pady=20)
        
        frame_principal = ttk.Frame(self.frame_actual)
        frame_principal.pack(fill=BOTH, expand=True, padx=20)
        
        frame_form = ttk.Labelframe(frame_principal, text="Datos del Héroe", bootstyle="info")
        frame_form.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(frame_form, text="Nombre:", bootstyle="primary").pack(anchor=W, pady=(10, 5))
        self.entry_nombre = ttk.Entry(frame_form, width=30)
        self.entry_nombre.pack(fill=X, pady=(0, 15))
        self.entry_nombre.insert(0, "Aragorn")
        
        ttk.Label(frame_form, text="Clase:", bootstyle="primary").pack(anchor=W, pady=(10, 5))
        
        self.clase_seleccionada = ttk.StringVar(value="guerrero")
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
                variable=self.clase_seleccionada,
                bootstyle="info-toolbutton"
            ).pack(side=LEFT, padx=(0, 10))
        
        frame_stats = ttk.Labelframe(frame_principal, text="Estadísticas", bootstyle="success")
        frame_stats.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))
        
        self.meter_vida = Meter(
            frame_stats,
            metersize=150,
            padding=10,
            amountused=0,
            metertype="semi",
            subtext="VIDA",
            interactive=False,
            bootstyle="danger"
        )
        self.meter_vida.pack(pady=10)
        
        self.meter_ataque = Meter(
            frame_stats,
            metersize=150,
            padding=10,
            amountused=0,
            metertype="semi",
            subtext="ATAQUE",
            interactive=False,
            bootstyle="warning"
        )
        self.meter_ataque.pack(pady=10)
        
        self.meter_defensa = Meter(
            frame_stats,
            metersize=150,
            padding=10,
            amountused=0,
            metertype="semi",
            subtext="DEFENSA", 
            interactive=False,
            bootstyle="info"
        )
        self.meter_defensa.pack(pady=10)
        
        try:
            self.clase_seleccionada.trace_add('write', lambda *args: self.actualizar_stats_preview())
        except AttributeError:
            self.clase_seleccionada.trace('w', self.actualizar_stats_preview)
        self.actualizar_stats_preview()
        
        frame_botones = ttk.Frame(self.frame_actual)
        frame_botones.pack(fill=X, pady=20)
        
        btn_crear = ttk.Button(
            frame_botones,
            text="🎯 CREAR PERSONAJE",
            command=self.crear_personaje,
            bootstyle="success",
            width=20
        )
        btn_crear.pack(side=RIGHT, padx=(10, 0))
        
        btn_volver = ttk.Button(
            frame_botones,
            text="↩️ VOLVER",
            command=self.mostrar_pantalla_inicio,
            bootstyle="secondary",
            width=15
        )
        btn_volver.pack(side=RIGHT)
    
    def actualizar_stats_preview(self, *args):
        """Actualizar la vista previa de stats según la clase seleccionada"""
        stats = {
            "guerrero": {"vida": 120, "ataque": 18, "defensa": 15},
            "mago": {"vida": 80, "ataque": 12, "defensa": 8},
            "arquero": {"vida": 90, "ataque": 16, "defensa": 10}
        }
        
        clase = self.clase_seleccionada.get()
        stat = stats.get(clase, stats["guerrero"])
        
        self.meter_vida.configure(amountused=stat["vida"])
        self.meter_ataque.configure(amountused=stat["ataque"]) 
        self.meter_defensa.configure(amountused=stat["defensa"])
    
    def crear_personaje(self):
        """Crear el personaje y avanzar a la pantalla principal"""
        nombre = self.entry_nombre.get().strip()
        clase = self.clase_seleccionada.get()
        
        if not nombre:
            self.mostrar_mensaje("¡Debes ingresar un nombre para tu héroe!")
            return
        
        from modules.personaje import Personaje
        self.juego.jugador = Personaje(nombre, clase)
        
        self.mostrar_pantalla_principal()
    
    def mostrar_pantalla_principal(self):
        """Pantalla principal del juego con el personaje creado"""
        self.limpiar_pantalla()
        self.frame_actual = ttk.Frame(self.container)
        self.frame_actual.pack(fill=BOTH, expand=True)
        
        titulo = ttk.Label(
            self.frame_actual,
            text=f"AVENTURAS DE {self.juego.jugador.nombre.upper()}",
            font=("Helvetica", 16, "bold"),
            bootstyle="primary"
        )
        titulo.pack(pady=10)
        
        self.notebook = ttk.Notebook(self.frame_actual, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        frame_estado = ttk.Frame(self.notebook)
        self.crear_pestana_estado(frame_estado)
        self.notebook.add(frame_estado, text="🎭 ESTADO")
        
        frame_combate = ttk.Frame(self.notebook)
        self.crear_pestana_combate(frame_combate)
        self.notebook.add(frame_combate, text="⚔️ COMBATE")
        
        frame_habilidades = ttk.Frame(self.notebook)
        self.crear_pestana_habilidades(frame_habilidades)
        self.notebook.add(frame_habilidades, text="🔮 HABILIDADES")
        
        frame_inventario = ttk.Frame(self.notebook)
        self.crear_pestana_inventario(frame_inventario)
        self.notebook.add(frame_inventario, text="🎒 INVENTARIO")
    
    def crear_pestana_estado(self, parent):
        """Crear la pestaña de estado del personaje"""
        frame_principal = ttk.Frame(parent)
        frame_principal.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        frame_izquierda = ttk.Frame(frame_principal)
        frame_izquierda.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        
        frame_stats = ttk.Labelframe(frame_izquierda, text="Estadísticas Principales", bootstyle="info")
        frame_stats.pack(fill=BOTH, expand=True, pady=(0, 10))
        
        self.meter_vida_jugador = Meter(
            frame_stats,
            metersize=180,
            padding=15,
            amountused=100,
            metertype="semi",
            subtext="VIDA",
            interactive=False,
            bootstyle="danger",
            textright=f"/{self.juego.jugador.vida_maxima}",
            stripethickness=10
        )
        self.meter_vida_jugador.pack(pady=10)
        
        self.meter_mana_jugador = Meter(
            frame_stats,
            metersize=180,
            padding=15,
            amountused=100,
            metertype="semi",
            subtext="MANA",
            interactive=False,
            bootstyle="primary",
            textright=f"/{self.juego.jugador.mana_maximo}",
            stripethickness=10
        )
        self.meter_mana_jugador.pack(pady=10)
        
        frame_exp = ttk.Frame(frame_stats)
        frame_exp.pack(fill=X, pady=10)
        ttk.Label(frame_exp, text="EXPERIENCIA:", bootstyle="primary").pack(side=LEFT)
        ttk.Label(frame_exp, text=f"{self.juego.jugador.experiencia}/{self.juego.jugador.experiencia_necesaria}", 
                 bootstyle="success").pack(side=RIGHT)
        
        frame_secundarios = ttk.Labelframe(frame_izquierda, text="Atributos", bootstyle="success")
        frame_secundarios.pack(fill=BOTH, expand=True)
        
        stats_data = [
            ("Nivel", self.juego.jugador.nivel, "warning"),
            ("Ataque", self.juego.jugador.ataque, "danger"),
            ("Defensa", self.juego.jugador.defensa, "info"),
            ("Velocidad", self.juego.jugador.velocidad, "success"),
            ("Clase", self.juego.jugador.clase.title(), "primary")
        ]
        
        for stat, valor, style in stats_data:
            frame_stat = ttk.Frame(frame_secundarios)
            frame_stat.pack(fill=X, pady=8, padx=10)
            ttk.Label(frame_stat, text=stat, bootstyle="primary", width=12).pack(side=LEFT)
            ttk.Label(frame_stat, text=str(valor), bootstyle=style, font=("Helvetica", 10, "bold")).pack(side=RIGHT)
        
        ttk.Button(
            frame_secundarios,
            text="🔄 ACTUALIZAR",
            command=self.actualizar_estado_personaje,
            bootstyle="outline-primary"
        ).pack(side=BOTTOM, pady=10)
        
        frame_menu = ttk.Labelframe(frame_principal, text="Menú de Acciones", bootstyle="warning")
        frame_menu.pack(side=RIGHT, fill=BOTH, expand=True, padx=(5, 0))
        
        btn_batalla = ttk.Button(
            frame_menu,
            text="⚔️ IR A LA BATALLA",
            command=self.ir_a_batalla,
            bootstyle="danger",
            width=25
        )
        btn_batalla.pack(pady=15, padx=10)
        
        btn_inventario = ttk.Button(
            frame_menu,
            text="🎒 INVENTARIO",
            command=self.ir_a_inventario,
            bootstyle="info",
            width=25
        )
        btn_inventario.pack(pady=15, padx=10)
        
        btn_salir = ttk.Button(
            frame_menu,
            text="🚪 SALIR DEL JUEGO",
            command=self.salir_del_juego,
            bootstyle="secondary",
            width=25
        )
        btn_salir.pack(pady=15, padx=10)
    
    def crear_pestana_combate(self, parent):
        """Crear la pestaña de combate"""
        frame_principal = ttk.Frame(parent)
        frame_principal.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        frame_enemigos = ttk.Labelframe(frame_principal, text="Seleccionar Enemigo", bootstyle="warning")
        frame_enemigos.pack(fill=X, pady=(0, 10))
        
        frame_seleccion = ttk.Frame(frame_enemigos)
        frame_seleccion.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(frame_seleccion, text="Enemigo:", bootstyle="primary").pack(side=LEFT)
        
        self.combo_enemigos = ttk.Combobox(
            frame_seleccion,
            values=["Lobo", "Orco", "Araña Gigante", "Esqueleto", "Goblin"],
            state="readonly",
            width=15
        )
        self.combo_enemigos.current(0)
        self.combo_enemigos.pack(side=LEFT, padx=(10, 20))
        
        btn_iniciar_combate = ttk.Button(
            frame_seleccion,
            text="⚔️ INICIAR COMBATE",
            command=self.iniciar_combate,
            bootstyle="danger"
        )
        btn_iniciar_combate.pack(side=LEFT)
        
        frame_log = ttk.Labelframe(frame_principal, text="Log del Combate", bootstyle="secondary")
        frame_log.pack(fill=BOTH, expand=True, pady=(0, 10))
        
        self.texto_log = ttk.ScrolledText(
            frame_log,
            height=15,
            wrap=WORD,
            font=("Consolas", 10)
        )
        self.texto_log.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.texto_log.configure(state="disabled")
        
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
                command=lambda acc=texto: self.ejecutar_accion_combate(acc)
            )
            btn.pack(side=LEFT, padx=5)
    
    def crear_pestana_habilidades(self, parent):
        """Crear la pestaña de habilidades"""
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
        
        self.tabla_habilidades = Tableview(
            frame_principal,
            coldata=columnas,
            rowdata=datos,
            paginated=True,
            searchable=True,
            bootstyle="primary",
            height=200
        )
        self.tabla_habilidades.pack(fill=BOTH, expand=True)
        
        frame_info = ttk.Frame(frame_principal)
        frame_info.pack(fill=X, pady=(10, 0))
        
        ttk.Label(
            frame_info, 
            text=f"Habilidades desbloqueadas: {len(self.juego.jugador.habilidades)}",
            bootstyle="success"
        ).pack(side=LEFT)
    
    def crear_pestana_inventario(self, parent):
        """Crear la pestaña de inventario"""
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
    
    def actualizar_estado_personaje(self):
        """Actualizar la visualización del estado del personaje"""
        jugador = self.juego.jugador
        if jugador:
            porcentaje_vida = (jugador.vida_actual / jugador.vida_maxima) * 100
            porcentaje_mana = (jugador.mana_actual / jugador.mana_maximo) * 100
            
            self.meter_vida_jugador.configure(
                amountused=porcentaje_vida,
                textright=f"{jugador.vida_actual}/{jugador.vida_maxima}"
            )
            self.meter_mana_jugador.configure(
                amountused=porcentaje_mana,
                textright=f"{jugador.mana_actual}/{jugador.mana_maximo}"
            )
    
    def ir_a_batalla(self):
        """Crear pantalla de combate con enemigo random"""
        import random
        from modules.enemigo import Enemigo
        
        enemigos_data = self.juego.datos.get('enemigos', [])
        if not enemigos_data:
            self.mostrar_mensaje("No hay enemigos disponibles")
            return
        
        multiplicador = 1.0 + (self.nivel_dificultad - 1) * 0.15
        
        enemigo_random = random.choice(enemigos_data)
        enemigo = Enemigo(
            enemigo_random['nombre'], 
            enemigo_random.get('zona', 'bosque'), 
            enemigo_random,
            multiplicador_dificultad=multiplicador
        )
        
        self.mostrar_pantalla_combate(enemigo)
    
    def mostrar_pantalla_combate(self, enemigo):
        """Mostrar pantalla de combate con personaje y enemigo"""
        self.limpiar_pantalla()
        self.frame_actual = ttk.Frame(self.container)
        self.frame_actual.pack(fill=BOTH, expand=True)
        
        self.enemigo_actual = enemigo
        
        frame_titulo = ttk.Frame(self.frame_actual)
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
            text=f"Nivel de Dificultad: {self.nivel_dificultad}",
            font=("Helvetica", 12, "bold"),
            bootstyle="warning"
        )
        dificultad_label.pack(pady=(5, 0))
        
        frame_combatientes = ttk.Frame(self.frame_actual)
        frame_combatientes.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        frame_personaje = ttk.Labelframe(frame_combatientes, text=self.juego.jugador.nombre, bootstyle="info")
        frame_personaje.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(
            frame_personaje,
            text=f"Clase: {self.juego.jugador.clase.title()}",
            font=("Helvetica", 12),
            bootstyle="primary"
        ).pack(pady=5)
        
        porcentaje_vida = (self.juego.jugador.vida_actual / self.juego.jugador.vida_maxima) * 100
        self.meter_vida_combate = Meter(
            frame_personaje,
            metersize=200,
            padding=15,
            amountused=porcentaje_vida,
            metertype="semi",
            subtext="VIDA",
            interactive=False,
            bootstyle="danger",
            textright=f"{self.juego.jugador.vida_actual}/{self.juego.jugador.vida_maxima}",
            stripethickness=10
        )
        self.meter_vida_combate.pack(pady=10)
        
        porcentaje_mana = (self.juego.jugador.mana_actual / self.juego.jugador.mana_maximo) * 100
        self.meter_mana_combate = Meter(
            frame_personaje,
            metersize=200,
            padding=15,
            amountused=porcentaje_mana,
            metertype="semi",
            subtext="MANA",
            interactive=False,
            bootstyle="primary",
            textright=f"{self.juego.jugador.mana_actual}/{self.juego.jugador.mana_maximo}",
            stripethickness=10
        )
        self.meter_mana_combate.pack(pady=10)
        
        frame_enemigo = ttk.Labelframe(frame_combatientes, text=enemigo.nombre, bootstyle="warning")
        frame_enemigo.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))
        
        ttk.Label(
            frame_enemigo,
            text=f"Zona: {enemigo.zona.title()}",
            font=("Helvetica", 12),
            bootstyle="warning"
        ).pack(pady=5)
        
        porcentaje_vida_enemigo = (enemigo.vida_actual / enemigo.vida_maxima) * 100
        self.meter_vida_enemigo = Meter(
            frame_enemigo,
            metersize=200,
            padding=15,
            amountused=porcentaje_vida_enemigo,
            metertype="semi",
            subtext="VIDA",
            interactive=False,
            bootstyle="danger",
            textright=f"{enemigo.vida_actual}/{enemigo.vida_maxima}",
            stripethickness=10
        )
        self.meter_vida_enemigo.pack(pady=10)
        
        frame_stats_enemigo = ttk.Frame(frame_enemigo)
        frame_stats_enemigo.pack(pady=10)
        ttk.Label(frame_stats_enemigo, text=f"Ataque: {enemigo.ataque}", bootstyle="danger").pack()
        ttk.Label(frame_stats_enemigo, text=f"Defensa: {enemigo.defensa}", bootstyle="info").pack()
        
        frame_acciones = ttk.Labelframe(self.frame_actual, text="Acciones", bootstyle="success")
        frame_acciones.pack(fill=X, padx=20, pady=10)
        
        frame_botones = ttk.Frame(frame_acciones)
        frame_botones.pack(pady=10)
        
        btn_atacar = ttk.Button(
            frame_botones,
            text="⚔️ ATACAR",
            command=self.mostrar_menu_habilidades,
            bootstyle="danger",
            width=20
        )
        btn_atacar.pack(side=LEFT, padx=5)
        
        btn_defender = ttk.Button(
            frame_botones,
            text="🛡️ DEFENDER",
            command=self.defender,
            bootstyle="info",
            width=20
        )
        btn_defender.pack(side=LEFT, padx=5)
        
        btn_objeto = ttk.Button(
            frame_botones,
            text="🧪 USAR OBJETO",
            command=self.mostrar_menu_objetos,
            bootstyle="primary",
            width=20
        )
        btn_objeto.pack(side=LEFT, padx=5)
        
        btn_volver = ttk.Button(
            frame_botones,
            text="↩️ VOLVER",
            command=self.mostrar_pantalla_principal,
            bootstyle="secondary",
            width=20
        )
        btn_volver.pack(side=LEFT, padx=5)
        
        self.frame_menu_habilidades = ttk.Labelframe(self.frame_actual, text="Selecciona una Habilidad", bootstyle="primary")
    
    def mostrar_menu_habilidades(self):
        """Mostrar menú de habilidades sin cambiar de página"""
        habilidades_data = self.juego.datos.get('habilidades', [])
        clase_jugador = self.juego.jugador.clase
        
        habilidades_disponibles = [
            hab for hab in habilidades_data 
            if hab.get('clase', '').lower() == clase_jugador.lower()
        ]
        
        if not habilidades_disponibles:
            self.mostrar_mensaje("No tienes habilidades disponibles")
            return
        
        if hasattr(self, 'frame_menu_habilidades'):
            self.frame_menu_habilidades.destroy()
        
        self.frame_menu_habilidades = ttk.Labelframe(self.frame_actual, text="Selecciona una Habilidad", bootstyle="primary")
        self.frame_menu_habilidades.pack(fill=X, padx=20, pady=10)
        
        frame_habs = ttk.Frame(self.frame_menu_habilidades)
        frame_habs.pack(pady=10)
        
        for i, habilidad in enumerate(habilidades_disponibles):
            nombre = habilidad.get('nombre', '')
            daño = habilidad.get('daño_base', '0')
            costo = habilidad.get('coste_mana', '0')
            descripcion = habilidad.get('descripcion', '')
            
            tiene_mana = self.juego.jugador.mana_actual >= int(costo)
            
            frame_hab = ttk.Frame(frame_habs)
            frame_hab.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="ew")
            
            btn_hab = ttk.Button(
                frame_hab,
                text=f"{nombre}\nDaño: {daño} | Mana: {costo}",
                command=lambda h=habilidad: self.usar_habilidad(h),
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
    
    def usar_habilidad(self, habilidad):
        """Usar una habilidad seleccionada"""
        nombre = habilidad.get('nombre', '')
        daño = int(habilidad.get('daño_base', 0))
        costo = int(habilidad.get('coste_mana', 0))
        
        if self.juego.jugador.mana_actual < costo:
            self.mostrar_mensaje("¡No tienes suficiente mana!")
            return
        
        self.juego.jugador.mana_actual -= costo
        
        if daño > 0:
            daño_real = max(1, daño + (self.juego.jugador.ataque // 2) - (self.enemigo_actual.defensa // 3))
            self.enemigo_actual.recibir_daño(daño_real)
            self.mostrar_mensaje(f"¡{nombre} causa {daño_real} de daño a {self.enemigo_actual.nombre}!")
        else:
            if "Curar" in nombre:
                curacion = 30
                self.juego.jugador.curar(curacion)
                self.mostrar_mensaje(f"¡Te curas {curacion} de vida!")
            elif "Defender" in nombre:
                self.juego.jugador.defensa += 5
                self.mostrar_mensaje(f"¡Tu defensa aumenta!")
            elif "Esquivar" in nombre:
                self.juego.jugador.velocidad += 3
                self.mostrar_mensaje(f"¡Tu velocidad aumenta!")
        
        self.actualizar_combate_ui()
        
        if hasattr(self, 'frame_menu_habilidades'):
            self.frame_menu_habilidades.destroy()
        
        if not self.enemigo_actual.esta_vivo():
            exp_ganada = self.enemigo_actual.experiencia_otorgada
            self.juego.jugador.ganar_experiencia(exp_ganada)
            
            self.juego.jugador.vida_actual = self.juego.jugador.vida_maxima
            
            self.nivel_dificultad += 1
            
            self.mostrar_mensaje(
                f"¡Victoria! Ganas {exp_ganada} de experiencia.\n"
                f"Tu vida se restaura completamente.\n"
                f"La dificultad aumenta (Nivel {self.nivel_dificultad})"
            )
            self.mostrar_pantalla_principal()
            return
        
        self.turno_enemigo()
    
    def defender(self):
        """Acción de defender"""
        self.juego.jugador.defensa += 3
        self.mostrar_mensaje("¡Te defiendes! Tu defensa aumenta temporalmente")
        
        self.actualizar_combate_ui()
        
        self.turno_enemigo()
    
    def turno_enemigo(self):
        """Turno del enemigo: usa habilidad aleatoria"""
        if not hasattr(self, 'enemigo_actual') or not self.enemigo_actual.esta_vivo():
            return
        
        if not self.juego.jugador.esta_vivo():
            self.mostrar_mensaje("¡Has sido derrotado! Tu personaje ha sido curado automáticamente.")
            self.juego.jugador.vida_actual = self.juego.jugador.vida_maxima
            self.actualizar_combate_ui()
            return
        
        resultado = self.enemigo_actual.usar_habilidad_aleatoria(self.juego.jugador)
        
        mensaje = f"¡{self.enemigo_actual.nombre} usa {resultado['nombre']} y causa {resultado['daño']} de daño!"
        self.mostrar_mensaje(mensaje)
        
        self.actualizar_combate_ui()
        
        if not self.juego.jugador.esta_vivo():
            self.mostrar_mensaje("¡Has sido derrotado! Tu personaje ha sido curado automáticamente.")
            self.juego.jugador.vida_actual = self.juego.jugador.vida_maxima
            self.actualizar_combate_ui()
    
    def mostrar_menu_objetos(self):
        """Mostrar menú de objetos del inventario"""
        inventario = self.juego.jugador.inventario
        
        objetos_consumibles = {
            nombre: datos 
            for nombre, datos in inventario.items() 
            if datos.get('tipo') == 'consumible' and datos.get('cantidad', 0) > 0
        }
        
        if not objetos_consumibles:
            self.mostrar_mensaje("No tienes objetos consumibles en tu inventario")
            return
        
        if hasattr(self, 'frame_menu_objetos'):
            self.frame_menu_objetos.destroy()
        
        self.frame_menu_objetos = ttk.Labelframe(self.frame_actual, text="Selecciona un Objeto", bootstyle="primary")
        self.frame_menu_objetos.pack(fill=X, padx=20, pady=10)
        
        frame_objs = ttk.Frame(self.frame_menu_objetos)
        frame_objs.pack(pady=10)
        
        for i, (nombre, datos) in enumerate(objetos_consumibles.items()):
            cantidad = datos.get('cantidad', 0)
            mana = datos.get('mana', 0)
            
            frame_obj = ttk.Frame(frame_objs)
            frame_obj.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="ew")
            
            btn_obj = ttk.Button(
                frame_obj,
                text=f"{nombre}\nMana: +{mana} | Cantidad: {cantidad}",
                command=lambda n=nombre: self.usar_objeto(n),
                bootstyle="primary",
                width=20
            )
            btn_obj.pack()
        
        frame_objs.columnconfigure(0, weight=1)
        frame_objs.columnconfigure(1, weight=1)
    
    def usar_objeto(self, nombre_objeto):
        """Usar un objeto del inventario"""
        inventario = self.juego.jugador.inventario
        
        if nombre_objeto not in inventario:
            self.mostrar_mensaje("¡Objeto no encontrado!")
            return
        
        objeto = inventario[nombre_objeto]
        
        if objeto.get('cantidad', 0) <= 0:
            self.mostrar_mensaje("¡No tienes más de este objeto!")
            return
        
        objeto['cantidad'] -= 1
        
        if objeto.get('tipo') == 'consumible':
            mana_recuperado = objeto.get('mana', 0)
            if mana_recuperado > 0:
                mana_antes = self.juego.jugador.mana_actual
                self.juego.jugador.mana_actual = min(
                    self.juego.jugador.mana_maximo,
                    self.juego.jugador.mana_actual + mana_recuperado
                )
                mana_real = self.juego.jugador.mana_actual - mana_antes
                self.mostrar_mensaje(f"¡Usas {nombre_objeto} y recuperas {mana_real} de mana!")
        
        if objeto['cantidad'] <= 0:
            del inventario[nombre_objeto]
        
        self.actualizar_combate_ui()
        
        if hasattr(self, 'frame_menu_objetos'):
            self.frame_menu_objetos.destroy()
    
    def actualizar_combate_ui(self):
        """Actualizar la interfaz de combate"""
        if not hasattr(self, 'enemigo_actual'):
            return
        
        porcentaje_vida = (self.juego.jugador.vida_actual / self.juego.jugador.vida_maxima) * 100
        self.meter_vida_combate.configure(
            amountused=porcentaje_vida,
            textright=f"{self.juego.jugador.vida_actual}/{self.juego.jugador.vida_maxima}"
        )
        
        porcentaje_mana = (self.juego.jugador.mana_actual / self.juego.jugador.mana_maximo) * 100
        self.meter_mana_combate.configure(
            amountused=porcentaje_mana,
            textright=f"{self.juego.jugador.mana_actual}/{self.juego.jugador.mana_maximo}"
        )
        
        porcentaje_vida_enemigo = (self.enemigo_actual.vida_actual / self.enemigo_actual.vida_maxima) * 100
        self.meter_vida_enemigo.configure(
            amountused=porcentaje_vida_enemigo,
            textright=f"{self.enemigo_actual.vida_actual}/{self.enemigo_actual.vida_maxima}"
        )
    
    def ir_a_inventario(self):
        """Cambiar a la pestaña de inventario"""
        if hasattr(self, 'notebook'):
            self.notebook.select(3)
    
    def salir_del_juego(self):
        """Salir del juego"""
        self.juego.salir()
    
    def iniciar_combate(self):
        """Iniciar un combate con el enemigo seleccionado"""
        nombre_enemigo = self.combo_enemigos.get()
        if not nombre_enemigo:
            self.mostrar_mensaje("¡Selecciona un enemigo!")
            return
        
        from modules.enemigo import Enemigo
        enemigo = Enemigo(nombre_enemigo)
        
        self.texto_log.configure(state="normal")
        self.texto_log.delete(1.0, "end")
        
        resultado = self.juego.sistema_combate.iniciar_combate(self.juego.jugador, enemigo)
        
        for mensaje in self.juego.sistema_combate.log:
            self.texto_log.insert("end", mensaje + "\n")
        
        self.texto_log.configure(state="disabled")
        self.texto_log.see("end")
        
        self.actualizar_estado_personaje()
        
        if resultado:
            self.mostrar_mensaje("¡Victoria! Revisa tu experiencia ganada.")
        else:
            self.mostrar_mensaje("¡Derrota! Tu personaje ha sido curado automáticamente.")
            self.juego.jugador.vida_actual = self.juego.jugador.vida_maxima
            self.actualizar_estado_personaje()
    
    def ejecutar_accion_combate(self, accion):
        """Ejecutar una acción en el combate (placeholder)"""
        self.mostrar_mensaje(f"Acción: {accion} - En desarrollo")
    
    def mostrar_mensaje(self, mensaje):
        """Mostrar un mensaje emergente"""
        ttk.dialogs.Messagebox.show_info(
            title="Información",
            message=mensaje,
            parent=self.root
        )