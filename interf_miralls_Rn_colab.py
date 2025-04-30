# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 11:20:33 2025

@author: polji
"""

import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interactive, FloatSlider
from IPython.display import display

screen_size = 0.1    # pantalla 10 cm x 10 cm  
res = 1000           # 1000 x 1000 píxels
long_ona = 500e-9    # longitud d'ona (color verd)
dist_lent = 0.5      # distància de la lent expansora
default_mirror_diff = 0  # diferència de distància entre els braços (m)
default_angle = 0    # Angle o deformació inicial
default_potencia = 1    # Potència per defecte, variable més tard

# Pantalla
x = np.linspace(-screen_size/2, screen_size/2, res)
X, Y = np.meshgrid(x, x)
R = np.sqrt(X**2 + Y**2)

def calcul_intensitat(mirror_diff, escala, potencia):
    # Diferència de camí òptic  
    point_source_dco = -R**2/(2*dist_lent*1e3)
    
    # Els factors d'escala estan posats perquè la deformació sigui aproximadament equivalent en totes les potències de R
    factors_escala = {
        1.0: 1e-3,     # angle en mrad pel con
        1.5: 5e-2,     # intermig
        2.0: 1e-1,     # 1/m pel paraboloide
        2.5: 1e0,      # intermig
        3.0: 1e1,      # 1/m² pel cúbic
        3.5: 1e2,      # intermig
        4.0: 1e3       # 1/m³ pel quàrtic
    }
    escala_ajustada = escala * factors_escala[potencia]
    mirror_dco = -2 * R**potencia * escala_ajustada
    
    # Dco total
    dco = mirror_diff + point_source_dco + mirror_dco
    
    # Convertim dco a fase
    fase = 2 * np.pi * dco / long_ona
    
    # Calculem la intensitat, assumint llum perfectament monocromàtica, |g|=1
    return 0.5 * (1 + np.cos(fase))

def plot_interferometer(mirror_diff_um, escala, potencia):
    """
    Main plotting function that will be called by the interactive widget
    mirror_diff_um: mirror difference in micrometers
    escala: deformation scale
    potencia: power of R
    """
    mirror_diff = mirror_diff_um * 1e-6  # Convert µm to m
    
    # Create figure
    fig = plt.figure(figsize=(12, 8))
    gs = plt.GridSpec(1, 2, width_ratios=[3, 1])
    ax = fig.add_subplot(gs[0])
    text_ax = fig.add_subplot(gs[1])
    text_ax.axis('off')
    
    # Calculate and plot intensity
    new_intensitat = calcul_intensitat(mirror_diff, escala, potencia)
    img = ax.imshow(new_intensitat,
                   extent=[-screen_size/2, screen_size/2, -screen_size/2, screen_size/2],
                   cmap='gray', vmin=0, vmax=1)
    
    # Set title based on shape
    shape_names = {
        1.0: "Con",
        1.5: "R^1.5",
        2.0: "Paraboloide",
        2.5: "R^2.5",
        3.0: "Cúbic",
        3.5: "R^3.5",
        4.0: "Quàrtic"
    }
    ax.set_title(f'Interferòmetre de Michelson: mirall {shape_names.get(potencia, f"R^{potencia}")}')
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    plt.colorbar(img, ax=ax, label='intensitat')
    
    # Add units information to text area
    if potencia == int(potencia):
        units = {1: "mrad", 2: "1/m", 3: "1/m²", 4: "1/m³"}
        unit = units.get(int(potencia), f"1/m^{int(potencia)-1}")
    else:
        unit = f"1/m^{potencia-1}"
    
    text = f"Deformació actual: {escala:.3f} {unit}\n"
    text += f"Diferència miralls: {mirror_diff_um:.2f} µm\n"
    text += f"Potència de R: {potencia:.1f}"
    text_ax.text(0.1, 0.7, text, transform=text_ax.transAxes, verticalalignment='top')
    
    plt.tight_layout()
    plt.show()

# Create interactive widget
widget = interactive(
    plot_interferometer,
    mirror_diff_um=FloatSlider(min=-2, max=2, step=0.1, value=0, description='Δd (µm)'),
    escala=FloatSlider(min=0, max=1, step=0.001, value=0, description='Deformació'),
    potencia=FloatSlider(min=1, max=4, step=0.5, value=1, description='Potència R')
)

# Display the widget
display(widget)