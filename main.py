from SolarSystem import *
import matplotlib.pyplot as plt
from RunningPlot import RunningPlot
import turtle



ss = PLanetSystem(10)
mindist = 10 ** 30

gen = 0
while gen <=10:#mindist > ss.tol_dif * 5:
    ss.runAgeneration()
    mindist = ss.bestdistanceToJUpiterHist[-1:][0]
    print mindist

    gen += 1


print "Running last generation!!!!!!"
ss.run_simulation()
ss.selectProbes()

#ss.createSolarSystem()
#ss.run_simulation()

ss.make_plot()
ss.make_plot_best()

plt.figure(2)
plt.subplot(211)
plt.title("Best Distance")
plt.plot(ss.bestdistanceToJUpiterHist)
plt.subplot(212)
plt.title("Best Fit")
plt.plot(ss.maxFitHist)

plt.show()




