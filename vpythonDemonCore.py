import vpython as vp
import vpythonExtPrims as vpep
import vpythonCamera as vpc

def generateCore():
    core = vp.sphere(pos = vp.vector(0, 0, 0), radius = 0.6, color = vp.color.blue)
    hemi = vpep.hemisphereDown(1, core.radius * 1.1, vp.vector(0.5, 0.5, 0.5))
    demonCoreBase = vp.compound([core, hemi])
    demonCoreTop = vp.compound([vpep.hemisphere(1, core.radius * 1.1, vp.vector(0.5, 0.5, 0.5))])

    return(demonCoreBase, demonCoreTop)

class demonCoreExp:
    def __init__(self, center):
        demonCoreBase, demonCoreTop = generateCore()
        
        posCorr = center - demonCoreBase.pos
        demonCoreBase.pos += posCorr
        demonCoreTop.pos += posCorr

        screwDriver = vpep.screwDriver(0.2)
        screwDriver.rotate(vp.pi / 2, axis = vp.vec(0, 0, 1))
        screwDriver.rotate(vp.pi / 2, axis = vp.vec(1, 0, 0))
        screwDriver.pos = demonCoreTop.pos
        screwDriver.pos += vp.vector(0.5 * (demonCoreTop.width + screwDriver.width) * 0.995,
                                     -0.5 * demonCoreTop.height, 0)
        
        self.base = demonCoreBase
        self.top = demonCoreTop
        self.tool = screwDriver
        
        self.fetchAngOri()
        
    def fetchAngOri(self):
        oriAct = vpep.tiltOrigin(self.top)
        self.angOri = oriAct
        #return(oriAct)

    def toggleCoreScrewdriver(self, tilt, dt, num, film, framer, scene):
        vpep.toggleLid(self.top, [self.tool], self.angOri, tilt, dt, num, film, framer, scene)
    
def canyonWalls(h):
    xzer = 40 * h
    yer = 5 * h
    dustColor = vp.vector((255/255), (221/255), (170/255))
    
    wall1 = vp.box(pos = vp.vector((xzer / 2) + 20,yer / 2,0), size = vp.vector(xzer,yer,xzer), color = dustColor)
    wall2 = vp.box(pos = wall1.pos, size = wall1.size, color = wall1.color)
    wall2.pos.x *= -1
    floor = vpep.xzRect(40, xzer, vp.vector(0, 0, 0), dustColor)
    return(vp.compound([wall1, wall2, floor]))