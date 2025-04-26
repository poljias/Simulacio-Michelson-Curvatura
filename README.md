# Simulacio-Michelson-Curvatura

Aquest repositori conté simulacions interactives de l'interferòmetre de Michelson amb diferents tipus de miralls deformats.

## Índex

- [Contingut](#contingut)
  - [1. Interferòmetre amb Miralls Radials](#1-interferòmetre-amb-miralls-radials-interf_miralls_rn_spyderpy)
  - [2. Interferòmetre amb Mirall Esfèric](#2-interferòmetre-amb-mirall-esfèric-interf_mirall_esferic_spyderpy)
- [Paràmetres de les simulacions](#paràmetres-de-les-simulacions)
- [Com utilitzar les simulacions](#com-utilitzar-les-simulacions)
- [Detalls tècnics](#detalls-tècnics)

## Contingut

El repositori conté dues simulacions principals:

### 1. Interferòmetre amb Miralls Radials (`interf_miralls_Rn_spyder.py`)

Aquesta simulació permet visualitzar els patrons d'interferència quan un dels miralls té una deformació que segueix una potència de R (distància radial). Les característiques principals són:

- Permet variar la potència de R des de 1 fins a 4 (amb increments de 0.5)
  - R¹: Deformació cònica
  - R²: Deformació parabòlica
  - R³: Deformació cúbica
  - R⁴: Deformació quàrtica
- Controls interactius per:
  - Diferència de camí entre els braços (Δd)
  - Magnitud de la deformació
  - Potència de R

### 2. Interferòmetre amb Mirall Esfèric (`interf_mirall_esferic_spyder.py`)

Aquesta simulació es centra en el cas específic d'un mirall amb curvatura esfèrica. Característiques principals:

- Visualització dels anells d'interferència característics dels miralls esfèrics
- Detecció automàtica dels radis dels anells brillants
- Càlcul del radi de curvatura a partir de les posicions dels anells
- Controls interactius per:
  - Diferència de camí entre els braços (Δd)
  - Radi de curvatura del mirall (R)

## Paràmetres de les simulacions

Ambdues simulacions comparteixen alguns paràmetres bàsics:
- Pantalla: 10 cm × 10 cm
- Resolució: 1000 × 1000 píxels
- Longitud d'ona: 500 nm (llum verda)
- Distància de la lent expansora: 0.5 m

## Com utilitzar les simulacions

1. Assegureu-vos de tenir instal·lades les dependències necessàries:
   - numpy
   - matplotlib
   - Qt5

2. Si no teniu Spyder, executeu els scripts amb Python:
   ```bash
   python interf_miralls_Rn_spyder.py
   # o
   python interf_mirall_esferic_spyder.py
   ```

3. Utilitzeu els sliders interactius per modificar els paràmetres i observar els canvis en temps real en el patró d'interferència.

## Detalls tècnics

Les simulacions calculen la diferència de camí òptic (DCO) tenint en compte:
- La contribució de la font puntual (front d'ona esfèric)
- La deformació del mirall
- La diferència de camí entre els braços

La intensitat es calcula assumint una font perfectament monocromàtica amb grau de coherència |g|=1:
I = 0.5 * (1 + cos(2π * DCO / λ))