
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

# ==========================================================
# CONFIGURACION DE LA VENTANA PRINCIPAL
# ==========================================================

VENTANA = tk.Tk()
VENTANA.title("Graficador de Curvas Matematicas 3D")
VENTANA.geometry("1250x780")
VENTANA.minsize(1000, 650)

estilo = ttk.Style()
estilo.theme_use("clam")

estilo.configure(
    "TNotebook.Tab",
    font=("Arial", 11, "bold"),
    padding=[15, 8]
)

estilo.configure(
    "TButton",
    font=("Arial", 10, "bold"),
    padding=6
)

estilo.configure(
    "Titulo.TLabel",
    font=("Arial", 16, "bold")
)

# ==========================================================
# FUNCIONES GENERALES
# ==========================================================

def crear_entrada(parent, texto, valor="0"):

    marco = ttk.Frame(parent)
    marco.pack(fill="x", padx=8, pady=4)

    ttk.Label(
        marco,
        text=texto,
        width=22
    ).pack(side="left")

    entrada = ttk.Entry(marco, width=13)
    entrada.pack(side="left")

    entrada.insert(0, str(valor))

    return entrada


def obtener_valor(entrada):
    return float(entrada.get())


def mostrar_error(error):

    messagebox.showerror(
        "Error en los parametros",
        f"Verifica los datos ingresados.\n\n{error}"
    )


def configurar_grafica_3d(ax, titulo):

    ax.clear()

    ax.set_title(
        titulo,
        fontsize=13,
        fontweight="bold"
    )

    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")
    ax.set_zlabel("Eje Z")

    ax.grid(True)

    ax.set_box_aspect((1, 1, 1))

    ax.view_init(
        elev=25,
        azim=-55
    )


def actualizar_grafica(fig, canvas):

    fig.tight_layout()
    canvas.draw()


def configurar_limites_3d(ax, puntos):

    """
    Establece limites iguales para los tres ejes,
    evitando deformaciones visuales.
    """

    puntos = np.asarray(puntos)

    minimo = np.min(puntos, axis=0)
    maximo = np.max(puntos, axis=0)

    centro = (minimo + maximo) / 2

    rango = np.max(maximo - minimo)

    if rango < 1:
        rango = 1

    margen = rango * 0.65

    ax.set_xlim(
        centro[0] - margen,
        centro[0] + margen
    )

    ax.set_ylim(
        centro[1] - margen,
        centro[1] + margen
    )

    ax.set_zlim(
        centro[2] - margen,
        centro[2] + margen
    )

    ax.set_box_aspect((1, 1, 1))


# ==========================================================
# ENCABEZADO
# ==========================================================

ttk.Label(
    VENTANA,
    text="GRAFICADOR DE CURVAS MATEMATICAS EN 3D",
    style="Titulo.TLabel"
).pack(pady=12)

ttk.Label(
    VENTANA,
    text="Circunferencia | Elipse | Recta tridimensional"
).pack(pady=3)


# ==========================================================
# CREACION DE LAS TRES PESTAÑAS
# ==========================================================

pestanas = ttk.Notebook(VENTANA)

pestanas.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

tab_circunferencia = ttk.Frame(pestanas)
tab_elipse = ttk.Frame(pestanas)
tab_recta = ttk.Frame(pestanas)

pestanas.add(
    tab_circunferencia,
    text="1. Circunferencia 3D"
)

pestanas.add(
    tab_elipse,
    text="2. Elipse 3D"
)

pestanas.add(
    tab_recta,
    text="3. Recta 3D"
)


# ==========================================================
# 1. CIRCUNFERENCIA EN 3D
# ==========================================================

ttk.Label(
    tab_circunferencia,
    text="GRAFICA DE UNA CIRCUNFERENCIA EN 3D",
    style="Titulo.TLabel"
).pack(pady=10)

marco_circulo = ttk.Frame(tab_circunferencia)

marco_circulo.pack(
    fill="both",
    expand=True
)

panel_circulo = ttk.LabelFrame(
    marco_circulo,
    text="Parametros de la circunferencia"
)

panel_circulo.pack(
    side="left",
    fill="y",
    padx=10,
    pady=10
)

# Entradas del centro y radio

c_x = crear_entrada(
    panel_circulo,
    "Centro X",
    0
)

c_y = crear_entrada(
    panel_circulo,
    "Centro Y",
    0
)

c_z = crear_entrada(
    panel_circulo,
    "Centro Z",
    0
)

c_r = crear_entrada(
    panel_circulo,
    "Radio",
    5
)

ttk.Label(
    panel_circulo,
    text="Plano de la circunferencia:"
).pack(anchor="w", padx=8, pady=(12, 3))

plano_circulo = ttk.Combobox(
    panel_circulo,
    values=["XY", "XZ", "YZ"],
    state="readonly",
    width=15
)

plano_circulo.set("XY")
plano_circulo.pack(padx=8, pady=5)

ttk.Label(
    panel_circulo,
    text="Ecuacion:"
).pack(pady=(12, 2))

ttk.Label(
    panel_circulo,
    text="(x-h)² + (y-k)² = r²",
    font=("Arial", 10, "bold")
).pack(pady=5)

# Figura tridimensional

fig_circulo = Figure(
    figsize=(8, 6),
    dpi=100
)

ax_circulo = fig_circulo.add_subplot(
    111,
    projection="3d"
)

canvas_circulo = FigureCanvasTkAgg(
    fig_circulo,
    master=marco_circulo
)

canvas_circulo.get_tk_widget().pack(
    side="right",
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

toolbar_circulo = NavigationToolbar2Tk(
    canvas_circulo,
    marco_circulo,
    pack_toolbar=False
)

toolbar_circulo.update()
toolbar_circulo.pack(side="bottom", fill="x")


def graficar_circunferencia_3d():

    try:

        h = obtener_valor(c_x)
        k = obtener_valor(c_y)
        z0 = obtener_valor(c_z)
        r = obtener_valor(c_r)

        plano = plano_circulo.get()

        if r <= 0:
            raise ValueError(
                "El radio debe ser mayor que cero."
            )

        t = np.linspace(
            0,
            2 * np.pi,
            500
        )

        # Calculo de coordenadas segun el plano

        if plano == "XY":

            x = h + r * np.cos(t)
            y = k + r * np.sin(t)
            z = np.full_like(t, z0)

        elif plano == "XZ":

            x = h + r * np.cos(t)
            y = np.full_like(t, k)
            z = z0 + r * np.sin(t)

        else:  # Plano YZ

            x = np.full_like(t, h)
            y = k + r * np.cos(t)
            z = z0 + r * np.sin(t)

        configurar_grafica_3d(
            ax_circulo,
            "CIRCUNFERENCIA TRIDIMENSIONAL"
        )

        ax_circulo.plot(
            x,
            y,
            z,
            linewidth=2.8,
            label="Circunferencia"
        )

        ax_circulo.scatter(
            h,
            k,
            z0,
            color="red",
            s=65,
            label="Centro"
        )

        ax_circulo.legend()

        configurar_limites_3d(
            ax_circulo,
            np.column_stack((x, y, z))
        )

        actualizar_grafica(
            fig_circulo,
            canvas_circulo
        )

    except Exception as error:
        mostrar_error(error)


def limpiar_circunferencia():

    for entrada, valor in [
        (c_x, 0),
        (c_y, 0),
        (c_z, 0),
        (c_r, 5)
    ]:

        entrada.delete(0, tk.END)
        entrada.insert(0, str(valor))

    plano_circulo.set("XY")

    ax_circulo.clear()
    canvas_circulo.draw()


ttk.Button(
    panel_circulo,
    text="Graficar circunferencia 3D",
    command=graficar_circunferencia_3d
).pack(fill="x", padx=8, pady=(15, 5))

ttk.Button(
    panel_circulo,
    text="Limpiar grafica",
    command=limpiar_circunferencia
).pack(fill="x", padx=8, pady=5)


# ==========================================================
# 2. ELIPSE EN 3D
# ==========================================================

ttk.Label(
    tab_elipse,
    text="GRAFICA DE UNA ELIPSE EN 3D",
    style="Titulo.TLabel"
).pack(pady=10)

marco_elipse = ttk.Frame(tab_elipse)

marco_elipse.pack(
    fill="both",
    expand=True
)

panel_elipse = ttk.LabelFrame(
    marco_elipse,
    text="Parametros de la elipse"
)

panel_elipse.pack(
    side="left",
    fill="y",
    padx=10,
    pady=10
)

# Centro

e_x = crear_entrada(
    panel_elipse,
    "Centro X",
    0
)

e_y = crear_entrada(
    panel_elipse,
    "Centro Y",
    0
)

e_z = crear_entrada(
    panel_elipse,
    "Centro Z",
    0
)

# Semiejes

e_a = crear_entrada(
    panel_elipse,
    "Semieje mayor (a)",
    6
)

e_b = crear_entrada(
    panel_elipse,
    "Semieje menor (b)",
    3
)

ttk.Label(
    panel_elipse,
    text="Plano de la elipse:"
).pack(anchor="w", padx=8, pady=(12, 3))

plano_elipse = ttk.Combobox(
    panel_elipse,
    values=["XY", "XZ", "YZ"],
    state="readonly",
    width=15
)

plano_elipse.set("XY")
plano_elipse.pack(padx=8, pady=5)

ttk.Label(
    panel_elipse,
    text="Ecuacion:"
).pack(pady=(12, 2))

ttk.Label(
    panel_elipse,
    text="(x-h)²/a² + (y-k)²/b² = 1",
    font=("Arial", 10, "bold")
).pack(pady=5)

# Figura tridimensional

fig_elipse = Figure(
    figsize=(8, 6),
    dpi=100
)

ax_elipse = fig_elipse.add_subplot(
    111,
    projection="3d"
)

canvas_elipse = FigureCanvasTkAgg(
    fig_elipse,
    master=marco_elipse
)

canvas_elipse.get_tk_widget().pack(
    side="right",
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

toolbar_elipse = NavigationToolbar2Tk(
    canvas_elipse,
    marco_elipse,
    pack_toolbar=False
)

toolbar_elipse.update()
toolbar_elipse.pack(side="bottom", fill="x")


def graficar_elipse_3d():

    try:

        h = obtener_valor(e_x)
        k = obtener_valor(e_y)
        z0 = obtener_valor(e_z)

        a = obtener_valor(e_a)
        b = obtener_valor(e_b)

        plano = plano_elipse.get()

        if a <= 0 or b <= 0:
            raise ValueError(
                "Los semiejes deben ser positivos."
            )

        if a < b:
            raise ValueError(
                "El semieje mayor debe ser mayor o igual "
                "al semieje menor."
            )

        t = np.linspace(
            0,
            2 * np.pi,
            500
        )

        # Coordenadas segun el plano elegido

        if plano == "XY":

            x = h + a * np.cos(t)
            y = k + b * np.sin(t)
            z = np.full_like(t, z0)

        elif plano == "XZ":

            x = h + a * np.cos(t)
            y = np.full_like(t, k)
            z = z0 + b * np.sin(t)

        else:  # Plano YZ

            x = np.full_like(t, h)
            y = k + a * np.cos(t)
            z = z0 + b * np.sin(t)

        configurar_grafica_3d(
            ax_elipse,
            "ELIPSE TRIDIMENSIONAL"
        )

        ax_elipse.plot(
            x,
            y,
            z,
            linewidth=2.8,
            label="Elipse"
        )

        ax_elipse.scatter(
            h,
            k,
            z0,
            color="red",
            s=65,
            label="Centro"
        )

        ax_elipse.legend()

        configurar_limites_3d(
            ax_elipse,
            np.column_stack((x, y, z))
        )

        actualizar_grafica(
            fig_elipse,
            canvas_elipse
        )

    except Exception as error:
        mostrar_error(error)


def limpiar_elipse():

    for entrada, valor in [
        (e_x, 0),
        (e_y, 0),
        (e_z, 0),
        (e_a, 6),
        (e_b, 3)
    ]:

        entrada.delete(0, tk.END)
        entrada.insert(0, str(valor))

    plano_elipse.set("XY")

    ax_elipse.clear()
    canvas_elipse.draw()


ttk.Button(
    panel_elipse,
    text="Graficar elipse 3D",
    command=graficar_elipse_3d
).pack(fill="x", padx=8, pady=(15, 5))

ttk.Button(
    panel_elipse,
    text="Limpiar grafica",
    command=limpiar_elipse
).pack(fill="x", padx=8, pady=5)


# ==========================================================
# 3. RECTA EN 3D
# ==========================================================

ttk.Label(
    tab_recta,
    text="GRAFICA DE UNA RECTA EN 3D",
    style="Titulo.TLabel"
).pack(pady=10)

marco_recta = ttk.Frame(tab_recta)

marco_recta.pack(
    fill="both",
    expand=True
)

panel_recta = ttk.LabelFrame(
    marco_recta,
    text="Parametros de la recta"
)

panel_recta.pack(
    side="left",
    fill="y",
    padx=10,
    pady=10
)

ttk.Label(
    panel_recta,
    text="Punto inicial (P):",
    font=("Arial", 10, "bold")
).pack(anchor="w", padx=8, pady=8)

# Punto inicial

r_x = crear_entrada(
    panel_recta,
    "Coordenada X",
    0
)

r_y = crear_entrada(
    panel_recta,
    "Coordenada Y",
    0
)

r_z = crear_entrada(
    panel_recta,
    "Coordenada Z",
    0
)

ttk.Label(
    panel_recta,
    text="Vector de direccion (V):",
    font=("Arial", 10, "bold")
).pack(anchor="w", padx=8, pady=8)

# Vector director

r_dx = crear_entrada(
    panel_recta,
    "Direccion X",
    1
)

r_dy = crear_entrada(
    panel_recta,
    "Direccion Y",
    2
)

r_dz = crear_entrada(
    panel_recta,
    "Direccion Z",
    1
)

ttk.Label(
    panel_recta,
    text="Intervalo del parametro t:"
).pack(anchor="w", padx=8, pady=(12, 3))

r_tmin = crear_entrada(
    panel_recta,
    "Valor minimo de t",
    -10
)

r_tmax = crear_entrada(
    panel_recta,
    "Valor maximo de t",
    10
)

ttk.Label(
    panel_recta,
    text="Ecuaciones parametricas:",
    font=("Arial", 10, "bold")
).pack(pady=(12, 2))

ttk.Label(
    panel_recta,
    text="x = x0 + at\n"
         "y = y0 + bt\n"
         "z = z0 + ct",
    font=("Arial", 10)
).pack(pady=5)

# Figura tridimensional

fig_recta = Figure(
    figsize=(8, 6),
    dpi=100
)

ax_recta = fig_recta.add_subplot(
    111,
    projection="3d"
)

canvas_recta = FigureCanvasTkAgg(
    fig_recta,
    master=marco_recta
)

canvas_recta.get_tk_widget().pack(
    side="right",
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

toolbar_recta = NavigationToolbar2Tk(
    canvas_recta,
    marco_recta,
    pack_toolbar=False
)

toolbar_recta.update()
toolbar_recta.pack(side="bottom", fill="x")


def graficar_recta_3d():

    try:

        # Punto inicial

        x0 = obtener_valor(r_x)
        y0 = obtener_valor(r_y)
        z0 = obtener_valor(r_z)

        # Vector de direccion

        dx = obtener_valor(r_dx)
        dy = obtener_valor(r_dy)
        dz = obtener_valor(r_dz)

        # Intervalo del parametro

        t_min = obtener_valor(r_tmin)
        t_max = obtener_valor(r_tmax)

        if dx == 0 and dy == 0 and dz == 0:

            raise ValueError(
                "El vector de direccion no puede ser cero."
            )

        if t_min >= t_max:

            raise ValueError(
                "El valor maximo de t debe ser mayor "
                "que el minimo."
            )

        t = np.linspace(
            t_min,
            t_max,
            500
        )

        # Ecuaciones parametricas

        x = x0 + dx * t
        y = y0 + dy * t
        z = z0 + dz * t

        configurar_grafica_3d(
            ax_recta,
            "RECTA TRIDIMENSIONAL"
        )

        ax_recta.plot(
            x,
            y,
            z,
            linewidth=2.8,
            label="Recta"
        )

        ax_recta.scatter(
            x0,
            y0,
            z0,
            color="red",
            s=70,
            label="Punto inicial"
        )

        # Mostrar vector director

        ax_recta.quiver(
            x0,
            y0,
            z0,
            dx,
            dy,
            dz,
            color="green",
            length=1,
            normalize=False,
            label="Vector director"
        )

        ax_recta.legend()

        configurar_limites_3d(
            ax_recta,
            np.column_stack((x, y, z))
        )

        actualizar_grafica(
            fig_recta,
            canvas_recta
        )

    except Exception as error:
        mostrar_error(error)


def limpiar_recta():

    for entrada, valor in [
        (r_x, 0),
        (r_y, 0),
        (r_z, 0),
        (r_dx, 1),
        (r_dy, 2),
        (r_dz, 1),
        (r_tmin, -10),
        (r_tmax, 10)
    ]:

        entrada.delete(0, tk.END)
        entrada.insert(0, str(valor))

    ax_recta.clear()
    canvas_recta.draw()


ttk.Button(
    panel_recta,
    text="Graficar recta 3D",
    command=graficar_recta_3d
).pack(fill="x", padx=8, pady=(15, 5))

ttk.Button(
    panel_recta,
    text="Limpiar grafica",
    command=limpiar_recta
).pack(fill="x", padx=8, pady=5)


# ==========================================================
# INICIAR APLICACION
# ==========================================================

VENTANA.mainloop()
