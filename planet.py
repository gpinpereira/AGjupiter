# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 19:03:17 2016

@author: Guilherme
"""
import math
import logging
objetos = []
planets = []
probes = []
limiteValue = 10 ** 12
class Planet(object):

    def __init__ (self,name, mass, x, y, vx, vy,ax,ay, bodieRadius):
        global objetos
        objetos.append(self)

        self.G = 6.67408 * 10 ** -11
        self.name = name
        global planets
        if not "Probe" in self.name:
            planets.append(self)
        self.mass = mass

        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.ax = ax
        self.ay = ay

        self.bodieRadius = bodieRadius
        self.distanceToJupiter = 0
        self.killed = False

        self.x_history = []
        self.y_history = []

        self.generation = 0
        self.x_history.append(self.x)
        self.y_history.append(self.y)

    def rk4 (self,deltat):

        k1x = deltat * self.calc_ax(self.x)
        l1x = deltat * self.vx

        k2x = deltat * self.calc_ax(self.x + 0.5 * l1x)
        l2x = deltat * (self.vx + 0.5 * k1x)

        k3x = deltat * self.calc_ax(self.x + 0.5 * l2x)
        l3x = deltat * (self.vx + 0.5 * k2x)

        k4x = deltat * self.calc_ax(self.x + l3x)
        l4x = deltat * (self.vx + k3x)

        k1y = deltat * self.calc_ay(self.y)
        l1y = deltat * self.vy

        k2y = deltat * self.calc_ay(self.y + 0.5 * l1y)
        l2y = deltat * (self.vy + 0.5 * k1y)

        k3y = deltat * self.calc_ay(self.y + 0.5 * l2y)
        l3y = deltat * (self.vy + 0.5 * k3y)

        k4y = deltat * self.calc_ay(self.y + l3y)
        l4y = deltat * (self.vy + k3y)

        addx = (l1x + 2 * l2x + 2 * l3x + l4x) / 6
        addy = (l1y + 2 * l2y + 2 * l3y + l4y) / 6



        self.x += addx
        self.y += addy

        self.vx += (k1x + 2 * k2x + 2 * k3x + k4x) / 6
        self.vy += (k1y + 2 * k2y + 2 * k3y + k4y) / 6

        self.x_history.append(self.x)
        self.y_history.append(self.y)

        #self.manageMapLimit()

    def calc_ax(self, x):
        value = 0

        listplanet = getPlanets()



        for i in listplanet:

            if i != self and isinstance(i,Planet) and i.name != self.name:

                dx = x - i.x

                dy = i.y - self.y

                dsq = dx * dx + dy * dy  # distance squared
                dr = dsq ** 0.5
                #print "acalcAx"
                #print self.name
                #print i.name

                force = self.G * i.mass / dsq


                value += force * dx / dr
        #print "Value, ", value

        return -value

    def calc_ay(self, y):
        value = 0

        for i in getPlanets():

            if i != self and isinstance(i,Planet) and i.name != self.name:
                dx = i.x - self.x
                dy = y - i.y

                dsq = dx * dx + dy * dy  # distance squared
                dr = dsq ** 0.5

                force = self.G * i.mass / dsq

                value += force * dy / dr

        return -value

    def plotValues(self):

        return self.x_history, self.y_history

    def manageMapLimit(self):

        update = abs(self.x) > get_limite() or abs(self.y) > get_limite()
        if update:
            if abs(self.x) > get_limite():
                update_Limite(abs(self.x))

            elif abs(self.y) > get_limite():

                update_Limite(abs(self.y))




class Probe(Planet):

    def __init__(self,name,anglepos,angleDirec,earthRadius,limit):

        earth = getbodiebyname("Earth")
        logging.basicConfig(filename='probes1.log', level=logging.INFO)
        self.anglePos = anglepos
        self.angleDirec = angleDirec

        self.listAnglePos = self.gray_code_list(self.anglePos)

        self.listAngleDir = self.gray_code_list(self.angleDirec)


        self.earthRadius = earthRadius

        self.flightTime = 0

        self.reachedJupiter = False
        self.fitness = 0
        self.tolerance_distance = getbodiebyname("Jupiter").bodieRadius * 10
        self.maxTimeOfFlight = limit
        #self.liveTime = 0
        earthAtmosphere = 120 * 10 ** 3 # earth atmosphere high
        velocity = 24000
        extraHigh = 100 * 10 ** 5

        x = earth.x + (self.earthRadius + earthAtmosphere + extraHigh) * math.cos(self.anglePos * math.pi / 180)
        y = earth.y + (self.earthRadius + earthAtmosphere + extraHigh) * math.sin(self.anglePos  * math.pi/180)


        vx = velocity * math.cos((angleDirec + anglepos) * math.pi / 180)
        vy =  velocity * math.sin((angleDirec + anglepos) * math.pi / 180)

        Planet.__init__(self,name,120,x,y,vx,vy,0,0,20)
        global probes
        probes.append(self)

    def monitorProbe(self,totalTime):
        #print "Checking"
        self.flightTime = totalTime
        slowDown = False
        factor = 0

        for planet in getPlanets():
            if isinstance(self, Probe):
                #print "i'm a probe called " + self.name
                probe = self

                distancetoPlanet = ((planet.x - probe.x) ** 2 + (planet.y - probe.y) ** 2) ** 0.5

                if planet.name == "Jupiter":
                    self.updateDistanceToJupiter(distancetoPlanet)

                if distancetoPlanet <= planet.bodieRadius * 6:
                    slowDown = True

                    #print planet.bodieRadius * 6/distancetoPlanet
                    factor = int(planet.bodieRadius * 6/distancetoPlanet)

                if distancetoPlanet <= planet.bodieRadius:

                    #logging.info( probe.name + " crashed against " + planet.name )
                    if not self.reachedJupiter:
                        self.killed = True
                        killProbebyName(probe.name)

        if ((self.x) ** 2 + (self.y) ** 2) ** 0.5 > 10 ** 13:
            if not self.reachedJupiter:
                print "out of bound"
                killProbebyName(self.name)

        return slowDown ,factor

    def calcDistanceToJupiter(self):

        jupiter = getbodiebyname("Jupiter")

        juX = jupiter.x
        juY = jupiter.y

        x = self.x
        y = self.y

        self.distanceToJupiter = math.sqrt((juX-x)**2 + (juY-y)**2)

    def updateDistanceToJupiter(self,distance):

        self.distanceToJupiter = distance

        if self.distanceToJupiter <= self.tolerance_distance:
            logging.info(self.name + " reached jupiter")
            self.reachedJupiter = True

    def calcFitness(self):

        #dfit = 0
        r = 0.001
        timefactor =  r * float(self.maxTimeOfFlight)/float(self.flightTime)
        if self.distanceToJupiter < self.tolerance_distance:
            dfit = self.tolerance_distance

        else:
            dfit = self.distanceToJupiter

        distParameter = (1-r)*(100 * self.tolerance_distance/ dfit)

        self.fitness =  math.exp(2*(distParameter + timefactor))

        if self.killed:
            self.fitness = 0

    def gray_code_list(self,n):

        null = True
        gray = n ^ (n >> 1)
        alist = []
        s = "{0:0{1}b}".format(gray, n)
        for leter in s[-9:]:

                alist.append(int(leter))


        alist.reverse()

        while len(alist) < 9:

            alist.append(0)

        alist.reverse()

        return alist

killedProbes = []

def killedprobes():

    global killedProbes
    return killedProbes


def killProbebyName(name):
    global killedProbes
    killedProbes.append(getbodiebyname(name))
    listProbes = getAllProbes()
    listBodies = bodies()

    listBodies.remove(getbodiebyname(name))

    for probe in listProbes:

        if probe.name == name:
            listProbes.remove(probe)

    """
    for bodie in listBodies:
        #if bodieIndex < len(listBodies):
        bodie = listBodies[bodieIndex]
        if bodie.name == name:

            listBodies.pop(bodieIndex)

        #if bodieIndex < len(listProbes):

        probe = listProbes[bodieIndex]
        if probe.name == name:
            listProbes.pop(bodieIndex)
    """


def reset():
    global objetos
    objetos = []


def clearPlanets():

    global objetos
    global planets

    for bodie in objetos:

        if not isinstance(bodie,Probe):
            objetos.remove(bodie)

    planets = []


def resetProbes():

    global probes
    global objetos
    probes = []

    for bodie in objetos:

        if isinstance(bodie,Probe):
            #print bodie.name
            objetos.remove(bodie)


def getAllProbes():
    global probes
    return probes


def bodies():
    global objetos
    return objetos


def get_limite():
    return limiteValue


def update_Limite(value):
    global limiteValue

    limiteValue = value


def getbodiebyname(name):

    for bodie in bodies():

        if isinstance(bodie,Planet):
            if bodie.name == name:
                return bodie


def getPlanets():
    global planets

    return planets


def bodieExist(name):
    exist = False
    for bodie in bodies():

        if bodie.name == name:
            exist = True
            break
    return exist

