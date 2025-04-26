"""
Created on Wed Apr 23 19:31:29 2025

@author: polji
"""

import matplotlib
matplotlib.use('Qt5Agg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

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
        1.5: 1e-2,     # intermig
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

# Creem la figura
fig = plt.figure(figsize=(12, 8))  
gs = plt.GridSpec(1, 2, width_ratios=[3, 1]) 
ax = fig.add_subplot(gs[0])  
text_ax = fig.add_subplot(gs[1])  
text_ax.axis('off') 

plt.subplots_adjust(left=0.1, bottom=0.25, right=0.9, top=0.9)  


intensitat = calcul_intensitat(default_mirror_diff, default_angle, default_potencia)
img = ax.imshow(intensitat,
               extent=[-screen_size/2, screen_size/2, -screen_size/2, screen_size/2],
               cmap='gray', vmin=0, vmax=1)
ax.set_title('Interferòmetre de Michelson: miralls radials')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
plt.colorbar(img, ax=ax, label='intensitat')

ax_slider_d = plt.axes([0.2, 0.15, 0.4, 0.03])  
ax_slider_a = plt.axes([0.2, 0.10, 0.4, 0.03])  
ax_slider_p = plt.axes([0.2, 0.05, 0.4, 0.03])  

slider_d = Slider(ax_slider_d, 'Diferència miralls Δd (µm)', -2, 2, valinit=0)
slider_a = Slider(ax_slider_a, 'Deformació (mrad)', 0, 1, valinit=0)
slider_p = Slider(ax_slider_p, 'Potència de R', 1, 4, valinit=1, valstep=0.5)

slider_d.valtext.set_text(f'{0:.2f} µm')
slider_a.valtext.set_text(f'{0:.3f}')
slider_p.valtext.set_text(f'{1:.1f}')

def update(val):
    mirror_diff = slider_d.val * 1e-6  # Convert µm to m
    escala = slider_a.val
    potencia = slider_p.val
    
    new_intensitat = calcul_intensitat(mirror_diff, escala, potencia)
    img.set_data(new_intensitat)
    
    slider_d.valtext.set_text(f'{slider_d.val:.2f} µm')
    slider_a.valtext.set_text(f'{escala:.3f}')
    slider_p.valtext.set_text(f'{potencia:.1f}')
    
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
    
    # Cada dependència en R té una unitat diferent del factor de deformació
    if potencia == int(potencia):
        units = {1: "mrad", 2: "1/m", 3: "1/m²", 4: "1/m³"}
        unit = units.get(int(potencia), f"1/m^{int(potencia)-1}")
    else:
        unit = f"1/m^{potencia-1}"
    slider_a.label.set_text(f'Deformació ({unit})')
    
    fig.canvas.draw_idle()

slider_d.on_changed(update)
slider_a.on_changed(update)
slider_p.on_changed(update)

plt.show()