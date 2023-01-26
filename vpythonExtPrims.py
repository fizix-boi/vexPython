import vpython as vp
import numpy as np
import math as mp

#SCENE GENERATOR----------

def generateScene(hDes):
    wDes = int((7.2/4) * hDes)
    scene = vp.canvas(width = wDes, height = hDes, center = vp.vector(0, 0.5, 0), fov = 1)
    scene.autoscaling = False
    return(scene)

#HEMISPHERE FUNCTIONS----------

#Hemisphere Helpers

def zeroPointExtrustion(shape, extRad):
    res = []
    
    for point in shape:
        res.append([point[0] - extRad, point[1] - extRad])
        
    return(res)

def pointify(theta, radius):
    return([float(radius * vp.cos(theta)), float(radius * vp.sin(theta))])

#Hemisphere Makers

def hemisphere(outerRad, innerRad, color):
    pointVector = []
    pDens = 50 / outerRad # points per unit length
    numIn = np.floor(np.pi * innerRad * pDens).astype(int)
    numOut = np.floor(np.pi * outerRad * pDens).astype(int)

    outerTheta = np.linspace(0, vp.pi * 0.5, num = numOut)
    outerRadVec = outerRad * np.ones(numOut)
    innerTheta = np.linspace(vp.pi * 0.5, 0, num = numIn)
    innerRadVec = innerRad * np.ones(numOut)

    pointVector += (list(map(pointify, outerTheta, outerRadVec)))
    pointVector += (list(map(pointify, innerTheta, innerRadVec)))
    pointVector.append(pointVector[0])

    exr = 1e-4
    hemi = vp.extrusion(path = vp.paths.arc(radius = exr, angle1 = 0, angle2 = 2.1 * vp.pi),
                      shape = zeroPointExtrustion(pointVector, exr), color = color)
    
    return(hemi)

def hemisphereDown(outerRad, innerRad, color):
    hemi = hemisphere(outerRad, innerRad, color)
    hemi.rotate(angle = vp.pi, axis = vp.vector(1, 0, 0))
    hemi.pos = -hemi.pos
    return(hemi)

#Hemisphere Movers

def tiltOrigin(hemi):
    return(hemi.pos - 0.5 * vp.vector(hemi.length, hemi.height, hemi.width))

def tiltHemi(hemi, objs, angle, axis, origin):
    hemi.rotate(angle = angle, axis = axis, origin = origin)
    for obj in objs:
        obj.rotate(angle = angle, axis = axis, origin = origin)
        
def toggleLid(hemi, objs, angOri, angle, dt, num, filming, framer, scene):
    for it in range(num):
        tiltHemi(hemi, objs, angle / num, vp.vector(0, 0, 1), angOri)
        if(filming):
            vp.sleep(0.5)
            scene.capture('frame'+str(int(framer.frameNext)))
            framer.encFrame()
        else:
            vp.sleep(dt)
            
#PLANES

def xzRect(length, width, center, color):
    v0 = vp.vertex( pos = 0.5 * vp.vector(length,0,width) + center, color = color )
    v1 = vp.vertex( pos = 0.5 * vp.vector(-length,0,width) + center, color = color )
    v2 = vp.vertex( pos = 0.5 * vp.vector(-length,0,-width) + center, color = color )
    v3 = vp.vertex( pos = 0.5 * vp.vector(length,0,-width) + center, color = color )
    return(vp.quad( vs = [v0, v1, v2, v3] ))

#SCREWDRIVER

def genPoly(n, scaling):
    theta = np.linspace(0, 2 * np.pi, num = int(n + 1))
    stairs = (np.divide(theta, 2 * np.pi / n)).astype(int)
    thetaPlug = np.multiply(stairs, 2 * np.pi / n)

    siner = scaling * np.sin(thetaPlug)
    coser = scaling * np.cos(thetaPlug)
    
    poly = []
    
    for each in range(int(n + 1) - 1):
        poly.append([float(coser[each]), float(siner[each])])
    
    poly.append(poly[0])
    
    return(poly)
            
def screwDriver(scaling):
    
    #Hex Body

    hexBod = vp.extrusion(path = [vp.vector(0, 0, -4.5 * scaling), vp.vector(0, 0, 0)],
                 shape = genPoly(6, scaling), color = vp.vector(0.8, 0.2, 0.2))
    
    #Butt
    
    buttSize = 1.7
    butt = vp.ellipsoid(pos = vp.vector(0, 0, -4.75 * scaling),
                        length = buttSize * scaling, width = 1 * scaling, height = buttSize * scaling,
                       color = vp.vector(1, 1, 1))
    
    #Blue Lead-In
    
    lenConn = 1.5
    nummer = 100

    yVecFir = np.linspace(lenConn / 2, -lenConn / 2, num = nummer)
    yVecSec = np.linspace(-lenConn / 2, lenConn / 2, num = nummer)

    stretch = 2
    xscale = 0.4
    xVecFir = (1 + np.square(yVecFir) / stretch) * xscale
    xVecSec = np.zeros(nummer)

    connOutline = []

    for each in range(nummer):
        connOutline.append([float(xVecFir[each] * scaling), float(yVecFir[each] * scaling)])

    for each in range(nummer):
        connOutline.append([float(xVecSec[each] * scaling), float(yVecSec[each] * scaling)])

    connOutline.append(connOutline[0])
    
    leadIn = vp.extrusion(path = vp.paths.arc(radius = 0.2 * scaling, angle1 = 0, angle2 = 2.1 * vp.pi),
                      shape = connOutline, color = vp.vector(0.1, 0, 0.8))
    leadIn.pos = vp.vector(0, 0, scaling * 0.95 * lenConn / 2)
    leadIn.rotate(angle = 3 * vp.pi / 2)
    
    #Shaft
    
    shaftL = 0.4 * scaling
    shaftH = shaftL
    shaftW = 6 * scaling
    shaft = vp.box(pos = vp.vector(0, 0, shaftW / 2), size = vp.vector(shaftL, shaftH, shaftW),
                color = 0.7 * vp.vector(1, 1, 1))
    
    #Triangle Head
    
    triHead = vp.extrusion(path = [vp.vector(0, 0, shaftL), vp.vector(0, 0, 0)],
                 shape = genPoly(3, (shaftL / (vp.sqrt(3)))), color = shaft.color)
    triHead.pos = vp.vec(0, 0, shaftW + (vp.sqrt(3) / 4) * shaftL)
    triHead.rotate(angle = (3 * vp.pi) / 2, axis = vp.vector(0, 1, 0))
    
    #Compounding
    
    screwDriver = vp.compound([hexBod, butt, leadIn, shaft, triHead])
    screwDriver.rotate(angle = 3 * vp.pi / 2)
    screwDriver.pos = vp.vector(0, 0, 0)
    
    return(screwDriver)