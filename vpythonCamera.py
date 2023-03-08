import vpython as vp
import numpy as np
import math as mp

#CAMERA MOVEMENTS
            
def inspectate(obj, numDiv, dur):
    durStep = dur / 3
    for it in range(numDiv):
        obj.rotate(angle = (2 * vp.pi / numDiv), axis = vp.vector(1, 0, 0))
        vp.sleep(durStep / numDiv)
        
    for it in range(numDiv):
        obj.rotate(angle = (2 * vp.pi / numDiv), axis = vp.vector(0, 1, 0))
        vp.sleep(durStep / numDiv)
        
    for it in range(numDiv):
        obj.rotate(angle = (2 * vp.pi / numDiv), axis = vp.vector(0, 0, 1))
        vp.sleep(durStep / numDiv)

def pathVectorize(px, py, pz):
    numPoints = len(px) #all should be same
    path = []
    
    for it in range(numPoints):
        newVec = vp.vector(float(px[it]), float(py[it]), float(pz[it]))
        path.append(newVec)
    
    return(path)
        
def moveCamera(scene, path, dt, ranger, filming, framer):
    for point in path:
        scene.camera.pos = point
        if(ranger > 0):
            scene.range = ranger
        if(filming):
            vp.sleep(0.5)
            scene.capture('frame'+str(int(framer.frameNext)))
            framer.encFrame()
        else:
            vp.sleep(dt)
        
def moveFixedCamera(scene, path, looker, dt, ranger, filming, framer):
    for point in path:
        scene.camera.pos = point
        diff = looker - point
        scene.forward = diff / diff.mag
        scene.center = looker
        if(ranger > 0):
            scene.range = ranger
        if(filming):
            vp.sleep(0.5)
            scene.capture('frame'+str(int(framer.frameNext)))
            framer.encFrame()
        else:
            vp.sleep(dt)
            
def stillShot(scene, numFrame, framer):
    for it in range(numFrame):
        scene.capture('frame'+str(int(framer.frameNext)))
        framer.encFrame()
    vp.sleep(0.5)#0.2 * numFrames)
        
def ambientLinCom(ambientScaling, linearProp, colorVector):
    return(((1 - linearProp) * (ambientScaling * vp.vector(1, 1, 1))) + (linearProp * colorVector))

class globalFrames:
    def __init__(self):
        self.frameNext = 1
        
    def encFrame(self):
        self.frameNext += 1
        
    def decFrame(self):
        self.frameNext -= 1