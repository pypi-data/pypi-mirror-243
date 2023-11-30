# SPDX-FileCopyrightText: 2021 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0
"""
The aim of these Paretotools functions is to find the longest distance on
axes x or y for every couple of points that can solve the optimization problem.
"""
import numpy as np
def getXorYmid(xy, normX, normY, xmin, ymin):
    """
    Finds the middle point between x and y.
    :param xy: list of tuples including x and y
    :param normX: norm of X
    :param normY: norm of Y
    :param xmin : minimial abscisse of the xy couple
    :param ymin : minimial ordinate of the xy couple
    :return: the index of the objective function, the middle of [XY].
     """
    xyT=np.array(xy).T
    xyNorm=np.array([((xyT[0,:]-xmin)/normX),((xyT[1,:]-ymin)/normY)]).T.\
        tolist()

    #p1, p2, d = maxDist(xyNorm)
    p1, p2 = maxDist(xyNorm)
    dX = abs(p2[0]-p1[0])    #on suppose que p2 est bien plus grand que p1
    dY = abs(p2[1]-p1[1])
    if dX > dY :
        return 0, (p1[0]+p2[0])/2*normX+xmin
    else:
        return 1, (p1[1]+p2[1])/2*normY+ymin


def maxDist(points):
    points = sorted(points, key=lambda x: x[0])  # Presorting x-wise
    pts2 = [pt for pt in points] #copy
    pts1 = np.array(points[0:-1]).T
    pts2 = np.array(pts2[1:]).T

    dist = (pts1[0] - pts2[0]) ** 2 + (pts1[1] - pts2[1]) ** 2
    index = np.argmax(dist)
    return points[index], points[index+1]



if __name__ == '__main__':
    a = [[9953.86318652108,3702.5292382627013],
    [16922.450708122255,1312.920633183176],
    [13483.690450357713,1790.842361273781],
    [11890.18707155824,2268.764075340589],
    [10963.413555536845,2746.685796235864],
    [10358.889713185245,3224.6075172528217],
    [11347.58068777548,2520.915738089411],
    [12741.29819530203,1977.522534854665],
    [14135.015696837956,1661.5621851434228],
    [15528.733518913752,1456.2150724085136]]

    x=[xy[0] for xy in a]
    y=[xy[1] for xy in a]

    #print( maxDist(a) )
    #print( getXorYmid(a, 15528-9953, 3702-1456, 9953,1456) )
    print(maxDist(a))

