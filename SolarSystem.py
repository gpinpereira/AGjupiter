from planet import *
import matplotlib.pyplot as plt
import math
import random
import logging

class PLanetSystem:

    def __init__(self,numberOfProbes):


        self.earthRadius = 6371 * 10 ** 3
        self.limit = int(24 * 3600 * 365 * 10)
        self.createSolarSystem()
        self.createNrandomProbes(numberOfProbes)

        self.survivedProbes = []
        self.fittesProbes = []
        self.deltat = 1
        self.time = 0

        self.maxFitHist = []
        self.minFitHist = []
        self.meanFitHist = []
        self.bestdistanceToJUpiterHist = []

        self.optimoumAngPos = 0
        self.optimoumAngDir = 0
        self.generations = 0
        logging.basicConfig(filename='SolarSistem.log',level=logging.DEBUG)

        plt.figure(1)

        self.tol_dif = getbodiebyname("Jupiter").bodieRadius * 10
        print self.tol_dif, " m (tolerance distance)"

    def run_simulation(self):
        flag = -1
        intervalflag = 0.05
        self.time = 0
        self.deltat = 1
        while self.time < int(self.limit * 1.2):
            flag += 1
            if flag == 500:
                #self.make_plot_launch()
                pass

            for bodie in bodies():

                if isinstance(bodie,Planet):

                    if bodie.name != 'Sol':
                        #print bodie.name
                        bodie.rk4(self.deltat)

            self.monitorSimulation()

            if self.time >= int(self.limit * 1.2 * intervalflag):
                intervalflag += 0.05
                logging.debug("\n\nCurrent Time: "+  str(self.time)+ "\nLimit: " + str(self.limit)+"\nPercentage: "+ str(intervalflag - 0.05))
            self.time += self.deltat

        #self.examProbes()
        #self.geneticAlgorithmCycle()
        #self.make_plot()

    def make_plot(self):
        plt.subplot(211)
        for bodie in bodies():

            if isinstance(bodie, Planet): # safety first
                if bodie.name != 'Sol':
                    if not isinstance(bodie,Probe):
                        plt.plot(bodie.plotValues()[0],bodie.plotValues()[1],"r")
                    else:
                        plt.plot(bodie.plotValues()[0], bodie.plotValues()[1], "g")

        limit_value = get_limite()

        plt.title("Last Probes")
        plt.xlim([-limit_value,limit_value])
        plt.ylim([-limit_value,limit_value])


    def make_plot_best(self):

        bestFit = 0

        bestProbe = 0#Probe("nothing",0,0,0,0)
        bestDistance = 0
        for p in getAllProbes():

            if isinstance(p,Probe):
                #p.calcFitness()

                if round(p.fitness,5) > round(bestFit,5):
                    print "Best Fitness," , p.fitness
                    bestFit = p.fitness
                    bestDistance = p.distanceToJupiter
                bestProbe = p

        #self.bestdistanceToJUpiterHist.append(bestDistance)
        #self.maxFitHist.append(bestFit)
        plt.subplot(212)
        plt.plot(bestProbe.plotValues()[0], bestProbe.plotValues()[1], "g")
        for bodie in bodies():

            if isinstance(bodie, Planet):  # safety first
                if bodie.name != 'Sol':
                    if not isinstance(bodie, Probe):
                        plt.plot(bodie.plotValues()[0], bodie.plotValues()[1], "r")
                    else:
                        if round(bestFit,5) <= round(bodie.fitness,5):
                            print "Printing a bet probe!!!!!!!!!!!!!"


        #value = value[:-1] + ")\nplt.show()"

        limit_value = get_limite()

        plt.title("Best Probe")
        plt.xlim([-limit_value, limit_value])
        plt.ylim([-limit_value, limit_value])
        plt.show()
        #exec value

    def make_plot_launch(self):

        bodie = getbodiebyname("Earth")

        hist = int(len(bodie.plotValues()[0]) * 0.01)

        earthx = bodie.plotValues()[0][:hist]
        earthy = bodie.plotValues()[1][:hist]

        fig, ax = plt.subplots()

        limit_value = 0
        for bodie in getAllProbes():

            probx = bodie.plotValues()[0][:hist]
            proby = bodie.plotValues()[1][:hist]

            newX = []
            newY = []
            for index in range(len(probx)):
                newX.append(probx[index] - earthx[index])
                newY.append(proby[index] - earthy[index])

            valuex = abs(max(newX, key=abs))
            valuey = abs(max(newY, key=abs))

            value = 0
            if valuex > valuey:
                value = valuex
            else:
                value = valuey

            if value > limit_value:
                limit_value = value

            plt.figure(1)
            plt.plot(newX, newY, "g--")
            ax = plt.gca()
            ax.set_xticklabels([])

        earthListX = []
        earthListY = []

        for i in range(0,360,1):
            earthListX.append(self.earthRadius * math.cos(i))
            earthListY.append(self.earthRadius * math.sin(i))
        plt.figure(1)
        plt.plot(earthListX, earthListY, color="b")
        ax = plt.gca()
        ax.set_xticklabels([])

        limit_value = (self.earthRadius  + 120000) * 10
        print "Limit, ", limit_value
        print "Number of probes Left, ", self.numberOfProbes()
        plt.xlim([-limit_value, limit_value])
        plt.ylim([-limit_value, limit_value])
        plt.show()

    def createSolarSystem(self):

        clearPlanets()
        sol = Planet("Sol", 1.98 * 10 ** 30, 0, 0, 0, 0, 0, 0, 695700000 * 2)

        earth = Planet("Earth", 5.97 * 10 ** 24,
                       -2.813761281023670 * 10 ** 06 * 10 ** 3, 1.471285071392669 * 10 ** 8 * 10 ** 3,
                       -3.027475347346017 * 10 ** 01 * 10 ** 3, -6.893180165346682 * 10 ** -01 * 10 ** 3, 0, 0, 6371000)

        mec = Planet("Mercury", 5.97 * 10 ** 24,
                     -3.843238989443087 * 10 ** 07 * 10 ** 3, 3.238336656666842 * 10 ** 07 * 10 ** 3,
                     -4.130694227828092 * 10 ** 01 * 10 ** 3, -3.525872881413886 * 10 ** 01 * 10 ** 3, 0, 0, 2440000)

        ven = Planet("Venus", 5.97 * 10 ** 24,
                     -1.632827050987058 * 10 ** 07 * 10 ** 3, -1.074436746674122 * 10 ** 8 * 10 ** 3,
                     3.438674745503773 * 10 ** 01 * 10 ** 3, -5.400214769638323 * 10 ** 0 * 10 ** 3, 0, 0, 3390000)

        mar = Planet("Marte", 5.97 * 10 ** 24,
                     -2.414562659761738 * 10 ** 8 * 10 ** 3, -4.136573308066428 * 10 ** 7 * 10 ** 3,
                     4.995903002113890 * 10 * 3, -2.181170191355551 * 10 * 10 ** 3, 0, 0, 3390000)

        jupiter = Planet("Jupiter", 1.89 * 10 ** 27,
                         -6.436111326348454 * 10 ** 8 * 10 ** 3, -4.962076837072723 * 10 ** 8 * 10 ** 3,
                         7.828371525631897 * 1 * 10 ** 3, -9.740141258437975 * 1 * 10 ** 3, 0, 0, 69911000)

    def monitorSimulation(self):

        for probe in getAllProbes():
            duble = probe.monitorProbe(self.time)
            if bodieExist(probe.name) and duble[0]:

                self.deltat = 300/duble[0]
            else:
                self.deltat = 3600

    def numberOfProbes(self):
        return len(getAllProbes())

    def createNrandomProbes(self,N):

        for i in range(N):
            randomPosition = int(random.uniform(0,360))

            if bool(int(round(random.uniform(0,1)))):
                randomDirection = int(random.uniform(0,135))
            else:
                randomDirection = int(random.uniform(360-135, 360))
            aprobe = Probe("Probe " + str(i),randomPosition,randomDirection,self.earthRadius,self.limit)

    def examProbes(self):

        self.survivedProbes = getAllProbes()

        allProbes = self.survivedProbes + killedprobes()
        print "Survived: " ,len(self.survivedProbes)
        print "Killed: ", len(killedprobes())
        for p in allProbes:
            if isinstance(p,Probe):
                print p.listAnglePos
                print p.listAngleDir
                print '\n'
                p.calcFitness()

    def geneticAlgorithmCycle(self):

        self.selectProbes()
        self.pairAndmatefittest()

    def runAgeneration(self):

        self.generations += 1
        print "\nGenerations"
        print self.generations
        self.createSolarSystem() # probes are created in __init__ or from the GA algorithm

        self.run_simulation()

        self.geneticAlgorithmCycle()

    def randomCrossList(self,list1,list2):

        if len(list1) != len(list2):
            raise Exception('"Error list not the same size')
            #randomPos = 0
        else:
            randomPos = random.randint(0,len(list2))
        return list1[:randomPos] + list2[randomPos:]

    def selectProbes(self):
        self.survivedProbes = getAllProbes()
        maxfit = 0
        minfit = 2
        allProbes = self.survivedProbes# + killedprobes()

        print "\nSurvived: ", len(self.survivedProbes)
        print "Killed: ", len(killedprobes())

        bestdistance = 0
        for p in allProbes:
            if isinstance(p, Probe):
                p.calcFitness()
                #print p.name
                #print p.fitness
                if p.fitness > maxfit:
                    maxfit = p.fitness
                    self.optimoumAngPos = p.anglePos
                    self.optimoumAngDir = p.angleDirec
                    bestdistance = p.distanceToJupiter
                if p.fitness <= minfit:
                    minfit = p.fitness


        print "\nMaxfit:" , maxfit
        print "Minfit:", minfit
        median = (maxfit + minfit) * 0.5
        print "Median: ", median
        print "Optium angle position: ", self.optimoumAngPos
        print "Optium angle direction: ", self.optimoumAngDir


        self.bestdistanceToJUpiterHist.append(bestdistance)
        self.maxFitHist.append(maxfit)
        self.minFitHist.append(minfit)
        self.meanFitHist.append(median)
        breedingProbes = allProbes


        # allProbes[9]
        for probe in allProbes:

            if isinstance(probe,Probe):
                #print probe.name
                #print probe.fitness
                if probe.generation >= 2:
                    if probe.fitness < median:
                        print "deleted"
                        breedingProbes.remove(probe)
        print "Total probes after selection: ", len(breedingProbes)
        self.fittesProbes = breedingProbes

    def pairAndmatefittest(self):

        resetProbes()
        sumFit = 0
        self.mutationposition = random.randint(0,8)
        self.numberofBirths = 0


        print len(self.fittesProbes), " probes to mate."
        for i in self.fittesProbes:
            sumFit += i.fitness
        i = 0

        oldProbes =self.fittesProbes[:]

        numberofmate = 0
        while len(self.fittesProbes) > 1 :

            if len(self.fittesProbes) > 1:

                number1 = random.randint(0,len(self.fittesProbes) -1)
                number2 = random.randint(0,len(self.fittesProbes) -1)
                while number2 == number1:
                    number2 = random.randint(0, len(self.fittesProbes)-1)

                mate1 = self.fittesProbes[number1]
                mate2 = self.fittesProbes[number2]

                self.fittesProbes.remove(mate1)
                self.fittesProbes.remove(mate2)

                if isinstance(mate1,Probe) and isinstance(mate2,Probe):
                    numberofmate += 1

                    numberOfChilds = int(round(1 + (mate1.fitness + mate2.fitness) * len(self.fittesProbes) / sumFit))

                    for numberChild in range(numberOfChilds):
                        self.numberofBirths += 1
                        childDir = self.randomCrossList(mate1.listAngleDir,mate2.listAngleDir)
                        childDir[self.mutationposition] += 1
                        if childDir[self.mutationposition] > 1:
                            childDir[self.mutationposition] = 0
                        childPosAng = self.randomCrossList(mate1.listAnglePos,mate2.listAnglePos)

                        childPosAng[self.mutationposition] += 1
                        if childPosAng[self.mutationposition] > 1:
                            childPosAng[self.mutationposition] = 0

                        childDir = self.convertGrayToInt(childDir)
                        childPosAng = self.convertGrayToInt(childPosAng)

                        aprobe = Probe("Probe " + str(i), childPosAng, childDir, self.earthRadius, self.limit)

                        i += 1
        print "Catching old probes"
        self.fittesProbes = []
        m = 0
        for oldProbe in oldProbes:
            v = oldProbe.generation
            aprobe = Probe("Probe " + str(i), oldProbe.anglePos, oldProbe.angleDirec, self.earthRadius, self.limit)
            aprobe.generation = v + 1
            #self.fittesProbes.remove(oldProbe)
            i += 1
            m+= 1

        self.totalpopulation = len(getAllProbes())
        print "Old people: ", m
        print "Total number of offsprigs: ", self.numberofBirths
        print "Avarage of " + str(self.numberofBirths/numberofmate) + " per couple"
        print "Total population: ", self.totalpopulation

    def convertGrayToInt(self,list):

        #list.reverse()

        binlist = []
        lastvalue = 1
        i = 0
        for leter in list:

            if i == 0:
                binlist.append(leter)
                lastvalue = leter
            else:
                newValue = lastvalue + leter

                if newValue > 1:
                    newValue = 0

                lastvalue = newValue
                binlist.append(newValue)

            #binlist.reverse()


            i += 1

        value = 0
        index = 0
        for i in binlist:
            value = value * 2 + i
            index += 1

        return value

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











