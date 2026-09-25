import tkinter as tk
from tkinter import ttk, messagebox


# ==========================================
# MEMORIA PRINCIPAL
# ==========================================

datos = [
    {"nombre": "Ana", "edad": 28, "ciudad": "Bogotá"},
    {"nombre": "Luis", "edad": 34, "ciudad": "Cali"},
    {"nombre": "Marta", "edad": 22, "ciudad": "Bogotá"},
    {"nombre": "Carlos", "edad": 40, "ciudad": "Medellín"}
]


# ==========================================
# CONFIGURACION DE LA CACHE
# ==========================================

TAMANO_CACHE = 3

cache = []

hits = 0
misses = 0


# ==========================================
# BUSCAR EN MEMORIA PRINCIPAL
# ==========================================

def buscar_en_memoria(tipo, valor):

    resultado = []

    for persona in datos:

        if tipo == "Nombre":

            if persona["nombre"].lower() == valor.lower():
                resultado.append(persona)

        elif tipo == "Ciudad":

            if persona["ciudad"].lower() == valor.lower():
                resultado.append(persona)

        elif tipo == "Edad":

            if persona["edad"] == int(valor):
                resultado.append(persona)

    return resultado


# ==========================================
# BUSCAR EN CACHE
# ==========================================

def buscar_en_cache(tipo, valor):

    for elemento in cache:

        if (
            elemento["tipo"] == tipo
            and elemento["valor"].lower() == valor.lower()
        ):

            return elemento["resultado"]

    return None


# ==========================================
# AGREGAR A CACHE
# ==========================================

def agregar_a_cache(tipo, valor, resultado):

    # Si ya existe, no duplicarlo
    for elemento in cache:

        if (
            elemento["tipo"] == tipo
            and elemento["valor"].lower() == valor.lower()
        ):

            return

    # Si está llena, elimina el más antiguo
    if len(cache) >= TAMANO_CACHE:

        cache.pop(0)

    cache.append({
        "tipo": tipo,
        "valor": valor,
        "resultado": resultado
    })


# ==========================================
# MOSTRAR RESULTADOS
# ==========================================

def mostrar_resultados(resultado):

    # Limpiar tabla
    for item in tabla_resultados.get_children():

        tabla_resultados.delete(item)

    # Insertar resultados
    for persona in resultado:

        tabla_resultados.insert(
            "",
            "end",
            values=(
                persona["nombre"],
                persona["edad"],
                persona["ciudad"]
            )
        )


# ==========================================
# ACTUALIZAR CACHE VISUAL
# ==========================================

def actualizar_cache_visual():

    for item in tabla_cache.get_children():

        tabla_cache.delete(item)

    for posicion, elemento in enumerate(cache, start=1):

        tabla_cache.insert(
            "",
            "end",
            values=(
                posicion,
                elemento["tipo"],
                elemento["valor"],
                len(elemento["resultado"])
            )
        )


# ==========================================
# ACTUALIZAR ESTADISTICAS
# ==========================================

def actualizar_estadisticas():

    total = hits + misses

    if total > 0:

        efectividad = (hits / total) * 100

    else:

        efectividad = 0

    label_hits.config(
        text=f"HITS: {hits}"
    )

    label_misses.config(
        text=f"MISSES: {misses}"
    )

    label_efectividad.config(
        text=f"Efectividad: {efectividad:.1f}%"
    )


# ==========================================
# REALIZAR BUSQUEDA
# ==========================================

def realizar_busqueda():

    global hits, misses

    tipo = combo_tipo.get()

    valor = entrada_busqueda.get().strip()

    # Validar búsqueda vacía
    if valor == "":

        messagebox.showwarning(
            "Campo vacío",
            "Escribe un valor para buscar."
        )

        return

    # Validar edad
    if tipo == "Edad":

        if not valor.isdigit():

            messagebox.showerror(
                "Edad inválida",
                "Para buscar por edad debes escribir un número."
            )

            return

    # ======================================
    # BUSCAR EN CACHE
    # ======================================

    resultado = buscar_en_cache(tipo, valor)

    # ======================================
    # CACHE HIT
    # ======================================

    if resultado is not None:

        hits += 1

        label_estado.config(
            text="CACHE HIT",
            fg="#00c853"
        )

        label_mensaje.config(
            text=f"Resultado encontrado en caché: {tipo} = {valor}"
        )

    # ======================================
    # CACHE MISS
    # ======================================

    else:

        misses += 1

        label_estado.config(
            text="CACHE MISS",
            fg="#ff1744"
        )

        label_mensaje.config(
            text=f"Buscando en memoria principal: {tipo} = {valor}"
        )

        resultado = buscar_en_memoria(
            tipo,
            valor
        )

        # Guardar resultado en caché
        agregar_a_cache(
            tipo,
            valor,
            resultado
        )

    # Mostrar resultados
    mostrar_resultados(resultado)

    # Actualizar interfaz
    actualizar_cache_visual()
    actualizar_estadisticas()

    # Mensaje si no hubo resultados
    if len(resultado) == 0:

        label_mensaje.config(
            text="No se encontraron usuarios con ese criterio."
        )


# ==========================================
# REGISTRAR USUARIO
# ==========================================

def registrar_usuario():

    nombre = entrada_nombre.get().strip()

    edad = entrada_edad.get().strip()

    ciudad = entrada_ciudad.get().strip()

    # ======================================
    # VALIDACIONES
    # ======================================

    if nombre == "" or edad == "" or ciudad == "":

        messagebox.showwarning(
            "Datos incompletos",
            "Completa nombre, edad y ciudad."
        )

        return

    if not edad.isdigit():

        messagebox.showerror(
            "Edad inválida",
            "La edad debe ser un número."
        )

        return

    edad = int(edad)

    if edad <= 0:

        messagebox.showerror(
            "Edad inválida",
            "La edad debe ser mayor que 0."
        )

        return

    # ======================================
    # AGREGAR A MEMORIA PRINCIPAL
    # ======================================

    datos.append({
        "nombre": nombre,
        "edad": edad,
        "ciudad": ciudad
    })

    messagebox.showinfo(
        "Usuario registrado",
        f"El usuario {nombre} fue registrado correctamente."
    )

    # Limpiar campos
    entrada_nombre.delete(0, tk.END)
    entrada_edad.delete(0, tk.END)
    entrada_ciudad.delete(0, tk.END)


# ==========================================
# MOSTRAR MEMORIA PRINCIPAL
# ==========================================

def mostrar_memoria():

    ventana_memoria = tk.Toplevel(ventana)

    ventana_memoria.title(
        "Memoria Principal"
    )

    ventana_memoria.geometry(
        "480x360"
    )

    ventana_memoria.configure(
        bg="#121212"
    )

    titulo = tk.Label(
        ventana_memoria,
        text="MEMORIA PRINCIPAL",
        font=("Arial", 14, "bold"),
        bg="#121212",
        fg="white"
    )

    titulo.pack(
        pady=12
    )

    tabla_memoria = ttk.Treeview(
        ventana_memoria,
        columns=(
            "nombre",
            "edad",
            "ciudad"
        ),
        show="headings",
        height=10
    )

    tabla_memoria.heading(
        "nombre",
        text="Nombre"
    )

    tabla_memoria.heading(
        "edad",
        text="Edad"
    )

    tabla_memoria.heading(
        "ciudad",
        text="Ciudad"
    )

    tabla_memoria.column(
        "nombre",
        width=150,
        anchor="center"
    )

    tabla_memoria.column(
        "edad",
        width=70,
        anchor="center"
    )

    tabla_memoria.column(
        "ciudad",
        width=150,
        anchor="center"
    )

    tabla_memoria.pack(
        padx=12,
        pady=8
    )

    for persona in datos:

        tabla_memoria.insert(
            "",
            "end",
            values=(
                persona["nombre"],
                persona["edad"],
                persona["ciudad"]
            )
        )


# ==========================================
# LIMPIAR CACHE
# ==========================================

def limpiar_cache():

    global hits, misses

    respuesta = messagebox.askyesno(
        "Limpiar caché",
        "¿Seguro que quieres eliminar toda la caché?"
    )

    if respuesta:

        cache.clear()

        hits = 0
        misses = 0

        actualizar_cache_visual()

        actualizar_estadisticas()

        for item in tabla_resultados.get_children():

            tabla_resultados.delete(item)

        label_estado.config(
            text="CACHE VACÍA",
            fg="white"
        )

        label_mensaje.config(
            text="La caché ha sido limpiada."
        )


# ==========================================
# LIMPIAR BUSQUEDA
# ==========================================

def limpiar_busqueda():

    entrada_busqueda.delete(
        0,
        tk.END
    )

    for item in tabla_resultados.get_children():

        tabla_resultados.delete(item)

    label_estado.config(
        text="LISTO",
        fg="white"
    )

    label_mensaje.config(
        text="Escribe un criterio para realizar una búsqueda."
    )


# ==========================================
# VENTANA PRINCIPAL
# ==========================================

ventana = tk.Tk()

ventana.title(
    "Simulador de Memoria Caché"
)

ventana.geometry(
    "760x620"
)

ventana.resizable(
    False,
    False
)

ventana.configure(
    bg="#121212"
)


# ==========================================
# ESTILOS
# ==========================================

estilo = ttk.Style()

estilo.theme_use(
    "clam"
)

estilo.configure(
    "Treeview",
    background="#1e1e1e",
    foreground="white",
    fieldbackground="#1e1e1e",
    rowheight=22,
    font=("Arial", 9)
)

estilo.configure(
    "Treeview.Heading",
    background="#333333",
    foreground="white",
    font=("Arial", 9, "bold")
)


# ==========================================
# TITULO
# ==========================================

titulo = tk.Label(
    ventana,
    text="SIMULADOR DE MEMORIA CACHÉ",
    font=("Arial", 17, "bold"),
    bg="#121212",
    fg="white"
)

titulo.pack(
    pady=(12, 3)
)


subtitulo = tk.Label(
    ventana,
    text="Sistema de búsqueda y almacenamiento en caché",
    font=("Arial", 9),
    bg="#121212",
    fg="#aaaaaa"
)

subtitulo.pack(
    pady=(0, 8)
)


# ==========================================
# REGISTRO DE USUARIO
# ==========================================

frame_registro = tk.LabelFrame(
    ventana,
    text=" REGISTRAR USUARIO ",
    font=("Arial", 10, "bold"),
    bg="#1e1e1e",
    fg="white",
    padx=8,
    pady=6
)

frame_registro.pack(
    padx=15,
    pady=5,
    fill="x"
)


# Nombre

tk.Label(
    frame_registro,
    text="Nombre:",
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 9, "bold")
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)


entrada_nombre = tk.Entry(
    frame_registro,
    width=14,
    font=("Arial", 9),
    bg="#333333",
    fg="white",
    insertbackground="white"
)

entrada_nombre.grid(
    row=0,
    column=1,
    padx=5
)


# Edad

tk.Label(
    frame_registro,
    text="Edad:",
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 9, "bold")
).grid(
    row=0,
    column=2,
    padx=5
)


entrada_edad = tk.Entry(
    frame_registro,
    width=6,
    font=("Arial", 9),
    bg="#333333",
    fg="white",
    insertbackground="white"
)

entrada_edad.grid(
    row=0,
    column=3,
    padx=5
)


# Ciudad

tk.Label(
    frame_registro,
    text="Ciudad:",
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 9, "bold")
).grid(
    row=0,
    column=4,
    padx=5
)


entrada_ciudad = tk.Entry(
    frame_registro,
    width=14,
    font=("Arial", 9),
    bg="#333333",
    fg="white",
    insertbackground="white"
)

entrada_ciudad.grid(
    row=0,
    column=5,
    padx=5
)


# Botón registrar

boton_registrar = tk.Button(
    frame_registro,
    text="REGISTRAR",
    command=registrar_usuario,
    font=("Arial", 9, "bold"),
    bg="#2e7d32",
    fg="white",
    relief="flat",
    padx=10,
    pady=4
)

boton_registrar.grid(
    row=0,
    column=6,
    padx=8
)


# ==========================================
# BUSCADOR
# ==========================================

frame_busqueda = tk.LabelFrame(
    ventana,
    text=" BUSCAR USUARIOS ",
    font=("Arial", 10, "bold"),
    bg="#1e1e1e",
    fg="white",
    padx=8,
    pady=6
)

frame_busqueda.pack(
    padx=15,
    pady=5,
    fill="x"
)


tk.Label(
    frame_busqueda,
    text="Buscar por:",
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 9, "bold")
).pack(
    side="left",
    padx=5
)


combo_tipo = ttk.Combobox(
    frame_busqueda,
    values=[
        "Nombre",
        "Edad",
        "Ciudad"
    ],
    state="readonly",
    width=10,
    font=("Arial", 9)
)

combo_tipo.set(
    "Ciudad"
)

combo_tipo.pack(
    side="left",
    padx=5
)


tk.Label(
    frame_busqueda,
    text="Valor:",
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 9, "bold")
).pack(
    side="left",
    padx=5
)


entrada_busqueda = tk.Entry(
    frame_busqueda,
    width=20,
    font=("Arial", 9),
    bg="#333333",
    fg="white",
    insertbackground="white"
)

entrada_busqueda.pack(
    side="left",
    padx=5
)


boton_buscar = tk.Button(
    frame_busqueda,
    text="BUSCAR",
    command=realizar_busqueda,
    font=("Arial", 9, "bold"),
    bg="#1565c0",
    fg="white",
    relief="flat",
    padx=12,
    pady=4
)

boton_buscar.pack(
    side="left",
    padx=5
)


boton_limpiar_busqueda = tk.Button(
    frame_busqueda,
    text="LIMPIAR",
    command=limpiar_busqueda,
    font=("Arial", 9, "bold"),
    bg="#424242",
    fg="white",
    relief="flat",
    padx=10,
    pady=4
)

boton_limpiar_busqueda.pack(
    side="left"
)


# ==========================================
# ESTADO
# ==========================================

frame_estado = tk.Frame(
    ventana,
    bg="#1e1e1e"
)

frame_estado.pack(
    padx=15,
    pady=5,
    fill="x"
)


label_estado = tk.Label(
    frame_estado,
    text="LISTO",
    font=("Arial", 15, "bold"),
    bg="#1e1e1e",
    fg="white"
)

label_estado.pack(
    pady=(6, 2)
)


label_mensaje = tk.Label(
    frame_estado,
    text="Selecciona un criterio y realiza una búsqueda.",
    font=("Arial", 9),
    bg="#1e1e1e",
    fg="#aaaaaa"
)

label_mensaje.pack(
    pady=(0, 6)
)


# ==========================================
# RESULTADOS
# ==========================================

tk.Label(
    ventana,
    text="RESULTADOS DE LA BÚSQUEDA",
    font=("Arial", 11, "bold"),
    bg="#121212",
    fg="white"
).pack(
    anchor="w",
    padx=15,
    pady=(5, 3)
)


tabla_resultados = ttk.Treeview(
    ventana,
    columns=(
        "nombre",
        "edad",
        "ciudad"
    ),
    show="headings",
    height=4
)


tabla_resultados.heading(
    "nombre",
    text="Nombre"
)

tabla_resultados.heading(
    "edad",
    text="Edad"
)

tabla_resultados.heading(
    "ciudad",
    text="Ciudad"
)


tabla_resultados.column(
    "nombre",
    width=200,
    anchor="center"
)

tabla_resultados.column(
    "edad",
    width=100,
    anchor="center"
)

tabla_resultados.column(
    "ciudad",
    width=200,
    anchor="center"
)


tabla_resultados.pack(
    padx=15,
    fill="x"
)


# ==========================================
# PARTE INFERIOR
# ==========================================

frame_inferior = tk.Frame(
    ventana,
    bg="#121212"
)

frame_inferior.pack(
    padx=15,
    pady=8,
    fill="x"
)


# ==========================================
# ESTADISTICAS
# ==========================================

frame_estadisticas = tk.LabelFrame(
    frame_inferior,
    text=" ESTADÍSTICAS ",
    font=("Arial", 9, "bold"),
    bg="#1e1e1e",
    fg="white"
)

frame_estadisticas.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 6)
)


label_hits = tk.Label(
    frame_estadisticas,
    text="HITS: 0",
    font=("Arial", 9, "bold"),
    bg="#1e1e1e",
    fg="#00c853"
)

label_hits.pack(
    pady=3
)


label_misses = tk.Label(
    frame_estadisticas,
    text="MISSES: 0",
    font=("Arial", 9, "bold"),
    bg="#1e1e1e",
    fg="#ff1744"
)

label_misses.pack(
    pady=3
)


label_efectividad = tk.Label(
    frame_estadisticas,
    text="Efectividad: 0.0%",
    font=("Arial", 9, "bold"),
    bg="#1e1e1e",
    fg="white"
)

label_efectividad.pack(
    pady=3
)


# ==========================================
# CACHE
# ==========================================

frame_cache = tk.LabelFrame(
    frame_inferior,
    text=" CONTENIDO DE LA CACHE ",
    font=("Arial", 9, "bold"),
    bg="#1e1e1e",
    fg="white"
)

frame_cache.pack(
    side="right",
    fill="both",
    expand=True,
    padx=(6, 0)
)


tabla_cache = ttk.Treeview(
    frame_cache,
    columns=(
        "posicion",
        "tipo",
        "valor",
        "resultados"
    ),
    show="headings",
    height=3
)


tabla_cache.heading(
    "posicion",
    text="#"
)

tabla_cache.heading(
    "tipo",
    text="Tipo"
)

tabla_cache.heading(
    "valor",
    text="Valor"
)

tabla_cache.heading(
    "resultados",
    text="Result."
)


tabla_cache.column(
    "posicion",
    width=25,
    anchor="center"
)

tabla_cache.column(
    "tipo",
    width=55,
    anchor="center"
)

tabla_cache.column(
    "valor",
    width=90,
    anchor="center"
)

tabla_cache.column(
    "resultados",
    width=55,
    anchor="center"
)


tabla_cache.pack(
    padx=6,
    pady=6
)


# ==========================================
# BOTONES FINALES
# ==========================================

frame_botones = tk.Frame(
    ventana,
    bg="#121212"
)

frame_botones.pack(
    pady=(0, 12)
)


boton_memoria = tk.Button(
    frame_botones,
    text="VER MEMORIA PRINCIPAL",
    command=mostrar_memoria,
    font=("Arial", 9, "bold"),
    bg="#6a1b9a",
    fg="white",
    relief="flat",
    padx=10,
    pady=6
)

boton_memoria.pack(
    side="left",
    padx=4
)


boton_limpiar_cache = tk.Button(
    frame_botones,
    text="LIMPIAR CACHE",
    command=limpiar_cache,
    font=("Arial", 9, "bold"),
    bg="#c62828",
    fg="white",
    relief="flat",
    padx=10,
    pady=6
)

boton_limpiar_cache.pack(
    side="left",
    padx=4
)


# ==========================================
# ENTER PARA BUSCAR
# ==========================================

entrada_busqueda.bind(
    "<Return>",
    lambda event: realizar_busqueda()
)


# ==========================================
# INICIAR PROGRAMA
# ==========================================

ventana.mainloop()
