# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 00:48:15 2016

@author: Guilherme
"""

from planet import *
from math import *
import matplotlib.pyplot as plt

G = 6.67408 * 10 ** -11
deltat = 3600 
limite = 3600 * 24 * 365 * 12     # um ano

posicao_x = []
posicao_y = []
posicao_x_jupiter = []
posicao_y_jupiter = []
distancia = []
distancia_jupiter = []

planetas = []
sol = Planet("Sol",1.98 * 10 ** 30,0,0,0,0,0,0)

terra = Planet("Terra", 5.97 * 10 ** 24,4.48456 * 10 ** 10,1.40453 * 10 ** 11,  -2.88626 * 10 ** 4, 8.95990 * 10 ** 3, 0, 0)

direcao_terra = atan(terra.y / terra.x) 
angulo_posicao = 90 + direcao_terra
raio =  sqrt(terra.x**2 + terra.y**2)

print(raio * cos(direcao_terra))
print(raio * sin(direcao_terra))
sonda = Planet("Sonda", 120,10000 * cos(angulo_posicao) + raio * cos(direcao_terra),
               10000 * sin(angulo_posicao) + raio * sin(direcao_terra),  
                -2.88626 * 10 ** 4, 8.95990 * 10 ** 3,0,0)

escala_x = terra.x
escala_y = terra.y
jupiter = Planet ("Jupiter",1.89 * 10 ** 27,-7.53 * 10 ** 11,2.93 * 10 ** 11, -4888.42 ,-11562.4,0,0)

#evaluate ax
def ax(myself,x):
    value = 0
    for i in bodies():
        if i != myself:
            R = ((((myself.x - i.x) ** 2) + ((myself.y - i.y) ** 2)) ** 0.5)
            value += G * i.mass * (x - i.x) / (abs (R)) ** 3
            
    return -value

#evaluta ay
def ay(myself,y):
    value = 0
    for i in bodies():
        if i != myself:
            R = ((((myself.x - i.x) ** 2) + ((myself.y - i.y) ** 2)) ** 0.5)
            value = value + G * i.mass * (y - i.y) / (abs (R)) ** 3
            
    return -value

def aceleration_of_all_planets(myself):
    for i in myself.bodies(): # evalute ax and ay for all planets
        if i != sol:
            i.ax = ax(myself,i)
            i.ay = ay(myself,i)
            print(i.name)
            print(i.ax)
            print(i.ay)
          
def rk4 (myself,deltat):
    
    k1x = deltat * ax(myself,myself.x)
    l1x = deltat * myself.vx
    
    k2x = deltat * ax(myself, myself.x + 0.5 *  l1x)
    l2x = deltat * (myself.vx +  0.5 * k1x)
    
    k3x = deltat * ax(myself, myself.x + 0.5 * l2x)
    l3x = deltat * (myself.vx +  0.5 * k2x)
    
    k4x = deltat * ax(myself , myself.x +  l3x)
    l4x = deltat * (myself.vx + k3x)
        
    
    
    k1y = deltat * ay(myself,myself.y)
    l1y = deltat * myself.vy
    
    k2y = deltat * ay(myself, myself.y +  0.5 *  l1y)
    l2y = deltat * (myself.vy + 0.5 * k1y)
    
    k3y = deltat * ay(myself, myself.y +  0.5 * l2y)
    l3y = deltat * (myself.vy +  0.5 * k3y)
    
    k4y = deltat * ay(myself , myself.y + l3y)
    l4y = deltat * (myself.vy + k3y)
    

    myself.x = myself.x + (l1x + 2 * l2x + 2 * l3x + l4x) / 6
    myself.y = myself.y + (l1y + 2 * l2y + 2 * l3y + l4y) / 6
    
    myself.vx = myself.vx + (k1x + 2 * k2x + 2 * k3x + k4x) / 6
    myself.vy = myself.vy + (k1y + 2 * k2y + 2 * k3y + k4y) / 6


    print myself.x
    
tempo = 0
limite = 3600 * 2
while tempo <= (limite):
    for i in bodies():
        if i != sol:
            rk4(i,deltat)
        
    posicao_x.append(terra.x)
    posicao_y.append(terra.y)
    posicao_x_jupiter.append(sonda.x)
    posicao_y_jupiter.append(sonda.y)
    distancia.append(  (terra.x ** 2 + terra.y ** 2) ** 0.5   ) 
    
    tempo = tempo + deltat
    
escala = max (posicao_x)

if escala < abs ( min (posicao_x)):
    escala = abs ( min (posicao_x))
    
if escala < max(posicao_y):
    escala = max (posicao_y)
    
if escala < abs ( min (posicao_y)):
    escala = abs ( min (posicao_y))

escala = escala * 1.1

Apoapsis = max(distancia)
Periapsis = min(distancia)  
Exc = (Apoapsis - Periapsis) / (Apoapsis + Periapsis)
print(terra.x)
print("Error x")
print( 100 * abs(terra.x - 4.54779 * 10 ** 10) / abs(terra.x)  )
print("\n")
print(terra.y)
print("Error y")
print( 100 * abs(terra.y - 1.40255 * 10 ** 11) / abs(terra.y) )
print("\n")
print(Exc)

plt.plot(posicao_x,posicao_y,'b',posicao_x_jupiter,posicao_y_jupiter,'r' )
plt.xlim(- escala_x , escala)
plt.ylim(- escala , escala)
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')
plt.show()  