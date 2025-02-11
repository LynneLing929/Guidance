import math
import random
import numpy.core.multiarray
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np
from scipy.optimize import curve_fit
from lmfit import Model
import random

def Model2(alphaArray, beta, theta):
    #where alpha is less than 6*beta: in this case, P1 = 1
    #where alpha/beta>1: in this case, P1 = 1/6

    # Period = math.ceil(alpha/beta)
    # Ratio = theta/beta #ratio between response time constant and time taken for each item
    # No = 0 #Number of lines/maximum number of lingering possibilities (i.e. total probabilities that one has encountered the target)
    # # (e.g. at this time, you could be lingering on the first or the second == 2 possibilities )
    # PR = 0 #Proportion of first line/Proportion of the given period that can be attributed to the earliest possible item
    # LA = 0 # Label of the first line/The earliest possible item one is on currently
    #gamma = constant term
    P1_list = list()
    for alpha in alphaArray:
        if alpha <= 6 * beta:
            CurrentPeriod = math.ceil(alpha / beta)
        # if CurrentPeriod ==1:
        #     P1 = 1/6
        # else:
            MaximumNumberPossible = divmod(alpha, beta)[0]
            m=-1
            l = list()

            for i in range(1, int(MaximumNumberPossible+1)):
                if alpha>i*beta+theta:
                    m = 0
                    l.append(m)
                elif alpha<=i*beta+theta:
                    m = 1
                    l.append(m)

            if l.count(1) == 0:
                FirstLineLabel = 0
                NumberofLines = 0
            else:
                FirstLineLabel= l.index(1) + 1
                NumberofLines = l.count(1)
            ProbabilitiesFromLingering = NumberofLines/(7-FirstLineLabel)

            # where the first line is
            if FirstLineLabel !=0:
                m = 7 - FirstLineLabel
                temp = 1
                while m > 7 - CurrentPeriod:
                    temp = temp * (m - 1) / m
                    m = m - 1
                # from when the first line ends
                P1 = ProbabilitiesFromLingering + temp*(1/(7-CurrentPeriod))
            else:
                P1 = 1/(7-CurrentPeriod)
        else:
            P1 = 1


        P1_list.append(P1)
    return P1_list


def ParametreEstimation(SOA,data):
    ParametreList = []
    OutputList = []
    ResidualList = []
    for b in range(round(data[4]/6),1000,2):
        for t in range(50,1000,2):
            P1_output = Model2(SOA,b,t)
            Currentlist = [b,t]
            ParametreList.append(Currentlist)
            OutputList.append(P1_output)
    for i in range(0,len(ParametreList)):
        Residual = 0
        for n in range(0,len(data)):
            Residual = Residual+(OutputList[i][n]-data[n])**2

        ResidualList.append(Residual)

    index = ResidualList.index(min(ResidualList))
    print(ParametreList[index])
    return ParametreList[index]

SOAList = [300,550, 750, 1200,1550]
ObservedData = [0.208333333,0.375,0.380952381,0.5,0.566666667]
Results = ParametreEstimation(SOAList,ObservedData)

#Plotting the empirical and expected data
EstimatedValues = Model2(SOAList,Results[0],Results[1])
X_Y_Spline = make_interp_spline(SOAList, EstimatedValues)
X_ = np.linspace(min(SOAList), max(SOAList), 200)
Y_ = X_Y_Spline(X_)
plt.plot(SOAList,ObservedData, label = "Empirical Data")
plt.plot(SOAList, EstimatedValues, label = "b = " +str(Results[0])+" , c = " + str(Results[1]) )
plt.legend(loc = "upper left", fontsize = "xx-small")
plt.show()
