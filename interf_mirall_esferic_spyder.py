# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 19:31:29 2025

@author: polji
"""

import matplotlib
matplotlib.use('Qt5Agg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Paràmetres bàsics
screen_size = 0.1    # pantalla 10 cm x 10 cm  
res = 1000           # 1000 x 1000 píxels
long_ona = 500e-9    # longitud d'ona (color verd)
dist_lent = 500    # distància de la lent expansora
default_mirror_diff = 0  # diferència de distància entre els braços (m)
default_curvature = 0    # radi de curvatura inicial

# Pantalla
x = np.linspace(-screen_size/2, screen_size/2, res)
X, Y = np.meshgrid(x, x)
R = np.sqrt(X**2 + Y**2)

def compute_intensitat(mirror_diff, radi_curv):
    # Diferència de camí òptic  
    dco = mirror_diff - R**2/(2*dist_lent)  # Font puntual (front d'ona esfèric)
                                            # El signe negatiu és el conveni escollit en aquest codi
    # Mirall corbat
    if radi_curv > 0: # per R=0 és un cas especial, en aquest codi significa un mirall pla
        dco += -R**2/(2*radi_curv)  # Mirall convex. S'afegeix un altre terme negatiu perquè els rajos 
                                           # de les puntes de la font encara recorren més distància
    # Convertim dco a fase
    fase = 2 * np.pi * dco / long_ona
    
    # Calcular intensitat, assumint font perfectament monocromàtica, és a dir, |g|=1
    return 0.5 * (1 + np.cos(fase))

def calcular_radi_curv(r1, r2):
    """
    r1: radi del primer anell brillant (m)
    r2: radi del segon anell brillant (m)
    
    Per anells consecutius m i m+1:
    r_{m+1}^2/(2R) - r_m^2/(2R) = λ
    Llavors R = (r_{m+1}^2 - r_m^2)/(2λ)
    """
    if r1 is None or r2 is None or r1 >= r2: # per assegurar que no troba anells falsos 
        return None
        
    dr2 = r2*r2 - r1*r1
    R = dr2/(2*long_ona)
    
    if R > 0:
        return R
    return None

def trobar_anells(intensitat): # ens busca els 2 primers anells consecutius més brillants aproximadament
    # Fem servir el perfil d'un dels costats
    perfil = intensitat[res//2, res//2:]
    
    # Trobem els màxims locals
    maxims_posicions = []
    maxims_valors = []
    
    for i in range(1, len(perfil)-1):
        if perfil[i] > perfil[i-1] and perfil[i] > perfil[i+1]: 
            # Mirem que sigui un pic notable, per evitar pics falsos
            if perfil[i] > 0.7:  #per evitar pics falsos
                maxims_posicions.append(i)
                maxims_valors.append(perfil[i])
    
    if len(maxims_posicions) >= 2:
        # Ordenem els pics per posició
        ordenacio_indexs = np.argsort(maxims_posicions)
        ordenacio_posicions = np.array(maxims_posicions)[ordenacio_indexs]
        
        # Primer anell
        r1_idx = ordenacio_posicions[0]
        r1 = abs(x[r1_idx + res//2])
        
        # Busquem el segon anell a una distància sqrt(2), ja que ho prediu la teoria, evitant pics falsos
        expect_r2_idx = r1_idx * np.sqrt(2)  # Posició esperada del segon anell

        # Trobem el pic més proper a aquesta distància
        r2_idx = None
        min_diff = float('inf')
        for pos in ordenacio_posicions[1:]:
            diff = abs(pos - expect_r2_idx)
            if diff < min_diff:
                min_diff = diff
                r2_idx = pos
        
        if r2_idx is not None:
            r2 = abs(x[r2_idx + res//2])
            return r1, r2
    
    return None, None

# Creació de la figura
fig = plt.figure(figsize=(12, 8))
gs = plt.GridSpec(1, 2, width_ratios=[3, 1])
ax = fig.add_subplot(gs[0])
text_ax = fig.add_subplot(gs[1])
text_ax.axis('off')

plt.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.9)

# Plot inicial
intensitat = compute_intensitat(default_mirror_diff, default_curvature)
img = ax.imshow(intensitat,
               extent=[-screen_size/2, screen_size/2, -screen_size/2, screen_size/2],
               cmap='gray', vmin=0, vmax=1)
ax.set_title('Interferòmetre de Michelson: mirall esfèric')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
plt.colorbar(img, ax=ax, label='intensitat')

# Afegim sliders
ax_slider_d = plt.axes([0.2, 0.1, 0.4, 0.03])
ax_slider_r = plt.axes([0.2, 0.05, 0.4, 0.03])

slider_d = Slider(ax_slider_d, 'Distància miralls Δd (µm)', -2, 2, valinit=0)
slider_r = Slider(ax_slider_r, 'Radi curvatura R (m)', 0, 10, valinit=0)

slider_d.valtext.set_text(f'{0:.2f} µm') # valors en µm
slider_r.valtext.set_text(f'{0:.2f} m')

# Add text for measurements in the right area
text_measurements = text_ax.text(0.1, 0.7, '', transform=text_ax.transAxes,
                               verticalalignment='top')

def update(val):
    mirror_diff = slider_d.val * 1e-6  # Convertim µm a m
    curvature = slider_r.val
    
    new_intensitat = compute_intensitat(mirror_diff, curvature)
    img.set_data(new_intensitat)
    
    slider_d.valtext.set_text(f'{slider_d.val:.2f} µm')
    slider_r.valtext.set_text(f'{slider_r.val:.2f} m')
    
    # càlcul del radi de curvatura a partir dels anells
    if curvature > 0.3:  # així s'eviten curvatures extremes
        r1, r2 = trobar_anells(new_intensitat)
        if r1 is not None and r2 is not None:
            r1_theory = np.sqrt(2 * 1 * curvature * long_ona)  # Primer anell (m=1)
            r2_theory = np.sqrt(2 * 2 * curvature * long_ona)  # Segon anell (m=2)
            
            print(f"\nPer curvatura R = {curvature:.2f} m:")
            print(f"Anells detectats: r1 = {r1*1000:.2f} mm, r2 = {r2*1000:.2f} mm")
            print(f"Predicció teòrica: r1 = {r1_theory*1000:.2f} mm, r2 = {r2_theory*1000:.2f} mm")
            
            R_calc = calcular_radi_curv(r1, r2)
            if R_calc is not None:
                text = f"Radi primer anell brillant: {r1*1000:.2f} mm\n"
                text += f"Radi segon anell brillant: {r2*1000:.2f} mm\n"
                text += f"distància entre anells: {((r2-r1)*1000):.2f} mm\n"
                text += f"Estimated curvature radius: {R_calc:.2f} m\n"
                text += f"(Predicció teòrica: r1 = {r1_theory*1000:.2f} mm, r2 = {r2_theory*1000:.2f} mm)"
                text_measurements.set_text(text)
            else:
                text = f"Radi primer anell brillant: {r1*1000:.2f} mm\n"
                text += f"Radi segon anell brillant: {r2*1000:.2f} mm\n"
                text += f"distància entre anells: {((r2-r1)*1000):.2f} mm\n"
                text += "No es pot calcular el radi de curvatura"
                text_measurements.set_text(text)
        else:
            text_measurements.set_text('No es poden detectar bé els anells')
    else:
        text_measurements.set_text('')
    
    fig.canvas.draw_idle()

slider_d.on_changed(update)
slider_r.on_changed(update)

plt.show()