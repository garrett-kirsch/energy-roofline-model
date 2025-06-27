#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------- curve ----------
def draw_energy_efficiency():
    e_p  = e_p_var.get()
    e_m  = e_m_var.get()
    p_0  = p_0_var.get()
    t_s  = t_s_var.get()

    # Energy Efficiency -> EE_s
    x = np.linspace(1e-6, 50, 1000)          # OI axis (flop / byte)
    y_EE_s = 1 / (e_p + (e_m / x) + (p_0 / t_s ))  # efficiency (1/pJ)

    ax.clear()
    ax.plot(x, y_EE_s, label="Energy efficiency")

    # Esenv
    y_E_senv = np.minimum(1 / e_p, x / e_m)
    ax.plot(x, y_E_senv, label="E_senv")

    ax.set_xlabel("Operational Intensity (flop / byte)")
    ax.set_ylabel("Energy Efficiency (flop / joule)")
    ax.grid(True)
    ax.legend()
    canvas.draw_idle()

# ---------- Tk / Matplotlib boilerplate ----------
root = tk.Tk()
root.title("Energy Roofline Model")

fig = Figure(figsize=(6, 4), dpi=100)
ax  = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# parameters
e_p_var = tk.DoubleVar(value=1.0)   # pJ per flop
e_m_var = tk.DoubleVar(value=10.0)  # pJ per byte
p_0_var = tk.DoubleVar(value=200.0) # background power → pJ/sec
t_s_var = tk.DoubleVar(value=10)   # peak FLOP/s

def add_control(row, label, var, frm, to_):
    ttk.Label(root, text=label).grid(row=row, column=0, sticky="e")
    slider = ttk.Scale(root, from_=frm, to=to_, variable=var,
                       orient="horizontal", command=lambda _=None: draw_energy_efficiency())
    slider.grid(row=row, column=1, sticky="ew", padx=5)
    entry = ttk.Entry(root, textvariable=var, width=10)
    entry.grid(row=row, column=2, padx=5)
    entry.bind("<Return>", lambda *_: draw_energy_efficiency())

root.columnconfigure(1, weight=1)
add_control(1, "εₚ  (pJ / flop)",  e_p_var,  1, 50)
add_control(2, "εₘ  (pJ / byte)",  e_m_var,  1,   200)
add_control(3, "P₀   (pW)",        p_0_var,  10,  1000)
add_control(4, "Tₛ   (GFLOP/s)",   t_s_var,  1,  1000)

draw_energy_efficiency()
root.mainloop()
